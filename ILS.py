import numpy as np

import abc

# 定义抽象基类
class ILS(abc.ABC):#iterative lengthening search
    init_state=None

    def __init__(self,init_state):
        self.init_state=init_state
        
    @abc.abstractmethod
    def area(self):
        """计算面积的抽象方法"""
        pass

    @abc.abstractmethod
    def perimeter(self):
        """计算周长的抽象方法"""
        pass