from chap3.search import State


static_id=0

class TictactoeState(State):
    board =[[0,0,0],[0,0,0],[0,0,0]]
    _dir=[[0,1],#right
          [1,0],#down
          [1,1],[1,-1]]#四个方向
    def __init__(self,board):
        self.board=board
        global static_id
        self.id=static_id
        static_id+=1

    def __get_score(self,who):
        if who==1:
            return [1,0]
        else: return [0,1]


    def who_win(self):
        '''8个方向检测，[0,0]:[right,down,main],
                    [0,1]:[right],[0,2]:[down,second],
                    [1,0]:[right],[2,0]:[right]
                对应的方向 right:0,down:1,main:2,second:3
        '''
        '''if self.id<=4:
            return [0,0]'''
        t00=self.board[0][0]#下标00开始3个方向
        t=self.__check_goal(t00,[0,0],[0,1,2])
        if t:return self.__get_score(t00)
        t01=self.board[0][1]
        t=self.__check_goal(t01,[0,1],[1])
        if t: return self.__get_score(t01)
        t02=self.board[0][2]
        t = self.__check_goal(t02, [0, 2], [1, 3])
        if t:return self.__get_score(t02)
        t10=self.board[1][0]
        t = self.__check_goal(t10, [1,0], [0])
        if t: return self.__get_score(t10)
        t20=self.board[2][0]
        t = self.__check_goal(t20, [2,0], [0])
        if t: return self.__get_score(t20)



    def __check_goal(self,value,start_point,dir_ind):
        '''dir_ind表示需要测试的方向列表下标'''
        t=start_point
        if value==0:
            return False
        for ind in dir_ind:
            while t[0]<3 and t[1]<3:
                if self.board[t[0]][t[1]]!=value:
                    return False#测试未通过
                t[0]+=t[0]+self._dir[ind][0]
                t[1]+=t[1]+self._dir[ind][1]
        return True#全部相等




init_state=[[0,0,1],
            [0,2,1],
            [2,0,1]]
ts=TictactoeState(init_state)
ts2=TictactoeState(init_state)
print(ts.get_id())
print(ts2.get_id())
print(ts.who_win())

