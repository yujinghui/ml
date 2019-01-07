import numpy as np
import math


def loadDataSet(fileName):
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineAr = line.strip().split('\t')
        dataMat.append([float(lineAr[0]), float(lineAr[1])])
        labelMat.append(float(lineAr[2]))
    return dataMat, labelMat


import random


# choose a j which does not equals i ,j and i are in range of m
def selectJrand(i, m):
    j = i
    while j == i:
        j = int(random.uniform(0, m))
    return j


def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj


'''
  dataMatIn : data set.
  classLabels : label.
  C: constants , slack variable to allow
  toler : tolerance.
  maxIter: max iteration counts before exit.
'''


def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = np.mat(dataMatIn)
    labelMat = np.mat(classLabels).transpose()
    b = 0
    m, n = np.shape(dataMatrix)
    alphas = np.mat(np.zeros((m, 1)))
    iter = 0
    while (iter < maxIter):
        alphaPairChanged = 0
        for i in range(m):
            fXi = float(np.multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[i, :].T)) + b
            Ei = fXi - float(labelMat[i])
            if ((labelMat[i] * Ei < -toler) and (alphas[i] < C)) or \
                    ((labelMat[i] * Ei > toler) and alphas[i] > 0):
                j = selectJrand(i, m)
                fXj = float(np.multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[j, :].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if labelMat[i] != labelMat[j]:
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])

                if L == H:
                    print("L==H")
                    continue

                eta = 2.0 * dataMatrix[i, :] * dataMatrix[j, :].T - \
                      dataMatrix[i, :] * dataMatrix[i, :].T - \
                      dataMatrix[j, :] * dataMatrix[j, :].T

                if eta >= 0:
                    print("eta >= 0")
                    continue
                alphas[j] = alphas[j] - labelMat[j] * (Ei - Ej) / eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if np.abs(alphas[j] - alphaJold) < 0.00001:
                    print("j not move enough")
                    continue

                alphas[i] = alphas[i] + labelMat[j] * labelMat[i] * (alphaJold - alphas[j])
                b1 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[i, :].T - \
                     labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[i, :] * dataMatrix[j, :].T
                b2 = b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[j, :].T - \
                     labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j, :] * dataMatrix[j, :].T

                if 0 < alphas[i] < C:
                    b = b1
                elif 0 < alphas[j] < C:
                    b = b2
                else:
                    b = (b1 + b2) / 2.0

                alphaPairChanged = alphaPairChanged + 1
                print("iter : %d i:%d, pairs changed %d" % (iter, i, alphaPairChanged))
        if alphaPairChanged == 0:
            iter = iter + 1
        else:
            iter = 0

        print("iteration number is %d" % iter)

    return b, alphas

if __name__ == "__main__":
    dataArr, labelArr = loadDataSet("svmTestSet.txt")
    b, alphas = smoSimple(dataArr, labelArr, 0.06, 0.001, 40)
    print(alphas)
    print(b)
