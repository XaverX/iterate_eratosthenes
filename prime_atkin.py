# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 20:00:00 2020

Prime-Test with Atkin
    A: 4x2 + y2 = n : all x, odd y
    B: 3x2 + y2 = n : odd x, even y
    C: 3x2 - y2 = n : x > y : x + y odd

on modulo 60 remainders
     1 : 'A',  7 : 'B', 11 : 'C', 13 : 'A',
    17 : 'A', 19 : 'B', 23 : 'C', 29 : 'A',
    31 : 'B', 37 : 'A', 41 : 'A', 43 : 'B',
    47 : 'C', 49 : 'A', 53 : 'A', 59 : 'C'

@author: Berthold Braun

https://en.wikipedia.org/wiki/Sieve_of_Atkin

limit ← 1000000000        // arbitrary search limit

// set of wheel "hit" positions for a 2/3/5 wheel
rolled twice as per the Atkin algorithm
s ← {1,7,11,13,17,19,23,29,31,37,41,43,47,49,53,59}

// Initialize the sieve with enough wheels to include limit:
for n ← 60 × w + x where w ∈ {0,1,...,limit ÷ 60}, x ∈ s:
    is_prime(n) ← false

// Put in candidate primes:
//   integers which have an odd number of
//   representations by certain quadratic forms.
// Algorithm step 3.1:
for n ≤ limit, n ← 4x²+y² where x ∈ {1,2,...} and y ∈ {1,3,...}
    // all x's odd y's
    if n mod 60 ∈ {1,13,17,29,37,41,49,53}:
        is_prime(n) ← ¬is_prime(n)   // toggle state
// Algorithm step 3.2:
for n ≤ limit, n ← 3x²+y² where x ∈ {1,3,...} and y ∈ {2,4,...}
    // only odd x's and even y's
    if n mod 60 ∈ {7,19,31,43}:
        is_prime(n) ← ¬is_prime(n)   // toggle state
// Algorithm step 3.3:
for n ≤ limit, n ← 3x²-y² where x ∈ {2,3,...} and y ∈ {x-1,x-3,...,1}
    //all even/odd odd/even combos
    if n mod 60 ∈ {11,23,47,59}:
        is_prime(n) ← ¬is_prime(n)   // toggle state

// Eliminate composites by sieving, only for those occurrences on the wheel:
for n² ≤ limit, n ← 60 × w + x where w ∈ {0,1,...}, x ∈ s, n ≥ 7:
    if is_prime(n):
        // n is prime, omit multiples of its square; this is sufficient
        // because square-free composites can't get on this list
        for c ≤ limit, c ← n² × (60 × w + x) where w ∈ {0,1,...}, x ∈ s:
            is_prime(c) ← false

// one sweep to produce a sequential list of primes up to limit:
output 2, 3, 5
for 7 ≤ n ≤ limit, n ← 60 × w + x where w ∈ {0,1,...}, x ∈ s:
    if is_prime(n): output n

