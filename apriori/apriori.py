def localDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


def createC1(dataSet):
    """
     去重，排序
    :param dataSet:
    :return:
    """
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    # the diff between py2 and py3.
    return list(map(frozenset, C1))


def scanD(D, Ck, minSupport):
    """
    这里是求出单个元素的支持度.
    :param D:
    :param Ck:
    :param minSupport:
    :return:
    """
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] = ssCnt[can] + 1
    num_items = float(len(D))
    ret_list = []
    support_data = {}
    for key in ssCnt:
        support = ssCnt[key] / num_items
        if support >= minSupport:
            ret_list.insert(0, key)
        support_data[key] = support
    return ret_list, support_data


def apriori_gen(lk, k):
    retlist = []
    lenlk = len(lk)
    for i in range(lenlk):
        for j in range(i + 1, lenlk):
            l1 = list(lk[i])[:k - 2]
            l2 = list(lk[j])[:k - 2]
            l1.sort()
            l2.sort()
            if l1 == l2:
                retlist.append(lk[i] | lk[j])
    return retlist


def apriori(dataset, min_support=0.5):
    cl = createC1(dataset)
    d = list(map(set, dataset))
    l1, supportdata = scanD(d, cl, min_support)
    l = [l1]
    k = 2
    while len(l[k - 2]):
        ck = apriori_gen(l[k - 2], k)
        lk, supk = scanD(d, ck, min_support)
        supportdata.update(lk)
        k = k + 1
    return l, supportdata


def rulesfromconseq(freqset, h1, support_data, bigrulelist, min_conf):
    m = len(h1[0])
    if len(freqset) > m + 1:
        hmp1 = apriori_gen(h1, m + 1)
        hmp1 = calcconf(freqset, hmp1, support_data, bigrulelist, min_conf)
        if len(hmp1) > 1:
            rulesfromconseq(freqset, hmp1, support_data, bigrulelist, min_conf)


def calcconf(freqset, h1, support_data, bigrulelist, min_conf):
    prunedh = []
    for conseq in h1:
        conf = support_data[freqset] / support_data[freqset - conseq]
        if conf >= min_conf:
            bigrulelist.append((freqset - conseq, conseq, conf))
            prunedh.append(conseq)
    return prunedh


def generate_rules(li, support_data, min_conf=0.7):
    bigrulelist = []
    for i in range(1, len(li)):
        for freqset in li[i]:
            h1 = [frozenset([item]) for item in frozenset]
            if i > 1:
                rulesfromconseq(freqset, h1, support_data, bigrulelist, min_conf)
            else:
                calcconf(freqset, h1, support_data, bigrulelist, min_conf)
    return bigrulelist


if __name__ == "__main__":
    dataset = localDataSet()
    datasets = list(map(set, dataset))
    items = createC1(dataset)
    print(scanD(items, datasets, 0.5))
