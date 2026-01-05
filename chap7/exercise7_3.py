from abc import ABC, abstractmethod


class PL:
    _id:str
    '''命题变量'''
    _value:bool
    '''真值'''

    def __init__(self,id,value=None,exp=None):
        self._id=id
        self._value=value

    def has_value(self):
        if self._value==None:
            return False
        return True

    def compute_value(self,model):#计算真值
        v=model.dict_value.get(self.id)
        return v

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,id):
        self._id=id

    def get_id_set(self,var_set):
        var_set.add(self.id)
        return var_set



class Not(PL):
    '''单元素运算符,取反'''
    pl:PL
    def __init__(self,pl,value=None):
        if isinstance(pl,PL):
            self.pl=pl
            super().__init__('¬' + pl.id, value=value)
        else:#输入字符
            self.pl=PL(pl)
            super().__init__('¬' + pl, value=value)


    @property
    def value(self):
        if self.pl.has_value():
            return not self.pl.value
        return None

    @value.setter
    def value(self,value):
        self._value=value

    def set_id_value(self,id,value):
        self.pl.set_id_value(id,value)

    def compute_value(self,model):
        return not self.pl.compute_value(model)

    def get_id_set(self, var_set):
        return self.pl.get_id_set(var_set)


class OpComputable(ABC, PL):
    '''二元可计算逻辑的对象，继承于谓词逻辑PL'''
    @abstractmethod
    def _compute_step(self,l_value,r_value,*arg):#arg用于多元情况
        '''子类需要根据自己的情况返回真值'''
        pass

    @abstractmethod
    def _get_op_str(self):
        pass

    def get_id_set(self,var_set):
        return self.left.get_id_set(var_set)|self.right.get_id_set(var_set)

    def compute_value(self,model):
        l_value= self.left.compute_value(model)
        r_value= self.right.compute_value(model)
        return self._compute_step(l_value,r_value)


    def __init__(self,left,right,*args):
        if isinstance(left, PL):
            self.left=left
        else:#如果是字符
            self.left=PL(left)
        if isinstance(right , PL):
            self.right=right
        else:
            self.right=PL(right)
        PL.__init__(self, '('+self.left.id +self._get_op_str()+ self.right.id+')', None)


class Impli(OpComputable):
    def _get_op_str(self):
        return '→'

    def _compute_step(self,l_value,r_value):
        if l_value and not r_value:
            return False
        return True


class Or(OpComputable):
    def _get_op_str(self):
        return '∨'

    def _compute_step(self,l_value,r_value):
        if l_value or r_value:
            return True
        return False

class And(OpComputable):
    def _get_op_str(self):
        return '∧'

    def _compute_step(self,l_value,r_value):
        if not l_value or not r_value:
            return False
        return True
    
class Model:#模型类，对命题指派具体值
    _dict_value:dict
    def __init__(self):
        self._dict_value={}

    @property
    def dict_value(self):
        return self._dict_value

    def put(self,id,value):
        self.dict_value[id]=value

id_set=set()
ex=Not(Impli(Not('s'),Impli(Not(Or('p','q')),'p')))
m=Model()
m.put('p',True)
m.put('s',True)
m.put('q',True)
print(ex.id)
print(ex.get_id_set(id_set))
print(m.dict_value)
v=ex.compute_value(m)
print(v)



















A=PL('A',True)
B=PL('B',False)
te=Impli(B,Impli(A,B))





