from typing import List, TypedDict
import tiktoken


class Option(TypedDict):
    # options = [{"title": ..., "content": ...}, ...]
    title: str
    content: str


class History(TypedDict):
    # history = [{"role" : "user", "content" : ...},
    #            {"role" : "bot", "content" : ...}, ...]
    role: str
    content: str


class Recommendation(TypedDict):
    rank: int
    title: str


def process_options_qa(options: List[Option]):
    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = 0
    options_str = ""
    for i, option in enumerate(options):
        string_to_add = f"Option {i + 1} <{option['title']}>: {option['content']}"
        tokens += len(tokenizer.encode(string_to_add))
        if tokens > 16000:
            break
        options_str += string_to_add
    return options_str


def process_options_history(options: List[Option],
                            history: List[History]):
    options_str = ""
    for i, option in enumerate(options):
        options_str += f"Option {i + 1} <{option['title']}>: {option['content']}"

    history_str = ""
    for conversation in history:
        history_str += "\n".join(f"{key}: {value}" for key, value in conversation.items())

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


def get_sufficiency_decision_prompt(options: List[Option],
                                    history: List[History],
                                    ):
    # history = [{"user" : ...}, {"bot": ...}, ...]
    # options = [{"title": ..., "content": ...}, ...]
    options_str, history_str = process_options_history(options, history)

    system = """
You are an AI assistant who can analyze and make recommendations based on provided information. 
In this task, you have been given a set of options and a query stemming from a conversation. 
Your responsibility is to analyze the given data and determine if the information is enough to recommend just one item from the options.
"""
    assistant1 = f"Options:\n``` {options_str} ```"
    assistant2 = f"History:\n``` {history_str} ```"
    user = """
Based on these details, is the information sufficient to recommend only one item? 
Respond with 'yes' or 'no' only.
"""
    prompt = [{"role": "system", "content": system},
              {"role": "assistant", "content": assistant1},
              {"role": "assistant", "content": assistant2},
              {"role": "user", "content": user}]
    return prompt


def get_question_from_history(options: List[Option],
                              history: List[History]):
    options_str, history_str = process_options_history(options, history)
    system = f"""
You are an AI assistant who can analyze and generate new question to collect more information from the user.
In this task, you have been given a set of options and a history of a conversation. 
Given the current information isn't sufficient, 
your task is to generate a new question to ask the user in order to gather more information to decide best option for the user. 
This new question should be relevant to the options and the query you have. 
"""
    assistant1 = f"Options:\n``` {options_str} ```"
    assistant2 = f"History:\n``` {history_str} ```"
    user = """
Based on these details and considering the information is not sufficient to recommend only one item, 
what additional question would you ask the user to gain more relevant information?

Output as json format:
{
    "question": "..."
}
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
You are an AI assistant who can analyze and answer the query from context.
In this task, you have been given a query and a set of options.
Your task is to generate an answer to the query based on the options.
"""
    assistant1 = f"Options:\n``` {options_str} ```"
    assistant2 = f"Query:\n``` {query} ```"
    user = """
Based on these details, what would be your answer to the query?
Answer in Korean politely.
Answer must be based on the options given.
Do not use any external resources.
"""
    prompt = [{"role": "system", "content": system},
              {"role": "assistant", "content": assistant1},
              {"role": "assistant", "content": assistant2},
              {"role": "user", "content": user}]
    return prompt
