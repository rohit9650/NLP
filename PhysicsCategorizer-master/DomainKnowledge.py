import csv

# DomainKnowledge.py
# ------------
# Author: Ayush Parolia and Karan N. Prabhu

standardFormulaList = {}
derivedFormulaList = {}
concepts = set()
multiWordDict = {}

def init():
    global standardFormulaList, derivedFormulaList, concepts, multiWordDict
    standardFormulaList.clear()
    derivedFormulaList.clear()
    concepts.clear()
    multiWordDict.clear()
    createStdFormulaList()
    createDrvFormulaList()
    createMultiWordDict()

def createStdFormulaList():
    global standardFormulaList
    global concepts
    inputFile = './DomainSpecific/StandardFormulaList.csv'
    with open(inputFile, 'r') as readFile:
        dataIter = csv.reader(readFile, delimiter=',')
        for data in dataIter:
            for con in data[1:]:
                concepts.add(con)
            if data[0] in standardFormulaList.keys():
                standardFormulaList[data[0]].append(set(data[1:]))
            else:
                standardFormulaList[data[0]] = [set(data[1:])]

def createDrvFormulaList():
    global derivedFormulaList
    global concepts
    inputFile = './DomainSpecific/DerivedFormulaList.csv'
    with open(inputFile, 'r') as readFile:
        dataIter = csv.reader(readFile, delimiter=',')
        for data in dataIter:
            for con in data[1:]:
                concepts.add(con)
            if data[0] in derivedFormulaList.keys():
                derivedFormulaList[data[0]].append(set(data[1:]))
            else:
                derivedFormulaList[data[0]] = [set(data[1:])]

def createMultiWordDict():
    global concepts
    global multiWordDict
    for concept in concepts:
        multiWord = concept.split('_')
        if len(multiWord) > 1:
            if multiWord[0] in multiWordDict.keys():
                multiWordDict[multiWord[0]].append(multiWord[1:])
            else:
                multiWordDict[multiWord[0]] = [multiWord[1:]]

def getStdFormulaList():
    global standardFormulaList
    return standardFormulaList

def getDrvFormulaList():
    global derivedFormulaList
    return derivedFormulaList

def getConcepts():
    global concepts
    return concepts

def getMultiWordDict():
    global multiWordDict
    return multiWordDict