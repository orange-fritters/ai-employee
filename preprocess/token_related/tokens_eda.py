import pandas as pd

df = pd.read_csv('preprocess/token_related/token_count.csv')

# df = df.sort_values(by=['tokens'], ascending=False)
# print(df.to_html('preprocess/token_related/token_count.html'))

# df = df.sort_values(by=['notag_token'], ascending=False)
# print(df.to_html('preprocess/token_related/token_count_notag.html'))

# print(df['tokens'].sum())

sum = 0
for row in df.iterrows():
    sum += (row[1]['tokens'] * 0.0015 + 200 * 0.002) / 1000

print(sum, "dollars ", sum * 1267.14, " won")
