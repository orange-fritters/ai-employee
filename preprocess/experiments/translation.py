import time
from typing import List
import pandas as pd
import json
import numpy as np
import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential
import tiktoken


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


def translate(query, method):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    prompt_message = [
        {"role": "system",
            "content": """
                - You must translate the following sentence into English.
                - Output only translation, No prose or explanation, indicators.
                """},
        {"role": "assistant",
            "content": f"Translate {query} to english keeping the format."
         },
        {"role": "user",
            "content": """
                - You are an Korean English translator. 
                - Query is used for document search with embedding.
                - You only contain information inside the query.
                - Translation output must be in form of 
                "The asker is { description of whom } is in situation of { situation }.
                So the asker might need service for example { possible services } "
                """},
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt_message,
            temperature=0
        )
    except:
        return "Error", 0

    translated = response['choices'][0]['message']['content']

    df = pd.read_parquet('preprocess/experiments/files/articles_eng.parquet')
    df = df.dropna(axis=0)
    df['total_embed'] = df['total_embed'].apply(lambda x: np.array(x))
    df['content_eng_embed'] = df['content_eng_embed'].apply(lambda x: np.array(x))
    df['target_eng_embed'] = df['target_eng_embed'].apply(lambda x: np.array(x))
    total_embed = np.array(df['total_embed'].tolist())
    content_eng_embed = np.array(df['content_eng_embed'].tolist())
    target_eng_embed = np.array(df['target_eng_embed'].tolist())

    try:
        query_embed = openai.Embedding.create(
            engine="text-embedding-ada-002",
            input=[translated])
    except Exception as e:
        print(e)
        return ["Error"]*10, 0

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

    in_token = len(encoding.encode(query))
    for prompt in prompt_message:
        in_token += len(encoding.encode(prompt['content']))
    embed_token = len(encoding.encode(translated))
    out_token = len(encoding.encode(translated))

    total_dollar = 0.0015 * in_token + 0.0001 * embed_token + 0.002 * out_token
    total_won = total_dollar * 1.3
    top_10_idx = np.argsort(similarity)[-10:]
    return df.iloc[top_10_idx]['title'].values.tolist(), total_won


def rerank_gpt(method="total"):
    result_dict = {}
    query_df = pd.read_parquet('preprocess/experiments/files/query_embed.parquet')
    encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
    articles = pd.read_parquet('preprocess/experiments/files/articles_eng.parquet')
    for i in range(975, len(query_df), 25):

        query = query_df.iloc[i]['query']
        print(f"[Query {i}]", query)
        start = time.time()
        titles, total_won = translate(query, method)

        articles = articles[articles['title'].isin(titles)]

        string = ""
        for title in titles:
            string += title + ", "

        prompt_message = [
            {"role": "system",
             "content": """
                - You are RankGPT, an intelligent assistant that can rank service based on their relevancy to the situation.
                """},
            {"role": "assistant",
             "content": f"The situation : {query} \n Services : {string}"
             },
            {"role": "user",
             "content": """
                - Among the given services, You have to rank the top three most relevant services to the situation.
                - Do not include prose or explanation, indicators, Only korean titles.
                - You must only contain services that the asker is able to benefit from.
                
                - Output must be in form of 
                " 
                { 1. Most relevant sercvice  }
                { 2. Second relevant sercvice }
                { 3. Third relevant sercvice }
                "

                - You only contain title from the Services given.
                """},
        ]
        for prompt in prompt_message:
            total_won += 0.0015 * len(encoder.encode(prompt['content'])) * 1.3

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt_message,
                temperature=0
            )
        except Exception as e:
            print(e)
            continue

        response = response['choices'][0]['message']['content']

        response = response.split("\n")
        response = [r[3:].strip() for r in response]
        # response = [response[2], response[1], response[0]]
        total_won += 0.002 * len(encoder.encode(response[0])) * 1.3
        total_won += 0.002 * len(encoder.encode(response[1])) * 1.3
        total_won += 0.002 * len(encoder.encode(response[2])) * 1.3
        for title in response:
            print(title)
        print(f"[{time.time() - start:.2f}초 {total_won:.2f}원]")
        print()
        result_dict[i] = [query, titles, response[0], response[1], response[2]]

        result_df = pd.DataFrame.from_dict(result_dict, orient='index',
                                           columns=['query', 'titles', '1', '2', '3'])
        result_df.to_csv('preprocess/experiments/files/rerank_gpt_2.csv')


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

    for i in range(0, len(query_df), 5):
        query = query_df.iloc[i]['query']
        print(query)
        translate_rerank(query, method)
        print()


if __name__ == '__main__':
    # find_missing()
    # print_some()
    # embed()
    # rerank_gpt()
    # articles = pd.read_parquet('preprocess/experiments/files/articles_eng.parquet')
    # print(articles.iloc[0]['target_eng'])

    df = pd.read_csv('preprocess/experiments/files/rerank_gpt.csv')
    df = df[['query', '1', '2', '3']]
    df.to_html('preprocess/experiments/files/rerank_gpt.html')
