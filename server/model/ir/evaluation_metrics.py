## hit rate
## hit rate by sim doc
## ndcg

from score_ensemble import ensemble
import numpy as np

def hr_k(models, weight, data, k):
    """
        models(list): model list  ex. [bm25, gpt ,,,]
        weight(list): weight list ex. [1, 2, 3]
        doc_sim(np.array): document similarity 
    """

    count = 0

    for key, value in data.items():
        index = value['index']
        questions = value['questions']

        for q in questions:
            score_list = [model.get_score(q) for model in models]
            score = ensemble(score_list, weight, type = "normalize")

            rank = score.argsort()[::-1].argsort()[index] + 1
            if rank <= k:
                count += 1
            
    return count / (len(data) * len(questions))

def hr_sim_k(models, weight, data, doc_sim, doc_sim_cnt, k):
    """
        models(list): model list  ex. [bm25, gpt ,,,]
        weight(list): weight list ex. [1, 2, 3]
        data(dict): article-query dataset
        doc_sim(np.array): document similarity 
        doc_sim_count(int): 고려할 similar doc의 개수
        k(int): 성능평가에 포함할 doc 개수
    """
    count = 0

    for key, value in data.items():

        index = value['index']
        questions = value['questions']

        top_n = doc_sim[index].argsort()[::-1][:doc_sim_cnt]

        for q in questions:
            score_list = [model.get_score(q) for model in models]
            score = ensemble(score_list, weight, type = "normalize")

            include = False

            for t in top_n:

                rank = score.argsort()[::-1].argsort()[t] + 1 ## index의 순위
                if rank <= k:
                    include = True

            if include:
                count += 1

    return count / (len(data) * len(questions))


def dcg(y_true, y_score, k = None, use_rank = False):
    discount = 1 / (np.log2(np.arange(len(y_true))+2))

    if k is not None:
        discount[k:] = 0

    if use_rank:
        y_true = y_true.argsort().argsort() 

    ranked = y_true[y_score.argsort()[::-1]]
    cum_gain = discount.dot(ranked.T)

    return cum_gain


def ndcg(y_true, y_score, k = None, use_rank = False):
    gain = dcg(y_true, y_score, k, use_rank)
    norm_gain = dcg(y_true, y_true, k, use_rank)

    gain /= norm_gain

    return gain



def ndcg_k(models, weight, data, doc_sim, k):

    ndcg_score = 0

    for key, value in data.items():
        index = value['index']
        questions = value['questions']
        answer = doc_sim[index]
        top_n = doc_sim[index].argsort()[::-1][:5]

        for q in questions:
            score_list = [model.get_score(q) for model in models]
            score = ensemble(score_list, weight, type = "normalize")
            ndcg_score += ndcg(answer, score, k)

    return ndcg_score / (len(data) * len(questions))


def eval_result(models, weight, data, doc_sim, doc_sim_cnt, k):
    eval_hr = hr_k(models, weight, data, k)
    eval_hr_sim = hr_sim_k(models, weight, data, doc_sim, doc_sim_cnt, k)
    eval_ndcg = ndcg_k(models, weight, data, doc_sim, k)

    return [eval_hr, eval_hr_sim, eval_ndcg]




    