import numpy as np

embedding = np.load('data/embeds/embeddings_notag.npy')
doc_doc = embedding.dot(embedding.T)

np.save('data/embeds/doc_doc_notag.npy', doc_doc)
