def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open("dataTestSet.txt")
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(lineArr[2])
    return dataMat, labelMat


import math
import numpy as np


def sigmoid(inx):
    return 1.0 / (1 + np.exp(-inx))


def gradAscent(dataMatIn, classLabels):
    dataMatrix = np.mat(dataMatIn)
    labelMat = np.mat(classLabels).transpose()
    m, n = np.shape(dataMatrix)
    alpha = 0.001
    # iterate for 500 times
    maxCycles = 500
    weights = np.ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)
        error = (labelMat.astype("float64") - h)
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights


import matplotlib.pyplot as plt


def plotBestFit(wei):
    weights = wei.getA()
    dataMat, labelMat = loadDataSet()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('Y1')
    plt.show()


def stocGradAscent0(dataMatrix, classLabels):
    m, n = np.shape(dataMatrix)
    alpha = 0.01
    weights = np.ones(n)
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i] * (weights.transpose())))
        error = np.mat(classLabels[i]).astype("float64") - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights.transpose()


if __name__ == '__main__':
    dataArr, labelMat = loadDataSet()
    # res = gradAscent(dataArr, labelMat)
    res = stocGradAscent0(np.array(dataArr), labelMat)
    plotBestFit(res)
