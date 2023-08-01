import ast
import numpy as np
import pandas as pd
from preprocess.embed_final.retriever import Embed


retriever = Embed()

queries = pd.read_csv("preprocess/emed_final/query_final_final.csv")
queries['embed'] = queries['embed'].apply(ast.literal_eval)

hit_1 = 0
hit_5 = 0
for i, row in queries.iterrows():
    query = row['query']
    title = row['title']
    embed = np.array(row['embed'])
    sim = np.dot(retriever.embed, embed).reshape(-1)
    sim = np.sort(sim)[::-1]
    rank, top1 = retriever.rank_from_title(sim, title)
    if rank == 1:
        hit_1 += 1
    if rank <= 5:
        hit_5 += 1
    if rank > 5:
        print(f"{i}th query: {query}")
        print(f"    rank: {rank} ground truth: {title} pred: {top1}")

print(f"hit@1: {hit_1 / len(queries)}")
print(f"hit@5: {hit_5 / len(queries)}")
