import os
import re
import pandas as pd


def prettify():
    # Specify the directory
    directory = 'server/articles'
    data = []

    # List all files in the directory
    for filename in sorted(os.listdir(directory)):
        # Check if the file is an HTML file
        if filename.endswith('.html'):
            inpath = os.path.join(directory, filename)

            # Open the file and read its contents
            with open(inpath, 'r', encoding='utf-8') as f:
                content = f.read()

            sections = re.split('1. 대상|2. 내용|3. 방법|4. 문의', content)
            if len(sections) >= 5:
                data.append([filename] + sections[1:5])  # Ignore the first section as it is the content before "1. 대상"

    # Create a DataFrame and write it to a parquet file
    df = pd.DataFrame(data, columns=['filename', 'target', 'content', '방법', '문의'])
    df = df[['filename', 'target', 'content']]
    df.to_csv('server/articles_m.csv')


def process():
    csv_file = pd.read_csv('server/articles_m.csv')
    data = []
    for i, row in csv_file.iterrows():
        # Remove HTML tags
        title = row['filename']
        clean_target = re.sub('<.*?>', '', row['target'])
        clean_content = re.sub('<.*?>', '', row['content'])

        # Reduce multiple spaces to one
        clean_target = ' '.join(clean_target.split())
        clean_content = ' '.join(clean_content.split())
        data.append([title, clean_target, clean_content])

    df = pd.DataFrame(data, columns=['filename', 'target', 'content'])
    df.to_parquet('server/articles.parquet')
    df.to_csv('server/articles.csv')


if __name__ == '__main__':
    prettify()
    # process()
