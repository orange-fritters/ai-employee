from time import sleep
from typing import List
import pandas as pd
import json
import numpy as np
import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential

with open('server/model/utils/config.json') as f:
    config = json.load(f)
openai.api_key = config['chatgpt']['secret']


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str, engine="text-similarity-davinci-001", **kwargs) -> List[float]:
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], engine=engine, **kwargs)["data"][0]["embedding"]


def find_missing():
    info_sheet = pd.read_csv('preprocess/experiments/files/info_sheet.csv')
    # ['index', 'title', 'filename', 'article_tag', 'article_notag', 'queries', 'summary', 'keywords']

    articles_eng = pd.read_parquet('preprocess/experiments/files/articles_eng.parquet')
    # ['filename', 'target', 'content', 'content_embed', 'target_embed', 'content_eng', 'target_eng']
    missing = []
    for filename in info_sheet['filename']:
        if filename not in articles_eng['filename'].values:
            missing.append(filename)

    for i, row in articles_eng[['filename', 'content_eng', 'target_eng']].iterrows():
        if None in row.values.tolist():
            missing.append(row['filename'])
        elif 'Error' in row['content_eng'] or 'Error' in row['target_eng']:
            missing.append(row['filename'])

    # ['기타지원_02.html', '기타지원_14.html', '노령층지원_20.html', '보훈대상자지원_29.html', '보훈대상자지원_31.html',
    #  '생계지원_02.html', '생계지원_11.html', '임신보육지원_26.html', '임신보육지원_30.html', '장애인지원_60.html',
    #  '장애인지원_82.html', '장애인지원_83.html', '청소년청년지원_04.html', '취업지원_06.html', '취업지원_23.html',
    #  '취업지원_32.html']

    missing_idx = info_sheet[info_sheet['filename'].isin(missing)].index
    print(missing_idx)
    # [1, 13, 105, 183, 185, 196, 205, 261, 265, 346, 368, 369, 373, 431, 448, 457]

    articles_eng_dict = {}
    for i in range(len(info_sheet)):
        filename = info_sheet.loc[i, 'filename']

        if not i in missing_idx:
            articles_eng_dict[i] = articles_eng[articles_eng['filename'] == filename].values[0].tolist()
        else:
            articles_eng_dict[i] = [info_sheet.loc[i, 'title'],
                                    info_sheet.loc[i, 'filename'],
                                    None,   # 'target'
                                    None,   # 'content'
                                    None,   # 'content_embed'
                                    None,   # 'target_embed'
                                    None,   # 'content_eng'
                                    None    # 'target_eng'
                                    ]

    articles_eng_df = pd.DataFrame.from_dict(articles_eng_dict, orient='index',
                                             columns=['title', 'filename', 'target', 'content', 'content_embed',
                                                      'target_embed', 'content_eng', 'target_eng'])

    articles_eng_df.to_parquet('preprocess/experiments/files/articles_eng.parquet')


def print_some():
    df = pd.read_parquet('preprocess/experiments/files/articles_eng.parquet')
    total = [1, 13, 105, 183, 185, 196, 205, 261, 265, 346, 368, 369, 373, 431, 448, 457]
    wrong_format = [105, 183, 196, 205, 265, 369, 373, 431]
    wrong_translation = [1, 13, 185, 261, 346, 368, 448, 457]

    format_files = ['노령층지원_20.html',
                    '보훈대상자지원_29.html',
                    '생계지원_02.html',
                    '생계지원_11.html',
                    '임신보육지원_30.html',
                    '장애인지원_83.html',
                    '청소년청년지원_04.html',
                    '취업지원_06.html']

    format_zip = list(zip(wrong_format, format_files))


