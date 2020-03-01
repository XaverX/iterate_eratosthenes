# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 21:55:14 2019

@author: Berthold Braun
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


def findMinimum(S):
    """
    knowing there is an "1"
    next lowest remaining number in ESieve is always prime
    """
    return S[1]


def productPrimes(P):
    """
    gives the frame inside which we compute the next numbers
    """
    return FT.reduce(OP.mul, P, 1)


def lengthList(P):
    """
    formula that shows us the expected size of array of differences
    length = (2-1)*(3-1)*(5-1)*(7-1)*.. = product over all (p-1)
    """
    return FT.reduce(OP.mul, [max(1, x-1) for x in P], 1)


@profile
def DoAllTheStuff():
    MAX2SHOW = 500
    MAXPRIME = 23  # where should we stop - lists/sets grow very fast
    #
    # let's start with no primes, "1" already removed, found "2" at first
    Primes = [2, 3]
    ESieve = [5]  # point to the first block of remaining number w/o "1"
    curPrime = 1  # only for having an initialized comparable number
    # first known primes give a product = PPrime which gives the block frame
    # Primes = [2, 3, 5] --> 30
    # ESieve = [1, 7, 11, 13, 17, 19, 23, 29]  <--> 01..31..61..91..
    #
    Primes = [2, 3, 5]
    ESieve = [1, 7, 11, 13, 17, 19, 23, 29]
    Primes = [2, 3]
    ESieve = [1, 5]
    Strikes = set()
    #
    while curPrime < MAXPRIME:
        PPrime = productPrimes(Primes)  # current size of frame
        curPrime = findMinimum(ESieve)  # next prime - next to be removed num
        print('\ncurPrime', curPrime)
        #
        print('Primes:', Primes, '(', fInt(PPrime), ')', sep=' ')
        #
        Strikes = set(p*curPrime for p in ESieve)
        if False:
            print('Strikes', len(Strikes))  # , Strikes
            Q = sorted(list(Strikes))
            print(Q[0: min(MAX2SHOW, len(Q))], '\n')
        #
        E = ESieve.copy()
        ESieve.clear()
        for k in range(curPrime):
            print(k, end=' ')
            Z = [k*PPrime + e for e in E]
            S = [z for z in Z if z not in Strikes]
            ESieve.extend(S)
        #
        Primes.append(curPrime)
        print('\nESieve', len(ESieve))  # , ESieve
        # print(ESieve, '\n')
        curPQ = curPrime * curPrime
        print(' --> ',
              Primes, sep='')
        print(' +++ ',
              [q for q in ESieve if q < curPQ if q > 1],
              ' ( ', fInt(curPQ), ' ) ...', sep='')
#        print(' ~~~ ',
#              [q for i, q in enumerate(ESieve) if q > curPQ and i < MAX2SHOW],
#              ' ... ', sep='')


if __name__ == "__main__":
    DoAllTheStuff()
