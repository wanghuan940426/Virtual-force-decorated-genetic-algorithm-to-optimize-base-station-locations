import copy
import random
import matplotlib.pyplot as plt
import os
import time
import numpy as np
import math

from Chromosome import Chromosome
from scence import scence
from record import record
from kdtree import kdtree


class GeneticAlgorithm:
    def __init__(self, L, M, N, R, M_grid, pm, pc, pop_size, max_gen, file_path_name,
                 Dth, k1, w1, w2, maxdis, GA_step, VF_step, seed_number):

        '''
            :param L: 场景变长，Km
            :param M: 基站总数
            :param N: 待选数
            :param R: 基站半径
            :param M_grid: 栅格数
            :param pm: 变异概率
            :param pc: 交叉概率
            :param pop_size: 种群大小
            :param max_gen: 最大迭代次数

            :param Dth: 两个点的距离等于这个时既无引力又无斥力
            :param k1: 感知距离系数
            :param w1: 引力系数
            :param w2: 斥力系数
            :param maxdis: 单次移动最大距离
            :param GA_step: 每GA_step步进行虚拟力引导
            :param VF_step: 每VF_step步离散化操作
        '''

        self.L = L
        self.M = M
        self.N = N
        self.R = R
        self.M_grid = M_grid
        self.pm = pm
        self.pc = pc
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.scence = scence(L, M, N, R, M_grid)

        self.Dth = Dth
        self.k1 = k1
        self.w1 = w1
        self.w2 = w2
        self.maxdis = maxdis
        self.GA_step = GA_step
        self.VF_step = VF_step
        self.Rs = k1 * R

        self.kdtree = kdtree(self.scence.sum_sites)

        para_dict = {'L':L, 'M':M, 'N':N, 'R':R, 'M_grid':M_grid, 'pm':pm, 'pc':pc,
                     'pop_size':pop_size, 'max_gen':max_gen, 'Dth':Dth, 'k1':k1,
                     'w1':w1, 'w2':w2, 'maxdis':maxdis, 'GA_step':GA_step, 'VF_step':VF_step, 'seed_number':seed_number}

        self.record = record(file_path_name)
        self.record.write_scence_para(para_dict)

        self.pop = []
        self.bests = [0] * max_gen
        self.g_best = 0

    def ga(self):
        """
        算法主函数
        :return:
        """
        start = time.time()
        self.init_pop()
        best = self.find_best()
        self.g_best = copy.deepcopy(best)
        y = [0] * self.max_gen
        self.record.write_cover_rate([0, self.g_best.y, self.g_best.y, self.g_best.y, self.g_best.y])
        for i in range(self.max_gen):
            self.cross()
            self.mutation()
            if (i+1) % self.GA_step == 0:
                for ii in range(self.pop_size):  # 由于编码经过交叉变异与之前不同，因此需要重新计算覆盖率，也就是适应性
                    self.pop[ii].func()
                best_for_vf = self.find_best()
                self.ori_point_index = copy.deepcopy(best_for_vf.x)
                self.ori_point = self.index_to_point(self.ori_point_index)
                self.cal_point_index = copy.deepcopy(best_for_vf.x)
                self.cal_point = self.index_to_point(self.cal_point_index)

                for j in range(self.VF_step):
                    self.vfa()
                    self.ori_point = copy.deepcopy(self.cal_point)
                self.ori_point = self.match_neighbor_point()
                #print(len(set([tuple(i) for i in self.ori_point])))
                select_chromosome = random.randint(0,self.pop_size-1)
                self.ori_point_index = self.point_to_index(self.ori_point)
                self.pop[select_chromosome].x = self.ori_point_index
                self.pop[select_chromosome].coding()
            self.select()
            best = self.find_best()
            self.bests[i] = best
            if self.g_best.y < best.y:
                self.g_best = copy.deepcopy(best)
            y[i] = self.g_best.y
            #print(self.g_best.y)
            self.cal_max_min_mean(i)

        excuteTime = time.time() - start
        self.record.write_cover_rate(excuteTime)


    def init_pop(self):
        """
        初始化种群
        :return:
        """
        for i in range(self.pop_size):
            chromosome = Chromosome(M, N, self.scence)
            self.pop.append(chromosome)

    def cal_max_min_mean(self, i):
        all_cov = []
        for idx in self.pop:
            all_cov.append(idx.y)
        all_cov = np.array(all_cov)
        value = [i, round(np.min(all_cov),5), round(np.mean(all_cov),5), round(np.max(all_cov),5), self.g_best.y]
        self.record.write_cover_rate(value)
        self.record.my_flush()

    def cross(self):
        """
        交叉，为了保证交叉后，每条基因的1的个数恒定，需要交换两条基因中，为1的某些部分。具体做法是，随机选两条不同的基因i与j，
        :return:
        """
        for i in range(int(self.pop_size / 2)):
            if self.pc > random.random():
                # randon select 2 chromosomes in pops
                i = 0
                j = 0
                while i == j:#这里随机选两条基因用于交叉
                    i = random.randint(0, self.pop_size-1)
                    j = random.randint(0, self.pop_size-1)
                pop_i = self.pop[i]
                pop_j = self.pop[j]

                #这里用于记录这两条基因，其中record_i_1中记录基因i中为1但基因j中为0的位置，其中record_j_1中记录基因i中为0但基因j中为1的位置，均由小到大
                record_i_1 = []
                record_j_1 = []
                for tmp in range(pop_i.code_length):
                    if (pop_i.code[tmp]==1) and (pop_j.code[tmp]==0):
                        record_i_1.append(tmp)
                    if (pop_i.code[tmp]==0) and (pop_j.code[tmp]==1):
                        record_j_1.append(tmp)
                # print(len(record_i_1))
                # print(len(record_j_1))
                assert(len(record_i_1)==len(record_j_1))

                if len(record_i_1)==0:
                    continue

                index = random.randint(0,len(record_i_1))#随机选个数，这个数之前的全部交换
                for tmp in range(index):
                    code_index_i = record_i_1[tmp]
                    code_index_j = record_j_1[tmp]

                    pop_i.code[code_index_i] = 0 if (pop_i.code[code_index_i]*2-1)>0 else 1
                    pop_i.code[code_index_j] = 0 if (pop_i.code[code_index_j]*2-1)>0 else 1

                    pop_j.code[code_index_i] = 0 if (pop_j.code[code_index_i]*2-1)>0 else 1
                    pop_j.code[code_index_j] = 0 if (pop_j.code[code_index_j]*2-1)>0 else 1

    def mutation(self):
        """
        变异
        :return:
        """
        for i in range(self.pop_size):
            if self.pm > random.random():
                pop = self.pop[i]
                # select mutation index
                index0 = 0
                index1 = 0
                while True:
                    this_rand = random.randint(0, self.M-1)
                    if pop.code[this_rand]==0:
                        index0 = this_rand
                        break
                while True:
                    this_rand = random.randint(0, self.M-1)
                    if pop.code[this_rand]==1:
                        index1 = this_rand
                        break
                pop.code[index0], pop.code[index1] = pop.code[index1], pop.code[index0]

    def select(self):
        """
        轮盘赌选择
        :return:
        """
        # calculate fitness function
        sum_f = 0
        for i in range(self.pop_size):#由于编码经过交叉变异与之前不同，因此需要重新计算覆盖率，也就是适应性
            self.pop[i].func()

        # guarantee fitness > 0
        min = self.pop[0].y
        max = self.pop[0].y
        for i in range(self.pop_size):
            if self.pop[i].y < min:
                min = self.pop[i].y
            if self.pop[i].y > max:
                max = self.pop[i].y


        p = [0] * self.pop_size  # 然后计算每个个体的概率
        if max==min:
            for i in range(self.pop_size):
                p[i] = self.pop[i].y
        else:
            for i in range(self.pop_size):
                p[i] = (self.pop[i].y - min)/ (max-min)

        # roulette
        for i in range(self.pop_size):#首先计算适应性的和
            sum_f += p[i]
        for i in range(self.pop_size):
            p[i] = p[i] / sum_f
        q = [0] * self.pop_size#根据概率计算每个个体处于轮盘的位置
        q[0] = 0
        for i in range(self.pop_size):
            s = 0
            for j in range(0, i+1):
                s += p[j]
            q[i] = s
        # start roulette
        v = []
        for i in range(self.pop_size):
            r = random.random()
            if r < q[0]:
                tmp = copy.deepcopy(self.pop[0])
                v.append(tmp)
            for j in range(1, self.pop_size):
                if q[j - 1] < r <= q[j]:
                    tmp = copy.deepcopy(self.pop[j])
                    v.append(tmp)
        self.pop = v

    def find_best(self):
        """
        找到当前种群中最好的个体
        :return:
        """
        best = copy.deepcopy(self.pop[0])
        for i in range(self.pop_size):
            if best.y < self.pop[i].y:
                best = copy.deepcopy(self.pop[i])
        return best

    def vfa(self):
        self.cover_rate = self.scence.cal_cov_vf(self.ori_point)
        self.cal_point = []
        for i in range(self.N):
            point = self.ori_point[i]
            point_att, point_rej = self.cal_related_point(i, point)
            att_add_list, rej_add_list = self.cal_force_vector(point, point_att, point_rej)
            force_sum = self.cal_sum_force(att_add_list, rej_add_list)
            newpoint = self.cal_remove_distance(point, force_sum)
            self.cal_point.append(newpoint)

    def cal_related_point(self, i, point):
        point_att = []
        point_rej = []
        for j in range(self.N):
            if i != j:
                dis = np.linalg.norm(np.array(point) - np.array(self.ori_point[j]))
                if dis >= self.Rs or dis == self.Dth:
                    pass
                # 引力
                elif dis < self.Rs and dis > self.Dth:
                    point_att.append(self.ori_point[j])
                # 斥力
                elif dis < self.Dth:
                    point_rej.append(self.ori_point[j])
        return (point_att, point_rej)

    def cal_force_vector(self, point, point_att, point_rej):
        att_add_list = []
        rej_add_list = []
        for temp in point_att:
            att_add_list.append([temp[0] - point[0], temp[1] - point[1]])
        for temp in point_rej:
            rej_add_list.append([-temp[0] + point[0], -temp[1] + point[1]])
        return (att_add_list, rej_add_list)

    def cal_sum_force(self, att_add_list, rej_add_list):
        att_force_list = []
        rej_force_list = []
        force_sum = [0, 0]
        for temp in att_add_list:
            fx, fy = self.depart_att(temp)
            att_force_list.append([fx, fy])
        for temp in rej_add_list:
            fx, fy = self.depart_rej(temp)
            rej_force_list.append([fx, fy])
        for temp in att_force_list:
            force_sum[0] += temp[0]
            force_sum[1] += temp[1]
        for temp in rej_force_list:
            force_sum[0] += temp[0]
            force_sum[1] += temp[1]
        return force_sum

    def depart_att(self, temp):
        dij = math.sqrt(temp[0] ** 2 + temp[1] ** 2)
        fx, fy = 0, 0
        if dij < self.Rs and dij > self.Dth:
            fw = self.w1 * (dij - self.Dth)
            fx = round(fw * (temp[0] / dij), 5)
            fy = round(fw * (temp[1] / dij), 5)
        elif dij == self.Dth:
            fx, fy = 0, 0
        elif dij > self.Rs:
            fx, fy = 0, 0
        return fx, fy

    # 斥力反比例
    def depart_rej(self, temp):
        dij = math.sqrt(temp[0] ** 2 + temp[1] ** 2)
        fx, fy = 0, 0
        if dij <= self.Dth and dij > 0.001:
            fw = self.w2 * (1 / dij)
            fx = round(fw * (temp[0] / dij), 4)
            fy = round(fw * (temp[1] / dij), 4)
        elif dij <= 0.001:
            fx = random.random() * 10
            fy = random.random() * 10
        return fx, fy

    def cal_remove_distance(self, point, force_sum):
        fs = math.sqrt(force_sum[0] ** 2 + force_sum[1] ** 2)
        l = self.L - 0.866*self.R
        if fs != 0:
            new_point_ideal = [0, 0]
            new_point_ideal[0] = point[0] + force_sum[0] / fs * self.maxdis * math.exp(-1 / fs)
            new_point_ideal[1] = point[1] + force_sum[1] / fs * self.maxdis * math.exp(-1 / fs)
        else:
            new_point_ideal = point
        if new_point_ideal[0] <= 0.866*self.R or new_point_ideal[0] >= l or new_point_ideal[1] <= 0.866*self.R or new_point_ideal[1] >= l:
            new_point_ideal = point
        return new_point_ideal

    def match_neighbor_point(self):
        ori_point = []
        for i in self.cal_point:
            ori_point.append(self.kdtree.serch(i))
        return ori_point

    def index_to_point(self, index):
        point = []
        for idx in index:
            point.append(self.scence.sum_sites[idx])
        return point

    def point_to_index(self, point):
        index = []
        for idx, i in enumerate(self.scence.sum_sites):
            if i in point:
                index.append(idx)
        return index




