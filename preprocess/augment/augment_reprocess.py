import os
import re
import json


# Check it worked
with open("data/augmented/final.json") as f:
    data = json.load(f)

for key, value in data.items():
    print(value['index'])
    print(value['questions'])

# 162,
exit()

# 1. replace '\n\n' with '\n'.
for key, value in data.items():
    data[key]['response'] = value['response'].replace('\n\n', '\n')


# 2. Regex
for key, value in data.items():
    data[key]['response'] = re.sub(r'Situation\s\d+:\s', '', value['response'])
    data[key]['response'] = re.sub(r'Scenario\s\d+:\s', '', value['response'])
    data[key]['response'] = re.sub(r'상황\s\d+:\s', '', value['response'])
    data[key]['response'] = re.sub(r'사례\s\d+:\s', '', value['response'])

# 2. Replace
for key, value in data.items():
    data[key]['response'] = value['response'].replace('"', '')
    data[key]['response'] = value['response'].replace('상황: ', '')
    data[key]['response'] = value['response'].replace('상황 ', '')
    data[key]['response'] = value['response'].replace('상담자: ', '')
    data[key]['response'] = value['response'].replace('상담 받는 사람: ', '')
    data[key]['response'] = value['response'].replace('상담받는 사람: ', '')
    data[key]['response'] = value['response'].replace('상담 수신자 상황: ', '')
    data[key]['response'] = value['response'].replace('상담자님, ', '')
    data[key]['response'] = value['response'].replace('상담자에게: ', '')
    data[key]['response'] = value['response'].replace('상담자 상황: ', '')
    data[key]['response'] = value['response'].replace('상담자에게 말하기: ', '')
    data[key]['response'] = value['response'].replace('상담 대상자: ', '')
    data[key]['response'] = value['response'].replace('상담 대상: ', '')
    data[key]['response'] = value['response'].replace('상담 속 상황: ', '')
    data[key]['response'] = value['response'].replace('코언셜리: ', '')
    data[key]['response'] = value['response'].replace('상담 대상자 상황: ', '')
    data[key]['response'] = value['response'].replace('상담 대상자의 상황: ', '')
    data[key]['response'] = value['response'].replace('Situation: ', '')
    data[key]['response'] = value['response'].replace('Counsellee: ', '')
    data[key]['response'] = value['response'].replace('Counsellee의 상황: ', '')
    data[key]['response'] = value['response'].replace('Counsellee\'s Situation: ', '')
    data[key]['response'] = value['response'].replace('상담 받는 사람의 상황: ', '')
    data[key]['response'] = value['response'].replace('상담 받는 이 : ', '')
    data[key]['response'] = value['response'].replace('상담 수신인 상황: ', '')

    data[key]['response'] = value['response'].replace(':', '.')

    data[key]['response'] = re.sub(r'[a-zA-Z]', '', value['response'])


# 6. numbering
# to_replace = []
# for key, value in data.items():
#     lines = value['response'].strip().split('\n')
#     if len(lines) != 5:
#         to_replace.append(int(key))

# # 7. manual correction
# weird = [13, 17, 34, 57, 65, 76, 78, 80, 81, 83,
#          88, 92, 95, 97, 113, 133, 137, 141, 156, 160,
#          168, 169, 170, 175, 180, 181, 186, 195, 204,
#          210, 215, 236, 242, 245, 247, 249, 250, 251, 252, 253,
#          256, 261, 274, 280, 288, 290, 300, 301, 303, 309,
#          314, 322, 324, 325, 326, 332, 335, 336, 337, 339,
#          340, 358, 359, 383, 402, 404, 408, 411, 412, 417,
#          422, 429, 447, 450, 42, 43, 47, 48, 392, 461
#          ]

# for w in weird:
#     if not w in to_replace:
#         to_replace.append(int(w))

# saving the data
with open(f'data/augmented/generated_m.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open(f'data/augmented/generated_m.json', 'r') as f:
    data = json.load(f)
