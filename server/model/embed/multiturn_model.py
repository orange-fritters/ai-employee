import ast
import json
import logging
import numpy as np
import pandas as pd
from typing import List

import openai
from openai import ChatCompletion, OpenAIError

import model.embed.embed_prompt as get_prompt
import model.embed.exceptions as exceptions
from model.utils.schemas import History, RankTitle, Recommendation, Option
from model.embed.embed_base import EmbedBase


class MultiTurn(EmbedBase):
    """Model for embedding translation and scoring"""

    MODEL_KEY_FILE = "model/files/config.txt"
    OPENAI_MODEL = "gpt-3.5-turbo"
    EMBEDDING_ENGINE = "text-embedding-ada-002"
    DOCUMENT_FILE_PATH = "model/files/processed_doc.csv"

    def __init__(self):
        """
        Initialize the model.

        self.data: A pandas dataframe containing the processed documents.
        self.embed: A numpy array containing the document embeddings.

        """
        openai.api_key_path = self.MODEL_KEY_FILE
        self.data = pd.read_csv(self.DOCUMENT_FILE_PATH)
        self.embed = np.array(self.data['title_embed'].apply(ast.literal_eval).to_list())

    def get_score(self,
                  query: str) -> np.array:
        """ Get the similarity scores between the query and the documents using translation and embedding."""
        query_eng = self._translate_query_to_english(query)
        query_embed = self._generate_embeddings(query_eng)
        query_embed = np.array(query_embed)  # 1536, 1
        sim = np.dot(self.embed, query_embed).reshape(-1)  # 462, 1
        return sim

    def get_question_from_history(self,
                                  titles: List[RankTitle],
                                  history: List[History]):
        """ Generate a question from the chat history. """
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

    def get_answer_from_history(self,
                                titles: List[RankTitle],
                                history: List[History]) -> str:
        """ Generate an answer from the chat history. """
        current_options = self.get_contents_from_title(titles)
        prompt = get_prompt.get_recommend_from_history(current_options, history)
        try:
            response = ChatCompletion.create(
                model=self.OPENAI_MODEL,
                messages=prompt,
                temperature=0
            )
            answer = response['choices'][0]['message']['content']
            answer = json.loads(answer)['answer']

            return answer

        except OpenAIError as e:
            logging.error(f"Decision failed with error: {str(e)}")
            raise exceptions.AnsweringFailedError("Answering failed.") from e

    def get_recommendation_new_history(self,
                                       history: List[History]) -> List[Recommendation]:
        """ Get new top 5 recommendations from the chat history. """
        translated_history = ""
        for conversation in history:
            role = conversation.role
            query = conversation.content
            query_eng = self._translate_query_to_english(query)
            translated_history += f"{role}: {query_eng}\n"
        embed = self._generate_embeddings(translated_history)
        embed = np.array(embed)  # 1536, 1
        sim = np.dot(self.embed, embed).reshape(-1)  # 462, 1
        top_n_index = sim.argsort()[::-1][:5]
        top_titles = self.data.loc[top_n_index]['title_kor'].tolist()
        print("new recommendation: ", top_titles)
        return [{"rank": i, "title": title} for i, title in enumerate(top_titles)]

    def decide_information_sufficiency(self,
                                       titles: List[RankTitle],
                                       history: List[History],
                                       ) -> bool:
        """ Decide whether the information of conversation is sufficient for recommendation or not. """
        # titles : [RankTitle(title='title_of_service', rank=0), RankTitle...]
        # history : [History(role='uesr', content='query_from_user'), History...]
        options = self.get_contents_from_title(titles)
        prompt = get_prompt.get_sufficiency_decision_prompt(options, history)
        try:
            response = ChatCompletion.create(
                model=self.OPENAI_MODEL,
                messages=prompt
            )
            response = response['choices'][0]['message']['content']
            response = json.loads(response)
            print(response)
            yes_or_no = response['sufficient']
            return yes_or_no == "yes" or yes_or_no == "Yes"

        except OpenAIError as e:
            logging.error(f"Decision failed with error: {str(e)}")
            raise exceptions.DecisionFailedError("Failed to decide the sufficiency.") from e

    def get_contents_from_title(self,
                                titles: List[RankTitle],
                                ):
        """ From the ranked titles, get the contents of the documents. """
        # titles : [RankTitle(title='title_of_service', rank=0), RankTitle...]
        title_of_ranked_list = [title.title for title in titles]
        rank_df = self.data[self.data["title_kor"].isin(title_of_ranked_list)]

        options: List[Option] = []
        for i, row in rank_df.iterrows():
            title = row["title_kor"]
            contents = row["document"].split("Summary :")[1].split("Keywords :")[0]
            # filename = row["filename"]
            # with open(os.path.join('articles', filename), 'r') as f:
            #     contents = f.read()
            options.append(Option(title=title, content=contents))
        return options
