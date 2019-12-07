# -*- coding:utf-8 -*-

import random
import numpy as np


class scence:
    def __init__(self, L, M, N, R, M_grid):
        '''
        :param L: 场景变长，Km
        :param M: 基站总数
        :param N: 待选数
        :param R: 基站半径
        :param M_grid: 栅格数
        '''
        self.L = L
        self.M = M
        self.N = N
        self.R = R
        self.M_grid = M_grid

        self.Initial_scene()

        self.con_grid()

    # 初始化规划场景
    # l为规划区域的边长，l为待选的站点数目
    def Initial_scene(self):
        self.sum_sites = [[round(random.random()*self.L, 3) for _i in range(2)] for _j in range(self.M)]
        #print(self.sum_sites)


    #后期可以用kd_tree加速算法
    # 计算覆盖率,采用均匀的栅格点覆盖
    # m表示边长的单位，m_g表示栅格的
    # 输出为一个m_g*m_g的矩阵
    def con_grid(self):
        a = np.linspace(0, self.L, self.M_grid)
        self.cov_list = []
        for i in range(len(a)):
            for j in range(len(a)):
                self.cov_list.append([a[i], a[j]])

    # 计算覆盖率
    def cal_cov(self, choose_BS_list):
        point = []
        for tmp in choose_BS_list:
            point.append(self.sum_sites[tmp])
        cov_num = 0
        all_point = len(self.cov_list)
        for i in range(all_point):
            for j in range(len(point)):
                if (np.linalg.norm(np.array(self.cov_list[i]) - np.array(point[j]))) <= self.R:
                    cov_num += 1
                    break
        cov_rate = round(cov_num / all_point, 5)
        return cov_rate

    def cal_cov_vf(self, point):
        cov_num = 0
        all_point = len(self.cov_list)
        for i in range(all_point):
            for j in range(len(point)):
                if (np.linalg.norm(np.array(self.cov_list[i]) - np.array(point[j]))) <= self.R:
                    cov_num += 1
                    break
        cov_rate = round(cov_num / all_point, 5)
        return cov_rate



if __name__ == '__main__':
    my_scence = scence(50, 200, 40, 5, 50*1)
    choose_BS_list = [3,12,40]
    cov_rate = my_scence.cal_cov(choose_BS_list)
    print(cov_rate)
