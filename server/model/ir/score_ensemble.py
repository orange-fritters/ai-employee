from sklearn.preprocessing import normalize
import numpy as np

def ensemble(scores, weight, type =  None):
    ## scores: model output _ np.array (462,)

    ensembled = np.zeros_like(scores[0], dtype = float)

    if type == "normalize":
        scores = np.array(scores)
        scores = normalize(scores)

    elif type == "rank":
        scores = [score.argsort().argsort() for score in scores]

    for i in range(len(scores)):
        ensembled += scores[i] * weight[i]

    return ensembled