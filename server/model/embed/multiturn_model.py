import ast
import json
import logging
import numpy as np
import pandas as pd
from typing import List
import re

import openai
from openai import ChatCompletion, OpenAIError

import model.embed.embed_prompt as get_prompt
import model.embed.exceptions as exceptions
from model.embed.embed_prompt import Option, History, Recommendation
from model.embed.embed_base import EmbedBase


class MultiTurn(EmbedBase):
    """Model for embedding translation and scoring"""

    MODEL_KEY_FILE = "model/files/config.txt"
    OPENAI_MODEL = "gpt-3.5-turbo"
    EMBEDDING_ENGINE = "text-embedding-ada-002"
    DOCUMENT_FILE_PATH = "model/files/processed_doc.csv"

    def __init__(self):
        openai.api_key_path = self.MODEL_KEY_FILE
        self.data = pd.read_csv(self.DOCUMENT_FILE_PATH)
        self.docs_arr = np.array(self.data['title_embed'].apply(ast.literal_eval).to_list())
        self.embed = np.array(self.data['title_embed'].apply(ast.literal_eval).to_list())

    def get_score(self,
                  query: str) -> np.array:
        query_eng = self._translate_query_to_english(query)
        query_embed = self._generate_embeddings(query_eng)
        query_embed = np.array(query_embed)  # 1536, 1
        sim = np.dot(self.embed, query_embed).reshape(-1)  # 462, 1
        return sim

    def get_recommendation_new_history(self,
                                       history: List[History]) -> List[Recommendation]:
        translated_history = ""
        for conversation in history:
            role = conversation["role"]
            query = conversation["content"]
            query_eng = self._translate_query_to_english(query)
            translated_history += f"{role}: {query_eng}\n"
        embed = self._generate_embeddings(translated_history)
        embed = np.array(embed)  # 1536, 1
        sim = np.dot(self.embed, embed).reshape(-1)  # 462, 1
        top_n_index = sim.argsort()[::-1][:5]
        top_titles = self.data.loc[top_n_index]['title_kor'].tolist()

        return [{"rank": i + 1, "title": title} for i, title in enumerate(top_titles)]

    def generate_question_based_on_history(self,
                                           titles: List[str],
                                           history: List[History]):
        current_options = self.get_contents_from_title(titles)
        prompt = get_prompt.get_question_from_history(current_options, history)
        try:
            response = ChatCompletion.create(
                model=self.OPENAI_MODEL,
                messages=prompt,
            )
            question = response['choices'][0]['message']['content']
            question = json.loads(question)['question']

            return question

        except OpenAIError as e:
            logging.error(f"Decision failed with error: {str(e)}")
            raise exceptions.QuestionGenerationFailedError("Failed to decide the sufficiency.") from e

    def decide_information_sufficiency(self,
                                       titles: List[str],
                                       history: List[History],
                                       ) -> bool:
        options = self.get_contents_from_title(titles)
        prompt = get_prompt.get_sufficiency_decision_prompt(options, history)
        try:
            response = ChatCompletion.create(
                model=self.OPENAI_MODEL,
                messages=prompt,
            )
            yes_or_no = response['choices'][0]['message']['content']
            return yes_or_no == "yes"

        except OpenAIError as e:
            logging.error(f"Decision failed with error: {str(e)}")
            raise exceptions.DecisionFailedError("Failed to decide the sufficiency.") from e

    def get_contents_from_title(self,
                                titles: List[str],
                                ):
        title_of_ranked_list = [title["title"] for title in titles]
        rank_df = self.data[self.data["title_kor"].isin(title_of_ranked_list)]

        options = []
        for i, row in rank_df.iterrows():
            title = row['title']
            content = re.search(r'Contents :(.*?)Target :', row['document']).group(1)
            target = re.search(r'Target :(.*?)Keywords :', row['document']).group(1)
            doc = {"title": title, "content": content, "target": target}
            options.append(doc)

        return options
