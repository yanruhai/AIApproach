from chap5.py_chess import PlayChess, ChessState
from tictactoe import TictactoeState

class PostorderTravelTree(PlayChess):


    def player(self, state:ChessState):
        return 1

    def utility(self, state, player):
       return state.who_win()

    def __init__(self):
        pass

    def terminal_test(self,node):
        if node>30:
            return True
        return False

    def actions(self,node):
        return node.get_actions()

    def result(self,node,act):
        return act

    def last_visit(self,limit,node):
        '''b是分支数,node是第一个访问的节点，一般是1'''
        stack=[]
        k=0#子节点从左往右的编号
        d=0#深度
        while True:
            stack.append((node, k,d))
            b_list=self.actions(node)
            if k<len(b_list):
                    if not self.terminal_test(node):#子节点存在
                        node=self.result(node,b_list[k])#向下移动,新节点
                        k=0
                        d+=1
                    else:
                        node, k,d = stack.pop()
                        k += 1
            else:#走完最后一个节点
                print(node)
                if len(stack) <= 1:
                    break
                else:
                    stack.pop()  # 当前的数据不要了
                    node, k ,d= stack.pop()
                    k += 1









board =[[0,0,0],[0,0,0],[0,0,0]]
ts= TictactoeState(board)
post=PostorderTravelTree()
post.last_visit(3,ts)
