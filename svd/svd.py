from numpy import linalg as la
from numpy import *


def svdEst(dataMat, user, simMeas, item):
    """
    :param dadtaMat: 训练数据集
    :param user: 用户编号
    :param simMeas:  相似度计算方法
    :param item: 未评分物品边哈
    :return:ratSimTotal/simTotal 评分（0～5之间的值）
    """
    m, n = shape(dataMat)
    simTotal = 0.0
    ratSimTotal = 0.0
    U, Sigma, VT = la.svd(dataMat)
