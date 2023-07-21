import json
import numpy as np
import pandas as pd

# print(len(pd.read_parquet('preprocess/embedding/embeddings.parquet')))
# print(pd.read_parquet('preprocess/embedding/embeddings.parquet').tail())
# print(pd.read_parquet('preprocess/embedding/embeddings.parquet')['title'].duplicated())
# exit()


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

exit()

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
    query_doc_similarity = {}

    for query_id, query in query_embeddings.items():
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

    top_documents = {}
    for query_id, doc_scores in query_doc_similarity.items():
        sorted_docs = sorted(doc_scores.items(), key=lambda x: np.mean(x[1]), reverse=True)
        top_docs = [doc_id for doc_id, _ in sorted_docs[:7]]
        top_documents[query_id] = top_docs
    print(top_documents)


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


if __name__ == '__main__':
    query_doc_similarity()
