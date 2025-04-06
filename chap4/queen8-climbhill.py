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
        count=10
        last_sc=temp_sc
        while last_sc>0:
            temp_sc=self.tune()
            if not temp_sc:
                count-=1
            print(f"count={count}")
            last_sc=self.score
            if count==0:
                count=10
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

'''ss=[73, 12, 78, 16, 99, 97, 23, 26, 48, 86, 32, 34, 40, 33, 6, 8, 52, 38, 30, 58, 49, 54, 63, 60, 25, 15, 68, 88, 0, 61, 81, 13, 47, 83, 89, 22, 82, 85, 62, 91, 11, 51, 46, 70, 93, 90, 35, 20, 43, 27, 59, 76, 1, 87, 24, 99, 3, 75, 2, 28, 45, 96, 69, 0, 50, 42, 92, 5, 98, 1, 72, 39, 14, 31, 10, 18, 67, 71, 84, 19, 21, 36, 44, 29, 37, 4, 66, 41, 9, 17, 65, 74, 7, 56, 53, 55, 57, 64, 77, 80]
f=Queen(k,ss)
print(f.score)'''

