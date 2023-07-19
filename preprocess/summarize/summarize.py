import json
import openai
import os
import tiktoken
import random


def count_tokens(text: str):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))


def count_all_tokens(system: str,
                     assistant: str,
                     user: str):
    prompt_tokens = 0
    prompt_tokens += count_tokens(system)
    prompt_tokens += count_tokens(assistant)
    prompt_tokens += count_tokens(user)
    print(prompt_tokens)


def get_response_openai(system: str,
                        assistant: str,
                        user: str):
    prompt_tokens, generated_tokens = 0, 0

    prompt_tokens += count_tokens(system)
    prompt_tokens += count_tokens(assistant)
    prompt_tokens += count_tokens(user)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant",
                 "content": assistant},
                {"role": "user",
                 "content": user},
                {"role": "system",
                 "content": system},
            ],
            presence_penalty=1.2
        )
    except Exception as e:
        print(e)
        return None, None

    generated_tokens += count_tokens(response['choices'][0]['message']['content'])
    price_dollar = (prompt_tokens * 0.0015 + generated_tokens * 0.002) / 1000
    price = f'{prompt_tokens+generated_tokens} tokens {price_dollar:.2f}$ {price_dollar * 1227:.2f}WON'
    return response['choices'][0]['message']['content'], price


if __name__ == "__main__":
    with open('server/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    openai.api_key = config['chatgpt']['secret']

    # SYSTEM = f"""
    #     You are an AI summarizer.
    #     You are given a document about introduction of welfare service in Korean.
    #     Summary must contain the main points of the document, such as
    #     the purpose of the service, the target of the service, and the contents of the service.
    #     After the summary, extract the keywords of the document and mark them with hashtags.
    #     Do not include very general keywords.
    #     Include only the keywords that are very specific to the service.
    #     For better search it is recommeded to include the synonyms of the keywords.
    #     You don't have to include very specific details in summarization.
    #     Do not include indicators, generate just the texts.

    #     Output:
    #     Three to Four sentences of summary including target, purpose and contents of the service.
    #     #keywords #of #the #document #in #Korean #language #with #synonyms
    #     """
    SYSTEM = """
        Summarize the document with three sentence including the target, purpose and support of the service.
        Then, append the 10 specific keywords of the document with 5 synonyms.
        Do not include the way to apply for the service and the way to use it.
        
        Check the summary and keywords in Korean.
        Double check summarization plus 10 keyword with 5 synonyms in Korean.
        """
    ASSISTANT = ""
    USER = f"""
        Output Format:
        \"""
        요약: 
        Three  sentences of summary including target, purpose and support of the service.
        
        키워드:
        1. keyword1 #synonym1 #synonym2 #synonym3 #synonym4 #synonym5
        2. keyword2 #synonym1 s#ynonym2 sy#nonym3 syn#onym4 syno#nym5
        ...
        10. keyword10 #synonym1 #synonym2 #synonym3 #synonym4 #synonym5
        \"""
        No location or phone number never at the keywords.
        Write the summary of the document in Korean and append the keywords.
        Write every keywords with 5 synonyms.
        """
    with open("data/embeds/embeddings_notag.json") as file:
        embeddings = json.load(file)

    summary_dict = {}
    for i, article in enumerate(sorted(os.listdir('data/notags'))):
        ASSISTANT = ""
        with open(f'data/notags/{article}', 'r', encoding='utf-8') as f:
            ASSISTANT += f.read()[:]

        response, price = get_response_openai(SYSTEM, ASSISTANT, USER)
        if response is None:
            continue

        summary_dict[article] = {
            "filename": embeddings[str(i)]['filename'],
            "title": embeddings[str(i)]['title'],
            "index": i,
            "summary": response,
        }

        print(f'{i} {article} {price}')
        print(response)
        print()

        with open('data/summary/some_file.json', 'w', encoding='utf-8') as f:
            json.dump(summary_dict, f, indent=4, ensure_ascii=False)
