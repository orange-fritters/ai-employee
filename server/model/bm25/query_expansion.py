from typing import List, Dict

def drop_stopword(query: List[str]):

    stopword = ["지원", "서비스", "신청", "대상", "내용", "방법", "복지", "경우", "기준", "가능", "문의", "구분", "확인", "포함", "해당",
            "도움", "문제", "제공", "제도", "대상자", "혜택", "수혜자", "어느", "어떤", "얼마", "구체", "목적"]
    
    word_list = []
    for word in query:
        if word not in stopword:
            word_list.append(word)
        
    if len(word_list) <= 1:
        word_list.append("None")

    return word_list


def add_similar_word(query: List[str], similar_word_dict: Dict[str, List[str]]):

    word_list = []

    for word in query:
        if word in similar_word_dict.keys():
            word_list.append(similar_word_dict[word])

    word_list = sum(word_list, [])

    return query, word_list


def weight_original_word(query: List[str], similar_word: List[str], w: int = 3):
    return query * 3 + similar_word
 

def query_expand(query: List[str], similar_word_dict: Dict[str, List[str]]):
    query = drop_stopword(query)
    query, similar_word = add_similar_word(query, similar_word_dict)
    query = weight_original_word(query, similar_word)

    return query