def embed():
    df = pd.read_parquet('preprocess/experiments/files/articles_eng.parquet')
    # content_eng_embed_list = []
    target_eng_embed_list = []
    total_embed_list = []
    for i, row in df.iterrows():
        if None in row.values.tolist():
            # content_eng_embed_list.append(None)
            target_eng_embed_list.append(None)
            total_embed_list.append(None)
        else:
            # content_eng_embed = openai.Embedding.create(
            #     engine="text-embedding-ada-002",
            #     input=[row['content_eng']])
            target_eng_embed = openai.Embedding.create(
                engine="text-embedding-ada-002",
                input=[row['target_eng']])
            total_embed = openai.Embedding.create(
                engine="text-embedding-ada-002",
                input=[row['content_eng'], row['target_eng']])
            # content_eng_embed = content_eng_embed["data"][0]["embedding"]
            target_eng_embed = target_eng_embed["data"][0]["embedding"]
            total_embed = total_embed["data"][0]["embedding"]

            # content_eng_embed_list.append(content_eng_embed)
            target_eng_embed_list.append(target_eng_embed)
            total_embed_list.append(total_embed)

            print(f"[{i}/{len(df)}] {i/len(df) * 100}%")
    # df['content_eng_embed'] = content_eng_embed_list
    df['target_eng_embed'] = target_eng_embed_list
    df['total_embed'] = total_embed_list

    df.to_parquet('preprocess/experiments/files/articles_eng.parquet')


def translate_test(query, method):
    prompt_message = [
        {"role": "assistant",
            "content": """
                - You must translate the following sentence into English.
                - Output only translation, No prose or explanation, indicators.
                """},
        {"role": "user",
            "content": f"Translate {query} to english keeping the format."
         },
        {"role": "system",
            "content": """
                - You are an Korean English translator. 
                - Query is used for document search with embedding.
                - You only contain information inside the query.
                - Translation output must be in form of "The asker is { description of whom } is in situation of { situation }\" ".
                """},
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt_message,
        )
    except:
        return "Error"

    translated = response['choices'][0]['message']['content']
    translated += "So, the asker is looking for a social welfare service that can help the asker."
    df = pd.read_parquet('preprocess/experiments/files/articles_eng.parquet')
    df = df.dropna(axis=0)
    df['total_embed'] = df['total_embed'].apply(lambda x: np.array(x))
    df['content_eng_embed'] = df['content_eng_embed'].apply(lambda x: np.array(x))
    df['target_eng_embed'] = df['target_eng_embed'].apply(lambda x: np.array(x))
    total_embed = np.array(df['total_embed'].tolist())
    content_eng_embed = np.array(df['content_eng_embed'].tolist())
    target_eng_embed = np.array(df['target_eng_embed'].tolist())

    query_embed = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=[translated])

    query_embed = np.array(query_embed["data"][0]["embedding"]).reshape(-1, 1)

    total_similarity = np.dot(total_embed, query_embed).reshape(-1)
    content_eng_similarity = np.dot(content_eng_embed, query_embed).reshape(-1)
    target_eng_similarity = np.dot(target_eng_embed, query_embed).reshape(-1)
    stacked = np.stack([total_similarity, content_eng_similarity, target_eng_similarity], axis=0)

    if method == "sum":
        similarity = np.sum(stacked, axis=0)
    elif method == "content":
        similarity = content_eng_similarity
    elif method == "target":
        similarity = target_eng_similarity
    elif method == "max":
        stacked = np.stack([total_similarity, content_eng_similarity, target_eng_similarity], axis=0)
        similarity = np.max(stacked, axis=0)
    elif method == "min":
        stacked = np.stack([total_similarity, content_eng_similarity, target_eng_similarity], axis=0)
        similarity = np.min(stacked, axis=0)
    elif method == "hardvote":
        stacked = np.stack([total_similarity, content_eng_similarity, target_eng_similarity], axis=0)
        similarity = np.argmax(stacked, axis=0)
    elif method == "content+target":
        similarity = content_eng_similarity + target_eng_similarity
    elif method == "total":
        similarity = total_similarity
    else:
        raise ValueError("Invalid method")

    top_10_idx = np.argsort(similarity)[-15:]
    return df.iloc[top_10_idx]['title'].values.tolist()


