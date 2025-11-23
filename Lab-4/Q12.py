import itertools
import copy
import random

def NGram(Gram: int = 1, Paragraph: list = None, Smoothing = None):
    L_List = []
    G_List = []

    if Paragraph is None:
        return

    # Unigrams
    if Gram >= 1:
        Gram_1 = {}
        total = 0
        for sentence in Paragraph:
            for word in sentence:
                Gram_1[word] = Gram_1.get(word, 0) + 1
                total += 1

        Count_1 = copy.deepcopy(Gram_1)
        for Keys in Gram_1.keys():
            Gram_1[Keys] = Gram_1[Keys] / total

        L_List.append(Count_1)
        G_List.append(Gram_1)


    # Bigrams
    if Gram >= 2:
        Gram_2 = {}
        for sentence in Paragraph:
            for i in range(len(sentence)-1):
                s = tuple(sentence[i:i+2])
                Gram_2[s] = Gram_2.get(s, 0) + 1

        Count_2 = copy.deepcopy(Gram_2)
        for Keys in Gram_2.keys():
            Gram_2[Keys] = Gram_2[Keys] / sum(v for k,v in Count_2.items() if k[0] == Keys[0])

        L_List.append(Count_2)
        G_List.append(Gram_2)

    # Trigrams
    if Gram >= 3:
        Gram_3 = {}
        for sentence in Paragraph:
            for i in range(len(sentence)-2):
                s = tuple(sentence[i:i+3])
                Gram_3[s] = Gram_3.get(s, 0) + 1

        Count_3 = copy.deepcopy(Gram_3)
        for Keys in Gram_3.keys():
            Gram_3[Keys] = Gram_3[Keys] / sum(v for k,v in Count_3.items() if k[:2] == Keys[:2])

        L_List.append(Count_3)
        G_List.append(Gram_3)

    # Quadgrams
    if Gram >= 4:
        Gram_4 = {}
        for sentence in Paragraph:
            for i in range(len(sentence)-3):
                s = tuple(sentence[i:i+4])
                Gram_4[s] = Gram_4.get(s, 0) + 1

        Count_4 = copy.deepcopy(Gram_4)
        for Keys in Gram_4.keys():
            Gram_4[Keys] = Gram_4[Keys] / sum(v for k,v in Count_4.items() if k[:3] == Keys[:3])

        L_List.append(Count_4)
        G_List.append(Gram_4)

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

        Smoothing(Gram=Gram, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4)

    return L_List, G_List


import itertools

def Laplace_Smooth(Gram=1, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None):
    V = list(L1.keys())

    if Data is None:  # Apply to whole vocabulary
        if Gram >= 2:
            for Bi in itertools.product(V, repeat=2):
                G2[Bi] = (L2.get(Bi, 0) + 1) / (L1.get(Bi[0], 0) + len(V))
        if Gram >= 3:
            for Tri in itertools.product(V, repeat=3):
                G3[Tri] = (L3.get(Tri, 0) + 1) / (L2.get(Tri[:2], 0) + len(V))
        if Gram >= 4:
            for Quad in itertools.product(V, repeat=4):
                G4[Quad] = (L4.get(Quad, 0) + 1) / (L3.get(Quad[:3], 0) + len(V))
    else:  # Apply to new sentence
        if Gram >= 1:
            for token in Data:
                if token not in L1:
                    G1[token] = 1 / (sum(L1.values()) + len(V))
            if Gram == 1:
                return G1.get(Data[-1], 0)

        if Gram >= 2:
            for i in range(len(Data)-1):
                s = tuple(Data[i:i+2])
                if s not in L2:
                    G2[s] = (L2.get(s, 0) + 1) / (L1.get(s[0], 0) + len(V))
            if Gram == 2:
                return G2.get(s, 0)

        if Gram >= 3:
            for i in range(len(Data)-2):
                s = tuple(Data[i:i+3])
                if s not in L3:
                    G3[s] = (L3.get(s, 0) + 1) / (L2.get(s[:2], 0) + len(V))
            if Gram == 3:
                return G3.get(s, 0)

        if Gram >= 4:
            for i in range(len(Data)-3):
                s = tuple(Data[i:i+4])
                if s not in L4:
                    G4[s] = (L4.get(s, 0) + 1) / (L3.get(s[:3], 0) + len(V))
            if Gram == 4:
                return G4.get(s, 0)


def AddK_Smooth(Gram=1, k=0.5, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None):
    V = list(L1.keys())

    if Data is None:
        if Gram >= 2:
            for Bi in itertools.product(V, repeat=2):
                G2[Bi] = (L2.get(Bi, 0) + k) / (L1.get(Bi[0], 0) + k * len(V))
        if Gram >= 3:
            for Tri in itertools.product(V, repeat=3):
                G3[Tri] = (L3.get(Tri, 0) + k) / (L2.get(Tri[:2], 0) + k * len(V))
        if Gram >= 4:
            for Quad in itertools.product(V, repeat=4):
                G4[Quad] = (L4.get(Quad, 0) + k) / (L3.get(Quad[:3], 0) + k * len(V))
    else:
        if Gram >= 1:
            for token in Data:
                if token not in L1:
                    G1[token] = k / (sum(L1.values()) + k * len(V))
            if Gram == 1:
                return G1.get(Data[-1], 0)

        if Gram >= 2:
            for i in range(len(Data)-1):
                s = tuple(Data[i:i+2])
                if s not in L2:
                    G2[s] = (L2.get(s, 0) + k) / (L1.get(s[0], 0) + k * len(V))
            if Gram == 2:
                return G2.get(s, 0)

        if Gram >= 3:
            for i in range(len(Data)-2):
                s = tuple(Data[i:i+3])
                if s not in L3:
                    G3[s] = (L3.get(s, 0) + k) / (L2.get(s[:2], 0) + k * len(V))
            if Gram == 3:
                return G3.get(s, 0)

        if Gram >= 4:
            for i in range(len(Data)-3):
                s = tuple(Data[i:i+4])
                if s not in L4:
                    G4[s] = (L4.get(s, 0) + k) / (L3.get(s[:3], 0) + k * len(V))
            if Gram == 4:
                return G4.get(s, 0)


