import numpy as np
import csv
import DomainKnowledge as DM
import Preprocessor as pp
from gensim import models
from sklearn import svm
from sklearn import naive_bayes
from sklearn.linear_model import perceptron

# Categorizer.py
# ------------
# Author: Ayush Parolia and Karan N. Prabhu

# Initialize the model
model = svm.LinearSVC()
# model = perceptron.Perceptron(n_iter=1000, class_weight ="balanced", penalty='l2', alpha=0.0001)
# model = naive_bayes.GaussianNB()UnicodeDecodeError: 'utf-8' codec can't decode byte 0x93 in position 3795: invalid start byte
word2VecModel = models.Word2Vec.load('./Word2Vec/models/model02')
stdFormulaList = {}
drvFormulaList = {}
concepts = []
multiWordDict = {}
thresholdFormulaConf = 0.5

def readFile(filePath):
    with open(filePath, 'r', encoding='utf-8', errors='ignore') as destFile:
        dataIter = csv.reader(destFile, delimiter=',',quotechar='"')
        data = [data for data in dataIter]
    dataArray = np.asarray(data)
    return dataArray

def getConceptConfidence(words):
    global concepts, word2VecModel
    vector = {}

    for concept in concepts:
        max_confidence = 0
        for word in words:
            try:
                confidence = word2VecModel.similarity(concept, word)
            except:
                confidence = 0
            if max_confidence < confidence:
                max_confidence = confidence
        if max_confidence <= 0:
            vector[concept] = 0
        else:
            vector[concept] = max_confidence

    return vector

def getFormulaConfidence(conceptConf):
    global stdFormulaList, drvFormulaList, thresholdFormulaConf
    nameList = []
    valueList = []

    for formulaName in stdFormulaList.keys():
        for formula in stdFormulaList[formulaName]:
            # confidence = 0
            confidence = 1
            alpha = len(formula)
            for concept in formula:
                # confidence = confidence + conceptConf[concept]
                confidence = confidence * conceptConf[concept]
            if conceptConf[formulaName] > thresholdFormulaConf:
                # confidence = confidence + conceptConf[formulaName]
                confidence = confidence * conceptConf[formulaName]
                alpha = alpha + 1
            # confidence = confidence/alpha
            nameList.append(formulaName)
            valueList.append(confidence)
            if confidence > thresholdFormulaConf:
                conceptConf[formulaName] = 1

    for formulaName in drvFormulaList.keys():
        if formulaName == 'dummy':
            continue
        for formula in drvFormulaList[formulaName]:
            # confidence = 0
            confidence = 1
            for concept in formula:
                # confidence = confidence + conceptConf[concept]
                confidence = confidence * conceptConf[concept]
            # confidence = confidence/len(formula)
            nameList.append(formulaName)
            valueList.append(confidence)
    return nameList, valueList

def getFeatureVector(words):
    conceptConf = getConceptConfidence(words)
    nameVector, valueVector = getFormulaConfidence(conceptConf)
    return np.asarray(valueVector + list(conceptConf.values()))

def getTopNConcepts(text, n):
    global model, multiWordDict
    words = pp.parse(text, multiWordDict)
    conceptConf = getConceptConfidence(words)
    count = 0
    result = []

    for w in sorted(conceptConf, key=conceptConf.get, reverse=True):
        result.append(w)
        count = count + 1
        if count == n:
            break

    return result

def getTopNFormulae(text, n):
    global model, multiWordDict, thresholdFormulaConf
    words = pp.parse(text, multiWordDict)
    nameList, valueList = getFormulaConfidence(getConceptConfidence(words))
    result = {}
    index = 0

    for value in valueList:
        result[nameList[index]] = value
        index = index + 1

    return sorted(result, key=result.get, reverse=True)[0:n]

def conceptCount():
    global concepts
    return len(concepts)

def formulaCount():
    global stdFormulaList, drvFormulaList
    return len(stdFormulaList.keys()) + len(drvFormulaList.keys())


def getClassName(label):
    if label[0] == '0':
        return "Circular motion and Gravitation"
    elif label[0] == '1':
        return "Electromagnetism"
    elif label[0] == '2':
        return "Force in 2D"
    elif label[0] == '3':
        return "Kinematics"
    elif label[0] == '4':
        return "Momentum and collisions"
    elif label[0] == '5':
        return "Newton's Law"
    elif label[0] == '6':
        return "Optics"
    elif label[0] == '7':
        return "Projectile Motion"
    elif label[0] == '8':
        return "Thermodynamics"
    elif label[0] == '9':
        return "Work Power and Energy"
    else:
        return "Unknown"

def getCategory(text):
    global model, multiWordDict
    words = pp.parse(text, multiWordDict)
    return getClassName(model.predict([getFeatureVector(words)]))

def init():
    global model, stdFormulaList, drvFormulaList, concepts, multiWordDict

    # Get Data
    print("Loading Physics questions from default dataset ...")
    train_data = readFile('./Datasets/Training1.csv')
    validation_data = readFile('./Datasets/Validation1.csv')
    test_data = readFile('./Datasets/Testing1.csv')
    print("Done!")

    # Get Domain Knowledge
    print("Loading Domain Knowledge ...")
    DM.init()
    stdFormulaList = DM.getStdFormulaList()
    drvFormulaList = DM.getDrvFormulaList()
    concepts = DM.getConcepts()
    multiWordDict = DM.getMultiWordDict()
    print("Done!")

    # Generate Matrix
    print("Generating feature matrix for training ...")
    words = pp.parse(train_data[0,0], multiWordDict)
    X_Train = getFeatureVector(words)
    for i in range(1, train_data.shape[0]):
        words = pp.parse(train_data[i,0], multiWordDict)
        X_Train = np.vstack([X_Train, getFeatureVector(words)])

    words = pp.parse(validation_data[0,0], multiWordDict)
    X_Validation = getFeatureVector(words)
    for i in range(1, validation_data.shape[0]):
        words = pp.parse(validation_data[i,0], multiWordDict)
        X_Validation = np.vstack([X_Validation, getFeatureVector(words)])

    words = pp.parse(test_data[0,0], multiWordDict)
    X_Test = getFeatureVector(words)
    for i in range(1, test_data.shape[0]):
        words = pp.parse(test_data[i,0], multiWordDict)
        X_Test = np.vstack([X_Test, getFeatureVector(words)])

    Y_Train = train_data[:,1]
    Y_Validation = validation_data[:,1]
    Y_Test = test_data[:,1]
    print("Done!")

    # Train the model
    print("Training ...")
    model.fit(X_Train, Y_Train)
    print("Done!")

    # Predict the result
    print("\n Training Data:")
    print("Prediction " + str(model.predict(X_Train)))
    print("Actual     " + str(Y_Train))
    print("Accuracy   " + str(model.score(X_Train,Y_Train)*100) + "%")

    print("\n Vaildation Data:")
    print("Prediction " + str(model.predict(X_Validation)))
    print("Actual     " + str(Y_Validation))
    print("Accuracy   " + str(model.score(X_Validation,Y_Validation)*100) + "%")

    print("\n Test Data:")
    print("Prediction " + str(model.predict(X_Test)))
    print("Actual     " + str(Y_Test))
    print("Accuracy   " + str(model.score(X_Test,Y_Test)*100) + "%")


if __name__ == '__main__':
    init()
