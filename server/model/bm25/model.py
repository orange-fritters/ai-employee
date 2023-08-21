from model.bm25.bm25 import BM25
import numpy as np


class Model:
    def __init__(self):
        self.bm25 = BM25()
        self.data = self.bm25.data

    def get_topN_title(self, query, n=5):
        score_bm25 = self.bm25.get_score(query)
        score_bm25 = (score_bm25 - np.mean(score_bm25)) / np.std(score_bm25)

        top_n_index = score_bm25.argsort()[::-1][:5]
        top_titles = self.data.loc[top_n_index]['title_kor'].tolist()

        return [{"rank": i + 1, "title": title} for i, title in enumerate(top_titles)]
