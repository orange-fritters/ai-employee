from typing import List
import tiktoken
from model.utils.schemas import History, Option


def process_options_qa(options: List[Option]):
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = 0
    options_str = ""
    for i, option in enumerate(options):
        string_to_add = f"Option {i + 1} <{option.title}>: {option.content}"
        tokens += len(tokenizer.encode(string_to_add))
        if tokens > 16000:
            break
        options_str += string_to_add
    return options_str


def process_options_history(options: List[Option],
                            history: List[History]):
    # options = [Option(title="title", content="content"), ...]
    # history = [History(role="user", content="content"), ...]
    options_str = ""
    for i, option in enumerate(options):
        options_str += f"<{option.title}>: {option.content}\n\n"

    history_str = ""
    for conversation in history:
        history_str += "\n".join([f"{conversation.role}: {conversation.content}"])

    return options_str, history_str


def get_translation_prompt(query: str):
    prompt = [{"role": "user", "content": f"""
        Translate the following Korean sentence into English.
        
        Korean:
            ```{query}```
        Output:
            ```
            {{ translated output }}
            ```
        """}]
    return prompt


def process_option_get_title(options: List[Option]):
    title_str = ""
    for i, option in enumerate(options):
        title_str += f"{option.title}, "


def get_sufficiency_decision_prompt(options: List[Option],
                                    history_str: str,
                                    ):
    # options = [{"title": ..., "content": ...}, ...]
    # history = [{"user" : ...}, {"bot": ...}, ...]
    title_str = process_option_get_title(options)
    options_str = process_options_qa(options)

    system = """
You are an AI assistant.
In this task, you have been given a set of options and a conversation. 
Your responsibility is to score 0-1 whether information in the Converation is sufficient to recommend one service from the options.
Score generous.
    1.0 : One of the option exactly fits the user.
    0.66 : At least one option is possible.
    0.33 : We need to ask more questions.
    0.0 : No option is possible.
"""
    assistant1 = f"Options:\n``` {options_str} ```"
    assistant2 = f"Conversation:\n``` {history_str} ```"
    user = f"""
Based on the conversation, is one of {title_str} best fit to the user?

You are a JSON answer bot. Don't answer other words.
Answer format is JSON 
{{
    "reason": "reason for your decision"
    "sufficiency": {{ 0~1 }}
}}

"""
    prompt = [{"role": "assistant", "content": assistant1},
              {"role": "assistant", "content": assistant2},
              {"role": "system", "content": system},
              {"role": "user", "content": user}]
    return prompt


def get_question_from_history(options: List[Option],
                              history: List[History]):
    options_str, history_str = process_options_history(options, history)
    system = f"""
You are an AI assistant.
In this task, you have been given a set of options and a history of a conversation. 
Given the current information isn't sufficient, 
your task is to generate a new question to ask the user in order to gather more information to decide best option for the user. 
This new question should be relevant to the options and the query you have. 
"""
    assistant1 = f"Options:\n``` {options_str} ```"
    assistant2 = f"Conversation:\n``` {history_str} ```"
    user = """
Based on these details and considering the information is not sufficient to recommend only one item, 
what additional question would you ask the user to gain more relevant information?
If the last conversaiton user answered is a question, you can answer it based on the options given.

You are a JSON answer bot. Don't answer other words. Output as json format:
{
    "reason": "reason for the decision",
    "response": "..."
}

Answer in Korean politely.
"""
    prompt = [{"role": "system", "content": system},
              {"role": "assistant", "content": assistant1},
              {"role": "assistant", "content": assistant2},
              {"role": "user", "content": user}]

    return prompt


def get_answer_from_history(options: List[Option],
                            history: List[History]):
    options_str, history_str = process_options_history(options, history)
    system = f"""
You are an AI assistant.
In this task, you have been given a set of options and a history of a conversation. 
Your task is recommending one service to user based on the information from conversation. 
This recommendation should be relevant to the options and the conversation you referenced. 
"""
    assistant1 = f"Options:\n``` {options_str} ```"
    assistant2 = f"Conversation:\n``` {history_str} ```"
    user = """
Recommend one service to user based on the conversation.

You are a JSON answer bot. Don't answer other words. Output as json format:
{
    "reason": "reason for the decision",
    "response": "..."
}

Answer in Korean politely.
"""
    prompt = [{"role": "system", "content": system},
              {"role": "assistant", "content": assistant1},
              {"role": "assistant", "content": assistant2},
              {"role": "user", "content": user}]

    return prompt


def get_answer_from_question(query: str,
                             options: List[Option]):
    options_str = process_options_qa(options)
    system = f"""
You are an AI assistant.
In this task, you have been given a query and a set of options.
Your task is to generate an answer to the query based on the options.
"""
    assistant1 = f"Options:\n``` {options_str} ```"
    assistant2 = f"Query:\n``` {query} ```"
    user = """
Based on these details, answer the question based on the Conversation history?
Answer in Korean politely.
Answer must be based on the options given.
Do not use any external resources.
"""
    prompt = [{"role": "system", "content": system},
              {"role": "assistant", "content": assistant1},
              {"role": "assistant", "content": assistant2},
              {"role": "user", "content": user}]
    return prompt


def get_recommend_from_history(options: List[Option],
                               history: List[History]):
    options_str, history_str = process_options_history(options, history)
    system = f"""
You are an AI assistant who can analyze and recommend some item from the context and Options.
In this task, you have been given a conversatio history and a set of options.
Your task is to recommend one item using the conversatio history based on the options.
"""
    assistant1 = f"Options:\n``` {options_str} ```"
    assistant2 = f"Conversation History:\n``` {history_str} ```"
    user = f"""
Based on these details, what would you recommend from the options?
Answer in Korean politely.
Answer must be based on the options given.
Do not use any external resources.

You are a JSON answer bot. Don't answer other words.
Output as json format:
{{
    "reason": "reason for your decision",
    "answer" : "a suggestion from the options in sentence format"
}}

Answer in Korean politely.
"""
    prompt = [{"role": "system", "content": system},
              {"role": "assistant", "content": assistant1},
              {"role": "assistant", "content": assistant2},
              {"role": "user", "content": user}]
    return prompt
