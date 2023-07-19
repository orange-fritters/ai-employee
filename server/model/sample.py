import pandas as pd
import json


class Model:
    def __init__(self,
                 info_dir: str):
        self.name = 'Model'
        self.data = pd.read_csv(info_dir)

    def get_recommendation(self, query: str):
        titles = self.data.sample(5)["title"].tolist()
        response = [{"rank": i + 1, "title": title} for i, title in enumerate(titles)]
        return json.dumps(response)

    def get_filename(self, title: str):
        return self.data[self.data['title'] == title]['filename'].tolist()[0]

    def get_questions(self, filename: str):
        return self.data[self.data['filename'] == filename]['queries'].tolist()

    def get_summary(self, filename: str):
        return self.data[self.data['filename'] == filename]['summary']

    def get_keywords(self, filename: str):
        return self.data[self.data['filename'] == filename]['keywords'].tolist()

    def get_article_notag(self, filename: str):
        return self.data[self.data['filename'] == filename]['article_notag']

    def get_article_tag(self, filename: str):
        return self.data[self.data['filename'] == filename]['article_tag']
