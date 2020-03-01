# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 21:55:14 2019

@author: Berthold Braun
"""


# import sys
# import os
# import math as M
import time as TI
import datetime as DT
# import threading as TH
import multiprocessing as MP
import itertools as IT
import operator as OP
import functools as FT
# import collections as CL
# from collections import deque as DQ
from collections import OrderedDict as OD
from collections import namedtuple as NT
#
# import numpy as np
# import numba as na
#
import cProfile
import pstats
import io


# ESieve = [1, 7, 11, 13, 17, 19, 23, 29]
# XJumps = bytes([6, 4, 2, 4, 2, 4, 6, 2])
# Primes = [2, 3, 5]
# XJumps = bytes([4, 2])
# Primes = [2, 3]
XJumps = bytes([2])
Primes = [2]

Strikes = set()
XFrame = OD()
ZDatas = OD()
curPrime = 1
# thisPool = MP.pool.Pool()
# MAXPROCS = 5
MAX2SHOW = 24
MAXPRIME = 23  # where should we stop - lists/sets grow very fast

Xtuple = NT('Xtuple',
            ['prime', 'step', 'start', 'finit', 'frame', 'strikes', 'jumpers'])


def profile(fnc):
    """
    decorator for profiling
    """
    def DoIt(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return DoIt


def delay(ms):
    """
    stop working for some milli seconds
    """
    TI.sleep(ms / 1000.0)


def timeDiff(TA, TZ=None):
    """
    show me how much time we took
    """
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA


def fInt(i, sep='.'):
    """
    thousand separator
    """
    cyc = IT.cycle(['', '', sep])
    s = str(i)
    last = len(s) - 1
    formatted = [(cyc.__next__() if idx != last else '') + char
                 for idx, char in enumerate(reversed(s))]
    return ''.join(reversed(formatted))


def nextPrime(L):
    return 1 + L[0]


def productPrimes(P):
    """
    x = (2)*(3)*(5)*(7)*.. = product over all (p)
    """
    return FT.reduce(OP.mul, P, 1)


def lengthList(P):
    """
    x = (2-1)*(3-1)*(5-1)*(7-1)*.. = product over all (p-1)
    """
    return FT.reduce(OP.mul, [max(1, x-1) for x in P], 1)


def DelayPeriod(N):
    T = 200
    A = 12
    B = 8
    C = 5
    return N * T / (N + C) * (N + A) / (N + B) * N


def genJumpers(P, A, E, S, J):
    z = A
    a = A
    if a in S:
        a -= J[-1]
    for q in J:
        z += q
        if z in S:
            continue
        yield z - a
        a = z
    return None


def makeAJumper(k, prime, start, finit, strikes, jumpers, rd):
    rd[k] = bytes(genJumpers(prime, start, finit, strikes, jumpers))


def makeJumpers(p, K):
    T0 = DT.datetime.now()
    ProX = []
    MPM = MP.Manager()
    rd = MPM.dict()
    Z = OD()
    print('creating ...  ', end='', flush=True)
    for k in range(p):
        XT = K[k]
        pName = f'PY_{p:03}_{k:03}'
        pArgs = (k, XT.prime, XT.start, XT.finit, XT.strikes, XT.jumpers, rd)
        qq = MP.Process(target=makeAJumper, name=pName, args=pArgs)
        ProX.append(qq)
        print(k, qq.name, sep=' ', end='   ', flush=True)
    print()
    print('starting ...  ', end='', flush=True)
    for qq in ProX:
        qq.start()
        delay(5)
        print(qq.name, qq.ident, sep=' ', end='   ', flush=True)
    print()
    print('waiting  ...  ', end='', flush=True)
    while True:  # any(qq.is_alive() for qq in ProX):
        delay(5)
        if not any(qq.is_alive() for qq in ProX):
            break
        R = [(i, qq.name, qq.ident)
             for i, qq in enumerate(ProX)
             if qq.is_alive()]
        print(R, end='     ')
        delay(DelayPeriod(len(R)))
    print()
    print('joining  ...  ', end='', flush=True)
    for qq in ProX:
        #
        print(qq.name, end='   ', flush=True)
        qq.join()
        qq.close()
    print()
    for k in range(p):
        # print(k, rd[k])
        Z.setdefault(k, rd[k])
    T1 = DT.datetime.now()
    print(timeDiff(T0, T1))
    return Z


def checkSymmetryTwo(B):
    u = len(B) - 1
    v = u // 2
    C = [not bool(b - c) for (b, c) in zip(B[0:v:1], B[-2:-v-1:-1])]
    return (all(C), B[-1] == 2)


def createESieve(B, maxlen=MAX2SHOW):
    A = [(b + 1)
         for b, c in zip(IT.accumulate(B, OP.add), IT.count())
         if c < maxlen]
    return A


# @profile
def DoAllTheStuff():
    TA = DT.datetime.now()
    global curPrime, Primes, Strikes, XJumps, XFrame, ZDatas
    while curPrime < MAXPRIME:
        curPrime = nextPrime(XJumps)
        iFrameOld = productPrimes(Primes)
        iLenJPold = lengthList(Primes)
        print('\nPrimes:', Primes, '+', '<<_ ', curPrime, ' _>>', sep=' ')

        Primes.append(curPrime)
        iFrameNew = productPrimes(Primes)
        iLenJPnew = lengthList(Primes)
        print('product: (', fInt(iFrameOld), '/', fInt(iFrameNew), ')',
              ' length: {', fInt(iLenJPold), '/', fInt(iLenJPnew), '}',
              sep=' ')

        Strikes = set(((x + 1) % iFrameOld * curPrime)
                      for x in IT.accumulate(XJumps, OP.add))
        print('Strikes:', '(', fInt(len(Strikes)), ')',
              # sorted(list(Strikes))[0:min(len(Strikes), MAX2SHOW)],
              sep=' ')

        ZDatas.clear()
        XFrame.clear()
        for k in range(curPrime):
            kStart = 1 + k * iFrameOld
            kFinit = kStart + iFrameOld
            S = set(s for s in Strikes if kStart <= s <= kFinit)
            XT = Xtuple(curPrime, k, kStart, kFinit, iFrameOld, S, XJumps)
            XFrame.setdefault(k, XT)
        ZDatas = makeJumpers(curPrime, XFrame)
        XJumps = bytes(0)
        for k in range(curPrime):
            XJumps = XJumps.__add__(ZDatas[k])
        # print(list(XJumps)[0:min(len(XJumps), MAX2SHOW)])
        # print(createESieve(XJumps))  # MAX2SHOW
        # print(checkSymmetryTwo(XJumps))
    TZ = DT.datetime.now()
    print(timeDiff(TA, TZ))


if __name__ == "__main__":
    DoAllTheStuff()
