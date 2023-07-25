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

    df = pd.read_csv('preprocess/embedding/info_sheet.csv')
    title_dir_map = {}
    for i, row in df.iterrows():
        title_dir_map[row['title']] = i

    with open('preprocess/title_id.json', 'w', encoding='utf-8') as f:
        json.dump(title_dir_map, f, ensure_ascii=False, indent=2)
