from model.bm25.bm25 import BM25
from model.embed.multiturn_model import MultiTurn
import numpy as np


class Ensemble:
    def __init__(self):
        self.multiturn = MultiTurn()
        self.bm25 = BM25()
        self.data = self.multiturn.data

    def get_topN_title(self, query, n=5):
        score_embed = self.multiturn.get_score(query)
        score_bm25 = self.bm25.get_score(query)

        score_embed = (score_embed - np.mean(score_embed)) / np.std(score_embed)
        score_bm25 = (score_bm25 - np.mean(score_bm25)) / np.std(score_bm25)

        score = score_embed + score_bm25 * 0.4
        top_n_index = score.argsort()[::-1][:5]
        top_titles = self.data.loc[top_n_index]['title_kor'].tolist()

        return [{"rank": i + 1, "title": title} for i, title in enumerate(top_titles)]
