from typing import Dict, List


def get_multiturn_prompt(target_explanation: str,
                         history: str,
                         user_input: str) -> List[Dict[str, str]]:
    prompt = [
        {"role": "assistant",
         "content":
            f"""
            target : {target_explanation}
            """},
        {"role": "assistant",
         "content":
            f"""
            history : {history}
            """},
        {"role": "user", "content": user_input},
        {"role": "system", "content": f"""
            You are a counselor to answer the question from the user. 
            You should re-ask a question to pick one service to recommend. 
            Write a question to ask a  counsellee to get more information and verify which might fit him most.
            Question should be in Korean.
            Reference the previous history and (1) ask more or (2) choose service and explain.
            You should never use information that is not in the above passage.
            What is your response to the question?
         """},
    ]

    return prompt


def get_answer_from_document(document: str, query: str):
    prompt = f"""
    오로지 아래 내용에만 기반하여 질문에 대해 답해주십시오.
    내용에 없는 내용은 생성하지 말아주십시오.

    ### 내용 :
    {document}

    ### 질문 :
    {query}
    """
    return prompt


def get_summary(target: str, content: str, title: str):
    prompt = f"""
    ### 대상 : {target}
    ### 내용 : {content}
          {title}의 대상과 내용에 대해 쉬운 말로 세 문장 이내로 요약하시오.
        - 마침표 이후에는 \n을 사용하시오.
        - 오로지 요약문만 출력하시오.
        - 문의 방법은 절대 포함하지 마시오.
        - 존댓말을 사용하시오 (습니다. 입니다. ~입니다.)
    """
    return prompt


def get_recommendation(query: str, title_string: str):
    prompt = [
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
    return prompt


def get_translated_query(query: str):
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
    return prompt_message
