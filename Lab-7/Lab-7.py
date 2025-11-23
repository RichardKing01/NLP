import itertools
import copy
import math
import random

import copy
import math

def Divider(Data, Validation: int, Test: int):
    Train_Set = copy.deepcopy(Data[:len(Data) - (Validation + Test)])
    Validation_Set = copy.deepcopy(Data[len(Data) - (Validation + Test): len(Data) - Test])
    Test_Set = copy.deepcopy(Data[len(Data) - Test:])
    return Train_Set, Validation_Set, Test_Set


def PMI_Bigram(Validate, Test, G1=None, G2=None):
    Dict_Valid = {}
    Dict_Test = {}

    for item in Validate:
        try:
            Dict_Valid[item] = (G2.get(item, 0) * sum(G1.values())) / (G1[item[0]] * G1[item[1]])
        except:
            Dict_Valid[item] = 0

    for item in Test:
        try:
            Dict_Test[item] = (G2.get(item, 0) * sum(G1.values())) / (G1[item[0]] * G1[item[1]])
        except:
            Dict_Test[item] = 0

    return Dict_Test, Dict_Valid


def TF_IDF(Gram=1, Test=None, Set=None, L1=None, L2=None, L3=None, L4=None):
    L = {1: L1, 2: L2, 3: L3, 4: L4}[Gram]

    def Grammafy(Set, Gram):
        Set_Gramafied = []
        for sentence in Set:
            Gramafied = []
            for i in range(len(sentence) - (Gram - 1)):
                s = tuple(sentence[i:i + Gram])
                Gramafied.append(s)
            Set_Gramafied.append(Gramafied)
        return Set_Gramafied

    Test_Gram = Grammafy(Test, Gram)
    Set_Grammafied = Grammafy(Set, Gram)

    TF_IDF_set = {}
    Sum = sum(L.values())

    # Flatten Set_Grammafied so we can get unique grams
    unique_grams = set(it for sent in Set_Grammafied for it in sent)

    for g in unique_grams:
        TF = L.get(g, 0) / Sum
        Count = sum([1 for sentence in Test_Gram if g in sentence])
        IDF = (len(Test_Gram) + 1) / (1 + Count)
        IDF = math.log(IDF)
        TF_IDF_set[g] = TF * IDF

    return TF_IDF_set, Set_Grammafied


def Vectorize(Gram=1, Test=None, Set=None, L1=None, L2=None, L3=None, L4=None):
    TF_IDF_Set, Set_Grammafied = TF_IDF(Gram, Test, Set, L1=L1, L2=L2, L3=L3, L4=L4)

    Vectors = []
    for sentence in Set_Grammafied:
        Vectored_Sentence = []
        for g in sentence:
            Vectored_Sentence.append(TF_IDF_Set.get(g, 0))
        Vectors.append(Vectored_Sentence)

    return Vectors


def Nearest_Neighbor(Gram=1, Test=None, Set=None, L1=None, L2=None, L3=None, L4=None):
    Vectors = Vectorize(Gram, Test, Set, L1=L1, L2=L2, L3=L3, L4=L4)

    Nearest = {}

    def cosine(a, b):
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        if na == 0 or nb == 0:
            return 0
        return dot / (na * nb)

    for i in range(len(Vectors)):
        Best = None
        Best_Grade = float('-inf')
        for j in range(len(Vectors)):
            if j != i:
                Grade = cosine(Vectors[i], Vectors[j])
                if Grade > Best_Grade:
                    Best = j
                    Best_Grade = Grade
        Nearest[i] = Best

    return Nearest
