import numpy as np
import json

embedding = np.load('data/doc_doc_notag.npy')
json_embed = json.load(open('data/embeddings_notag.json', 'r'))

INDEX = 143
print(json_embed[str(INDEX)]["title"])
for i in np.argsort(embedding[INDEX])[::-1][:10]:
    print(json_embed[str(i)]["title"], " ", json_embed[str(i)]["filename"], " : ", embedding[INDEX][i])
