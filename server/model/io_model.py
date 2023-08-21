from typing import List
import openai
import json
import pandas as pd
import os

from model.utils.schemas import Option, RankTitle


class IOModel:
    DOCUMENT_FILE_PATH = "model/files/processed_doc.csv"

    def __init__(self,
                 info_dir: str,
                 article_eng_dir: str = "model/files/articles_eng.parquet",
                 info_sheet_dir: str = "model/files/info_sheet.csv"):
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        openai.api_key = OPENAI_API_KEY

        self.name = 'Model'
        self.data = pd.read_csv(info_dir)
        self.article_eng = pd.read_parquet(article_eng_dir)
        self.info_sheet = pd.read_csv(info_sheet_dir)
        self.titles_total_list = self.data['title'].tolist()
        self.doc_data = pd.read_csv(self.DOCUMENT_FILE_PATH)


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
        try:
            return json.dumps(str(self.data[self.data['title'] == title]['summary'].item()))

        except Exception as e:
            print(e)
            return json.dumps("다시 시도해주세요.")

    def get_keywords(self, filename: str):
        return self.data[self.data['filename'] == filename]['keywords'].tolist()

    def get_article_notag(self, filename: str):
        return self.data[self.data['filename'] == filename]['article_notag']

    def get_article_tag(self, filename: str):
        return self.data[self.data['filename'] == filename]['article_tag']
    
    def get_contents_from_title(self,
                                titles: List[RankTitle],
                                ):
        """ From the ranked titles, get the contents of the documents. """
        # titles : [RankTitle(title='title_of_service', rank=0), RankTitle...]
        title_of_ranked_list = [title.title for title in titles]
        rank_df = self.doc_data[self.doc_data["title_kor"].isin(title_of_ranked_list)]

        options: List[Option] = []
        for i, row in rank_df.iterrows():
            title = row["title_kor"]
            contents = row["document"].split("Summary :")[1].split("Keywords :")[0]
            options.append(Option(title=title, content=contents))
        return options

