import pickle
import pandas as pd
from kiwipiepy import Kiwi
from rank_bm25 import BM25Okapi
from model.bm25.text_preprocess import text_preprocess
from model.bm25.query_expansion import query_expand


class BM25():
    DOCUMENT_FILE_PATH = "model/files/processed_doc.csv"

    def __init__(self):

        with open("model/bm25/articles_preprocessed.pkl", 'rb') as f:
            articles_preprocessed = pickle.load(f)

        with open("model/bm25/word_similarity.pkl", 'rb') as f:
            self.similar_word_dict = pickle.load(f)

        self.tokenizer = Kiwi()
        self.min_len = articles_preprocessed['min_len']
        self.including_pos = articles_preprocessed['including_pos']
        self.excluding_pos = articles_preprocessed['excluding_pos']
        self.tokenized = articles_preprocessed['tokenized']
        self.model = BM25Okapi(self.tokenized)
        self.data = pd.read_csv(self.DOCUMENT_FILE_PATH)

    def get_score(self, query: str):

        tokenized_query = text_preprocess(
            self.tokenizer, query, self.min_len, self.including_pos, self.excluding_pos
        )
        expanded_query = query_expand(tokenized_query, self.similar_word_dict)

        score = self.model.get_scores(expanded_query)
        return score
