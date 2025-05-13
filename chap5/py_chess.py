import abc

from chap3.search import State


class ChessState(State):

    _depth=0#树深度

    @property
    def depth(self):
        return self._depth


    @depth.setter
    def depth(self, value):
        self._depth=value





class PlayChess(abc.ABC):

    @abc.abstractmethod
    def player(self,state):
       pass

    @abc.abstractmethod
    def actions(self,state):
        pass

    @abc.abstractmethod
    def result(self,state,act):
        pass

    @abc.abstractmethod
    def terminal_test(self,state):
        pass

    @abc.abstractmethod
    def utility(self,state,player):
        pass