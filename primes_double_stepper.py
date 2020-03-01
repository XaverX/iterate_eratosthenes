# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:31:01 2019

@author: Berthold
"""


# import sys
# import os
# import math as M
import time as TI
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


MAXPRIME = 19
cPrim = 5
cJumpers = bytes([6, 4, 2, 4, 2, 4, 6, 2])
PRIMES = [2, 3, 5]
#    cPrim = 3
#    cJumpers = bytearray([4, 2])
#    PRIMES = [2, 3]
#    cPrim = 2
#    cJumpers = bytearray([2])
#    PRIMES = [2]
#    cPrim = 1
#    cJumpers = bytes([1])
#    PRIMES = []


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


def genJumpers(cPrim, cStep, startFrame, finitFrame, strikeCompare, Jumpers):
    print(f'#{cStep:>3}{cPrim:>3}   ',
          f'{fInt(startFrame):>18}',
          f'{fInt(finitFrame):>18}',
          f'{fInt(strikeCompare):>18}',
          sep='')  # , Jumpers
    z = startFrame
    a = startFrame
    if a == strikeCompare:
        a -= Jumpers[-1]
        strikeCompare += cPrim
    for j in Jumpers:
        z += j
        if z == strikeCompare:
            strikeCompare += cPrim
            continue
        if z >= strikeCompare:
            strikeCompare += cPrim
        yield z - a
        a = z
    return None


def makeJumpers(cPrim, k, frameStart, frameFinit, strikeComp, J):
    return bytes([
            j for
            j in genJumpers(cPrim, k, frameStart, frameFinit, strikeComp, J)
            ])


# @profile
def DoAllTheStuff():
    global PRIMES, cJumpers, cPrim
    TA = DT.datetime.now()
    # ...
    while cPrim < MAXPRIME:
        T0 = DT.datetime.now()
        J = cJumpers  # .copy()
        cPrim = nextPrime(cJumpers)
        cJumpers = bytes([])  # cJumpers.clear()
        cDist = productPrimes(PRIMES)
        PRIMES.append(cPrim)
        # cGoal = productPrimes(PRIMES)
        #
        for k in range(cPrim):
            strikeComp = k * cDist
            frameStart = strikeComp + 1
            frameFinit = frameStart + cDist
            strikeComp = ((strikeComp // cPrim) + 1) * cPrim
            #
#            cJumpers.extend(makeJumpers(
#                    cPrim, k, frameStart, frameFinit, strikeComp, J)
#                    )
            cJumpers.__add__(makeJumpers(
                    cPrim, k, frameStart, frameFinit, strikeComp, J)
                    )
        print(cJumpers)
        T1 = DT.datetime.now()
        print(f'{cPrim:>4}', '  -> ', timeDiff(T0, T1), sep='')
    # ...
    TZ = DT.datetime.now()
    print('overall: ', timeDiff(TA, TZ), sep='')


if __name__ == "__main__":
    DoAllTheStuff()
    print(PRIMES)
