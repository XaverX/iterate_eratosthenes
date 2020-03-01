# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:02:01 2019

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
    lowest remaining number in ESieve is always prime
    """
    return min(S)


def productPrimes(P):
    """
    gives the frame inside which we compute the next numbers
    """
    return FT.reduce(OP.mul, P, 1)


@profile
def DoAllTheStuff():
    MAXPRIME = 23  # where should we stop - lists/sets grow very fast
    #
    # let's start with no primes, "1" already removed, found "2" at first
    Primes = []
    ESieve = set([2])  # point to the first block of remaining number w/o "1"
    curPrime = 1  # only for having an initialized comparable number
    # first known primes give a product = PPrime which gives the block frame
    # Primes = [2, 3, 5] --> 30
    # ESieve = set([7, 11, 13, 17, 19, 23, 29])  <--> 01..31..61..91..
    Strikes = set()
    #
    while curPrime < MAXPRIME:
        PPrime = productPrimes(Primes)  # current size of frame
        curPrime = findMinimum(ESieve)  # next prime - next to be removed num
        ESieve.add(1)  # needed to compute all strike numbers
        print('\ncurPrime', curPrime)
        #
        print('Primes:', Primes, '(', fInt(PPrime), ')', sep=' ', end=' --> ')
        Primes.append(curPrime)
        print('Primes:', Primes, sep=' ')
        #
        Strikes = set(p*curPrime for p in ESieve)
        # print('Strikes', len(Strikes))  # , Strikes
        # Q = sorted(list(Strikes))
        # print(Q[0: min(MAX2SHOW, len(Q))])
        Strikes.add(1)  # needed to remove "1" in ESieve
        #
        ESieve.update(k*PPrime + e
                      for (k, e) in IT.product(range(curPrime), ESieve))
        ESieve.difference_update(Strikes)
        print('ESieve', len(ESieve))  # , ESieve
        Q = sorted(list(ESieve))
        curPQ = curPrime * curPrime
        print([q for q in Q if q < curPQ])


if __name__ == "__main__":
    DoAllTheStuff()
