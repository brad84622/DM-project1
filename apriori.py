import numpy as np

def main():
    f=np.loadtxt('op.data','int')
    (m,n)=(f.shape)
    minSupport=0.5
    d={}
    C1 = []
    for i in range(f[-1, 0]):
        d[i+1] = []
    for i in range(m):
        d[f[i, 0]].append(f[i, 2])
        if not f[i][2] in C1:
            C1.append(f[i][2])
    C1.sort()
    B1=[]
    for i in range(len(C1)):
        B1.append(frozenset({C1[i]}))
    D=[]
    for i in range(len(d)):
        D.append(d[i+1])
    (L1, supportData)=scanD(D,B1,0.5)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
            Ck = aprioriGen(L[k-2], k)
            Lk, supK = scanD(D, Ck, minSupport) 
            supportData.update(supK)
            if len(Lk) == 0:
                break
            L.append(Lk)
            k += 1
    rules = generateRules(L, supportData, minConf=0.7)
    print('rules: ', rules)
    
def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                key=can
                if key not in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D)) 
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k):    
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[: k-2]
            L2 = list(Lk[j])[: k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = []
    for conseq in H: 
        conf = supportData[freqSet]/supportData[freqSet-conseq] 
        if conf >= minConf:
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
            

def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

main()