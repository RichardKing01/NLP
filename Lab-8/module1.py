import re
import math

#Q1
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

def compute_tf_with_normalization(sentence, smoothing=False):
    TF = {}
    for word in sentence:
        try:
            TF[word] += 1
        except:
            TF[word] = 1

    length = len(sentence)

    if not smoothing:
        for key in TF.keys():
            TF[key] /= length

    else:
        denom = 0
        for key in TF.keys():
            denom += (1 + math.log(TF[key]))

        for key in TF.keys():
            TF[key] /= denom

    return TF

def compute_idf(sentence, sentences, smoothing=False):
    IDF = {}
    N = len(sentences)
    for word in sentence:
        IDF[word] = 0
        for s in sentences:
            if word in s:
                IDF[word] += 1

    if not smoothing:
        for key in IDF.keys():
            IDF[key] = math.log(N/IDF[key])

    else:
        for key in IDF.keys():
            IDF[key] = math.log(((1+N)/(1+IDF[key]))) + 1

    return IDF

def compute_tf_idf_scores(sentences, smoothing=False):
    TF_IDF = {}
    for sentence in sentences:
        List = []
        TF = compute_tf_with_normalization(sentence, smoothing)
        IDF = compute_idf(sentence, sentences, smoothing)
        for key in TF.keys():
            List.append(TF[key]*IDF[key])

        TF_IDF[sentence] = List

    return TF_IDF

#Q2)
sentences = [
    "The boy hugs the cat.",
    "The boys are hugging the dogs.",
    "The dogs are chasing the cats.",
    "The dog and the cat sit quietly.",
    "The boy is sitting on the dog."
]

def Wordpiece(sentences):
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

##Q3

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

def AddK_Smoothing(Gram=1, L1=None, L2=None, L3=None, L4=None, G1=None, G2=None, G3=None, G4=None, Data=None, K=0.3):

    if Gram >= 1:
        total_count = sum(L1.values())
        V = len(L1)  # vocabulary size
        for word in L1:
            G1[word] = (L1[word] + K) / (total_count + K * V)

    if Gram >= 2 and L2 is not None:
        for bigram in L2:
            history = bigram[0]
            history_count = L1.get(history, 0)
            G2[bigram] = (L2[bigram] + K) / (history_count + K * len(L1))

    if Gram >= 3 and L3 is not None:
        for trigram in L3:
            history = trigram[:2]
            history_count = L2.get(history, 0)
            G3[trigram] = (L3[trigram] + K) / (history_count + K * len(L1))

    if Gram >= 4 and L4 is not None:
        for quadgram in L4:
            history = quadgram[:3]
            history_count = L3.get(history, 0)
            G4[quadgram] = (L4[quadgram] + K) / (history_count + K * len(L1))


Inform = ["Check out https://example.com for more info!", "Your package #12345 will arrive tomorrow.", "Download the report from https://reports.com."]
Reminder = ["Meeting at 3pm, don't forget to bring the files.", "The meeting is starting in 10 minutes.", "Reminder: submit your timesheet by 5pm today."]
Promo = ["Order 3 items, get 1 free! Limited offer!!!", "Win $1000 now, visit http://winbig.com!!!", "Exclusive deal for you: buy 2, get 1 free!!!"]

Inform = [preprocess(s) for s in Inform]
Reminder = [preprocess(s) for s in Reminder]
Promo = [preprocess(s) for s in Promo]

Inform_Count, Inform_Probability = NGram(2, Inform, AddK_Smoothing)
Reminder_Count, Reminder_Probability = NGram(2, Reminder, AddK_Smoothing)
Promo_Count, Promo_Probability = NGram(2, Promo, AddK_Smoothing)


test_sentence = "You will get an exclusive offer in the meeting!"
test_tokens = preprocess(test_sentence)

test_bigrams = [tuple(test_tokens[i:i+2]) for i in range(len(test_tokens)-1)]

prob_Inform = sentence_probability(test_bigrams, Inform_Probability)
prob_Reminder = sentence_probability(test_bigrams, Reminder_Probability)
prob_Promo = sentence_probability(test_bigrams, Promo_Probability)

def sentence_probability(sentence, Count_dict, K=0.3):
    Count_bigram = Count_dict[0]  # bigram counts
    Count_unigram = Count_dict[1]  # unigram counts

    prob = 1.0

    # generate bigrams from sentence
    bigrams = [tuple(sentence[i:i+2]) for i in range(len(sentence)-1)]

    # Vocabulary size for Add-K smoothing
    V = len(Count_unigram)

    for bg in bigrams:
        bg_count = Count_bigram.get(bg, 0)
        history_count = Count_unigram.get(bg[0], 0)

        # Add-K smoothing formula
        prob_bg = (bg_count + K) / (history_count + K*V)
        prob *= prob_bg

    return prob

test_sentence = preprocess("You will get an exclusive offer in the meeting!")
p_inform = sentence_probability(test_sentence, (Inform_Count, Inform_Probability))
p_reminder = sentence_probability(test_sentence, (Reminder_Count, Reminder_Probability))
p_promo = sentence_probability(test_sentence, (Promo_Count, Promo_Probability))

print(f"Inform: {p_inform} | Reminder: {p_reminder} | Promotion: {p_promo}")
