import json
import os

to_fix = [
    3, 10, 13, 14, 24, 65, 71, 76, 81, 95, 98, 110, 117, 134, 138, 160, 163, 165, 199, 208, 212, 215, 234, 236, 249,
    256, 264, 274, 289, 290, 300, 302, 309, 314, 322, 325, 326, 336, 338, 346, 383, 384, 388, 398, 400, 402, 417,
    420, 449, 460, 43, 44, 17, 34, 57, 78, 80, 83, 88, 92, 97, 113, 133, 137, 141, 156, 168, 169, 170, 175, 180,
    181, 186, 195, 204, 210, 242, 245, 247, 250, 251, 252, 253, 261, 280, 288, 301, 303, 324, 332, 335, 337, 339,
    340, 358, 359, 404, 408, 411, 412, 422, 429, 447, 450, 42, 47, 48, 392, 461
]

with open("data/augmented/data_regen.json") as f:
    data = json.load(f)

with open("data/augmented/generated_m.json") as f:
    data_regen = json.load(f)

for i, doc_dir in enumerate(sorted(os.listdir('data/notags'))):
    if i in to_fix:
        data_regen[str(i)] = data[str(i)]

with open(f'data/augmented/generated_m.json', 'w') as f:
    json.dump(data_regen, f, indent=2)
