import json
import numpy as np
import pandas as pd


def check_embed_shape():
    with open('preprocess/embedding/embeddings_fill.json', 'r', encoding='utf-8') as f:
        embeddings = json.load(f)
    info_sheet = pd.read_csv('server/model/info_sheet.csv')

    for i, row in info_sheet.iterrows():
        print(embeddings[str(i)]['title'], row['title'])


def make_embed():
    with open('preprocess/embedding/embeddings_fill.json', 'r', encoding='utf-8') as f:
        embeddings = json.load(f)

    zero = np.zeros((462, 462))
    for i in embeddings.keys():
        for j in embeddings.keys():
            i_embeds = [kk for kk in embeddings[i].keys()]
            j_embeds = [kk for kk in embeddings[j].keys()]

            i_embeds.remove('title')
            j_embeds.remove('title')

            score = 0
            for k in range(7):
                score += np.dot(embeddings[i][i_embeds[k]], embeddings[j][j_embeds[k]])
            zero[int(i)][int(j)] = score

    np.save('preprocess/embedding/doc_doc.npy', zero)


def get_similar_docs():
    doc_doc = np.load('preprocess/embedding/doc_doc.npy')
    similarity = {}
    for i in range(462):
        similarity[i] = doc_doc[i].argsort()[-21:-1][::-1].tolist()

    with open('preprocess/embedding/similarity.json', 'w', encoding='utf-8') as f:
        json.dump(similarity, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # check_embed_shape()
    # make_embed()
    get_similar_docs()