"""

# import sys
# import os
# import math as M
import time as TI
import datetime as DT

# import threading as TH
# import multiprocessing as MP

import itertools as IT
# import operator as OP
# import functools as FT
# import collections as CL
# from collections import deque as DQ
# from collections import OrderedDict as OD
# from collections import namedtuple as NT
#
import cProfile
import pstats
import io


xDEBUG = 1
xTRACE = 2
xERROR = 3
xAWARN = 4
xINFOS = 5
xPRINT = 6


maxP = 3_000  # stop
counter = 0  # count the number of ATKIN calls over all
P = [2, 3, 5]  # first konwon primes - building the ATKIN wheel
Q = [4, 9, 25]  # and there squares
#
# distances on ATKIN wheel
L = [6, 4, 2, 4, 2, 4, 6, 2]
# the remainders on modulo 60 - cases for ATKIN formulas
D = {1: 'A',  7: 'B',
     11: 'C', 13: 'A', 17: 'A', 19: 'B', 23: 'C', 29: 'A', 31: 'B',
     37: 'A', 41: 'A', 43: 'B', 47: 'C', 49: 'A', 53: 'A', 59: 'C'}
#
# helper lists to ckeck the maximum and/or minimum x and y values
XX1 = [0, 1]  # für alle
XXC = [0, 3]  # für C
XX3 = [0, 3]  # für B
XX4 = [0, 4]  # für A


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


def gen_number(L):
    # endless loop about first distances between sieved numbers
    n = 1
    for i in IT.cycle(L):
        n += i
        yield n


def add_squares(n):
    global XX1, XXC, XX3, XX4
    # helper lists - see ATKIN formulas
    # we need to know the sqares and there multiples with 3 (B) and 4 (A)
    # for case C we have to think about possible reachable values a bit tricky
    k = len(XX1)
    while True:
        z = k * k
        if z >= n: break
        XX1.append(z)
        k += 1
    #
    k = len(XX4)  # für A
    while True:
        z = k * k * 4
        if z >= n: break
        XX4.append(z)
        k += 1
    k = len(XX3)  # für B
    while True:
        z = k * k * 3
        if z >= n: break
        XX3.append(z)
        k += 1
    #
    k = len(XXC)  # für C
    while True:
        z = k * k * 3
        y = (k - 1) * (k - 1)
        if z - y > n: break
        XXC.append(z)
        k += 1


DEBUG_LEVEL = xERROR
DBGL = lambda d: d >= DEBUG_LEVEL


def out_print(*T, SEP='\t', FLUSH=False, END='\n'):
    """
    DEBUG_LEVEL:
        xDEBUG = 1
        xTRACE = 2
        xERROR = 3
        xAWARN = 4
        xINFOS = 5
        xPRINT = 6
        """
    for t in T:
        print(t, sep=SEP, flush=FLUSH, end=END)


def count_solutions(n):
    """
    A: 4x2 + y2 = n : all x, odd y
    B: 3x2 + y2 = n : odd x, even y
    C: 3x2 - y2 = n : x > y : x + y odd
    """
    global counter
    # get the case for ATKIN : A, B, C - see formulas
    T = D[n % 60]
    # s : that is only for print(f'') 
    s = len(str(maxP)) + 1
    if DBGL(xTRACE): out_print('')
    if T == '':
        pass
    elif T == 'A':
        if DBGL(xTRACE): out_print(f'{n:{s}}', 'A: 4x2 + y2 = n : all x, odd y')
        # set formula and get valid range of numbers
        ATKIN = lambda x, y: XX4[x] + XX1[y]
        X = [x for x in range(XX4.index(XX4[1]), 1+XX4.index(XX4[-1]))]
        Y = [y for y in range(XX1.index(XX1[1]), 1+XX1.index(XX1[-1]), 2)]
        # if DBGL(xTRACE): out_print('x:', X, 'y:', Y)
    elif T == 'B':
        if DBGL(xTRACE): out_print(f'{n:{s}}', 'B: 3x2 + y2 = n : odd x, even y')
        ATKIN = lambda x, y: XX3[x] + XX1[y]
        X = [x for x in range(XX3.index(XX3[1]), 1+XX3.index(XX3[-1]), 2)]
        Y = [y for y in range(XX1.index(XX1[2]), 1+XX1.index(XX1[-1]), 2)]
        # if DBGL(xTRACE): out_print('x:', X, 'y:', Y)
    elif T == 'C':
        if DBGL(xTRACE): out_print(f'{n:{s}}', 'C: 3x2 - y2 = n : x > y : x + y odd')
        ATKIN = lambda x, y: XXC[x] - XX1[y]
        i = -1
        while XXC[i-1] >= n:
            i -= 1
        X = [x for x in range(XXC.index(XXC[i]), 1+XXC.index(XXC[-1]))]
        Y = [y for y in range(XX1.index(XX1[1]), XXC.index(XXC[-1]))]
        # if DBGL(xTRACE): out_print('x:', X, 'y:', Y)
    #
    z = 0  # counter for prime not prime toggle
    c = 0  # counter for number of ATKIN calls per given n
    yy = 0
    # if DBGL(xTRACE): out_print(n, T, SEP=' ', END=' ', FLUSH=True)
    t = str(f'{n:{s}} {T}')
    # if DBGL(xTRACE): out_print(n, T)
    if T != 'C': Y.reverse()
    for x in X:
        for y in Y:
            # if we break inner loop some of y values need not to be computed
            # think about value x from small to big and y (A,B only) hi to low
            if yy != 0:
                if T == 'C':
                    if y < yy: continue
                else:
                    if y > yy: continue
            yy = 0
            # for A,B we have optimized lists - for C we need additional checks
            if T == 'C':
                if y >= x: continue
                if ((x+y) % 2) == 0: continue
            # if DBGL(xTRACE): out_print('(', x, y, SEP=' ', END=' ', FLUSH=True)
            t = t + ' (' + str(f'{x} {y} ')
            # all atkin formulas are as prepared lambda functions 
            m = ATKIN(x, y)
            c += 1
            counter += 1
            # most case - we need to go into inner loop again
            if m > n:
                # if DBGL(xTRACE): out_print('#', ')', SEP=' ', END=' ', FLUSH=True)
                t = t + '#)'
                continue
            # need to remember y to jump over not needed values
            yy = y
            if T == 'C': yy -= 2  # to get the odd/even even/odd change
            # that was a match - we count the appearance
            if m == n:
                # if DBGL(xTRACE): out_print('=', ')', SEP=' ', END=' ', FLUSH=True)
                t = t + '=)'
                z += 1
                break
            # looping in inner loop makes no sense here - step forward outer
            # if ((T != 'C') and (m < n)) or ((T == 'C') and (m > n)):
            if m < n:
                # if DBGL(xTRACE): out_print('^', ')', SEP=' ', END=' ', FLUSH=True)
                t = t + '^)'
                break
    #
    # if DBGL(xTRACE): out_print(z, c, SEP=' ', FLUSH=True)
    # t = t + str(f'\n{z} {c}')
    t = str(f'{n} {T} {z} {c}')
    if DBGL(xINFOS): out_print(t, FLUSH=True)
    return z


@profile
def DoAllTheStuff():
    TA = DT.datetime.now()
    #
    # the give n will be prime if number of solution is an odd number
    isEven = lambda z: z % 2 == 0
    # get next number over a wheel of known primes {2,3,5}
    N = gen_number(L)
    # preparing the helper lists to jump over known primes
    add_squares(5)
    while True:
        # get 7, 11, 13, ...
        n = next(N)
        if n > maxP:
            break
        # and expand helper lists dynamically
        add_squares(n)
        if isEven(count_solutions(n)):
            continue
        # we found a possible prime - final proofs then store
        for p, q in zip(P, Q):
            if q > n: continue
            if n % p == 0: break
            if n % q == 0: break
        else:
            # add to list and prepare the square for later comparison
            P.append(n)
            Q.append(n * n)
    #
    if DBGL(xTRACE): out_print('XX1', XX1)
    if DBGL(xTRACE): out_print('XXC', XXC)
    if DBGL(xTRACE): out_print('XX3', XX3)
    if DBGL(xTRACE): out_print('XX4', XX4)
    #
    print('', flush=True)
    print(len(P), counter, flush=True)
    if DBGL(xPRINT): out_print(P, FLUSH=True)
    # if DBGL(xPRINT): out_print(Q, FLUSH=True)
    #
    TZ = DT.datetime.now()
    print(timeDiff(TA, TZ))


if __name__ == "__main__":
    DoAllTheStuff()
    print('', flush=True)
