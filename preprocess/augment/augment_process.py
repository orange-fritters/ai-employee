import os
import re
import json

with open("data/augmented/data_regen.json") as f:
    data = json.load(f)

# 1. replace '\n\n' with '\n'.
for key, value in data.items():
    data[key]['response'] = value['response'].replace('\n\n', '\n')

# 2. delete the word between '권장 서비스: ' to '\n' using regex.
for key, value in data.items():
    data[key]['response'] = re.sub(r'권장 서비스: .*?\n', '\n', value['response'])
    data[key]['response'] = data[key]['response'].replace('권장 서비스: ', '')

# 3. delete the word "상황 {number}: " using regex, not between but all.
for key, value in data.items():
    data[key]['response'] = re.sub(r'상황 \d+:\s*', '', value['response'])
    data[key]['response'] = re.sub(r'\d+:\s*', '', value['response'])
    data[key]['response'] = re.sub(r'추천: .*?\.', '', value['response'])
    data[key]['response'] = re.sub(r'권장.*?\n', '', value['response'])
    data[key]['response'] = re.sub(r'추천 서비스: .*?\n', '', value['response'])
    data[key]['response'] = re.sub(r'권장: *?\.', '\n', value['response'])
    data[key]['response'] = re.sub(r'Situation \d+:', '\n', value['response'])
    data[key]['response'] = re.sub(r':.*?서비스', '', value['response'])

# 4. delete the word between \d. and ':' using regex.
for key, value in data.items():
    data[key]['response'] = re.sub(r'\d\..*?:', '\n', value['response'])
    data[key]['response'] = value['response'].replace('\n\n', '\n')

# 5. delete the english using regex.
for key, value in data.items():
    data[key]['response'] = re.sub(r'[a-zA-Z]', '', value['response'])

# 6. Special case
for key, value in data.items():
    data[key]['response'].replace('권장: 지진 보험', '\n')
    data[key]['response'].replace('추천 서비스: 저비용 치과 클리닉 프로그램', '\n')
    data[key]['response'].replace('서비스 ', '')
    data[key]['response'].replace('서비스 권장: 노인 동반자 프로그램', '\n')
    data[key]['response'].replace(' 국한없이 번역', '')
    data[key]['response'].replace('상담대상자의 상황: ', '')
    data[key]['response'].replace('긴급 재정 지원 프로그램', '')
    data[key]['response'].replace(': ', '')
    data[key]['response'].replace('상담자님, ', '')
    data[key]['response'].replace('낚시', '어업')
    data[key]['response'].replace('상담자의 대답을 제외하고 상담을 받는 사람의 상황을 추출합니다.', '')
    data[key]['response'].replace(' 이 상담말고,', '')
    data[key]['response'].replace('\n상황: ', '')
    data[key]['response'].replace('고문 받는 사람의 상황: ', '')
    data[key]['response'].replace('상담 받는 사람의 상황: ', '')
    data[key]['response'].replace('나의 상황: ', '')
    data[key]['response'].replace('   어린이의 도전적인 행동에 대한 양육 교육 및 지원.', '')


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

print(to_replace)
