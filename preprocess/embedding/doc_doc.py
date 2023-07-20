import json
import numpy as np


with open('preprocess/embedding/embeddings.json', 'r', encoding='utf-8') as f:
    embeddings = json.load(f)

size = len(embeddings.keys())
zero = np.zeros((size, size))
for ii, i in enumerate(embeddings.keys()):
    for jj, j in enumerate(embeddings.keys()):
        i_embeds = [kk for kk in embeddings[i].keys()]
        j_embeds = [kk for kk in embeddings[j].keys()]

        score = 0
        for k in range(7):
            score += np.dot(embeddings[i][i_embeds[k]], embeddings[j][j_embeds[k]])

        print(ii, jj)
        zero[ii][jj] = score

np.save('preprocess/embedding/doc_doc.npy', zero)
