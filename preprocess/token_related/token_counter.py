import tiktoken
import os
import csv

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

token_count_csv = open('preprocess/token_count.csv', 'w')
token_count_writer = csv.writer(token_count_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
token_count_writer.writerow(['title', 'tokens', 'notag_token'])

for i, filename in enumerate(sorted(os.listdir('data/articles'))):
    with open('data/articles/' + filename, 'r') as f:
        text = f.read()
        title = text.split('<span style="font-weight: bold">')[1].split('</span>')[0].strip()

    tokens = len(encoding.encode(text))

    with open(f'data/articles/{filename}'.replace('articles', 'notags'), 'r') as f:
        notag_token = len(encoding.encode(f.read()))

    print("title :", title, " tokens: ", tokens, " notag_token: ", notag_token)
    token_count_writer.writerow([title, tokens, notag_token])
