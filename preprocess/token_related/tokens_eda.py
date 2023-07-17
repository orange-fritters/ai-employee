import pandas as pd

df = pd.read_csv('preprocess/token_related/token_count.csv')

df = df.sort_values(by=['tokens'], ascending=False)
print(df.to_html('preprocess/token_related/token_count.html'))

df = df.sort_values(by=['notag_token'], ascending=False)
print(df.to_html('preprocess/token_related/token_count_notag.html'))
