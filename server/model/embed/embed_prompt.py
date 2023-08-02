from typing import List, DefaultDict


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


def get_sufficiency_decision_prompt(options: List[DefaultDict],
                                    history: List[DefaultDict],
                                    ):
    options_str = "\n".join(f"Option {i + 1} <{key}>: {value}" for i, (key, value) in enumerate(options.items()))
    history_str = "\n".join(f"{key}: {value}" for key, value in history.items())
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
