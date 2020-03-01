# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 11:00:00 2019

@author: Berthold
"""

#    import sys
import time
import itertools as IT
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


def lengthList(P):
    """
    x = (2-1)*(3-1)*(5-1)*(7-1)*.. = product over all (p-1)
    """
    return FT.reduce(OP.mul, [max(1, x-1) for x in P], 1)


# @profile
def DoAllTheStuff():
    MAXPRIME = 23
    LONGINT = 'int64'
    SHRTINT = 'int8'
    n = np.int64(2)  # n = 5
    P = np.array([2], dtype=LONGINT)  # P = [2, 3, 5]
    # J = np.array([6, 4, 2, 4, 2, 4, 6, 2], dtype=LONGINT)
    J = np.array([2], dtype=SHRTINT)
    S = np.array([], dtype=LONGINT)
    M = np.array([], dtype=LONGINT)
    K = np.array([], dtype=LONGINT)
    pp = np.int64(1)
    ppp = np.int64(1)
    ll = np.int64(1)
    lll = np.int64(1)

    while n < MAXPRIME:
        t0 = time.time()
        # current Primes with their product
        pp = FT.reduce(OP.mul, P, 1)  # OP.mul := lambda x, y: x * y
        ll = FT.reduce(OP.mul, [max(1, x-1) for x in P], 1)

        # current input JumpList
        # next prime in this step
        n = J[0] + 1

        print('N :: :: :: :: :: ', n)
        print('P :', P, fInt(pp), '-->', sep=' ', end=' ')
        P = np.append(P, n)  # P.append(n)
        ppp = pp * n
        lll = ll * (n - 1)
        print(fInt(ppp), '#', fInt(ll), '-->', fInt(lll),
              '#', f'{100*lll/ppp:>4.2f}%', sep=' ')
        print('J <', J.shape, J.size, J.itemsize,
              J[:min(5, J.size//2)], '..',  J[-min(6, J.size//2):])

        # base
        J = np.array(J.cumsum() + 1, dtype=LONGINT)
        print('K #', J.shape, J.size, J.itemsize,
              J[:min(6, J.size//2)], '..', J[-min(6, J.size//2):])

        # Strikes # unsorted rotated
        S = np.array(J * n, dtype=LONGINT)
        S[-1] %= ppp
        S = np.roll(S, shift=1)
        print('S x', S.shape, S.size, S.itemsize,
              S[:min(6, S.size//2)], '..', S[-min(6, S.size//2):])

        print('*', end='')
        K = np.ravel(
                np.array(np.arange(n) * pp, dtype=LONGINT)[:, np.newaxis] + J)
        J = np.array([0], dtype=LONGINT)
        ###
        print('*', end='')
        M = np.in1d(K, S, assume_unique=True, invert=True)
        S = np.array([0], dtype=LONGINT)
        print('*', end='')
        J = np.compress(M, K)
        M = np.array([], dtype=LONGINT)
        ###

        print('\b\b\bK _', J.shape, J.size, J.itemsize,
              J[:min(6, J.size//2)], '..', J[-min(6, J.size//2):])

        J = np.array(np.diff(J, prepend=1), dtype=SHRTINT)
        print('J >', J.shape, J.size, J.itemsize,
              J[:min(5, J.size//2)], '..', J[-min(6, J.size//2):])

        t1 = time.time()
        print(f'time used: {(t1-t0)*1000/1000:>12.3f}')
        print('\n')
        # break
    J.tofile('./jumplist.txt', sep=',')


ta = time.time()
if __name__ == "__main__":
    DoAllTheStuff()

tz = time.time()
print(f'time used: {(tz-ta)*1000/1000:>12.3f}')
