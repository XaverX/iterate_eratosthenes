# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 20:46:08 2019

@author: Berthold
"""


import datetime as DT
# import itertools as IT -> cycle
# from itertools import cycle
import itertools as IT
# import collections as CL -> deque
# import collections as CL -> OrderedDict
from collections import deque
import operator as OP


#    BAS = 30
#    HAL = [1, 7, 11, 13, 17, 19, 23, 29]
PPP = deque([])
QQQ = deque([])
CCC = {}
AAA = {}


def timeDiff(TA, TZ=None):
    """
    show me how much time we take
    """
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA
    print('-'.rjust(60, '-'), flush=True)


def gen_Primes():
    for p in PPP:
        yield p


def put_Primes(p, q):
    PPP.append(p)
    if q >= MAX:
        return
    QQQ.append(q)


def CMX(q):
    if q <= MAX:
        return True
    return False


def gen_Jumps():
    for d in IT.cycle(DIF):
        yield d


print("###", flush=True)
NN = 1  # 31
MAX = 10000  # >>1000
#    PRM = [2, 3, 5]
#    DIF = [6, 4, 2, 4, 2, 4, 6, 2]
#
#    PRM = [2, 3, 5, 7]
#    DIF = [10, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4,
#           2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 8, 6, 4, 6, 2, 4,
#           6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2]
#
PRM = [2, 3, 5, 7, 11]
DIF = [12, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 14, 4, 6, 2, 10, 2, 6, 6, 4, 2, 4, 6, 2, 10, 2, 4, 2, 12, 10, 2, 4, 2, 4, 6, 2, 6, 4, 6, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 6, 8, 6, 10, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 6, 10, 2, 10, 2, 4, 2, 4, 6, 8, 4, 2, 4, 12, 2, 6, 4, 2, 6, 4, 6, 12, 2, 4, 2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 10, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2, 10, 2, 4, 6, 6, 2, 6, 6, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 6, 4, 8, 6, 4, 6, 2, 4, 6, 8, 6, 4, 2, 10, 2, 6, 4, 2, 4, 2, 10, 2, 10, 2, 4, 2, 4, 8, 6, 4, 2, 4, 6, 6, 2, 6, 4, 8, 4, 6, 8, 4, 2, 4, 2, 4, 8, 6, 4, 6, 6, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2, 10, 2, 6, 4, 6, 2, 6, 4, 2, 4, 6, 6, 8, 4, 2, 6, 10, 8, 4, 2, 4, 2, 4, 8, 10, 6, 2, 4, 8, 6, 6, 4, 2, 4, 6, 2, 6, 4, 6, 2, 10, 2, 10, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 6, 6, 4, 6, 8, 4, 2, 4, 2, 4, 8, 6, 4, 8, 4, 6, 2, 6, 6, 4, 2, 4, 6, 8, 4, 2, 4, 2, 10, 2, 10, 2, 4, 2, 4, 6, 2, 10, 2, 4, 6, 8, 6, 4, 2, 6, 4, 6, 8, 4, 6, 2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 6, 6, 2, 6, 6, 4, 2, 10, 2, 10, 2, 4, 2, 4, 6, 2, 6, 4, 2, 10, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 12, 6, 4, 6, 2, 4, 6, 2, 12, 4, 2, 4, 8, 6, 4, 2, 4, 2, 10, 2, 10, 6, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 10, 6, 8, 6, 4, 2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 6, 4, 6, 2, 6, 4, 2, 4, 2, 10, 12, 2, 4, 2, 10, 2, 6, 4, 2, 4, 6, 6, 2, 10, 2, 6, 4, 14, 4, 2, 4, 2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 12, 2]
#
J = gen_Jumps()
T0 = DT.datetime.now()
while True:
    d = next(J)
    NN += d
#    print(NN)
    if NN >= MAX:
        break
#
    i = 0
    for iq in IT.zip_longest(IT.count(),
                             IT.takewhile(CMX, QQQ), fillvalue=None):
        i, q = iq
#
        if (q is None) or (NN < q):
            AAA['A'] = AAA.get('A', 0) + 1
            AAA[i] = AAA.get(i, 0) + 1
            put_Primes(NN, NN*NN)
#            print('Loop:', i)
#            print("add prime: ", NN)
            break
#
        p = PPP[i]
        i += 1
        st = divmod(NN, p)
        CCC['C'] = CCC.get('C', 0) + 1
        s, t = st
        # print(i, " :: ", NN, ":", p, "(", q, ")", "=", s, "R:", t)
        if t == 0:
            CCC[i] = CCC.get(i, 0) + 1
#            print(i, " :: ", NN, ":", p, "(", q, ")", "=", s, "R:", t)
#            print("drop this: ", NN)
            break

#
print(f"time used -> {timeDiff(T0)}", flush=True)
print("-->", flush=True)
# print([p for p in gen_Primes()])
#    print(PRM, '=', max(list(IT.accumulate(PRM, OP.mul))), "\n--> ",
#          DIF, '(', len(DIF), ')')
print(len(PRM)+len(PPP), max(PPP), '\n')
print(AAA, '\n')
print(CCC, '\n')