def TokenType_Smooth(Gram=1, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None):
    V = list(L1.keys())
    Vsize = len(V)

    if Data is None:
        if Gram >= 2:
            for Bi in itertools.product(V, repeat=2):
                G2[Bi] = (L2.get(Bi, 0) + Vsize) / (L1.get(Bi[0], 0) + Vsize)
        if Gram >= 3:
            for Tri in itertools.product(V, repeat=3):
                G3[Tri] = (L3.get(Tri, 0) + Vsize) / (L2.get(Tri[:2], 0) + Vsize)
        if Gram >= 4:
            for Quad in itertools.product(V, repeat=4):
                G4[Quad] = (L4.get(Quad, 0) + Vsize) / (L3.get(Quad[:3], 0) + Vsize)
    else:
        if Gram >= 1:
            for token in Data:
                if token not in L1:
                    G1[token] = Vsize / (sum(L1.values()) + Vsize)
            if Gram == 1:
                return G1.get(Data[-1], 0)

        if Gram >= 2:
            for i in range(len(Data)-1):
                s = tuple(Data[i:i+2])
                if s not in L2:
                    G2[s] = (L2.get(s, 0) + Vsize) / (L1.get(s[0], 0) + Vsize)
            if Gram == 2:
                return G2.get(s, 0)

        if Gram >= 3:
            for i in range(len(Data)-2):
                s = tuple(Data[i:i+3])
                if s not in L3:
                    G3[s] = (L3.get(s, 0) + Vsize) / (L2.get(s[:2], 0) + Vsize)
            if Gram == 3:
                return G3.get(s, 0)

        if Gram >= 4:
            for i in range(len(Data)-3):
                s = tuple(Data[i:i+4])
                if s not in L4:
                    G4[s] = (L4.get(s, 0) + Vsize) / (L3.get(s[:3], 0) + Vsize)
            if Gram == 4:
                return G4.get(s, 0)


def Probability_Finder(Gram=1, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Smoothing=None, Data=None):
    print(Gram)
    if Data is None or Smoothing is None:
        return

    if Gram == 1:
        for sentence in Data:
            Probability = 1
            for word in sentence:
                if word in L1:
                    Probability *= G1[word]
                else:
                    Probability *= Smoothing(Gram=1, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=word)
            print(f'{sentence} | Probability: {round(Probability, 6)}')

    if Gram == 2:
        for sentence in Data:
            Probability = 1

            if sentence[0] not in L1:
                Probability *= Smoothing(Gram=1, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=sentence[0])
            else:
                Probability *= G1[sentence[0]]

            # Bigrams
            for i in range(len(sentence) - 1):
                s = (sentence[i], sentence[i+1])
                print(s)
                if s in G2:
                    Probability *= G2[s]
                else:
                    Probability *= Smoothing(Gram=2, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=list(s))
            print(f'{sentence} | Probability: {round(Probability, 6)}')

    if Gram == 3:
        for sentence in Data:
            Probability = 1

            # First unigram
            word = sentence[0]
            if word in L1:
                Probability *= G1[word]
            else:
                Probability *= Smoothing(Gram=1, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=word)

            # First bigram
            w2 = sentence[1]
            bigram = (word, w2)
            Probability *= G2.get(bigram, Smoothing(Gram=2, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=list(bigram)))

            # Trigrams
            for i in range(len(sentence) - 2):
                s = (sentence[i], sentence[i+1], sentence[i+2])
                Probability *= G3.get(s, Smoothing(Gram=3, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=list(s)))
            print(f'{sentence} | Probability: {round(Probability, 6)}')

    if Gram == 4:
        for sentence in Data:
            Probability = 1

            # First unigram
            word = sentence[0]
            if word in L1:
                Probability *= G1[word]
            else:
                Probability *= Smoothing(Gram=1, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=word)

            # First bigram
            w2 = sentence[1]
            bigram = (word, w2)
            Probability *= G2.get(bigram, Smoothing(Gram=2, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=list(bigram)))

            # First trigram
            w3 = sentence[2]
            trigram = (word, w2, w3)
            Probability *= G3.get(trigram, Smoothing(Gram=3, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=list(trigram)))

            # Quadgrams
            for i in range(len(sentence) - 3):
                s = (sentence[i], sentence[i+1], sentence[i+2], sentence[i+3])
                Probability *= G4.get(s, Smoothing(Gram=4, L1=L1, L2=L2, L3=L3, L4=L4, G1=G1, G2=G2, G3=G3, G4=G4, Data=list(s)))
            print(f'{sentence} | Probability: {round(Probability, 6)}')
