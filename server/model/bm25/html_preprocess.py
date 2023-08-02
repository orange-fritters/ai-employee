import os
from bs4 import BeautifulSoup as bs
from typing import List
from text_preprocess import text_preprocess
import pickle
from kiwipiepy import Kiwi

def html_to_text(html_path: str) -> List[str]:
    articles = []

    articles_id = os.listdir(html_path)
    articles_id.sort()
     
    for aid in articles_id:
        file_path = os.path.join(html_path, aid)
        with open(file_path, 'r') as f:
            html = f.read()
        
        article = bs(html, 'html.parser')
        article = " ".join(article.text.replace("\n", "").split())
        articles.append(article)

    return articles


def save_tokenized_text(html_path, 
                    tokenizer, 
                    min_len: int = 1,
                    including_pos: List[str] = [],
                    excluding_pos: List[str] = []):
    
    articles = html_to_text(html_path)
    articles_preprocessed = [text_preprocess(tokenizer, article, min_len, including_pos, excluding_pos) for article in articles]

    result = {
        "min_len": min_len,
        "including_pos": including_pos,
        "excluding_pos": excluding_pos,
        "tokenized": articles_preprocessed
    }

    with open("articles_preprocessed.pkl", 'wb') as f:
        pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)



if __name__ == "__main__":

    tokenizer = Kiwi()

    save_tokenized_text("./articles/", 
                    tokenizer, 
                    min_len = 1,
                    including_pos = ["NNG", "MM", "NNP"],
                    excluding_pos = [])
    