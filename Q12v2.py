import itertools
import copy
import random

def NGram(Gram: int = 1, Paragraph: list = None, Smoothing = None):
    L_List = []
    G_List = []

    if Paragraph is None:
        return

    # --- Unigrams ---
    if Gram >= 1:
        Gram_1 = {}
        total = 0
        for sentence in Paragraph:
            for word in sentence:
                Gram_1[word] = Gram_1.get(word, 0) + 1
                total += 1

        Count_1 = copy.deepcopy(Gram_1)
        for k in Gram_1:
            Gram_1[k] = Gram_1[k] / total

        L_List.append(Count_1)
        G_List.append(Gram_1)

    # --- Bigrams ---
    if Gram >= 2:
        Gram_2 = {}
        for sentence in Paragraph:
            for i in range(len(sentence)-1):
                s = tuple(sentence[i:i+2])
                Gram_2[s] = Gram_2.get(s, 0) + 1

        Count_2 = copy.deepcopy(Gram_2)
        for k in Gram_2:
            Gram_2[k] = Gram_2[k] / Count_1.get(k[0], 1)

        L_List.append(Count_2)
        G_List.append(Gram_2)

    # --- Trigrams ---
    if Gram >= 3:
        Gram_3 = {}
        for sentence in Paragraph:
            for i in range(len(sentence)-2):
                s = tuple(sentence[i:i+3])
                Gram_3[s] = Gram_3.get(s, 0) + 1

        Count_3 = copy.deepcopy(Gram_3)
        for k in Gram_3:
            Gram_3[k] = Gram_3[k] / Count_2.get(k[:2], 1)

        L_List.append(Count_3)
        G_List.append(Gram_3)

    # --- Quadgrams ---
    if Gram >= 4:
        Gram_4 = {}
        for sentence in Paragraph:
            for i in range(len(sentence)-3):
                s = tuple(sentence[i:i+4])
                Gram_4[s] = Gram_4.get(s, 0) + 1

        Count_4 = copy.deepcopy(Gram_4)
        for k in Gram_4:
            Gram_4[k] = Gram_4[k] / Count_3.get(k[:3], 1)

        L_List.append(Count_4)
        G_List.append(Gram_4)

    # --- Apply Smoothing if Provided ---
    if Smoothing is not None:
        L1, G1 = L_List[0], G_List[0]
        L2 = L3 = L4 = None
        G2 = G3 = G4 = None
        if Gram >= 2:
            L2, G2 = L_List[1], G_List[1]
        if Gram >= 3:
            L3, G3 = L_List[2], G_List[2]
        if Gram >= 4:
            L4, G4 = L_List[3], G_List[3]

        Smoothing(Gram=Gram, L1=L1, L2=L2, L3=L3, L4=L4,
                  G1=G1, G2=G2, G3=G3, G4=G4, Data=None)

    return L_List, G_List

import itertools

def Good_Turing_Smoothing_Known(Gram=1, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None):
    # Select the correct dictionary
    L = {1: L1, 2: L2, 3: L3, 4: L4}[Gram]

    if Data not in L:
        return None

    C_MLE = L[Data]
    Nc = sum(1 for val in L.values() if val == C_MLE)
    Nc_1 = sum(1 for val in L.values() if val == C_MLE + 1)
    C_star = (C_MLE + 1) * (Nc_1 / Nc) if Nc != 0 else 0
    return (C_MLE, Nc, Nc_1, C_star)


def Good_Turing_Smoothing(Gram=1, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None):
    Dict = {}
    print(Data)
    if Data is None:
        return -1

    words_in_data = []
    for sentence in Data:
        for word in sentence:
            words_in_data.append(word)
    U = set(words_in_data)

    V = len(L1)

    N = sum(L1.values()) if Gram == 1 else sum(L2.values()) if Gram == 2 else sum(L3.values()) if Gram == 3 else sum(L4.values())
    N1 = sum(1 for val in (L1.values() if Gram == 1 else L2.values() if Gram == 2 else L3.values() if Gram == 3 else L4.values()) if val == 1)

    if Gram == 1:
        P = N1 / (N * (V - len(U)))
        for word in U:
            if word not in G1.keys():
                G1[word] = P
    else:
        V_n = len(L1.keys()) ** Gram
        P = (N1 / N) / (V_n - N)

        if Gram == 2:
            for sentence in Data:
                for i in range(len(sentence) - 1):
                    bigram = tuple(sentence[i:i + 2])
                    if bigram not in G2.keys():
                        Dict[bigram] = P
                    else:
                        Dict[bigram] = -1

        elif Gram == 3:
            for sentence in Data:
                for i in range(len(sentence) - 2):
                    trigram = tuple(sentence[i:i + 3])
                    if trigram not in G3.keys():
                        Dict[trigram] = P
                    else:
                        Dict[trigram] = -1

        elif Gram == 4:
            for sentence in Data:
                for i in range(len(sentence) - 3):
                    quadrigram = tuple(sentence[i:i + 4])
                    if quadrigram not in G4.keys():
                        Dict[quadrigram] = P
                    else:
                        Dict[quadrigram] = -1

    return Dict

def Deleted_Interpolated_Smoothing(Gram=4, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None):
    if Gram < 4:
        return

    l1, l2, l3, l4 = 1,1,1,1

    Quadrigrams = []
    PQ = {}
    for sentence in Data:
        for i in range(len(sentence)-3):
            Quadrigrams.append(sentence[i: i + 4])

    best_lambdas = None
    best_log_likelihood = -float('inf')

    for lambda4 in [0.0,0.1,...,1.0]:
        for lambda3 in [0.0,0.1,...,1.0-l1]:
            for lambda2 in [0.0,0.1,...,1.0-l1-l2]:
                lambda1 = 1.0 - l1 - l2 - l3
                log_likelihood = 0
                for Q in Quadrigrams:
                    P1 = G1.get(Q[3], Good_Turing_Smoothing(Gram=1, L1=L1, G1=G1, Data=[[Q[3]]]))
                    P2 = G2.get(tuple(Q[2:4]), Good_Turing_Smoothing(Gram=2, L1=L1, L2=L2, G2=G2, Data=[Q[2:4]]))
                    P3 = G3.get(tuple(Q[1:4]), Good_Turing_Smoothing(Gram=3, L1=L1, L2=L2, L3=L3, G3=G3, Data=[Q[1:4]]))
                    P4 = G4.get(tuple(Q), Good_Turing_Smoothing(Gram=4, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2 = G2, G3 = G3, G4=G4, Data=[Q]))

                    P_interp = lambda4*P4 + lambda3*P3 + lambda2*P2 + lambda1*P1
                    PQ[tuple(Q)] = P_interp
                    total += np.log(P_interp)
                if log_likelihood > best_log_likelihood:
                    best_log_likelihood = log_likelihood
                    best_lambdas = (l1,l2,l3,l4)
    return best_lambdas

import copy

def Divider(Data, Validation: int, Test: int):

    Train_Set = copy.deepcopy(Data[:len(Data) - (Validation + Test)])
    Validation_Set = copy.deepcopy(Data[len(Data) - (Validation + Test) : len(Data) - Test])
    Test_Set = copy.deepcopy(Data[len(Data) - Test:])

    return Train_Set, Validation_Set, Test_Set

