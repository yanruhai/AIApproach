import random

import numpy as np
from numpy.ma.core import arange

from queen8 import Queen

class QueenGenetic:
    queens=[]
    pair=0
    n=0
    def __init__(self,queens,n):
        self.queens=queens
        self.pair=len(queens)#有多少个queen
        self.n=n#n皇后

    def _fitness_function(self):
        fitness=[q.count_attacking_pairs() for q in self.queens]
        total=sum(fitness)
        for ind,i in enumerate(fitness):
            fitness[ind]=i/total
        # 按照概率选择数据
        select_queens = np.random.choice(arange(self.pair), size=self.pair, p=fitness)
        #print(selected_data)
        return select_queens

    def _select_crossover(self,select_queens):
        for q1, q2 in zip(select_queens[::2], select_queens[1::2]):
            if q1!=q2:
                k=random.randint(1,self.n-1)
                for i in arange(k):#交换
                    t=self.queens[q1].queens[i]
                    self.queens[q1].queens[i]=self.queens[q2].queens[i]
                    self.queens[q2].queens[i]=t

    def _mutation(self):
        p_m = 0.05  # 变异概率
        for j in range(self.pair):
            for i in range(self.n):  # 遍历染色体的n个基因位
                if random.uniform(0, 1) < p_m:
                    # 基因位 i 发生变异
                    t=random.randint(0,self.n)
                    self.queens[j].queens[i]=t#mutation

    def search(self):
        while True:
            fitness= self._fitness_function()
            self._select_crossover(fitness)
            self._mutation()
            for i in range(self.pair):
                cat=self.queens[i].count_attacking_pairs()
                #print(cat,end=',')
                if cat==0:
                    return self.queens[i]
            #print()



def create_queen(m,k,qs):
    for i in range(m):
        q1 = [random.randint(0, k - 1) for _ in range(k)]
        qt1 = Queen(k, q1)
        q2 = [random.randint(0, k - 1) for _ in range(k)]
        qt2 = Queen(k, q2)
        qs.append(qt1)
        qs.append(qt2)

k=100
random.seed=21
qs=[]
create_queen(25,k,qs)
qt=QueenGenetic(qs,k)
an= qt.search()
print(an.queens)











