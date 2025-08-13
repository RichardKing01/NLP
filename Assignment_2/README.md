Assignment 2 DFA and FST

1. Construct a deterministic finite automaton (DFA) that recognizes valid simplified Englishwords. An English word, for this problem, is defined as a string that:
● Starts with an lowercase letter
● Followed by zero or more lowercase letters.

The Program is written in Python and utilises no external libraries.

In this assignment, a text file was provided consisting for a large number of words, both 'legal' and 'illegal'. The goal of the first program is to parse through the text file for operable words. 
This is done by hard-coding the above conditions, using the in-built python functions. It first loads the words making sure to not include empty or strings with just indentations (spaces). The words are then passed through two functions, one which checks if the first word is lowercase, and if success, passes it to the next function which checks whether all characters are both characters and are in lowercase. If Success, it Adds then to an `Accepted` List, else if at any of the two functions it fails, it is rejected. 

#------

2. You are given all the nouns from the brown corpus (brown_nouns.txt). You need todesign a finite state transducer (FST) to generate the morph/grammatical features forevery word in the corpus. Your output should look like the following:
foxes = fox+N+PL (can be generalized as root+category+number)

The Following Properties must be Followed:
● E insertion | e is added after -s, -z, -x, ch, -sh before -s is added | example: watch/watches, fox/foxes
● Y replacement |  -y changes to -ie before -s | example: try/tries
● S addition | -s is added at the end | example: bag/bags

You need to ensure that incorrect words are not generated. You return an output “Invalid Word” in that case. Example: foxs = “Invalid Word”

The Program is written in Python and utilises no external libraries.

The Second Programme consists (Finite State Transducer) which uses Functions to simulate the Functioning of a FST, wherein considering a certain condition passes (a certain characters is found) it moves to another Node. 