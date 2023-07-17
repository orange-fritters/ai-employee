import numpy as np

embedding = np.load('data/embeddings.npy')
doc_doc = embedding.dot(embedding.T)

np.save('data/doc_doc.npy', doc_doc)
