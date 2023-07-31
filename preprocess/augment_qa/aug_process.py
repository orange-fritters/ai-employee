import json
import pandas as pd


def pp_rec():
    with open('preprocess/augment_qa/rec_data.json', 'r') as f:
        data = json.load(f)

    convert = {}
    for key, value in data.items():
        filename = value["desc"]["filename"]
        title = value["desc"]["title"]
        index = value["desc"]["index"]
        category = value["desc"]["category"]
        quesiton = value["data"]["translation"]
        convert[index] = {
            "filename": filename,
            "title": title,
            "index": index,
            "category": category,
            "question": quesiton,
        }

    df = pd.DataFrame.from_dict(convert, orient='index')
    df.to_csv("preprocess/augment_qa/rec_data.csv", index=False)


def pp_qa():
    with open('preprocess/augment_qa/qa_data.json', 'r') as f:
        data = json.load(f)

#   "0": {
#     "data": {
#       "changed_title_eng": "Emergency Care Service by Social Service Center",
#       "changed_title_kor": "사회서비스원 긴급돌봄 서비스",
#       "question_eng": "Who are the target beneficiaries of the Emergency Care Service provided by the Social Service Center?",
#       "question_kor": "사회서비스원이 제공하는 긴급돌봄 서비스의 대상 수혜자는 누구인가요?"
#     },
#     "desc": {
#       "filename": "기타지원_01.html",
#       "title": "사회서비스원 긴급돌봄 사업",
#       "index": 0,
#       "category": "기타지원",
#       "version": "gpt-3.5-turbo"
#     }
#   },

    convert = {}
    for key, value in data.items():
        filename = value["desc"]["filename"]
        title = value["desc"]["title"]
        index = value["desc"]["index"]
        category = value["desc"]["category"]
        quesiton = value["data"]["question_kor"]
        question_eng = value["data"]["question_eng"]
        convert[index] = {
            "filename": filename,
            "title": title,
            "index": index,
            "category": category,
            "question": quesiton,
            "question_eng": question_eng,
        }

    df = pd.DataFrame.from_dict(convert, orient='index')
    df.to_csv("preprocess/augment_qa/qa_data_eng.csv", index=False)


if __name__ == "__main__":
    pp_qa()
    # pp_rec()
