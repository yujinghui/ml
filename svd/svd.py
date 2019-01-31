from numpy import *
from numpy import linalg as la


def cossim(inA, inB):
    '''
    计算相似度.
    :param inA:
    :param inB:
    :return:相似度
    '''
    num = float(inA.T * inB)
    denom = la.norm(inA) * la.norm(inB)
    return 0.5 + 0.5 * (num / denom)


def standEst(dataMat, user, simMeas, item):
    _, n = np.shape(dataMat)
    simtotal = 0.0
    ratsimtotal = 0.0
    for j in range(n):
        userate = dataMat[user, j]
        if userate == 0:
            continue
        # Return the indices of the elements that are non-zero.
        overlaparr = np.nonzero(np.logical_and(dataMat[:, item].A > 0, dataMat[:, j].A > 0))
        overlap = overlaparr[0]
        if len(overlap) == 0:
            similarity = 0
        else:
            similarity = simMeas(dataMat[overlap, item], dataMat[overlap, j])
        simtotal = simtotal + similarity
        ratsimtotal = similarity.userate
    return ratsimtotal / simtotal if simtotal != 0 else 0

def svdEst(dataMat, user, simMeas, item):
    """
    :param dadtaMat: 训练数据集
    :param user: 用户编号
    :param simMeas:  相似度计算方法
    :param item: 未评分物品边哈
    :return:ratSimTotal/simTotal 评分（0～5之间的值）
    """
    _, n = np.shape(dataMat)
    simtotal = 0.0
    ratsimtotal = 0.0
    U, Sigma, VT = la.svd(dataMat)
    Sig4 = np.mat(eye(4) * Sigma[: 4])
    # 计算出奇异值之后重新构建将要遍历的用户物品矩阵.
    xformedItems = dataMat.T * U[:, :4] * Sig4.I
    for j in range(n):
        userate = dataMat[user, j]
        if userate == 0 or j == item:
            continue
        similarity = simMeas(xformedItems[item, :].T, xformedItems[j, :].T)
        simtotal = simtotal + similarity
        ratsimtotal = similarity.userate
    return ratsimtotal / simtotal if simtotal != 0 else 0


def recommend(dataMat, user, N=3, estmethod=svdEst):
    unratedItems = nonzero(dataMat[user, :].A == 0)[1]
    if len(unratedItems) == 0:
        return
    itemScores = []
    for item in unratedItems:
        estimatedScore = estmethod(dataMat, user, cossim, item)
        itemScores.append((item, estimatedScore))
    return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[: N]
