import csv

# Concepts.py
# -----------
# Author: Ayush Parolia and Karan N. Prabhu

def getConcepts():
    concepts = set()
    formulaFile = './DerivedFormulaList.csv'
    with open(formulaFile, 'r') as destFile:
        dataIter = csv.reader(destFile, delimiter=',')
        for data in dataIter:
            index = 0
            for con in data:
                if index != 0:
                    concepts.add(con.strip())
                index = index + 1
    print(concepts)

if __name__ == '__main__':
    getConcepts()
