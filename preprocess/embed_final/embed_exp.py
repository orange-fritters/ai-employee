import ast
import numpy as np
import pandas as pd
import re
from preprocess.embedding.embed import get_embed


# columns = ['index', 'category', 'filename', 'title', 'overall_description',
#            'content_description', 'content_long_description', 'target_description',
#            'target_long_description', 'target_synonyms', 'content_synonyms',
#            'keyword', 'summary', 'title_eng', 'summary_eng', 'keywords_eng']


def check_english(string: str):
    if re.search("[\uac00-\ud7a3]", string) or re.match("^[\W]+$", string):
        return False
    else:
        return True


def make_doc():
    df = pd.read_csv("preprocess/emed_final/emed_final.csv")

    df['target_synonyms'] = df['target_synonyms'].apply(ast.literal_eval)
    df['content_synonyms'] = df['content_synonyms'].apply(ast.literal_eval)
    df['keywords_eng'] = df['keywords_eng'].apply(lambda x: x.split(", "))

    final = pd.DataFrame(columns=['index', 'category', 'filename', 'title', 'document'])
    for i, row in df.iterrows():
        title = row['title_eng']
        category = row['category_eng']
        summary = row['summary_eng']
        contents = row['content_long_description']
        target = row['target_long_description']
        keywords = row['keywords_eng'] + row['target_synonyms'] + row['content_synonyms']

        doc = f"""
    Book:
        ```Welfare Service Guidebook```

    Title :
        ```{title}```

    Category :
        ```{category}```

    Summary :
        ```{summary}```

    Contents :
        ```{contents}```

    Target :
        ```{target}```

    Keywords :
        ```{keywords}```
        """
        final.loc[i] = [i, category, row['filename'], title, doc]

    final.to_csv("preprocess/emed_final/final_.csv", index=False)


def convert_query_english(query: str):
    content = f"""
    Translate the following Korean sentence into English.
    
    Korean:
        ```{query}```
    Output:
        ```
        {{ translation: }}
    """
    return [{"role": "user", "content": content}]


if __name__ == '__main__':
    df = pd.read_csv("preprocess/emed_final/final.csv")
    qs = pd.read_csv("preprocess/augment_qa/qa_data_eng.csv")

    query = qs.sample(1).reset_index(drop=True)
    q_eng = query['question_eng'][0]
    title = query['title'][0]

    q_embed, t, p = get_embed(q_eng)
    q_embed = np.array(q_embed)  # 1536, 1

    df['title_embed'] = df['title_embed'].apply(ast.literal_eval)
    title_embed = np.array(df['title_embed'].tolist())  # 462, 1536

    sim = np.dot(title_embed, q_embed)  # 462, 1
    sim = sim.reshape(-1)  # 462
    top_5 = np.argsort(sim)[-5:][::-1]

    top_5_title = df.loc[top_5]['title_kor'].tolist()
    print(f"질문: {q_eng}")
    print(f"제목: {title}")

    for i, t in enumerate(top_5_title):
        print(f"{i + 1}번째 유사도: {sim[top_5[i]]:.3f}")
        print(f"{i + 1}번째 제목: {t}")
        print()
