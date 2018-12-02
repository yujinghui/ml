from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy as np
import time
import matplotlib.pyplot as plt
 
if __name__ == '__main__':
    dataSet = np.random.rand(500,2)
    numSamples = len(dataSet)
    for k in range(2,10):
        clf = KMeans(n_clusters=k) #设定k  ！！！！！！！！！！这里就是调用KMeans算法
        s = clf.fit(dataSet) #加载数据集合
        mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
        for i in range(numSamples):
            plt.plot(dataSet[i][0], dataSet[i][1], mark[clf.labels_[i]]) #mark[markIndex])
        mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
        centroids =  clf.cluster_centers_
        for i in range(k):
            plt.plot(centroids[i][0], centroids[i][1], mark[i], markersize = 12)
        plt.show()