if __name__ == '__main__':

    '''
        :param L: 场景变长，Km
        :param M: 基站总数
        :param N: 待选数
        :param R: 基站半径
        :param M_grid: 栅格数
        :param pm: 变异概率
        :param pc: 交叉概率
        :param pop_size: 种群大小
        :param max_gen: 最大迭代次数
        
        :param Dth: 两个点的距离等于这个时既无引力又无斥力
        :param k1: 感知距离系数
        :param w1: 引力系数
        :param w2: 斥力系数
        :param maxdis: 单次移动最大距离
        :param GA_step: 每GA_step步进行虚拟力引导
        :param VF_step: 每VF_step步离散化操作
    '''



#############################################################################################################

#  1、固定场景参数，更改算法参数
#     L, M, N, R = 10, 400, 45, 1
#     M_grid = L * 4
#
#     max_gen = 500
#
#     pm_list = [0.1, 0.01]
#     pc_list = [0.8, 0.7]
#     pop_size_list = [10]
#
#     Dth= math.sqrt(3) * R
#     k1 = 2.5
#     w1 = 0.2
#     w2= 20
#     maxdis = 0.3
#     GA_step = 10
#     VF_step = 5
#
#     for pm in pm_list:
#         for pc in pc_list:
#             for pop_size in pop_size_list:
#                 print(str(pm)+'_'+str(pc))
#                 seed_number = 28
#                 random.seed(seed_number)
#                 file_path_name = './record/'+str(pm)+'_'+str(pc)+'_'+str(pop_size)+'.txt'
#                 algorithm = GeneticAlgorithm(L, M, N, R, M_grid, pm, pc, pop_size, max_gen, file_path_name,
#                                              Dth, k1, w1, w2, maxdis, GA_step, VF_step, seed_number)
#                 algorithm.ga()

