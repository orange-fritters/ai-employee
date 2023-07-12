import os
from rank_bm25 import BM25Okapi
from bs4 import BeautifulSoup as bs
from konlpy.tag import Mecab 


class BM25():
    def __init__(self):
        self.tokenizer = Mecab()

    def html_to_text(self, pth):
        articles_id = os.listdir(pth)
        articles_id
        
        articles = []
        
        for id in articles_id:
            f = open(pth + id, 'r')
            html = f.read()
            f.close()
            
            article = bs(html, 'html.parser')
            article = " ".join(article.text.replace("\n", "").split())
            articles.append(id + " : " + article)

        self.articles = articles
        return articles

    def bm25(self):
        tokenized_articles = [self.tokenizer.morphs(article) for article in self.articles]
        bm25 = BM25Okapi(tokenized_articles)
        self.bm25 = bm25
        return bm25

    def get_top_n(self, query, num = 3):
        tokenized_query = self.tokenizer.morphs(query)
        top_n = self.bm25.get_top_n(tokenized_query, self.articles, n=num)
        top_n_file_name = [re.split(":")[0].strip() for re in top_n]
        
        return top_n
        return top_n_file_name
        

if __name__ == "__main__":
    model = BM25()
    pth = ""
    query = "이사하고 싶어요"

    model.html_to_text(pth)
    model.bm25()
    top_n_file_list = model.get_top_n(query, 5)
    
    print(top_n_file_list)