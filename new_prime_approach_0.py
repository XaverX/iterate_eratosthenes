# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 16:27:00 2019

compute primes in an iterative manner
basic idea is sieve of Eratosthenes 



@author: Berthold
"""


# import sys as S
# import math as M
import time as TI
import datetime as DT
# import threading as TH
import itertools as IT
import operator as OP
import functools as FT
# import collections as CL
# from collections import deque as DQ
# from collections import OrderedDict as OD
# from collections import namedtuple as NT
# import regex as RX
import cProfile
import pstats
import io


# where to go at maximum - e.g. 23 or 29 (MemoryError)
# should be limited because jumplist become very long - see length_Jumps(P) 
MAXPRIME = 29

cPrime = 1  # cuurent prime number in actual step
Primes = []  # list of known prime numbers - outcome of this algorithm

# list of differences between remaining numbers in E-sieve 
# for computing we thinh always we a starting "1" 
Jumpers = bytearray()

# set of numbers that are multiples of current prime 
# these numbers will be erased in current step 
Strikes = set([])


def profile(fnc):

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
    show me how much time we take
    """
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA


def fDT(T, datefmt=None):
    if T is None: return str(None)
    if datefmt == 'delta6':
        s = f'{T.seconds:>7}.{T.microseconds:06}'
    elif datefmt == 'delta3':
        s = f'{T.seconds//60:>4}:{T.seconds%60:02}.{T.microseconds//1000:03}'
    elif datefmt == 'HMS3':
        s = T.strftime('%H:%M:%S.%f')
    elif datefmt == 'TS':
        s = T.strftime('%Y%m%d%H%M%S')
    elif datefmt == 'D':
        s = T.strftime('%d.%m.%Y')
    elif datefmt == 'T':
        s = T.strftime('%H:%M:%S')
    elif datefmt == 'DT':
        s = T.strftime('%d.%m.%Y %H:%M:%S')
    else:
        s = T.strftime('%Y-%m-%d %H:%M:%S')
    return s


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


nextPrime = lambda L: 1 + L[0]


partSumme = lambda L: FT.reduce(OP.add, L, 1)


def productPrimes(P):
    """
    multiply all until here known primes => list P :: 2*3*5*...
    this gives the range where list differences will be repeated 
    """
    return FT.reduce(OP.mul, P, 1)


def lengthJumps(P):
    """
    formula that shows us the expected size of array of differences
    length = (2-1)*(3-1)*(5-1)*(7-1)*.. = product over all (p-1) out of list P
    """
    return FT.reduce(OP.mul, [max(1, x-1) for x in P], 1)


def makeStrikes(J):
    """
    beginning with 1 and than adding all differences
    multiplied with current prime 
    this and following difference will be added
    this are the numbers where we should do something
    in sieve of Erathostenes this are the numbers which will be erased
    """
    p = nextPrime(J)
    # K = [p * partSumme(L) for L in [JL[0:i+1] for i in range(len(JL))] ]
    # K = [p * partSumme(LL) for LL in [L for L in [JL[0:i+1] for i in range(len(JL))]]]
    # K = [p * partSumme(j, J) for (j, J) in [(i, L[0:i]) for i in range(len(L))]]
    #
    # K = set()  # K = DQ([])
    K = [j*p for j in IT.accumulate(IT.chain([1], J), OP.add)]
    K.pop()
#    s = 1
#    K.add(s * p)  # K.append(s * p)
#    for i in range(len(J) - 1):
#        s += J[i]
#        K.add(s * p)  # K.append(s * p)
    return set(K)


def getAPoint(st, J, S):
    return [m for m in [j+st for j in IT.accumulate(J, OP.add)] if m not in S]


def getADiff(M, z):
    return [t[0]-t[1] for t in zip(M[:], [z]+M[:-1])]


def genDifferences(ends_with, start_at, finit_at, J, S):
    z = ends_with
    a = start_at
    for j in IT.cycle(J):
        a += j
        if a > finit_at:
            break
        if a in S:
            continue
        # print("gD", a, z, a-z, end=" :: ")
        yield a - z
        z = a
    return None


def makeJumpers(J, S, G=None):
    z = 1
    Z = dict([])
    if G is None:
        G = {0: (1, 0)}
    for k, V in G.items():
        print(k, end='  ', flush=True)
        v, w = V
        # print("makeJumpers", fInt(z), k, fInt(v), fInt(w), sep="\t",  end="  ", flush=True)
        Z.setdefault(k, bytearray([d for d in genDifferences(z, v, w, J, S)]))
        # print(end=".", flush=True)
        z = z + sum(Z.get(k, 0))
        # print(end=".", flush=True)
        # print(end=".\t", flush=True)
#        X = sorted([s for s in S if s >= v and s < w])
#        print(X if len(S) < 120 else 
#                (len(X), X[:3], " ._. ", X[-3:]), 
#                flush=True)
    else: print()
    return Z    


# if __name__ == "__main__":
#@profile
def RunPrimes():
    print("Los geht's!", flush=True)
    # preparation - this is the step before 
    Primes = []
    Jumpers = bytearray([1])
#    Primes = [2]
#    Jumpers = bytearray([2])
#    Primes = [2, 3]
#    Jumpers = bytearray([4, 2])
#    Primes = [2, 3, 5]
#    Jumpers = bytearray([6, 4, 2, 4, 2, 4, 6, 2])
    pDst  = productPrimes(Primes)
    #
    while True:
        print()
        T0 = DT.datetime.now()
        print(T0)
        cPrime = nextPrime(Jumpers)
        Primes.append(cPrime)
        pPrd = productPrimes(Primes)
        jLen = lengthJumps(Primes)
        print(cPrime, ' -->\t', Primes, '  \t', fInt(pDst), ' <--> ', fInt(pPrd), 
              '\t(', fInt(len(Jumpers)), ') --> (', fInt(jLen), ')',
              sep='', flush=True)
        #
        # print('(', fInt(len(Jumpers)), ')\t', Jumpers[0:min(120, len(Jumpers))], '  --> (', fInt(jLen), ')', sep='')
        # print(list(Jumpers))
        Strikes = makeStrikes(Jumpers)
        # S = list(Strikes); S = sorted(S)
        # print('(', len(Strikes), ')\t', S[0:min(120, len(S))], sep='')
        #
        jGroups = {k: (k*pDst+1, (k+1)*pDst+1) for k in range(cPrime)}
        # print(jGroups)
        #
        Z = makeJumpers(Jumpers, Strikes, jGroups)
        Jumpers = bytearray(IT.chain(*Z.values()))
        #
        # print(Jumpers[0:min(120, len(Jumpers))])
        #
        pDst  = productPrimes(Primes)
        T1 = DT.datetime.now()
        print(T1, f"for step {cPrime} used time -> {timeDiff(T0)}", flush=True)
        if cPrime >= MAXPRIME:
            break
    print(flush=True)

TA = DT.datetime.now()
print(TA)
RunPrimes()
TZ = DT.datetime.now()
print(TZ, f"totally used time -> {timeDiff(TA)}", flush=True)