def rerank_gpt(method="total"):
    query_df = pd.read_parquet('preprocess/experiments/files/query_embed.parquet')

    for i in range(0, len(query_df), 20 * 5 + 5):
        query = query_df.iloc[i]['query']
        print(query)
        titles = translate_test(query, method)
        # titles are of strings. join them with comma
        string = ", ".join(titles)

        prompt_message = [
            {"role": "assistant",
             "content": """
                - You are an Korean AI social welfare counsellor.
                - You are helping the asker to find the appropriate social welfare service.
                """},
            {"role": "user",
             "content": f"The situation : {query} \n Services : {string}"
             },
            {"role": "system",
             "content": """
                - You have to rank the title of services in order of possibility to benfit from it given a situation.
                - Only top 4 title of services are needed.
                - Output must be in form of 
                   "1. { Most probable title }
                    2. { Second most probable title }
                    ...
                    4. { Fourth most probable title }".
                - Include only titles in Korean, no prose or explanation, indicators, no translation to English.
                - You only contain title from the Services.
                - You only contain titles the asker can benefit from.
                """},
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt_message,
        )

        print(response['choices'][0]['message']['content'])
        print()


def translate_rerank(query, method):
    prompt_message = [
        {"role": "assistant",
            "content": """
                - You must translate the following sentence into English.
                - Output only translation, No prose or explanation, indicators.
                """},
        {"role": "user",
            "content": f"Translate {query} to english keeping the format."
         },
        {"role": "system",
            "content": """
                - You are an Korean English translator. 
                - Query is used for document search with embedding.
                - You only contain information inside the query.
                - Translation output must be in form of "The asker is { description of whom } is in situation of { situation }\" ".
                """},
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt_message,
        )
    except:
        return "Error"

    translated = response['choices'][0]['message']['content']
    translated += "So, the asker is looking for a social welfare service that can help the asker."
    df = pd.read_parquet('preprocess/experiments/files/articles_eng.parquet')
    df = df.dropna(axis=0)
    df['total_embed'] = df['total_embed'].apply(lambda x: np.array(x))
    df['content_eng_embed'] = df['content_eng_embed'].apply(lambda x: np.array(x))
    df['target_eng_embed'] = df['target_eng_embed'].apply(lambda x: np.array(x))
    total_embed = np.array(df['total_embed'].tolist())
    content_eng_embed = np.array(df['content_eng_embed'].tolist())
    target_eng_embed = np.array(df['target_eng_embed'].tolist())

    query_embed = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=[translated])

    query_embed = np.array(query_embed["data"][0]["embedding"]).reshape(-1, 1)

    total_similarity = np.dot(total_embed, query_embed).reshape(-1)
    content_eng_similarity = np.dot(content_eng_embed, query_embed).reshape(-1)
    target_eng_similarity = np.dot(target_eng_embed, query_embed).reshape(-1)
    stacked = np.stack([total_similarity, content_eng_similarity, target_eng_similarity], axis=0)

    if method == "sum":
        similarity = np.sum(stacked, axis=0)
    elif method == "content":
        similarity = content_eng_similarity
    elif method == "target":
        similarity = target_eng_similarity
    elif method == "max":
        stacked = np.stack([total_similarity, content_eng_similarity, target_eng_similarity], axis=0)
        similarity = np.max(stacked, axis=0)
    elif method == "min":
        stacked = np.stack([total_similarity, content_eng_similarity, target_eng_similarity], axis=0)
        similarity = np.min(stacked, axis=0)
    elif method == "hardvote":
        rerank_gpt
    top_10_idx = np.argsort(similarity)[-10:]
    top_10 = df.iloc[top_10_idx].copy()
    top_10["embedding"] = top_10["title"].apply(lambda x: get_embedding(x, engine="text-embedding-ada-002"))
    top_10["similarity"] = top_10["embedding"].apply(lambda x: np.dot(x, query_embed).reshape(-1)[0])
    top_10 = top_10.sort_values("similarity", ascending=False)
    for title in top_10['title'].values.tolist():
        print("    ", title)


def random_query(method="total"):
    querie_df = pd.read_parquet('preprocess/experiments/files/query_embed.parquet')
    queries = querie_df['query']

    q = queries.sample(1).values[0]
    print(q)
    translate_rerank(q, method)
    print()


def query_by_20(method):
    query_df = pd.read_parquet('preprocess/experiments/files/query_embed.parquet')

    for i in range(0, len(query_df), 20 * 5):
        query = query_df.iloc[i]['query']
        print(query)
        translate_rerank(query, method)
        print()


if __name__ == '__main__':
    # find_missing()
    # print_some()
    # embed()
    rerank_gpt()
