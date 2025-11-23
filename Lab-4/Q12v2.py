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

def Laplace_Smooth(Gram=1, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None):
    V = list(L1.keys())
    V_size = len(V)

    if Data is None:  # Apply to whole corpus
        if Gram >= 2:
            for Bi in L2.keys():
                G2[Bi] = (L2.get(Bi, 0) + 1) / (L1.get(Bi[0], 0) + V_size)
        if Gram >= 3:
            for Tri in L3.keys():
                G3[Tri] = (L3.get(Tri, 0) + 1) / (L2.get(Tri[:-1], 0) + V_size)
        if Gram >= 4:
            for Quad in L4.keys():
                G4[Quad] = (L4.get(Quad, 0) + 1) / (L3.get(Quad[:-1], 0) + V_size)

    else:  # Apply to new sentence/unseen n-gram
        if Gram == 1:
            word = Data[0]
            return (L1.get(word, 0) + 1) / (sum(L1.values()) + V_size)
        elif Gram == 2:
            bigram = tuple(Data)
            return (L2.get(bigram, 0) + 1) / (L1.get(bigram[0], 0) + V_size)
        elif Gram == 3:
            trigram = tuple(Data)
            return (L3.get(trigram, 0) + 1) / (L2.get(trigram[:-1], 0) + V_size)
        elif Gram == 4:
            quadgram = tuple(Data)
            return (L4.get(quadgram, 0) + 1) / (L3.get(quadgram[:-1], 0) + V_size)


def AddK_Smooth(Gram=1, k=0.5, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None):
    V = list(L1.keys())
    V_size = len(V)

    if Data is None:
        if Gram >= 2:
            for Bi in L2.keys():
                G2[Bi] = (L2.get(Bi, 0) + k) / (L1.get(Bi[0], 0) + k * V_size)
        if Gram >= 3:
            for Tri in L3.keys():
                G3[Tri] = (L3.get(Tri, 0) + k) / (L2.get(Tri[:2], 0) + k * V_size)
        if Gram >= 4:
            for Quad in L4.keys():
                G4[Quad] = (L4.get(Quad, 0) + k) / (L3.get(Quad[:3], 0) + k * V_size)
    else:
        if Gram == 1:
            word = Data[0]
            return (L1.get(word, 0) + k) / (sum(L1.values()) + k * V_size)
        elif Gram == 2:
            bigram = tuple(Data)
            return (L2.get(bigram, 0) + k) / (L1.get(bigram[0], 0) + k * V_size)
        elif Gram == 3:
            trigram = tuple(Data)
            return (L3.get(trigram, 0) + k) / (L2.get(trigram[:2], 0) + k * V_size)
        elif Gram == 4:
            quadgram = tuple(Data)
            return (L4.get(quadgram, 0) + k) / (L3.get(quadgram[:3], 0) + k * V_size)


# Edit Denom instead of vsize should k * unique bigrams starting with wn-1
def TokenType_Smooth(Gram=1, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None):
    V = list(L1.keys())
    Vsize = len(V)

    if Data is None:
        if Gram >= 2:
            for Bi in L2.keys():
                G2[Bi] = (L2.get(Bi, 0) + Vsize) / (L1.get(Bi[0], 0) + Vsize)
        if Gram >= 3:
            for Tri in L3.keys():
                G3[Tri] = (L3.get(Tri, 0) + Vsize) / (L2.get(Tri[:-1], 0) + Vsize)
        if Gram >= 4:
            for Quad in L4.keys():
                G4[Quad] = (L4.get(Quad, 0) + Vsize) / (L3.get(Quad[:-1], 0) + Vsize)
    else:
        if Gram == 1:
            word = Data[0]
            return (L1.get(word, 0) + Vsize) / (sum(L1.values()) + Vsize)
        elif Gram == 2:
            bigram = tuple(Data)
            return (L2.get(bigram, 0) + Vsize) / (L1.get(bigram[0], 0) + Vsize)
        elif Gram == 3:
            trigram = tuple(Data)
            return (L3.get(trigram, 0) + Vsize) / (L2.get(trigram[:2], 0) + Vsize)
        elif Gram == 4:
            quadgram = tuple(Data)
            return (L4.get(quadgram, 0) + Vsize) / (L3.get(quadgram[:3], 0) + Vsize)


def Probability_Finder(Gram=1, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Smoothing=None, Data=None):

    if Data is None or Smoothing is None:
        return

    for sentence in Data:
        Probability = 1.0

        # --- Unigram ---
        if Gram >= 1:
            word = sentence[0]
            Probability *= G1.get(word, Smoothing(Gram=1, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=[word]))

            if Gram >1:
                break

        # --- Bigram ---
        if Gram >= 2:
            for i in range(len(sentence)-1):
                bigram = tuple(sentence[i:i+2])
                Probability *= G2.get(bigram, Smoothing(Gram=2, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=list(bigram)))

                if Gram > 2:
                    break

        # --- Trigram ---
        if Gram >= 3:
            for i in range(len(sentence)-2):
                trigram = tuple(sentence[i:i+3])
                Probability *= G3.get(trigram, Smoothing(Gram=3, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=list(trigram)))

                if Gram >3:
                    break

        # --- Quadgram ---
        if Gram >= 4:
            for i in range(len(sentence)-3):
                quadgram = tuple(sentence[i:i+4])
                Probability *= G4.get(quadgram, Smoothing(Gram=4, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=list(quadgram)))

        print(f'{sentence} | Probability: {round(Probability, 12)}')

