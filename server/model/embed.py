import openai
import json
import re
import pandas as pd
import numpy as np


class Model:
    def __init__(self,
                 info_dir: str,
                 config_dir: str = "model/utils/config.json",
                 article_eng_dir: str = "model/files/articles_eng.parquet",
                 info_sheet_dir: str = "model/info_sheet.csv"):
        self.name = 'Model'
        self.config = json.load(open(config_dir, 'r'))
        openai.api_key = self.config['chatgpt']['secret']

        self.data = pd.read_csv(info_dir)
        self.article_eng = pd.read_parquet(article_eng_dir)
        self.info_sheet = pd.read_csv(info_sheet_dir)
        self.titles_total_list = self.data['title'].tolist()

    def get_target(self, title: str):
        return self.data[self.data['title'] == title]['target'].tolist()[0]

    def get_content_target(self, title: str):
        content = self.article_eng[self.article_eng['title'] == title]['content'].tolist()[0]
        target = self.article_eng[self.article_eng['title'] == title]['target'].tolist()[0]
        return content, target

    def get_recommendation(self, query: str):
        titles = self.data.sample(5)["title"].tolist()
        response = [{"rank": i + 1, "title": title} for i, title in enumerate(titles)]
        return json.dumps(response)

    def get_filename(self, title: str):
        return self.data[self.data['title'] == title]['filename'].tolist()[0]

    def get_questions(self, filename: str):
        return self.data[self.data['filename'] == filename]['queries'].tolist()

    def get_summary(self, title: str):
        print(self.data[self.data['title'] == title]['summary'].item())
        return json.dumps(str(self.data[self.data['title'] == title]['summary'].item()))

    def get_keywords(self, filename: str):
        return self.data[self.data['filename'] == filename]['keywords'].tolist()

    def get_article_notag(self, filename: str):
        return self.data[self.data['filename'] == filename]['article_notag']

    def get_article_tag(self, filename: str):
        return self.data[self.data['filename'] == filename]['article_tag']

    def get_gpt_recommendation(self,
                               query: str):
        titles = self.__translate_query(query)
        title_string = " ,".join(titles)

        # prompt_message = [
        #     {"role": "system",
        #      "content": """
        #         - You are RankGPT, an intelligent assistant that can rank service based on their relevancy to the situation.
        #         """},
        #     {"role": "assistant",
        #      "content": f"The situation : {query} \n Services : {title_string}"
        #      },
        #     {"role": "user",
        #      "content": """
        #         - Among the given services, You have to rank the top three most relevant services to the situation.
        #         - Do not include prose or explanation, indicators, Only korean titles.
        #         - You must only contain services that the asker is able to benefit from.

        #         - Output must be in form of
        #         "
        #         { 1. Most relevant sercvice  }
        #         { 2. Second relevant sercvice }
        #         { 3. Third relevant sercvice }
        #         "

        #         - You only contain title from the Services given.
        #         """},
        # ]

        prompt_message = [
            {"role": "system",
             "content": """
                - You are RankGPT, an intelligent assistant that can rank service based on their relevancy to the situation.
                """},
            {"role": "assistant",
             "content": f"The situation : {query} \n Services : {title_string}"
             },
            {"role": "user",
             "content": """
                - Among the given services, You have to rank the top five most relevant services to the situation.
                - Do not include prose or explanation, indicators, Only korean titles.
                - You must only contain services that the asker is able to benefit from.
                
                - Output must be in form of 
                " 
                { 1. Most relevant sercvice  }
                { 2. Second relevant sercvice }
                ...
                { 5. Fifth relevant sercvice }
                "

                - You only contain title from the Services given.
                """},
        ]

        for _ in range(2):
            print("Recommendation Loop")
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=prompt_message,
                    temperature=0
                )
            except Exception as e:
                print(e)
                return json.dumps([{"rank": i + 1, "title": "Error"} for i, title in enumerate(titles)])

            response = response['choices'][0]['message']['content']

            response = response.split("\n")
            response = [r[3:].strip() for r in response]
            # response = [response[2], response[1], response[0]]
            if all(title in title_string and title in self.titles_total_list for title in response):
                break
        else:
            return json.dumps([{"rank": i + 1, "title": "Error"} for i, title in enumerate(titles)])

        recs = [{"rank": i + 1, "title": title} for i, title in enumerate(response)]
        return json.dumps(recs)

    def __translate_query(self,
                          query: str):
        prompt_message = [
            {"role": "system",
                "content": """
                    - You must translate the following sentence into English.
                    - Output only translation, No prose or explanation, indicators.
                    """},
            {"role": "assistant",
                "content": f"Translate {query} to english keeping the format."
             },
            {"role": "user",
                "content": """
                    - You are an Korean English translator. 
                    - Query is used for document search with embedding.
                    - You only contain information inside the query.
                    - Translation output must be in form of 
                    "The asker is { description of whom } is in situation of { situation }.
                    So the asker might need service for example { possible services } "
                    """},
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt_message,
                temperature=0
            )
        except:
            return "Error", 0

        translated = response['choices'][0]['message']['content']
        self.article_eng = self.article_eng.dropna(axis=0)
        self.article_eng['total_embed'] = self.article_eng['total_embed'].apply(lambda x: np.array(x))
        total_embed = np.array(self.article_eng['total_embed'].tolist())

        try:
            query_embed = openai.Embedding.create(
                engine="text-embedding-ada-002",
                input=[translated])
        except Exception as e:
            print(e)
            return ["Error"]*10, 0

        query_embed = np.array(query_embed["data"][0]["embedding"]).reshape(-1, 1)
        similarity = np.dot(total_embed, query_embed).reshape(-1)
        top_10_idx = np.argsort(similarity)[-10:]
        return self.article_eng.iloc[top_10_idx]['title'].values.tolist()
