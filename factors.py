# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 22:15:13 2019

Faktorisieren aller Zahlen
Zerlegen der Zahlen in ihre Prim-Faktoren

@author: Berthold
"""

import datetime as DT
# import operator as OP
import itertools as IT
import collections as CL
# import collections as CL -> OrderedDict

"""

loop over all numbers until given limit
division test with known primes using square rule
find lowest divisor that gives also biggest remaining
create list of numbers, squares, lowest and biggest divisor
print out list showing the prime factors - recursive
use a linked list of factors given by computed list

"""


nMax = 100_000
nStart = 50_000
nFinit = 51_000
# number, square if prime else 0, lowest and biggest factor
LL = CL.OrderedDict()
PP = []


def timeDiff(TA, TZ=None):
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA
    print('-'.rjust(60, '-'), flush=True)


def cntDigits(Z):
    m = Z
    z = 0
    while m > 0:
        z += 1
        m //= 10
    return z


def getPrimes(N=0):
    for K, T in LL.items():
        if K == 1:
            continue
        if (N >= 1) and (K >= N):
            return
        if (T[1] == K):
            yield K


def storeNum(N):
    # print(">>> ", N)
    for K, T in LL.items():
        Q, L, H = T
        # print(K, Q, L, H)
        if (K == 1) or (Q == 0):
            continue
        if (N % K == 0):
            # print("mod=0", K)
            LL.setdefault(key=N, default=tuple([0, K, N // K]))
            return
    if (N >= K) or (N < Q):
        # print("add N", N)
        LL.setdefault(key=N, default=tuple([N * N, N, 1]))
        return


def showFactors(N, Z=0):
    T = LL[N]
    Q, L, H = T
    if (N == L):
        print(f'{N:{Z}} is prime')
        return
    print(f'{N:{Z}} = ', end="")
    lx = 0
    lc = 0
    while True:
        if L != lx:
            if lc > 1:
                print(f'^{lc}', end="")
            if (L == 1):
                break
            if lc > 0:
                print(f' * ', end="")
            print(L, end="")
            lx = L
            lc = 1
        else:
            lc += 1
        T = LL[H]
        Q, L, H = T
    print()


#   MAIN
T0 = DT.datetime.now()
#
Z = cntDigits(nMax)
LL.setdefault(key=1, default=tuple([1, 1, 1]))
#
for NN in IT.count(start=2, step=1):
    if NN > nMax:
        break
    storeNum(NN)
for NN in IT.count(start=nStart, step=1):
    if NN > nFinit:
        break
    showFactors(NN, Z)
#
# print([p for p in getPrimes()])
print(f"time used -> {timeDiff(T0)}", flush=True)
