# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 15:31:29 2019


compute primes in an iterative manner
basic idea is sieve of Eratosthenes


@author: Berthold
"""


# import sys as S
# import math as M
# import time as TI
import datetime as DT
# import threading as TH
# import multiprocessing as MP
import itertools as IT
import operator as OP
import functools as FT
# import collections as CL
# from collections import deque as DQ
# from collections import OrderedDict as OD
# from collections import namedtuple as NT
import cProfile
import pstats
import io


# where to go at maximum - e.g. 23 or 29 (MemoryError)
# should be limited because jumplist become very long - see length_Jumps(P)
MAXPRIME = 29
MAXPROCS = 5

cPrime = 1  # cuurent prime number in actual step
Primes = []  # list of known prime numbers - outcome of this algorithm

# list of differences between remaining numbers in E-sieve
# for computing we think always with a starting "1"
Jumpers = bytes()

# set of numbers that are multiples of current prime
# these numbers will be erased in current step
Strikes = set([])
jGroups = dict([])


nextPrime = lambda L: 1 + L[0]


partSumme = lambda L: FT.reduce(OP.add, L, 1)


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


def timeDiff(TA, TZ=None):
    """
    show me how much time we take
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


def productPrimes(P):
    """
    multiply all until here known primes => list P :: 2*3*5*...
    this gives the range in which list differences will be repeated
    """
    return FT.reduce(OP.mul, P, 1)


def lengthJumps(P):
    """
    formula that shows us the expected size of array of differences
    length = (2-1)*(3-1)*(5-1)*(7-1)*.. = product over all (p-1) out of list P
    """
    return FT.reduce(OP.mul, [max(1, x-1) for x in P], 1)


def makeStrikes():  # Jumpers
    """
    beginning with 1 and than adding all differences
    multiplied with current prime
    this and following difference will be added
    this are the numbers where we should do something
    in sieve of Erathostenes this are the numbers which will be erased
    """
    p = nextPrime(Jumpers)
    K = [j*p for j in IT.accumulate(IT.chain([1], Jumpers), OP.add)]
    K.pop()
    return set(K)


def genDifferences(start_at, finit_at):  # , J, S
    a = start_at
    z = start_at
    if a in Strikes:
        z -= Jumpers[-1]
    for j in Jumpers:  # IT.cycle(J):
        a += j
        if a > finit_at:
            break
        if a in Strikes:
            continue
        d = a - z
        z = a
        # assert(d > 0 and d <= 255), "not in range of byte"
        yield d
    return None


def makeJumpList(k, v, w, J, S):
    a = J[-1] if v in S else 0
    M = [m for m in [j+v for j in IT.accumulate(J, OP.add)] if m not in S]
    #
    # D = [t[0]-t[1] for t in zip(M[:], IT.chain([v], M[:-1]))]
    D = [M[n] - m for n, m in enumerate(IT.chain([v], M[:-1]))]
    #
    D[0] += a
    return (k, bytes(D))
    # return (k, bytes(d for d in genDifferences(v, w)))


@profile
def MyTest(J, S, G):
    Z = dict([])
    for k, V in G.items():
        print(k, end='  ', flush=True)
        v, w = V
        k, B = makeJumpList(k, v, w, J, S)  # , J, S
        Z.setdefault(k, B)
    else:
        print(flush=True)
    return Z


if __name__ == "__main__":
    Primes = [2, 3]
    Jumpers = bytes([4, 2])
    pDst = productPrimes(Primes)
    TA = DT.datetime.now()
    print(TA, "Los geht's!", flush=True)
    Z = dict([])
    #
    while True:
        print()
        Z.clear()
        jGroups.clear()
        T0 = DT.datetime.now()
        print(T0)
        #
        cPrime = nextPrime(Jumpers)
        Primes.append(cPrime)
        pPrd = productPrimes(Primes)
        jLen = lengthJumps(Primes)
        print(cPrime, ' -->\t', Primes,
              '  \t', fInt(pDst), ' <--> ', fInt(pPrd),
              '\t(', fInt(len(Jumpers)), ') --> (', fInt(jLen), ')',
              sep='', flush=True)
        T1 = DT.datetime.now()
        Strikes = makeStrikes()  # Jumpers
        T2 = DT.datetime.now()
        print(T2, f"makeStrikes -> {timeDiff(T1)}", flush=True)
        #
        jGroups = {k: (k*pDst+1, (k+1)*pDst+1) for k in range(cPrime)}
        T3 = DT.datetime.now()
        print(T2, f"grouping -> {timeDiff(T2)}", flush=True)
        #
        Z = MyTest(Jumpers, Strikes, jGroups)
#        for k, V in jGroups.items():
#            print(k, end='  ', flush=True)
#            v, w = V

#            k, B = makeJumpList(k, v, w, Jumpers, Strikes)  # , J, S
#            Z.setdefault(k, B)

#        else:
#            print(flush=True)
        #
        T4 = DT.datetime.now()
        print(T4, f"makeJumpers -> {timeDiff(T3)}", flush=True)
        #
        Jumpers = bytes(IT.chain(*Z.values()))
        T5 = DT.datetime.now()
        print(T5, f"makeBytes -> {timeDiff(T4)}", flush=True)
        #
        pDst = productPrimes(Primes)
        T9 = DT.datetime.now()
        print(T9, f"for step {cPrime} used time -> {timeDiff(T0)}", flush=True)
        if cPrime >= MAXPRIME:
            break
    print(flush=True)
    TZ = DT.datetime.now()
    print(TZ, f"totally used time -> {timeDiff(TA)}", flush=True)
