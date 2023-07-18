import json

with open("data/augmented/data_regen.json") as f:
    data = json.load(f)

for key, value in data.items():
    print(value['filename'])
    print(value['response'])
    print()
