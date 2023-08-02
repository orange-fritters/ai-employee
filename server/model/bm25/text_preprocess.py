import re
from typing import List


def clean(text: str):
    text = re.sub('☎([0-9]+-?[0-9]+)', " ", text)
    text = re.sub('[^\w\s\n]', "", text)
    return text

def tokenize(tokenizer, 
            text: str,
            min_len: int = 1,
            including_pos: List[str] = [],
            excluding_pos: List[str] = []):
            
    tokenizer.prepare()
    tokenized_text = tokenizer.analyze(text)

    token = []
    tokenized = tokenized_text[0][0]

    if including_pos == []:
        for i in range(len(tokenized)):
            if tokenized[i][1] not in excluding_pos and len(str(tokenized[i][0])) >= min_len: 
                token.append(tokenized[i][0])
    else:
        for i in range(len(tokenized)):
            if tokenized[i][1] in including_pos and len(str(tokenized[i][0])) >= min_len: 
                token.append(tokenized[i][0])

    return token


def text_preprocess(tokenizer, 
                    text: str,
                    min_len: int = 1,
                    including_pos: List[str] = [],
                    excluding_pos: List[str] = []):
    
    text = clean(text)
    text = tokenize(tokenizer, text, min_len, including_pos, excluding_pos)

    return text
