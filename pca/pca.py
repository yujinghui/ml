import matplotlib.pyplot as plt
import numpy as np


def loadDataSet(filename, delim='\t'):
    fr = open(filename)
    stringarr = [line.strip().split(delim) for line in fr.readlines()]
    datarr = [list(map(float, line)) for line in stringarr]
    return np.mat(datarr)


def pca(data_mat, topNFeat=1):
    """
    找出特征方差最大的那些(topNFeat)成分.
    因为方差小的那些特征并不会很好区分出数据间的差别.
    1. 计算方差及其特征值特征向量.
    2. 找出主成分并映射到新的空间.

    问题：
    1.为什么通过找到最大特征值就可以确定？
    答: min ||xi - xi|| **2 的最优化解是最大的特征值

    :param data_mat:
    :param topNFeat:
    :return:
    """
    # 求出矩阵每一列的均值.
    mean_vals = np.mean(data_mat, axis=0)
    data_centralised = data_mat - mean_vals
    cov_mat = np.cov(data_centralised, rowvar=0)
    # 求出特征值和特征向量.
    eigVals, eig_vects = np.linalg.eig(np.mat(cov_mat))
    # argsort将eig_vals数组进行排序，返回数组下标.
    eig_val_index = np.argsort(eigVals)
    # 找出最大的特征值的数组下标.
    eig_val_index = eig_val_index[: -(topNFeat + 1): -1]
    # 最大的特征值对应的特征向量
    red_eig_vects = eig_vects[:, eig_val_index]
    #
    low_d_data_mat = data_centralised * red_eig_vects
    reconstructed_mat = (low_d_data_mat * red_eig_vects.T)
    reconstructed_mat1 = reconstructed_mat + mean_vals
    return low_d_data_mat, reconstructed_mat1


if __name__ == '__main__':
    data_mat_res = loadDataSet("testSet.txt")
    low_d_mat, recon_mat = pca(data_mat_res, 1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = data_mat_res[:, 0].flatten().A[0]
    y = data_mat_res[:, 1].flatten().A[0]
    ax.scatter(x, y, marker='^', s=90)
    pcax = recon_mat[:, 0].flatten().A[0]
    pcay = recon_mat[:, 1].flatten().A[0]
    ax.scatter(pcax, pcay, marker='o', s=50, c='red')
    plt.show()
