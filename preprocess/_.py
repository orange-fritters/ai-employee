import pandas as pd
import tiktoken
import json


def random_result(i):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    result = pd.read_parquet('preprocess/embedding/result.parguet')
    sample = result.iloc[i]

    question = sample['query']
    embed_titles = sample['embed_titles']

    info_sheet = pd.read_csv('preprocess/embedding/info_sheet.csv', encoding='utf-8')
    notags = info_sheet[info_sheet['title'].isin(embed_titles)]['article_notag'].tolist()

    targets = []
    try:
        for notag in notags:
            with open(notag, 'r', encoding='utf-8') as f:
                notag = f.read()
            targets.append(notag.split('1. 대상')[1].split('2. 내용')[0])
    except IndexError:
        with open(notags[0], 'r', encoding='utf-8') as f:
            notag = f.read()

    total_token_counts = 0
    total_token_counts += len(encoding.encode(question))
    for notag in notags:
        with open(notag, 'r', encoding='utf-8') as f:
            notag = f.read()
        total_token_counts += len(encoding.encode(notag))

    # print(f'총 토큰 수: {total_token_counts}')
    # print("대상:")
    # for title, target in zip(embed_titles, targets):
    #     print(f'<{title}>의 대상: {target}')
    # print()
    # print(f'질문: {question}')

    return question, total_token_counts


def count_tokens():
    result = pd.read_parquet('preprocess/embedding/result.parguet')

    tokens = pd.DataFrame(columns=['question', 'total_token_counts'])
    for i, row in enumerate(result.iterrows()):
        question, total_token_counts = random_result(i)
        new_row = {'question': question, 'total_token_counts': total_token_counts}
        tokens.loc[i] = new_row
        if i % 100 == 0:
            print(f'{i}번째 질문 완료')

    tokens.to_csv('preprocess/mt_tokens.csv', index=False)
    tokens.sort_values(by=['total_token_counts'], ascending=False, inplace=True)
    tokens.to_html('preprocess/mt_tokens.html')


if __name__ == '__main__':
    info = pd.read_csv("/content/drive/MyDrive/ai-employee/info_sheet.csv")
    title_index = dict(zip(info['title'], info['index']))

    articles = pd.read_parquet("/content/drive/MyDrive/ai-employee/articles_embed.parquet")
    queries = pd.read_parquet("/content/drive/MyDrive/ai-employee/query_embed.parquet")

    articles['label'] = articles['title'].apply(lambda x: title_index[x])

    labels = articles['label'].unique().tolist()

    # for queries with index not in labels, drop row
    queries = queries[queries['index'].isin(labels)]
