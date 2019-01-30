'''
和霍夫曼树相似的地方，都是权重越高离根节点越近。
霍夫曼树离不开优先队列，fpgrowthtree并不需要，只是根据数据集构造一个树.
'''


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
