import matplotlib.pyplot as plt
import numpy as np

class My2DCoordination:

    def __init__(self, xrange, yrange):
        """
        初始化坐标范围.
        :param xrange:
        :param yrange:
        """
        self.plt = plt
        self.plt.figure()
        self.ax = plt.gca()
        self.ax.set_xlim([0, xrange])
        self.ax.set_ylim([0, yrange])
        self.x = []
        self.y = []

    def add_2d_vect(self, x, y):
        """
        为了更方便的理解矩阵运算，使用python matplotlib画出向量.
        :return:
        """
        self.x.append(x)
        self.y.append(y)
        self.ax.quiver((0,) * len(self.x), (0,) * len(self.y), self.x, self.y, angles='xy', scale_units='xy', scale=1)

    def add_all_2d_vect(self, x, y):
        """
        为了更方便的理解矩阵运算，使用python matplotlib画出向量.
        :return:
        """
        self.x.extend(x)
        self.y.extend(y)
        self.ax.quiver((0,) * len(self.x), (0,) * len(self.y), self.x, self.y, angles='xy', scale_units='xy', scale=1)

    def show(self):
        self.plt.draw()
        self.plt.show()

    def multi_matrix(self, matrix):
        x = []
        y = []
        data_mat = np.mat(matrix)
        for item in zip(self.x, self.y):
            res = np.dot(data_mat, np.array(item))
            x.append(res.item((0, 0)))
            y.append(res.item((0, 1)))
        return x, y


if __name__ == '__main__':
    coord = My2DCoordination(10, 10)
    coord.add_2d_vect(3, 4)
    x, y = coord.multi_matrix([[7, 2], [9, 5]])
    coord.add_all_2d_vect(x, y)
    coord.show()
