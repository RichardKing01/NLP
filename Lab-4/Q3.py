from Q12 import *

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

print(Para)

L, G = NGram(Gram=2, Paragraph= Para, Smoothing= Laplace_Smooth)
print(L, "\n\n")
print(G)