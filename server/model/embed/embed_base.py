import logging
import numpy as np

import openai
from openai import ChatCompletion, Embedding, OpenAIError

from model.embed.embed_prompt import get_translation_prompt, get_sufficiency_decision_prompt
from model.embed.exceptions import TranslationFailedError, EmbeddingFailedError


class EmbedBase:
    MODEL_KEY_FILE = "model/files/config.txt"
    OPENAI_MODEL = "gpt-3.5-turbo"
    EMBEDDING_ENGINE = "text-embedding-ada-002"

    def __init__(self):
        openai.api_key_path = self.MODEL_KEY_FILE

    def get_recommendations(self,
                            query: str,
                            top_k: int = 5) -> list:
        try:
            translated_query = self._translate_query_to_english(query)
            query_embeddings = self._generate_embeddings(translated_query)

            similarity_scores = self._calculate_similarity(self.docs_arr,
                                                           query_embeddings)

            top_5_indices = similarity_scores.argsort()[-top_k:][::-1]
            top_titles = self.data.iloc[top_5_indices]['title_kor'].tolist()
            return [{"rank": i + 1, "title": title} for i, title in enumerate(top_titles)]

        except (TranslationFailedError, EmbeddingFailedError) as e:
            logging.error(f"Failed to generate recommendations due to: {str(e)}")
            return [{"rank": i + 1, "title": "다시 시도해주세요."} for i in range(5)]

    def _translate_query_to_english(self,
                                    query: str) -> str:
        prompt = get_translation_prompt(query)
        try:
            response = ChatCompletion.create(
                model=self.OPENAI_MODEL,
                messages=prompt,
                temperature=0.0,
            )
            translated = response['choices'][0]['message']['content']
            return translated
        except OpenAIError as e:
            logging.error(f"Translation failed with error: {str(e)}")
            raise TranslationFailedError("Failed to translate the query.") from e

    def _generate_embeddings(self,
                             text: str) -> list:
        try:
            result = Embedding.create(
                engine=self.EMBEDDING_ENGINE,
                input=text
            )
            embeded_list = result["data"][0]["embedding"]
            return embeded_list
        except openai.error.InvalidRequestError as e:
            logging.error(f"Translation failed with error: {str(e)}")
            raise TranslationFailedError("Wrong translation format.") from e
        except OpenAIError as e:
            logging.error(f"Embedding creation failed with error: {str(e)}")
            raise EmbeddingFailedError("Failed to create the embedding.") from e

    def _calculate_similarity(self,
                              docs_embeddings: np.array,
                              query_embeddings: np.array) -> np.array:
        query_embeddings_array = np.array(query_embeddings)
        return np.dot(docs_embeddings, query_embeddings_array).reshape(-1)
