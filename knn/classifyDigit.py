import knn
import numpy as np
import os


def img2vect(filename):
    returnVect = np.zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j])
    return returnVect


def handwritingClassTest():
    hwLabels = []
    traingingFileList = os.listdir('trainingDigits')
    m = len(traingingFileList)
    trainingMat = np.zeros((m, 1024))
    for i in range(m):
        fileNameStr = traingingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vect('trainingDigits/%s' % fileNameStr)
    testFileList = os.listdir("testDigits")
    errCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileNameStr.split('_')[0])
        vectorUnderTest = img2vect('testDigits/%s' % fileNameStr)
        classifierResult = knn.classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        if classifierResult != classNumStr :
            errCount = errCount + 1
        print("calc is %d, real answer is %s" % (classifierResult, classNumStr))
    print("error rate is %f", errCount / float(mTest))
    print("error num is %d" % errCount)

handwritingClassTest()