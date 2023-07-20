import os
import re
import json
import pickle
from rank_bm25 import BM25Okapi
from bs4 import BeautifulSoup as bs
from kiwipiepy import Kiwi

### data 예상 구조
### data/articles/*.html
### data/summary.json

### tokenized data 예상 구조
### data/tokenized/articles.pkl
### data/tokenized/summary.pkt

class BM25():
    def __init__(self, 
                articles_path,
                data_type = "html",
                tokenize_including_pos = None, 
                tokenize_excluding_pos = "", 
                tokenize_min_len = 1, 
                update_data = True,):
        ## articles_path: article data(.html format) 위치 _ ex. "/data/articles/"
        ## tokenize_including_pos: 포함할 품사 list _ ex. ["NNG", "NNP"]
        ## tokenize_excluding_pos: 제외할 품사 list _ ex. ["JKS", "JKC"]
        ## tokenize_min_len: 최소 token 길이
        ## update_data: data 전처리 진행 및 업데이트 여부
        
        self.articles_path = articles_path 
        self.data_type = data_type
        self.tokenize_including_pos = tokenize_including_pos 
        self.tokenize_excluding_pos = tokenize_excluding_pos 
        self.tokenize_min_len = tokenize_min_len 
        self.update_data = update_data 
        self.tokenizer = Kiwi()

        self.get_preprocessed_articles()
        self.initialize_bm25()


    def html_to_text(self, pth):
        ## html files -> list(str)

        articles = []

        if self.data_type == "html":

            articles_id = os.listdir(pth)
            articles_id.sort()
            
            for id in articles_id:
                with open(pth + id, 'r') as f:
                    html = f.read()
                
                article = bs(html, 'html.parser')
                article = " ".join(article.text.replace("\n", "").split())
                articles.append(article)

        elif self.data_type == "summary":
            with open(pth) as f:
                summary = json.load(f)

            for key, value in summary.items():
                articles.append(value['summary'])

        return articles

    def clean(self, text):
        text = re.sub('☎([0-9]+-?[0-9]+)', " ", text)
        text = re.sub('[^\w\s\n]', "", text)
        return text

    def tokenize(self, text, including_pos, excluding_pos, min_len):
        ## including_pos, excluding_pos 중 방식 선택
        ## including_pos: 특정 품사만 선택
        ## including_pos: 특정 품사만 제외
        ## min_len: token 최소 길이 선택
        ## 시간 10초 정도 소요됨

        self.tokenizer.prepare()
        tokenized_text = self.tokenizer.analyze(text)

        token = []
        tokenized = tokenized_text[0][0]

        if including_pos == None:
            for i in range(len(tokenized)):
                if tokenized[i][1] not in excluding_pos and len(str(tokenized[i][0])) >= min_len: 
                    token.append(tokenized[i][0])
        else:
            for i in range(len(tokenized)):
                if tokenized[i][1] in including_pos and len(str(tokenized[i][0])) >= min_len: 
                    token.append(tokenized[i][0])

        return token


    def text_preprocess(self, text):
        text = self.clean(text)
        text = self.tokenize(text, self.tokenize_including_pos, self.tokenize_excluding_pos, self.tokenize_min_len)

        return text


    def get_preprocessed_articles(self):
        ## articles_path: /data/articles/ 형태로 받아온다고 가정
        ## -> summary 는 /data/summary.json ...

        ## upate_data: True -> data 다시 전처리해서 저장
        ## data/articles/*.html -> data/tokenized_data/articles.pkl 으로 저장

        ## upate_data: False -> 전처리해둔 data 불러와서 사용
        ## data/tokenized_data/articles.pkl 불러옴

        if self.update_data:
            articles = self.html_to_text(self.articles_path)
            articles_processed = [self.text_preprocess(article) for article in articles]

            data_path = self.articles_path.rstrip("/").rsplit("/", 1)[0]
            file_ver = self.data_type

            save_path = data_path + "/tokenized_articles/"
            file_name = file_ver + ".pkl"

            os.makedirs(os.path.dirname(save_path + file_name), exist_ok=True)
            with open(save_path + file_name, 'wb') as f:
                pickle.dump(articles_processed, f, pickle.HIGHEST_PROTOCOL)

            self.tokenized_articles = articles_processed

        else:
            
            data_path = self.articles_path.rstrip("/").rsplit("/", 1)[0]
            file_ver = self.data_type

            save_path = data_path + "/tokenized_articles/"
            file_name = file_ver + ".pkl"

            with open(save_path + file_name, 'rb') as f:
                articles_processed = pickle.load(f)

            self.tokenized_articles = articles_processed


    def initialize_bm25(self):
        model = BM25Okapi(self.tokenized_articles)
        self.model = model


    def get_score(self, query):
        tokenized_query = self.text_preprocess(query)
        score = self.model.get_scores(tokenized_query)
        return score



if __name__ == "__main__":
    ## example
    bm25 = BM25(articles_path = '/content/drive/MyDrive/KT/data/articles/',
            tokenize_excluding_pos = ["JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JX", "JC", "EC", "EF"],
            tokenize_min_len = 2)

    print(bm25.get_score("나는 혼자 아이를 양육하고 책임을 다루는데 어려움을 겪고 있어"))
