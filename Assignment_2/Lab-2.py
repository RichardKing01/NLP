file = open("brown_nouns.txt", "r")
content = file.read()
List = [x for x in content.split("\n") if x.strip()]
Accepted = []
N_Accepted = []

def Node_1(x):
    return x[0].islower()

def Node_2(x):
    return (x[1:len(x)].islower() and x[1:len(x)].isalpha())

for x in List:
    print(x)
    if Node_1(x):
        if Node_2(x):
            Accepted.append(x)
        else:
            N_Accepted.append(x)
    else:
        N_Accepted.append(x)

print(f"Accepted: {", ".join(list(set(Accepted)))}")
print(f"Not Accepted: {", ".join(list(set(N_Accepted)))}")
file.close()

del N_Accepted


def Norm(word, count):
    if len(word) == count:
        if word[-3:] == 'men':
            print(f"{word} = {word[:-3] + "man"}+N+PL")
        else:
            print(f"{word} = {word}+N+SG")

    elif word[count] in ['x', 'z']:
         Found_ZX(word, count+1)

    elif word[count] == 's':
        Found_S(word, count+1)

    elif word[count] == 'c':
        Found_C(word, count+1)

    elif word[count] == 'i':
        Found_I(word, count+1)

    else:
        Norm(word,count + 1)

##------------------------------------------------

def Found_ZX(word, count):
    if len(word) == count:
        print(f"{word} = {word}+N+SG")

    elif word[count] == 'e':
        Found_ZXSCHE(word, count+1)

    elif word[count] == 'i':
        Found_I(word, count+1)

    elif word[count] == 'c':
        Found_C(word, count+1)

    elif word[count] in ['x', 'z']:
         Found_ZX(word, count+1)

    elif word[count] == 's':
        Null(word, count+1)

    else:
        Norm(word,count + 1)

##------------------------------------------------

def Found_C(word, count):
    if len(word) == count:
        print(f"{word} = {word}+N+SG")

    elif word[count] == 'i':
        Found_I(word, count+1)

    elif word[count] == 'c':
        Found_C(word, count+1)

    elif word[count] in ['x', 'z']:
         Found_ZX(word, count+1)

    elif word[count] == 'h':
        Found_H(word, count+1)

    elif word[count] == 's':
        Found_S(word, count+1)

    else:
        Norm(word,count + 1)

##------------------------------------------------

def Found_S(word, count, From=0):
    if len(word) == count:
        if From == 0:
            print(f"{word} = {word[:-1]}+N+PL")
        if From == 1: #es
            print(f"{word} = {word[:len(word)-2]}+N+PL")
        if From == 2: #ies
            print(f"{word} = {word[:len(word)-3] + "y"}+N+PL")
        if From == 3: #ss
            print(f"{word} = {word}+N+SG")

    elif word[count] == 'i':
        Found_I(word, count+1)

    elif word[count] == 'c':
        Found_C(word, count+1)

    elif word[count] in ['x', 'z']:
         Found_ZX(word, count+1)

    elif word[count] == 'h':
        Found_H(word, count+1)

    elif word[count] == 's':
        Found_S(word, count+1, 3)

    elif word[count] == 'e':
        Found_ZXSCHE(word, count+1)

    else:
        Norm(word,count + 1)

##------------------------------------------------

def Found_H(word, count):
    if len(word) == count:
        print(f"{word} = {word}+N+SG")

    elif word[count] == 'i':
        Found_I(word, count+1)

    elif word[count] == 'c':
        Found_C(word, count+1)

    elif word[count] in ['x', 'z']:
         Found_ZX(word, count+1)

    elif word[count] == 'e':
        Found_ZXSCHE(word, count+1)

    elif word[count] == 's':
        Found_S(word, count+1)

    else:
        Norm(word, count+1)

##------------------------------------------------

def Found_ZXSCHE(word, count):
    if len(word) == count:
        print(f"{word} = {word}+N+SG")

    elif word[count] == 'i':
        Found_I(word, count+1)

    elif word[count] == 'c':
        Found_C(word, count+1)

    elif word[count] in ['x', 'z']:
         Found_ZX(word, count+1)

    elif word[count] == 's':
        Found_S(word, count+1, 1)

    else:
        Norm(word, count+1)

##------------------------------------------------

def Found_I(word, count):
    if len(word) == count:
        print(f"{word} = {word}+N+SG")

    elif word[count] == 'i':
        Found_I(word, count+1)

    elif word[count] == 'c':
        Found_C(word, count+1)

    elif word[count] in ['x', 'z']:
         Found_ZX(word, count+1)

    elif word[count] == 's':
        Found_S(word, count+1)

    elif word[count] == 'e':
        Found_IE(word, count+1)

    else:
        Norm(word, count+1)

##------------------------------------------------

def Found_IE(word, count):
    if len(word) == count:
        print(f"{word} = {word}+N+SG")

    elif word[count] == 'i':
        Found_I(word, count+1)

    elif word[count] == 'c':
        Found_C(word, count+1)

    elif word[count] in ['x', 'z']:
         Found_ZX(word, count+1)

    elif word[count] == 's':
        Found_S(word, count+1, 2)

    else:
        Norm(word, count+1)

def Null(word, count):
    print(f"Invalid word: {word}")

for word in list(set(Accepted)):
    Norm(word, 0)