#############################################################################################################


#############################################################################################################

#  2、固定算法参数，更改场景参数

#     R = 3
#
#     max_gen = 500
#
#     pm = 0.1
#     pc = 0.8
#     pop_size = 10
#
#     L_M_N_list = [(20, 180, 20)]
#
#     for L_M_N in L_M_N_list:
#         print(L_M_N)
#         L, M, N = L_M_N
#         M_grid = L * 4
#         random.seed(8)
#         file_path_name = './record/'+str(L)+'_'+str(M)+'_'+str(N)+'.txt'
#
#         algorithm = GeneticAlgorithm(L, M, N, R, M_grid, pm, pc, pop_size, max_gen, file_path_name)
#         algorithm.ga()

#############################################################################################################



#############################################################################################################

#  1、固定场景参数，更改算法参数
    L, M, N, R = 10, 600, 45, 1
    M_grid = L * 4

    max_gen = 500

    pm = 0.1
    pc = 0.8
    pop_size = 12

    Dth_list = [1.3*R, 1.5* R, 1.7*R, 1.9*R, 2.1*R, 1.1*R]
    k1 = 2.5
    w1 = 0.2
    w2 = 200
    maxdis = 0.15
    GA_step = 10
    VF_step = 5
    for Dth in Dth_list:
        print(str(Dth))
        seed_number = 20000
        random.seed(seed_number)
        file_path_name = './record1-1/'+str(w1)+'_'+str(w2)+'_'+str(Dth)+'.txt'
        algorithm = GeneticAlgorithm(L, M, N, R, M_grid, pm, pc, pop_size, max_gen, file_path_name,
                                     Dth, k1, w1, w2, maxdis, GA_step, VF_step, seed_number)
        algorithm.ga()

#############################################################################################################