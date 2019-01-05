import numpy as np

import operator

import json


def createDataSet():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistanceIndices = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistanceIndices[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    print(json.dumps(classCount))
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    print(json.dumps(sortedClassCount))
    return sortedClassCount[0][0]


'''
 parse txt to matrix
'''


def file2matrix(filename):
    emotionmapping = {"didntLike": 1, "smallDoses": 2, "largeDoses": 3}
    fr = open(filename)
    arrayOlines = fr.readlines()
    numberOfLines = len(arrayOlines)
    returnMat = np.zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOlines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(emotionmapping.get(listFromLine[-1].replace('\n', '')))
        index = 1 + index
    return returnMat, classLabelVector


#  min-max scaling
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - np.tile(minVals, (m, 1))
    normDataSet = normDataSet / np.tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


# testing 
def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix("/home/yujinghui/Workspaces/python/ml/knn/dataTestSet.txt")
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print("the classifer come back with %d, the real answer is :%d"%(classifierResult, datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print("the total error rate is %f" %(errorCount /float(numTestVecs)))

def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percenTats = float(input("percentage of time spent playing video games?"))
    ffMiles = float(input("frequent filer miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year"))
    datingDatMat, datingLabels = file2matrix('/home/yujinghui/Workspaces/python/ml/knn/dataTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDatMat)
    inArr = np.array([ffMiles, percenTats, iceCream])
    classifyResult = classify0((inArr - minVals)/ ranges, normMat, datingLabels, 3)
    print("you will probably like this person : ", resultList[classifyResult - 1])