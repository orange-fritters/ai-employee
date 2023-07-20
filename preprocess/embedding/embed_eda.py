import json
import numpy as np
import itertools

with open('preprocess/embedding/query.json', 'r', encoding='utf-8') as f:
    embeddings = json.load(f)

for k, v in embeddings.items():
    embeds = [kk for kk in v.keys()]
    pairs = list(itertools.combinations(embeds, 2))
    for pair in pairs:
        score = np.dot(v[pair[0]], v[pair[1]])
        print(pair, score)
    break
