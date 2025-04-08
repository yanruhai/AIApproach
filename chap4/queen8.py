import math
import random
import copy

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