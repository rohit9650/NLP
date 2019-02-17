from gensim import models

# Word2VecModel.py
# ------------
# Author: Ayush Parolia and Karan N. Prabhu

def generateNewModel():
    inputFileName = './wikiPages/wiki_00'
    outputFileName = './models/model03'
    sentences = models.word2vec.LineSentence(inputFileName)
    model = models.Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
    model.save(outputFileName)

if __name__ == '__main__':
    generateNewModel()