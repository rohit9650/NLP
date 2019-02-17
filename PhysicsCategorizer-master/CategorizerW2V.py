import numpy as np
import re
import csv
from gensim import models
from sklearn.linear_model import perceptron

# CategorizerW2V.py
# ------------
# Author: Ayush Parolia and Karan N. Prabhu

prepositions = {'is', 'it', 'and', 'as', 'in', 'the', 'to', 'this', 'its', 'of', 'a', 'by'}
word2VecModel = models.Word2Vec.load('./Word2Vec/models/model01')

def getWords(text):
    rawList = re.findall(r"[\w']+", text)
    return set(rawList)-prepositions

def readFile(filePath):
    with open(filePath, 'r') as destFile:
        dataIter = csv.reader(destFile, delimiter=',',quotechar='"')
        data = [data for data in dataIter]
    dataArray = np.asarray(data)
    return dataArray

def getFeatureVector(text, keywords):
    global word2VecModel
    textWords = getWords(text)
    vector = np.zeros(keywords.size)
    index = 0

    for key in keywords:
        max = 0
        for word in textWords:
            try:
                prob = word2VecModel.similarity(key, word)
            except:
                prob = 0
            if max < prob:
                max = prob
        vector[index] = max
        index = index + 1

    return vector

def main():
    keywords = readFile('./Keywords.csv')
    train_data = readFile('./Datasets/Shuffled/Training.csv')
    validation_data = readFile('./Datasets/Shuffled/Validation.csv')
    test_data = readFile('./Datasets/Shuffled/Testing.csv')

    X_Train = getFeatureVector(train_data[0,0],keywords)
    for i in range(1, train_data.shape[0]):
        X_Train = np.vstack([X_Train, getFeatureVector(train_data[i,0],keywords)])

    X_Validation = getFeatureVector(validation_data[0,0],keywords)
    for i in range(1, validation_data.shape[0]):
        X_Validation = np.vstack([X_Validation, getFeatureVector(validation_data[i,0],keywords)])

    X_Test = getFeatureVector(test_data[0,0],keywords)
    for i in range(1, test_data.shape[0]):
        X_Test = np.vstack([X_Test, getFeatureVector(test_data[i,0],keywords)])

    Y_Train = train_data[:,1]
    Y_Validation = validation_data[:,1]
    Y_Test = test_data[:,1]

    # Create the model
    model = perceptron.Perceptron(n_iter=490, class_weight ="balanced", penalty='l2', alpha=0.0001)
    model.fit(X_Train, Y_Train)

    # Predict the result
    print "\n Training Data:"
    print "Prediction " + str(model.predict(X_Train))
    print "Actual     " + str(Y_Train)
    print "Accuracy   " + str(model.score(X_Train,Y_Train)*100) + "%"

    print "\n Vaildation Data:"
    print "Prediction " + str(model.predict(X_Validation))
    print "Actual     " + str(Y_Validation)
    print "Accuracy   " + str(model.score(X_Validation,Y_Validation)*100) + "%"

    print "\n Test Data:"
    print "Prediction " + str(model.predict(X_Test))
    print "Actual     " + str(Y_Test)
    print "Accuracy   " + str(model.score(X_Test,Y_Test)*100) + "%"

if __name__ == '__main__':
    main()