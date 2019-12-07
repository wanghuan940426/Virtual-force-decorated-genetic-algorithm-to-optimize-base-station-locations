# -*- coding:utf-8 -*-

from scipy import spatial
import numpy as np

class kdtree:
    def __init__(self, data):
        self.tree = spatial.KDTree(data)
        self.data = self.tree.data

    def serch(self, point):
        result = self.tree.query(np.array(point))
        return self.data[result[1]].tolist()



if __name__ == '__main__':
    x, y = np.mgrid[0:5, 2:8]
    test = list(zip(x.ravel(), y.ravel()))
    my_kdtree = kdtree(test)
    point = [0,0]
    result = my_kdtree.serch(point)
    print(result)