import json
import re
import os

with open('data/summary/missing.json') as file:
    data = json.load(file)

# 1.
# "요약: " "요약: \n" --> "요약:\n"
# for key, value in data.items():
#     if value['summary'].startswith('요약: '):
#         value['summary'] = value['summary'].replace('요약: ', '요약:\n')
#     elif value['summary'].startswith('요약: \n'):
#         value['summary'] = value['summary'].replace('요약: \n', '요약:\n')

# 2.
# \n\n --> \n
# for key, value in data.items():
#     data[key]['summary'] = value['summary'].replace('\n\n', '\n')

# with open('data/summary/summary_m.json', 'w') as file:
#     json.dump(data, file, indent=4, ensure_ascii=False)

# 3.

# for key, value in data.items():
#     summary = value['summary'].split('키워드:')[0].split('요약:')[1]
#     keywords = value['summary'].split('키워드:')[1]

#     # split keywords by \d. plus space
#     keywords = re.split(r'\d+\. ', keywords)
#     processed = []
#     for kw in keywords:
#         if kw == '\n' or kw == '':
#             continue
#         for w in kw.split('#'):
#             if re.match(r'[a-zA-Z]+', w):
#                 continue
#             if re.match(r'\d+', w):
#                 continue
#             if len(w) > 30:
#                 continue
#             if len(w.split(',')) > 2:
#                 for ww in w.split(','):
#                     processed.append(ww.strip())

#             processed.append(w.strip())

#     data[key]['summary_processed'] = summary.strip()
#     data[key]['keywords'] = processed

# with open('data/summary/missing_m.json', 'w') as file:
#     json.dump(data, file, indent=2, ensure_ascii=False)
