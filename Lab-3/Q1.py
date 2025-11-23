class Node:
    def __init__(self, chr: str):
        self.children = []
        self.val = chr
        self.branch_val = 0
        self.ending = False

    def __str__(self):
        return self.val


def insert(n: Node, val: str) -> None:
    if len(val) == 0:
        n.ending = True
        return

    c = val[0]
    val = val[1:]
    for child in n.children:
        if str(child) == c:
            insert(child, val)
            break
    else:
        new = Node(c)
        n.children.append(new)
        n.branch_val += 1
        insert(new, val)


def Print(n: Node, string: str, string2: str, reverse: bool = False) -> None:
    string += str(n)
    string2 += str(n)

    if n.ending:
        if reverse:
            print(string[::-1], "=", string2[::-1])
        else:
            print(string, "=", string2)


    for child in n.children:
        if n.ending and n.branch_val == 1:
                Print(child, string, string2 + "+", reverse)
        else:
                Print(child, string, string2, reverse)


# ------------------------------------------------------------------------------
file = open("brown_nouns.txt", "r")
content = file.read()
List = [x for x in content.split("\n") if x.strip()]
Accepted = []

def Node_1(x):
    return x[0].islower()

def Node_2(x):
    return (x[1:].islower() and x[1:].isalpha())

for x in List:
    if Node_1(x) and Node_2(x):
        Accepted.append(x)

Accepted = list(set(Accepted))

# ------------------------------------------------------------------------------
print("Prefix Based")
Root = Node("")
for word in Accepted:
    insert(Root, word)

Print(Root, "", "", False)

# ------------------------------------------------------------------------------
print("\n\n\n")
print("Suffix Based")

Root = Node("")
for word in Accepted:
    insert(Root, word[::-1])

Print(Root, "", "", True)
