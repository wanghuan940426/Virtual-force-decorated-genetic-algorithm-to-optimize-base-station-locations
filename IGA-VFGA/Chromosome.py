# -*- coding:utf-8 -*-

import random


class Chromosome:
    def __init__(self, M, N, my_scence, alpha1, alpha2, alpha3):

        self.alpha1, self.alpha2, self.alpha3 = alpha1, alpha2, alpha3

        self.all_BS, self.choose_BS = M, N
        self.scence = my_scence

        self.x = [0]*self.choose_BS
        self.y = 0

        self.code = [0]*self.all_BS

        self.code_length = self.all_BS

        self.rand_init()

        self.func()


    def rand_init(self):
        self.code = [1]*self.choose_BS + [0]*(self.code_length-self.choose_BS)
        random.shuffle(self.code)


    def decoding(self):
        self.x=[]
        for idx, i in enumerate(self.code):
            if i == 1:
                self.x.append(idx)

    def func(self):
        self.decoding()
        self.y1 =  self.alpha1 * self.scence.cal_cov(self.x)

        self.y2=0
        self.y3=0
        for i in self.x:
            self.y2 += self.scence.cost[i]
            self.y3 += self.scence.accept[i]
        self.y2 = self.alpha2 * self.y2 / len(self.x)
        self.y3 = self.alpha3 * self.y3 / len(self.x)

        self.y = self.y1+self.y2+self.y3

    def coding(self):
        self.x.sort()
        self.code = [0] * self.all_BS
        for i in self.x:
            self.code[i] = 1
        while self.choose_BS != sum(self.code):
            self.code[random.randint(0,self.all_BS-1)]=1
        self.func()





if __name__ == '__main__':

    for i in range(20):
        L, M, N, R, R_grid = 50, 200, 40, 5, 50 * 1

        from scence import scence
        my_scence = scence(L, M, N, R, R_grid)
        chromosome = Chromosome(M, N, my_scence)
        print(chromosome.y)
