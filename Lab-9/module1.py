import math
import re

def preprocess(sentence):
    # 1. Handle zero-width joiner
    sentence = sentence.replace("\u200c", " ")

    # 2. Replace URLs (http, https, www)
    sentence = re.sub(r'https?://\S+|www\.\S+', '<URL>', sentence)

    # 3. Replace numbers (any continuous digits)
    sentence = re.sub(r'\d+', '<NUMBER>', sentence)


    sentence = re.sub(r'[^\w\s]', ' <PUNCT> ', sentence)

    sentence = sentence.lower()

    tokens = sentence.split()

    return tokens


def BPE(sentences, iteration=20):
    for sentence in range(len(sentences)):
        sentences[sentence] = preprocess(sentences[sentence])

        for word in range(len(sentences[sentence])):
            if "<" in sentences[sentence][word]:
                sentences[sentence][word] = [sentences[sentence][word]]
                continue

            sentences[sentence][word] = list(sentences[sentence][word])

    corpus = [word for sentence in sentences for word in sentence]

    for it in range(iteration):
        pairs = {}
        for word in corpus:
            for i in range(len(word)-1):
                pair = (word[i], word[i+1])
                if pair in pairs:
                    pairs[pair] += 1
                else:
                    pairs[pair] = 1

        if not pairs:
            break


        best_pair = None
        max_count = -1
        for pair in pairs:
            if pairs[pair] > max_count:
                best_pair = pair
                max_count = pairs[pair]


        new_corpus = []
        for word in corpus:
            new_word = []
            i = 0
            while i < len(word):
                if i < len(word)-1 and (word[i], word[i+1]) == best_pair:
                    new_word.append(word[i] + word[i+1])
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            new_corpus.append(new_word)
        corpus = new_corpus

    vocab = []
    for word in corpus:
        for token in word:
            if token not in vocab:
                vocab.append(token)

    return vocab


def WordPiece(sentences, iteration=1000):

    for i in range(len(sentences)):
        sentences[i] = preprocess(sentences[i])
        for j in range(len(sentences[i])):
            if "<" in sentences[i][j]:  # special tokens
                sentences[i][j] = [sentences[i][j]]
            else:
                sentences[i][j] = list(sentences[i][j])

    for it in range(iteration):
        pair_counts = {}
        symbol_counts = {}
        total_symbols = 0
        total_pairs = 0

        for sentence in sentences:
            for word in sentence:
                total_symbols += len(word)
                for i, sym in enumerate(word):
                    symbol_counts[sym] = symbol_counts.get(sym, 0) + 1
                    if i < len(word) - 1:
                        pair = (word[i], word[i+1])
                        pair_counts[pair] = pair_counts.get(pair, 0) + 1
                        total_pairs += 1

        if not pair_counts:
            break

        pair_scores = {}
        for pair, count_ab in pair_counts.items():
            a, b = pair
            count_a = symbol_counts[a]
            count_b = symbol_counts[b]
            mi = math.log((count_ab * total_symbols**2) / (count_a * count_b * total_pairs))
            pair_scores[pair] = mi

        best_pair = max(pair_scores, key=pair_scores.get)

        for s_idx in range(len(sentences)):
            for w_idx in range(len(sentences[s_idx])):
                word = sentences[s_idx][w_idx]
                new_word = []
                i = 0
                while i < len(word):
                    if i < len(word) - 1 and (word[i], word[i+1]) == best_pair:
                        new_word.append(word[i] + word[i+1])
                        i += 2
                    else:
                        new_word.append(word[i])
                        i += 1
                sentences[s_idx][w_idx] = new_word

    vocab = []
    for sentence in sentences:
        for word in sentence:
            for token in word:
                if token not in vocab:
                    vocab.append(token)

    return vocab

def Tokenize(sentence, vocab):

    List = []
    for word in sentence:
        if "<" in word:  # special tokens
            List.append(word)
            continue

        w = list(word)

        i = 0
        while i < len(w):

            match = None
            for j in range(len(w), i, -1):
                candidate = ''.join(w[i:j])
                if candidate in vocab:
                    match = candidate
                    w = w[:i] + [candidate] + w[j:]
                    i += 1
                    break

            if match is None:
                i += 1

        List.extend(w)

    return List