from sklearn.neighbors import KNeighborsClassifier

from sklearn import datasets

import numpy as np


np.random.seed(0)


iris = datasets.load_iris()

iris_x = iris.data

iris_y = iris.target


indices = np.random.permutation(len(iris_x))

# raw
iris_x_train = iris_x[:-10]
# labels
iris_y_train = iris_y[:-10]
iris_x_test = iris_x[-10:]
iris_y_test = iris_y[-10:]


knn = KNeighborsClassifier()

knn.fit(iris_x_train, iris_y_train)

iris_x_predict = knn.predict(iris_x_test)
probility = knn.predict_proba(iris_x_test)
neighborpoint=knn.kneighbors(iris_x_test[-1],5,False)
score=knn.score(iris_x_test,iris_y_test,sample_weight=None)


