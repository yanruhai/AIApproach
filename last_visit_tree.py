

def last_visit(limit,node,b):
    '''b是分支数,node是第一个访问的节点，一般是1'''
    stack=[]
    k=0
    added=b-2
    while True:
        stack.append((node, k))
        if k<b:
                if node*b-added+k<=limit:#子节点存在
                    node=node*b-added+k
                    k=0
                else:
                    node, k = stack.pop()
                    k += 1
        else:#走完最后一个节点
            print(node)
            if len(stack) <= 1:
                break
            else:
                stack.pop()  # 当前的数据不要了
                node, k = stack.pop()
                k += 1











b_tree=[0,1,2,3,4,5,6,7]
last_visit(31,1,5)
