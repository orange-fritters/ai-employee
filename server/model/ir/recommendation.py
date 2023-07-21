
import pandas as pd
import numpy as np
import json
from model.ir.bm25 import BM25


class Recommendation:
    def __init__(self, info_dir: str, articles_path: str):
        self.data = pd.read_csv(info_dir)
        self.bm25 = BM25(articles_path=articles_path,
                         update_data=False)

    def get_recommendation(self, score, n=5):
        top_n_index = score.argsort()[::-1][:n]
        return self.data.loc[top_n_index]['filename'].tolist()

    def get_bm25(self, query, n=5):
        score = self.bm25.get_score(query)
        top_n_index = np.argsort(score)[::-1][:n]
        titles = self.data.loc[top_n_index]['title'].tolist()
        response = [{"rank": i + 1, "title": title} for i, title in enumerate(titles)]
        return json.dumps(response)

    def get_bm25_python(self, query, n=5):
        score = self.bm25.get_score(query)
        top_n_index = np.argsort(score)[::-1][:n]
        titles = self.data.loc[top_n_index]['title'].tolist()
        return titles
