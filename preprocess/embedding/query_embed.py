import pandas as pd
import json
import openai


with open('server/model/utils/config.json') as config_file:
    config_data = json.load(config_file)
    openai.api_key = config_data["chatgpt"]["secret"]


def get_embedding(text):
    result = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=text)
    return result["data"][0]["embedding"]


with open('data/augmented/final.json', 'r', encoding='utf-8') as f:
    embeddings = json.load(f)

df = {}
index = 0
for k, value in embeddings.items():
    for query in embeddings[k]['questions']:
        index += 1
        if (index < 1590):
            continue
        embed = get_embedding(query)
        row = {
            'index': value['index'],
            'query': query,
            'embedding': embed
        }
        df[index] = row

        with open('preprocess/embedding/query_embed_back.json', 'w', encoding='utf-8') as f:
            json.dump(df, f, ensure_ascii=False, indent=2)

    print(f"[{index} | {462 * 5}] ")
