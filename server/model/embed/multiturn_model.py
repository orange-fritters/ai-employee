import ast
import logging
import numpy as np
import pandas as pd
from typing import Dict, List
import re

import openai
from openai import ChatCompletion, OpenAIError

from model.embed.embed_base import EmbedBase
from model.embed.embed_prompt import get_sufficiency_decision_prompt
from model.embed.exceptions import DecisionFailedError


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

    def get_recommendation_based_on_history(self, history):
        pass

    def generate_question_based_on_history(self, history):
        pass

    def update_options_based_on_new_info(self, options, user_response):
        pass

    def __decide_information_sufficiency(self,
                                         options: list,
                                         history: list,
                                         ) -> bool:
        prompt = get_sufficiency_decision_prompt(options, history)
        try:
            response = ChatCompletion.create(
                model=self.OPENAI_MODEL,
                messages=prompt,
            )
            yes_or_no = response['choices'][0]['message']['content']
            return yes_or_no == "yes"

        except OpenAIError as e:
            logging.error(f"Decision failed with error: {str(e)}")
            raise DecisionFailedError("Failed to decide the sufficiency.") from e

    def __get_contents_from_title(self,
                                  titles: List[Dict],
                                  ):
        # [{"rank": i + 1, "title": title} for i, title in enumerate(top_titles)]
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
