import os
import json
import random
import numpy as np
import pandas as pd
import tiktoken
from ir.recommendation import Recommendation

# print(len(pd.read_parquet('preprocess/embedding/embeddings.parquet')))
# print(pd.read_parquet('preprocess/embedding/embeddings.parquet').tail())
# print(pd.read_parquet('preprocess/embedding/embeddings.parquet')['title'].duplicated())
# exit()


def save_embeddings():
    with open('preprocess/embedding/embeddings.json', 'r', encoding='utf-8') as f:
        documents_embeddings = json.load(f)
    documents_embeddings = dict(sorted(documents_embeddings.items(), key=lambda x: int(x[0])))
    pd.DataFrame(documents_embeddings).T.reset_index().to_parquet(
        'preprocess/embedding/embeddings.parquet', index=True)

    with open('preprocess/embedding/query_embed.json', 'r', encoding='utf-8') as f:
        query_embeddings = json.load(f)
    query_embeddings = dict(sorted(query_embeddings.items(), key=lambda x: int(x[0])))
    pd.DataFrame(query_embeddings).T.to_parquet(
        'preprocess/embedding/query_embed.parquet', index=False)


# with open('preprocess/embedding/similarity.json', 'r', encoding='utf-8') as f:
#     answer_rank = json.load(f)
# pd.DataFrame(answer_rank).T.to_parquet(
#     'preprocess/embedding/similarity.parquet', index=False)

'''
query_embeddings = {
    "0": {
        "index": 0,
        "query": "저희 아이가 학교에서 코로나19에 노출되었고, 이번 주 동안 자가격리를 해야 해요",
        "embedding": [0.001, 0.002, ..., 0.001]]
        },
    "1": {


document_embeddings = {
    "0": {
        "title" : "사회서비스원 긴급돌봄 사업",
        "article" : [0.001, 0.002, ... , 0.001],
        "summary" : [0.001, 0.002, ... , 0.001],
        "keywords" : [0.001, 0.002, ... ,0.001],
        "article_summary" : [0.001, 0.002, ... , 0.001],
        "article_keywords" : [0.001, 0.002, ... , 0.001],
        "summary_keywords" : [0.001, 0.002, ... , 0.001],
        "article_summary_keywords" : [0.001, 0.002, ... , 0.001] 
        },
    "1": {
        ...

similarity = {
    "0": [
        299,
        102,
        14,
        197,
        1,
        244,
        103,
        228,
'''

'''[{i}/{len(query_embeddings)}] {percent}% completed'''


def query_doc_similarity():
    with open('preprocess/embedding/query_embed.json', 'r', encoding='utf-8') as f:
        query_embeddings = json.load(f)
    query_embeddings = dict(sorted(query_embeddings.items(), key=lambda x: int(x[0])))

    with open('preprocess/embedding/embeddings.json', 'r', encoding='utf-8') as f:
        documents_embeddings = json.load(f)
    documents_embeddings = dict(sorted(documents_embeddings.items(), key=lambda x: int(x[0])))

    query_doc_similarity = {}
    for i, (query_id, query) in enumerate(query_embeddings.items()):
        if i % 100 == 0:
            print(f'[{int(query_id)}/{len(query_embeddings)}] {round(int(query_id) / len(query_embeddings) * 100, 2)}% completed')

        query_vector = np.array(query["embedding"])
        for doc_id, doc in documents_embeddings.items():
            for key in doc.keys():
                if key == "title":
                    continue
                doc_vector = np.array(doc[key])
                similarity = np.dot(query_vector, doc_vector)

                if query_id not in query_doc_similarity:
                    query_doc_similarity[query_id] = {}

                if doc_id not in query_doc_similarity[query_id]:
                    query_doc_similarity[query_id][doc_id] = []

                query_doc_similarity[query_id][doc_id].append(similarity)

    with open('preprocess/embedding/query_doc_similarity.json', 'w', encoding='utf-8') as f:
        json.dump(query_doc_similarity, f, indent=4, ensure_ascii=False)


"""
query_doc_similarity = {
    "0": {
        "0": [0.001, 0.002, ... , 0.001],
        "1": [0.001, 0.002, ... , 0.001],
        ...,
        "461": [0.001, 0.002, ... , 0.001]
        },
    ...,
    "2311": {
        "0": [0.001, 0.002, ... , 0.001],
        ...,
        "461": [0.001, 0.002, ... , 0.001]
        }
    }
"""

"""
query_doc_similarity = {
    "0": {
        "0": [0.779, 0.75, ... , 0.781], (<-- 7 scores)
        "1": [0.78, 0.75, ... , 0.78],
        ...,
        "461": [0.78, 0.75, ... , 0.78]
        }
    ...,
    "2311": {
        "0": [0.78, 0.75, ... , 0.78],
        ...,
        }
    }
"""


