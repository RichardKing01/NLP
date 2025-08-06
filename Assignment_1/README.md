Assignment 1 - Tokenization
Provided a large database of text of a particular language from ai4bharat/IndicCorpV2; the program intends to tokenize words punctuations and other elements such as email-addresses, dates and so on. 

The Program is written in Python and utilises the Libraries re for regular expresssion, datasets to work with the dataset, and pandas to generate the parquet file. 

The Program also computes the following:
i) Total number of sentences
ii) Total number of words
iii) Total number of characters
iv) AVerage Sentence Length
v) average Word Length
vi) Type/Token Ratio

The Program, First iterates through the database that is streamed through. It then separates sentences based on Punctuation marks like the exclamation mark or the question mark. It further then splits the sentences to words (based on white spaces and/or punctuation marks), and then words into characters. Through it all, A counter for sentences, words and characters is maintained. 
The Program generates particularly two types of text files, one file which holds tokenized sentences formed by tokenized words (Tokenized-Q1.txt), the other text file (Q1.txt), shows the tokenizations through all the stages (sentences -> words -> characters) and also showcases URLs, email-addresses, dates , numbers and the like if any. It also shows you the word count and character count of the sentence.

The Program also generates the parquet files for both these.
It is important to note that the files added are samples and have tokenized a small portion of the entire dataset.

