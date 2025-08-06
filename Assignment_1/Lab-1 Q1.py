from datasets import load_dataset
import re
import pandas as pd

# Load streamed Telugu dataset
dataset = load_dataset("ai4bharat/IndicCorpV2", name="indiccorp_v2", split="tel_Telu", streaming=True)
Count = {'sentence': 0, 'words': 0, 'char': 0}

f = open("Q1.txt", "w", encoding="utf-8")
tokenized = open("Tokenized-Q1.txt", "w", encoding="utf-8")  # <-- Tokenized output
Mail = []
URL = []

for i, line in enumerate(dataset):
    text = line['text']

    # Break into sentences
    Sentences = re.findall(r'[\"“”]?[^\n.!?]*[.!?][\"”]?', text)

    for l in Sentences:
        Count['sentence'] += 1
        f.write(f"Line #{Count['sentence']}: {l}\n")
        print(l)

        words = re.split(r'\s+', l.strip())
        f.write(f"Words: {words}\n")
        print(f"Words: {words}")

        cleaned = []
        wc = 0
        tcc = 0

        for word in words:
            wc += 1
            word_clean = word.strip('.,!?;:“”‘’"\'')
            cleaned.append(word_clean)

            # Char count
            char = re.findall(r'[\u0C00-\u0C7F0-9@#$%^&*()_+=\-<>~`|{}\[\]\\\\]|[.,!?;:"“”‘’\']', word)
            cc = len(char)
            Count['char'] += cc
            tcc += cc

            f.write(f"word #{wc} - {word}: {char}\n")

            # URL detection
            url = None
            if re.fullmatch(r'.*\.{1}[\w]{2,}$', word):
                url = word

            # Mail detection
            mail = None
            if re.fullmatch(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}', word):
                mail = word

            if mail:
                Mail.append(mail)
                f.write(f"Mail: {mail}\n\n")
            elif url:
                URL.append(url)
                f.write(f"URLs: {url}\n")

            # Number detection
            if re.fullmatch(r'\b\d+\.\d+\b', word) or re.fullmatch(r'\b\d+\b', word):
                f.write(f"Number: {word}\n")

            # Date detection
            if re.fullmatch(r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})|(\d{4}-\d{2}-\d{2})|(\d{1,2}\s+[A-Za-z]+\s+\d{4})', word):
                f.write(f"Date: {word}\n")

            # Punctuation detection
            punctuation = re.findall(r'[.,!?;:"“”‘’\'\-–—]', word)
            if punctuation:
                f.write(f"Punctuation(s): {punctuation}\n")

        Count['words'] += wc
        f.write(f'\nSentence Statistics:\nTotal Word count: {wc} | Total character count: {tcc}\n\n')

        tokenized.write(" ".join(cleaned) + "\n")


# Final stats
f.write("\n\n---- Statistics of entire Corpus Parsed so far ----\n")
f.write(f"Sentence Count: {Count['sentence']} | Word Count: {Count['words']} | Character Count: {Count['char']}\n")
f.write(f"Average Sentence Length: {round(Count['words'] / Count['sentence'], 2)} | Average Word Length: {round(Count['char'] / Count['words'], 2)}\n")
f.close()
tokenized.close()

# --------------------------
data = []
with open("Q1.txt", "r", encoding="utf-8") as f:
    sentence = ""
    words = []
    urls = []
    mails = []
    dates = []
    puncts = []

    for line in f:
        if line.startswith("Line #"):
            if sentence:
                data.append({
                    "Sentence": sentence,
                    "Words": words,
                    "URLs": urls,
                    "Mails": mails,
                    "Dates": dates,
                    "Punctuations": puncts
                })
            sentence = line.split(":", 1)[1].strip()
            words, urls, mails, dates, puncts = [], [], [], [], []

        elif line.startswith("Words:"):
            words = eval(line.split(":", 1)[1].strip())

        elif line.startswith("URLs:"):
            url = eval(line.split(":", 1)[1].strip())
            urls.append(url)

        elif line.startswith("Mail:"):
            mail = eval(line.split(":", 1)[1].strip())
            mails.append(mail)

        elif line.startswith("Date:"):
            date = eval(line.split(":", 1)[1].strip())
            dates.append(date)

        elif line.startswith("Punctuation(s):"):
            punc = eval(line.split(":", 1)[1].strip())
            puncts.extend(punc)

    if sentence:
        data.append({
            "Sentence": sentence,
            "Words": words,
            "URLs": urls,
            "Mails": mails,
            "Dates": dates,
            "Punctuations": puncts
        })

df = pd.DataFrame(data)
df.to_parquet("Total.parquet", engine="pyarrow", index=False)
print("Parquet file saved as Total.parquet")

# Save tokenized lines as parquet
with open("Tokenized-Q1.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

df_tokenized = pd.DataFrame({
    "Tokenized": lines
})
df_tokenized.to_parquet("tokenized.parquet", engine="pyarrow", index=False)
print("Parquet file saved as tokenized.parquet")