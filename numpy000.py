# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 20:42:29 2019

@author: Berthold
"""

#    import sys
import time
#    import itertools as IT
import operator as OP
import functools as FT
import numpy as np
#
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


# @profile
def DoAllTheStuff():
    MAXPRIME = 23
    n = 2
    P = [2]
    J = np.array([2], dtype='int64')  # int8 = 6, 4, 2, 4, 2, 4, 6, 2
    K = np.array([], dtype='int64')

    while n < MAXPRIME:
        t0 = time.time()
        # current Primes with their product
        pp = FT.reduce(OP.mul, P, 1)

        # current input JumpList
        # next prime in this step
        n = J[0] + 1

        P.append(n)
        ppp = FT.reduce(OP.mul, P, 1)
        print('\nN :: :: :: :: :: ', n)

        # base
        K = np.array(J.cumsum() + 1, dtype='int64')

        # Strikes # unsorted?
        S = np.array(K.copy() * n, dtype='int64')
        S[-1] %= ppp

        print('P', P, pp, ppp)
        print('J', J.shape, J.size, J.itemsize, J)
        print('K', K.shape, K.size, K.itemsize, K)
        print('S', S.shape, S.size, S.itemsize, S)
        print('\n')

        K = np.array(np.arange(n) * pp, dtype='int64')[:, np.newaxis] + K
        # print('K', K.shape, K.size, K.itemsize, K)
        K = K.ravel()
        # print('K', K.shape, K.size, K.itemsize, K)

        K = np.compress(~np.in1d(K, S), K)
        L = np.array([1], dtype='int64')
        K = np.concatenate((L, K), axis=0)
        print('K', K.shape, K.size, K.itemsize, K)

        J = np.array(K[1:] - K[:-1], dtype='int64')
        print('J', J.shape, J.size, J.itemsize, J)
        print('\n')
        t1 = time.time()
        print((t1-t0)*1000)
        print('\n\n')


ta = time.time()
if __name__ == "__main__":
    DoAllTheStuff()

tz = time.time()
print((tz-ta)*1000)
