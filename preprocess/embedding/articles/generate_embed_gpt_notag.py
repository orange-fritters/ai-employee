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

    with open("server/config.json") as config_file:
        config_data = json.load(config_file)
        openai.api_key = config_data["chatgpt"]["secret"]

    embed_dict = {}
    embeddings = []
    for i, filename in enumerate(sorted(os.listdir('data/notags'))):
        with open('data/embeds/embeddings.json', 'r') as f:
            embed_dict = json.load(f)
            title = embed_dict[str(i)]["title"]

        with open('data/notags/' + filename, 'r') as f:
            text = f.read()

        if i % 10 == 0:
            print("title : ", title,  " Progress: " + str(i / len(os.listdir('data/notags')) * 100) + "%")

        embed = get_embedding(text)
        embeddings.append(embed)
        embed_elem = {
            "index": i,
            "filename": filename,
            "title": title,
            "tokens": len(encoding.encode(text)),
            "embedding": embed,
            "text": text,
        }
        embed_dict[i] = embed_elem
        time.sleep(0.5)

    embeddings = np.array(embeddings)
    np.save('data/embeds/embeddings_notag.npy', embeddings)
    with open('data/embeds/embeddings_notag.json', 'w') as f:
        json.dump(embed_dict, f, indent=2)
