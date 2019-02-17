import csv
import re
import numpy as np

# Preprocessor.py
# ------------
# Author: Ayush Parolia and Karan N. Prabhu

prepositions = {'is', 'it', 'and', 'as', 'in', 'the', 'to', 'this', 'its', 'of', 'a', 'by', 'if', 'an', 'at', 'he', 'she', 'his', 'her', 'with', 'upon', 'whom'}

def getWordSequence(text):
    rawList = [x.lower() for x in re.findall(r"[\w'/]+", text)]
    return rawList

def parse(text, multiWordDict):
    sequence = getWordSequence(text)
    wordList = []
    index = 0
    skipCount = 0

    for word in sequence:
        if skipCount > 0:
            skipCount = skipCount - 1
            index = index + 1
            continue
        newWord = word
        if word in multiWordDict.keys():
            for combo in multiWordDict[word]:
                skipCount = 0
                for i in range(0, len(combo)):
                    if i+index+1 > len(sequence)-1:
                        break
                    if combo[i] == sequence[i+index+1]:
                        newWord = newWord + "_" + sequence[i+index+1]
                        skipCount = skipCount + 1
                    else:
                        break
                if skipCount == len(combo):
                    break
                else:
                    skipCount = 0
                    newWord = word
        wordList.append(newWord)
        index = index + 1

    return set(wordList) - prepositions