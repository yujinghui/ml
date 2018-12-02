import numpy as np  
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])  
Y = np.array([1, 2, 3, 4, 5, 6])  
from sklearn.naive_bayes import GaussianNB  
clf = GaussianNB().fit(X, Y)  
print (clf.predict([[-0.8,-1]])  )