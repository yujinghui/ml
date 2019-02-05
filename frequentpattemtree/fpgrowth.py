'''
和霍夫曼树相似的地方，都是权重越高离根节点越近,
 都需要在构造树之前扫一遍数据集以便构造出节点权重（红黑）或者支持度（fptree)
霍夫曼树离不开优先队列，fpgrowthtree需要头指针表.
'''


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, num_occur):
        self.count = + self.count + num_occur

    def disp(self, index=1):
        for child in self.children.values():
            child.disp(index + 1)


def update_header(node, targetnode):
    """
    更新heddertable中的链表结构。
    :param node:
    :param targetnode:
    :return:
    """
    while node.nodeLink is not None:
        node = node.nodeLink
    node.nodeLink = targetnode


def update_tree(ordereditems, rettree, headertable, count):
    if ordereditems[0] in rettree.children:
        rettree.children[ordereditems[0]].inc(count)
    else:
        rettree.children[ordereditems[0]] = treeNode(ordereditems[0], count, rettree)
        if headertable[ordereditems[0]][1] is None:
            headertable[ordereditems[0]][1] = rettree.children[ordereditems[0]]
        else:
            update_header(headertable[ordereditems[0]][1], rettree.children[ordereditems[0]])
    if len(ordereditems) > 1:
        update_tree(ordereditems[1::], rettree[ordereditems[0]], headertable, count)


def create_tree(dataSet, minsup=1):
    """
    :param dataSet: 形如 {frozenset('a', 'f'): 1, ...} from createInitSet
    :param minsup:
    :return:
    """
    headertable = {}
    # 计算出每一个元素的支持度
    for trans in dataSet:
        for item in trans:
            # 这里dataSet[trans] 一直等于1.
            headertable[item] = headertable.get(item, 0) + dataSet[trans]
    # 移除支持度小于minsup的元素
    for k in headertable.keys():
        if headertable[k] < minsup:
            del headertable[k]

    freqitemset = set(headertable.keys())
    if len(freqitemset) == 0:
        return None, None

    for k in headertable.keys():
        headertable[k] = [headertable[k], None]
    rettree = treeNode('null set', 1, None)

    for transet, count in dataSet.items():
        locald = {}
        for item in transet:
            if item in freqitemset:
                locald[item] = headertable[item][0]
        if len(locald) > 0:
            ordereditems = [v[0] for v in sorted(locald.items(), key=lambda p: p[1], reverse=True)]
            update_tree(ordereditems, rettree, headertable, count)
    return rettree, headertable


def ascend_tree(leafnode, prefixpath):
    """
    自底向上查找直到根节点.
    :param leafnode:
    :param prefixpath:
    :return:
    """
    if leafnode.parent is not None:
        prefixpath.append(leafnode.name)
        ascend_tree(leafnode.parent, prefixpath)


def findprefixpath(basePat, treenode):
    """
    返回条件模式基.
    :param basePat: 感觉这个参数没啥用.
    :param treenode:
    :return:
    """
    codpats = {}
    while treenode is not None:
        prefixpath = []
        ascend_tree(treenode, prefixpath)
        if len(prefixpath) > 1:
            codpats[frozenset(prefixpath[1:])] = treenode.count
        treenode = treenode.nodeLink
    return codpats


def minetree(rettree, headertable, minsup, prefix, freqitemlist):
    bigl = [v[0] for v in sorted(headertable.items(), key=lambda p: p[1])]
    for basepat in bigl:
        newfreqset = prefix.copy()
        newfreqset.add(basepat)
        freqitemlist.append(newfreqset)
        condpattbases = findprefixpath(basepat, headertable[basepat][1])
        mycondtree, myhead = create_tree(condpattbases, minsup)
        if myhead is not None:
            minetree(mycondtree, myhead, minsup, newfreqset, freqitemlist)


if __name__ == "__main__":
    print(createInitSet(loadSimpDat()))