def top_document(k=5):
    with open('preprocess/embedding/query_doc_similarity.json', 'r', encoding='utf-8') as f:
        query_doc_similarity = json.load(f)
    with open('preprocess/embedding/query_embed.json', 'r', encoding='utf-8') as f:
        query_embeddings = json.load(f)
    info_sheet = pd.read_csv('preprocess/embedding/info_sheet.csv', encoding='utf-8')
    rec = Recommendation('preprocess/embedding/info_sheet.csv',
                         'data/articles/')
    top_documents = {}
    for query_id, doc_scores in query_doc_similarity.items():
        sorted_docs = sorted(doc_scores.items(), key=lambda x: np.max(x[1]), reverse=True)
        top_k_doc_ids = [sorted_docs[i][0] for i in range(k)]
        top_documents[query_id] = top_k_doc_ids

    result = {}
    for key, value in query_embeddings.items():
        print(f'query: {value["query"]}')
        embed_titles = [info_sheet["title"].iloc[doc] for doc in list(map(int, top_documents[key]))]
        bm25_titles = rec.get_bm25_python(value["query"])
        for title in embed_titles:
            print(f'embed title: {title}')
        for title in bm25_titles:
            print(f'bm25 title: {title}')

        result[key] = {
            "query": value["query"],
            "embed_titles": embed_titles,
            "bm25_titles": bm25_titles
        }
        print("\n\n")

    pd.DataFrame(result).T.to_parquet('preprocess/embedding/result.parguet', index=False)


def make_data_for_eda():
    # parguet
    # 2360 행 df
    # 원본 쿼리 str, [score 462개 (순서대로)], [label 1개]

    with open('preprocess/embedding/query_doc_similarity.json', 'r', encoding='utf-8') as f:
        query_doc_similarity = json.load(f)

    with open('preprocess/embedding/query_embed.json', 'r', encoding='utf-8') as f:
        query_embeddings = json.load(f)

    info_sheet = pd.read_csv('preprocess/embedding/info_sheet.csv', encoding='utf-8')

    dict_parquet = {}
    for key, value in query_embeddings.items():
        value["top_documents"] = query_doc_similarity[key]
        qeury = value["query"]
        scores = [max(seven_score) for seven_score in value["top_documents"].values()]
        label = query_embeddings[key]["index"]
        dict_parquet[key] = [qeury, scores, label]

    df = pd.DataFrame.from_dict(dict_parquet, orient='index', columns=['query', 'scores', 'label'])
    df.to_parquet('preprocess/embedding/eda.parquet', index=False)


def random_result():
    result = pd.read_parquet('preprocess/embedding/result.parguet')
    sample = result.sample(1).reset_index(drop=True)
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    question = sample['query'][0]
    # bm25_titles = sample['bm25_titles'][0]
    embed_titles = sample['embed_titles'][0]

    # print(f'embed: ')
    # for title in embed_titles:
    #     print(f'    {title}')

    # print(f'bm25: ')
    # for title in bm25_titles:
    #     print(f'    {title}')
    info_sheet = pd.read_csv('preprocess/embedding/info_sheet.csv', encoding='utf-8')
    notags = info_sheet[info_sheet['title'].isin(embed_titles)]['article_notag'].tolist()

    targets = []
    try:
        for notag in notags:
            with open(notag, 'r', encoding='utf-8') as f:
                notag = f.read()
            targets.append(notag.split('1. 대상')[1].split('2. 내용')[:-1])
    except IndexError:
        with open(notags[0], 'r', encoding='utf-8') as f:
            notag = f.read()

    total_token_counts = 0
    total_token_counts += len(encoding.encode(question))
    for notag in notags:
        with open(notag, 'r', encoding='utf-8') as f:
            notag = f.read()
        total_token_counts += len(encoding.encode(notag))

    # print(f'총 토큰 수: {total_token_counts}')
    print("대상:")
    for title, target in zip(embed_titles, targets):
        print(f'<{title}>의 대상: {target}')
    print()
    print(f'질문: {question}')

    return question, total_token_counts


def print_some_queries():
    with open('preprocess/embedding/query_embed.json', 'r', encoding='utf-8') as f:
        query_embeddings = json.load(f)
    info_sheet = pd.read_csv('preprocess/embedding/info_sheet.csv')

    for i in range(0, 2312, 72):
        doc_id = query_embeddings[str(i)]["index"]
        print("서비스: ", info_sheet["title"].iloc[doc_id])
        print("생성된 질문: ", query_embeddings[str(i)]["query"])

        print()


def random_doc_sample():
    # data/summary/summary_m.json

    with open('data/summary/summary_m.json', 'r', encoding='utf-8') as f:
        summary = json.load(f)

    sample = random.sample(list(summary.items()), 1)
    print('title: ', sample[0][1]['title'])
    print('summary: ', sample[0][1]['summary_processed'])
    print('keywords', sample[0][1]['keywords'])


if __name__ == '__main__':
    # query_doc_similarity()
    # top_document()
    # make_data_for_eda()
    random_result()
    # print_some_queries()
    # random_doc_sample()
