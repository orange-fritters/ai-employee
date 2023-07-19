import json
import re


def check_format(text):
    lines = text.split('\n\n')
    try:
        # Check the format of the summary
        if not lines[0].startswith('요약:'):
            print('Invalid format: Missing 요약')
            return False

        # Check the format of the keyword section
        if not lines[1].startswith('키워드:'):
            print('Invalid format: Missing 키워드:')
            return False

        # Check the format of the keywords
        keyword_pattern = re.compile(r'\d+\. .*(#\w+ )+#\w+')
        for line in lines[2:]:
            if not keyword_pattern.match(line):
                print(f'Invalid keyword format: {line}')
                return False
    except:
        return False
        # If no issues are found, return True
    return True


with open('data/summary/summary.json') as file:
    summary = json.load(file)

count = 0
for key, value in summary.items():
    if not check_format(value['summary']):
        print(key)
        print(value['summary'])
        print()
        count += 1

print(f'Total: {count}')
