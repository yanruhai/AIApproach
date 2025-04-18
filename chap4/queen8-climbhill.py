import numpy as np
import enum
import math
import random
import copy

from sympy import limit


class Queen:
    queens=[]
    limit=0
    score=0#可以互相攻击的对数
    def __init__(self,limit,queens:list):
        self.limit=limit
        self.queens=queens
        self.score=self.count_attacking_pairs()

    def count_attacking_pairs(self):
        """
        此函数用于计算 8 皇后棋盘上可相互攻击的皇后对数
        :param queens: 一个列表，索引表示列，值表示该行皇后所在的行
        :return: 可相互攻击的皇后对数
        """
        count = 0
        for i in range(self.limit):
            for j in range(i + 1, self.limit):
                # 检查是否在同一行
                if self.queens[i] == self.queens[j]:
                    count = count + 1
                # 检查是否在正对角线上
                if abs(self.queens[i] - self.queens[j]) == abs(i - j):
                    count = count + 1
        self.score=count
        return count

    def goal_check(self):
        if self.score==0:
            return True
        return False

    def tune(self):
        first_score=self.score
        for col in range(self.limit):
            temp_score=math.inf
            temp_i=0
            for i in range(self.limit):
                 self.queens[col]=i
                 score=self.count_attacking_pairs()
                 if score<temp_score:
                     temp_score=score
                     temp_i=i
            if temp_score<self.score:#找到了更好的解
                self.queens[col]=temp_i
                self.score=temp_score
                #print(self.queens)
                print(f"temp_score:{temp_score},first_score={first_score}")
                print(f"score:{self.score}")
                if self.goal_check():
                    return 0
        ts=first_score!=self.score#是否有更好的解
        return ts

    def check_local_minimum(self):
        for i in range(self.limit):#第i列
            for j in range(self.limit):
                qs=copy.copy(self.queens)
                qs[i]=j
                temp_queen=Queen(self.limit,qs)
                if temp_queen.score<self.score:
                    return True
        return False


    def search(self):
        temp_sc=self.count_attacking_pairs()
        last_sc=temp_sc
        while last_sc>0:
            temp_sc=self.tune()
            last_sc=self.score
            if self.goal_check():
                return self.queens
            if not temp_sc:
                t=self.check_local_minimum()
                if not t:#陷入局部最小值
                    qt = [random.randint(0, self.limit - 1) for _ in range(self.limit)]
                    self.queens=qt
                    self.count_attacking_pairs()#重新计算分数

        return self.queens









k=100
random.seed=21
q = [random.randint(0, k-1) for _ in range(k)]
#q=[1,1,1,1,1,1,1,1]
qu=Queen(k,q)
q=qu.search()
print(q)

'''ss=[62, 41, 71, 81, 9, 22, 12, 37, 18, 25, 42, 24, 26, 40, 58, 16, 64, 46, 52, 80, 84, 94, 34, 68, 65, 83, 10, 19, 47, 85, 79, 2, 28, 70, 27, 29, 89, 92, 97, 8, 78, 93, 75, 43, 87, 33, 3, 7, 0, 48, 86, 98, 31, 74, 17, 66, 1, 88, 11, 39, 51, 76, 5, 91, 99, 14, 73, 56, 90, 44, 36, 30, 95, 23, 21, 72, 96, 4, 54, 77, 50, 45, 38, 60, 67, 57, 6, 35, 53, 63, 20, 69, 15, 55, 61, 49, 32, 82, 59, 13]
f=Queen(k,ss)
print(f.score)'''

