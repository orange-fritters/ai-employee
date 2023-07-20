
import pandas as pd
import numpy as np
import json

class Recommendation:
    def __init__(self, info_dir: str):
        self.data = pd.read_csv(info_dir)

    def get_recommendation(self, score, n = 5):
        top_n_index = score.argsort()[::-1][:n]
        return self.data.loc[top_n_index]['filename'].tolist()

