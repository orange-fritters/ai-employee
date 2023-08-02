from bm25 import BM25
from retriever import Embed
import numpy as np

class Ensemble:
    def __init__(self):
        self.embed = Embed()
        self.bm25 = BM25()
        self.data = self.embed.data

    def get_topN_title(self, query, n = 5):

        score_embed = self.embed.get_score(query)
        score_bm25 = self.bm25.get_score(query)

        score_embed = (score_embed - np.mean(score_embed)) / np.std(score_embed)
        score_bm25 = (score_bm25 - np.mean(score_bm25)) / np.std(score_bm25)

        score = score_embed + score_bm25 * 0.4

        top_n_index = score.argsort()[::-1][:5]
        
        return self.data.loc[top_n_index]['title_kor'].tolist()

