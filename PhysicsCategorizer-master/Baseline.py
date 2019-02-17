import numpy as np
import re
import csv
from sklearn.linear_model import perceptron
from sklearn import svm
# from sklearn import naive_bayes

# Baseline.py
# ------------
# Author: Ayush Parolia and Karan N. Prabhu

prepositions = {'is', 'it', 'and', 'as', 'in', 'the', 'to', 'this', 'its', 'of', 'a', 'by'}
unigram = set()

def getWords(text):
    rawList = re.findall(r"[\w']+", text)
    return set(rawList)-prepositions

def extractFeatures(data):
    global unigram
    for i in range(data.size):
        unigram = unigram.union(getWords(data[i]))

def getVector(row):
    global unigram
    vector = np.zeros(len(unigram))
    index = 0
    rowWords = getWords(row)
    for item in unigram:
        if item in rowWords:
            vector[index] = 1
        index += 1
    return vector

def readFile(filePath):
    with open(filePath, 'r', encoding='utf-8', errors='ignore') as destFile:
        dataIter = csv.reader(destFile, delimiter=',',quotechar='"')
        data = [data for data in dataIter]
    dataArray = np.asarray(data)
    return dataArray

def main():
    global unigram
    train_data = readFile('./Datasets/Training0.csv')
    validation_data = readFile('./Datasets/Validation1.csv')
    test_data = readFile('./Datasets/Testing1.csv')

    # Extract features
    extractFeatures(train_data[:,0])

    X_Train = getVector(train_data[0,0])
    for i in range(1, train_data.shape[0]):
        X_Train = np.vstack([X_Train, getVector(train_data[i,0])])

    X_Validation = getVector(validation_data[0,0])
    for i in range(1, validation_data.shape[0]):
        X_Validation = np.vstack([X_Validation, getVector(validation_data[i,0])])

    X_Test = getVector(test_data[0,0])
    for i in range(1, test_data.shape[0]):
        X_Test = np.vstack([X_Test, getVector(test_data[i,0])])

    Y_Train = train_data[:,1]
    Y_Validation = validation_data[:,1]
    Y_Test = test_data[:,1]

    # Create the model
    # model = perceptron.Perceptron(n_iter=4, class_weight ="balanced", penalty='l2', alpha=0.0001)
    # model = naive_bayes.GaussianNB()
    model = svm.LinearSVC()
    model.fit(X_Train, Y_Train)

    print("Words: " + str(len(unigram)))

    # Predict the result
    print("Training Data:")
    print("Prediction " + str(model.predict(X_Train)))
    print("Actual     " + str(Y_Train))
    print("Accuracy   " + str(model.score(X_Train,Y_Train)*100) + "%")

    print("Vaildation Data:")
    print("Prediction " + str(model.predict(X_Validation)))
    print("Actual     " + str(Y_Validation))
    print("Accuracy   " + str(model.score(X_Validation,Y_Validation)*100) + "%")

    print("Test Data:")
    print("Prediction " + str(model.predict(X_Test)))
    print("Actual     " + str(Y_Test))
    print("Accuracy   " + str(model.score(X_Test,Y_Test)*100) + "%")

if __name__ == '__main__':
    main()
