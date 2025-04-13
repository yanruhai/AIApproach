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

    def tune_random(self,num_k):
        '''num_k是需要调整的个数'''
        if num_k==0:
            return
        numbers_col = random.sample(range(0, self.limit), num_k)
        numbers_row = random.sample(range(0, self.limit), num_k)
        for ind,col in enumerate(numbers_col):
           self.queens[col]=numbers_row[ind]
        self.count_attacking_pairs()


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

q=Queen(100,  [84, 33, 51, 4, 15, 44, 61, 88, 83, 78, 54, 18, 31, 70, 40, 7, 66, 76, 79, 57, 97, 35, 9, 23, 13, 96, 34, 39, 80, 75, 32, 74, 95, 12, 17, 38, 29, 43, 69, 67, 58, 45, 98, 73, 11, 55, 91, 72, 22, 47, 8, 41, 81, 10, 71, 24, 19, 99, 14, 94, 30, 77, 16, 87, 49, 46, 2, 90, 1, 89, 85, 93, 52, 26, 65, 48, 36, 82, 3, 6, 21, 28, 59, 27, 5, 50, 62, 42, 0, 60, 56, 63, 53, 68, 20, 25, 64, 92, 86, 37])
print(q.score)