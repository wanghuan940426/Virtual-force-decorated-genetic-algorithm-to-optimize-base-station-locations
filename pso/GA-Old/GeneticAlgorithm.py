import copy
import random
import matplotlib.pyplot as plt
import os
import time
import numpy as np

from Chromosome import Chromosome
from scence import scence
from record import record


class GeneticAlgorithm:
    def __init__(self, L, M, N, R, M_grid, pm, pc, pop_size, max_gen, file_path_name):
        """
        算法初始化
        :param L: 场景变长，Km
        :param M: 基站总数
        :param N: 待选数
        :param R: 基站半径
        :param M_grid: 栅格数
        :param pm: 变异概率
        :param pc: 交叉概率
        :param pop_size: 种群大小
        :param max_gen: 最大迭代次数
        :return:
        """
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

        para_dict = {'L':L, 'M':M, 'N':N, 'R':R, 'M_grid':M_grid, 'pm':pm, 'pc':pc,
                     'pop_size':pop_size, 'max_gen':max_gen}

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
            start_time = time.time()
            self.cross()
            self.mutation()
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

        # # plt
        # plt.figure(1)
        # x = range(self.max_gen)
        # plt.plot(x, y)
        # plt.ylabel('generations')
        # plt.xlabel('function value')
        # plt.show()

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
        for i in range(self.pop_size):
            if self.pop[i].y < min:
                min = self.pop[i].y
        if min < 0:#由于轮盘赌需要概率均大于零，那么某个个体的适应性小于0的话，需要将所有的个体的概率均加上最小的概率，以确保所有的概率值大于0
            for i in range(self.pop_size):
                self.pop[i].y = self.pop[i].y + (-1) * min

        # roulette
        for i in range(self.pop_size):#首先计算适应性的和
            sum_f += self.pop[i].y
        p = [0] * self.pop_size#然后计算每个个体的概率
        for i in range(self.pop_size):
            p[i] = self.pop[i].y / sum_f
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
    '''


#############################################################################################################

#  1、固定场景参数，更改算法参数
    L, M, N, R = 10, 600, 45, 1
    M_grid = L * 4

    max_gen = 500

    pm_list = [0.1]
    pc_list = [0.8]
    pop_size_list = [12]

    for pm in pm_list:
        for pc in pc_list:
            for pop_size in pop_size_list:
                print(str(pm)+'_'+str(pc))
                random.seed(60000)
                file_path_name = './record/'+str(pm)+'_'+str(pc)+'_'+str(pop_size)+'.txt'
                algorithm = GeneticAlgorithm(L, M, N, R, M_grid, pm, pc, pop_size, max_gen, file_path_name)
                algorithm.ga()

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