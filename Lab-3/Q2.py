import pandas as pd
import matplotlib.pyplot as plt

tokenized = open("Tokenized-Q1.txt", "r")
Para = tokenized.read()
Para = Para.split("\n")
remove = ['‘', '?', '.', '’', ',']

for sentence in range(len(Para)):
    Para[sentence] = Para[sentence].split(" ")

    for word in range(len(Para[sentence])):
        if "\u200c" in Para[sentence][word]:
            Para[sentence][word] = " ".join(Para[sentence][word].split("\u200c"))

        clean = ""
        for ch in Para[sentence][word]:
            if ch not in remove:
                clean += ch
        Para[sentence][word] = clean.lower()

Dictionary = {}
for sentence in Para:
    for word in sentence:
        if word not in Dictionary.keys():
            Dictionary[word] = 1
        else:
            Dictionary[word] += 1

sorted_items = sorted(Dictionary.items(), key=lambda x: x[1], reverse=True)
print(',' in Dictionary.keys())
# Take top 100 words
top_100 = sorted_items[:100]
W, C = zip(*top_100)
plt.bar(x = W, height = C, width=0.75)
plt.xticks(rotation=90, fontsize=5)
plt.title("Top 100 Most Frequent Words")
plt.ylabel("Frequency")
plt.xlabel("Words")
plt.show()

Counter = {}
for word in top_100:
    for sentence in Para:
        if word in sentence:
            if word not in Counter.keys():
                Counter[word] = 1
            else:
                Counter[word] +=1


Threhold = 3
sorted_items = sorted(Dictionary.items(), key=lambda x: x[1])
sorted_items = sorted_items[:len(sorted_items) - Threhold]
W, C = zip(*sorted_items)

filtered_top_100 = [(w, c) for w, c in top_100 if w in W]
print(len(filtered_top_100))
plt.bar(x = W, height = C, width=0.75)
plt.xticks(rotation=90, fontsize=5)
plt.title("Top 100 Most Frequent Words")
plt.ylabel("Frequency")
plt.xlabel("Words")
plt.show()
