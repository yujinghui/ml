import matplotlib.pyplot as plt


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

    def draw_2d_vect(self, x, y):
        """
        为了更方便的理解矩阵运算，使用python matplotlib画出向量.
        :return:
        """
        self.ax.quiver((0,), (0,), (x,), (y,), angles='xy', scale_units='xy', scale=1)
        self.plt.draw()
        self.plt.show()


if __name__ == '__main__':
    coord = My2DCoordination(10, 10)
    coord.draw_2d_vect(3, 4)
