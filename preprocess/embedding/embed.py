"""
1. benchmark set 만들기
- 요약
- 키워드
- notag 전문

의 조합 1 2 3 12 13 23 123 7가지 경우로 soft voting.
"""
from typing import List
import openai
import json
import os
import pandas as pd
import tiktoken

with open('server/model/utils/config.json') as config_file:
    config_data = json.load(config_file)
    openai.api_key = config_data["chatgpt"]["secret"]


def count_money(texts: List[str], encoder: tiktoken.Encoding):
    # $0.0001 / 1K tokens
    token_counts = 0
    for text in texts:
        token_counts += len(encoder.encode(text))
    price = token_counts * 0.0001 / 1000
    return token_counts, price


def get_embedding(texts: List[str], encoder: tiktoken.Encoding):
    token_counts, price = count_money(texts, encoder)
    result = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=texts)
    return result["data"][0]["embedding"], token_counts, price


if __name__ == "__main__":
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    info_sheet = pd.read_csv('server/model/info_sheet.csv')

    embeddings = {}
    df = pd.DataFrame(columns=['title', 'article', 'summary', 'keywords', 'article_summary',
                      'article_keywords', 'summary_keywords', 'article_summary_keywords'])
    for i, row in info_sheet.iterrows():
        article_notag = row['article_notag']
        summary = row['summary']
        keywords = row['keywords']
        title = row['title']

        with open(article_notag, 'r', encoding='utf-8') as f:
            article_notag = f.read()

        nt, tc_nt, p_nt = get_embedding([article_notag], encoding)
        s, tc_s, p_s = get_embedding([summary], encoding)
        kw, tc_kw, p_kw = get_embedding([keywords], encoding)
        nt_s, tc_nt_s, p_nt_s = get_embedding([article_notag, summary], encoding)
        nt_kw, tc_nt_kw, p_nt_kw = get_embedding([article_notag, keywords], encoding)
        s_kw, tc_s_kw, p_s_kw = get_embedding([summary, keywords], encoding)
        nt_s_kw, tc_nt_s_kw, p_nt_s_kw = get_embedding([article_notag, summary, keywords], encoding)

        total_token_counts = tc_nt + tc_s + tc_kw + tc_nt_s + tc_nt_kw + tc_s_kw + tc_nt_s_kw
        total_price = p_nt + p_s + p_kw + p_nt_s + p_nt_kw + p_s_kw + p_nt_s_kw

        print(f"[{i}/462] Token : {total_token_counts}, Price: ${total_price} {total_price * 1300}원")

        embeddings[title] = {
            'article': nt,
            'summary': s,
            'keywords': kw,
            'article_summary': nt_s,
            'article_keywords': nt_kw,
            'summary_keywords': s_kw,
            'article_summary_keywords': nt_s_kw
        }

        df.loc[i] = [title, article_notag, summary, keywords, nt_s, nt_kw, s_kw, nt_s_kw]

        with open('preprocess/embedding/embeddings.json', 'w', encoding='utf-8') as f:
            json.dump(embeddings, f, ensure_ascii=False, indent=4)

        df.to_csv('preprocess/embedding/embeddings.csv', index=False, encoding='utf-8-sig')

        if i == 10:
            with open(f'preprocess/embedding/backups/embeddings_{i}.json', 'w', encoding='utf-8') as f:
                json.dump(embeddings, f, ensure_ascii=False, indent=4)
            df.to_csv(f'preprocess/embedding/backups/embeddings_{i}.csv', index=False, encoding='utf-8-sig')
