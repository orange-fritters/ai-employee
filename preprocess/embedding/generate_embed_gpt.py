import openai
import os
import numpy as np
import tiktoken
import json
import time


def get_embedding(text):
    # 1535 elems as list
    result = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=text,)
    return result["data"][0]["embedding"]


if __name__ == "__main__":
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    embed_encoding = tiktoken.encoding_for_model("text-embedding-ada-002")

    with open("server/config.json") as config_file:
        config_data = json.load(config_file)
        openai.api_key = config_data["chatgpt"]["secret"]

    embed_dict = {}
    embeddings = []
    for i, filename in enumerate(sorted(os.listdir('data/articles'))):
        with open('data/articles/' + filename, 'r') as f:
            text = f.read()
            title = text.split('<span style="font-weight: bold">')[1].split('</span>')[0].strip()

        if i % 10 == 0:
            print("title : ", title,  " Progress: " + str(i / len(os.listdir('data/articles')) * 100) + "%")

        embed = get_embedding(text)
        embeddings.append(embed)
        embed_elem = {
            "index": i,
            "filename": filename,
            "title": title,
            "embedding": embed,
            "text": text,
            "tokens": len(encoding.encode(text)),
            "embed_tokens": len(embed_encoding.encode(text))
        }
        embed_dict[i] = embed_elem
        time.sleep(1)

    embeddings = np.array(embeddings)
    np.save('data/embeddings.npy', embeddings)
    with open('data/embeddings.json', 'w') as f:
        json.dump(embed_dict, f, indent=2)
