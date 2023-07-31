import os
import json
import openai
import pandas as pd
from preprocess.augment_qa.aug_qa import get_response
openai.api_key_path = "config.txt"


def convert_prompt(document: str,
                   title: str):
    content = f"""
    Service:
    {document}
    Title:
    {title}

    You will be provided with a description of welfare services. 
    Perform the following actions:

    1 - Write one short overall description of the service.
    2 - Write one short sentence about the content of the service.
    3 - Write two to three sentences about the content of the service.
    4 - Write one short sentence about the target of the service.
    5 - Write two to three sentences about the target of the service.
    6 - Extract 10 keywords from the given target of the service in English.
    7 - Give 3 synonyms for each extracted keywords of the target in English.
    8 - Extract 10 keywords from the given content about the service in English.
    9 - Give 3 synonyms for each extracted keywords about the content in English.

    Output the final result in json format.

    Final format:
    {{
        "overall_description" : <overall description>,
        "content_description" : <content description>,
        "content_long_description" : <content long description>,
        "target_description" : <target description>,
        "target_long_description" : <target long description>,
        "target_keywords" : <target keywords as list>,
        "target_synonyms" : <target synonyms as json>,
        "content_keywords" : <content keywords as list>,
        "content_synonyms" : <content synonyms as json>,
    }},

    Quesion and translation must include the converted easy version title.
    """
    return [{"role": "user", "content": content}]


if __name__ == "__main__":
    missing = {"missing": []}
    with open("data/summary/summary.json", "r") as f:
        summary = json.load(f)

    df = pd.DataFrame(columns=["index",
                               "category",
                               "filename",
                               "title",
                               "overall_description",
                               "content_description",
                               "content_long_description",
                               "target_description",
                               "target_long_description",
                               "target_synonyms",
                               "content_synonyms",
                               "keyword",
                               "summary"])
    for i, filename in enumerate(sorted(os.listdir('data/articles'))):
        with open(f"data/articles/{filename}") as f:
            document = f.read()
        title = summary[filename]["title"]
        res, price, delay, ver = get_response(convert_prompt(document, title))

        try:
            df.loc[i] = [i,
                         filename.split("_")[0],
                         filename,
                         title,
                         json.loads(res)["overall_description"],
                         json.loads(res)["content_description"],
                         json.loads(res)["content_long_description"],
                         json.loads(res)["target_description"],
                         json.loads(res)["target_long_description"],
                         json.loads(res)["target_synonyms"],
                         json.loads(res)["content_synonyms"],
                         summary[filename]["keywords"],
                         summary[filename]["summary_processed"]]
        except json.decoder.JSONDecodeError:
            print(res)
            missing["missing"].append(i)
            with open("preprocess/emed_final/missing.json", "a") as f:
                json.dump(missing, f, indent=4)
            continue

        df.to_csv("preprocess/emed_final/emed_final.csv", index=False)

        print("Data: \n", res)
        print(f"[{i}/462] Price: {price:.2f} Time: {delay:.2f} Version: {ver} Title: {title} ")
        print()
