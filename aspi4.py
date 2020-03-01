# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:30:00 2019

ASPI
alternate search of primes based on iteration
main idea based on the sieve of eratosthenes
using the differences between remaining numbers

@author: Berthold Braun
"""

import sys
import datetime as DT
import itertools as IT
#   import functools as FT
#   import copy as CC
#   import json as JSON
#   from collections import deque
#   https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-queues


#   Break On ...
maxProd = 9_999_999_999
maxJump = 1_100_000_000
maxStep = 11
maxPrim = 23

#   possible start values
cStep = 0
LPrim = []
cPrim = 1
cLCM = 1
jLEN = 1
LJump = (1,)  # tuple, list - what shall I use here?
#
#    cStep = 1
#    LPrim = [2]
#    cPrim = 2
#    cLCM = 2
#    jLEN = 1
#    LJump = [2]
#
#    cStep = 2
#    LPrim = [2, 3]
#    cPrim = 3
#    cLCM = 6
#    jLEN = 2
#    LJump = [4, 2]
#
#    cStep = 3
#    LPrim = [2, 3, 5]
#    cPrim = 5
#    cLCM = 30
#    jLEN = 8
#    LJump = [6, 4, 2, 4, 2, 4, 6, 2]
#


def timeDiff(TA, TZ=None):
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA


def nextPrim(L):
    """
    jump-list holds difference values
    next prime number is first jump-list-element plus 1
    """
    return 1 + L[0]


def gen_Strikes(p, L):
    """
    compute elements that should not appear in next jump-list
    given by the running sum of jumpers but starting with leading 1
    """
    for k in IT.accumulate(IT.chain([1], L)):
        yield p*k


def gen_Numbers(f, p, L):
    """
    only for watching correctness - starting with 1 needed for algorhythm
    these will be remaining numbers of sieve of eratosthenes
    """
    for k in IT.accumulate(IT.chain([1], IT.cycle(L))):
        yield k
        if k >= f:
            break


def gen_Jumpers(f, p, L):
    """
    compute the next row of jump-list-elements
    input: (have a look also to starting values see above)
        product of currently known prime = LCM
        the current prime - got from just computed jump-list
        the last computed jump-list it-self to reuse
    output:
        next jump-list-elements for coming up iterations
    """
    k0 = 1
    S = gen_Strikes(p, L)
    s = next(S)
    # needed something else for [1] as start element for running sum
    for k in IT.accumulate(IT.chain([1], IT.cycle(L))):
        if (k == s):
            # found a multiple of current prime
            # to be removed from like in sieve - so ignore it here
            # can this be substituted by using filter()?
            s = next(S)  # get next number to compare
            continue
        if k == 1:
            # 1 must be suppressed but needed for start
            continue  # do not output start element
        # output the difference between last and current number
        yield k - k0
        k0 = k
        # loop ends when if LCM is reached - that is after n=p times cycling
        # needed repeat(L, times=p) instead of cycle(L)
        if k >= f:
            break


T0 = DT.datetime.now()
while True:
    """
    Main-Loop
    preparing the next step/iteration
    creating the next jump-list
    to compute the next prim-number
    """
    TA = DT.datetime.now()
    cStep += 1
    cPrim = nextPrim(LJump)
    LPrim.append(cPrim)
    jLEN *= (cPrim - 1)  # product over all primes - 1
    cLCM *= cPrim  # product over all primes - least common multiple
    # cLCM = FT.reduce(lambda x, y: x*y, LPrim, 1)

    if (False  # when stop looping
            # or cStep >= maxStep
            # or cPrim >= maxPrim
            # or cLCM >= maxProd
            or jLEN >= maxJump
            or False):
        break

    # core: prepare generator and create next jump-list
    tJumpers = gen_Jumpers(cLCM, cPrim, LJump)
    # LJump = [j for j in tJumpers]
    LJump = tuple(j for j in tJumpers)

    print(f"step: {cStep:2}\tprime: {cPrim:2}")
    print(f"LCM={cLCM:16,}", LPrim)
    print(f"JMP={jLEN:16,}", LJump[0:min(48, jLEN)])

    tNumbers = gen_Numbers(211, cPrim, LJump)
    print(f"remaining E.-Sieve:  {list(n for n in tNumbers if n > 1)}")
    # tNumbers = gen_Numbers(cLCM, cPrim, LJump)
    # print(f"remaining E.-Sieve:  "
    #       + "{list(n for n in tNumbers if n > 1)[0:min(24, jLEN)]}")

    print(f"ratio={jLEN/cLCM:6.5f}\tused:{timeDiff(TA)}")
    print()  # wow - here are the results
    sys.stdout.flush()

    if (False  # when stop looping
            or cStep >= maxStep
            or cPrim >= maxPrim
            or cLCM >= maxProd
            # or jLEN >= maxJump
            or False):
        break

print(f"over all used time -> {timeDiff(T0)}")

"""

step:  1        prime:  2
LCM=               2 [2]
JMP=               1 (2,)
remaining E.-Sieve:  [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211]
ratio=0.50000   used:0:00:00

step:  2        prime:  3
LCM=               6 [2, 3]
JMP=               2 (4, 2)
remaining E.-Sieve:  [5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, 37, 41, 43, 47, 49, 53, 55, 59, 61, 65, 67, 71, 73, 77, 79, 83, 85, 89, 91, 95, 97, 101, 103, 107, 109, 113, 115, 119, 121, 125, 127, 131, 133, 137, 139, 143, 145, 149, 151, 155, 157, 161, 163, 167, 169, 173, 175, 179, 181, 185, 187, 191, 193, 197, 199, 203, 205, 209, 211]
ratio=0.33333   used:0:00:00

step:  3        prime:  5
LCM=              30 [2, 3, 5]
JMP=               8 (6, 4, 2, 4, 2, 4, 6, 2)
remaining E.-Sieve:  [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89, 91, 97, 101, 103, 107, 109, 113, 119, 121, 127, 131, 133, 137, 139, 143, 149, 151, 157, 161, 163, 167, 169, 173, 179, 181, 187, 191, 193, 197, 199, 203, 209, 211]
ratio=0.26667   used:0:00:00

step:  4        prime:  7
LCM=             210 [2, 3, 5, 7]
JMP=              48 (10, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2)
remaining E.-Sieve:  [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 127, 131, 137, 139, 143, 149, 151, 157, 163, 167, 169, 173, 179, 181, 187, 191, 193, 197, 199, 209, 211]
ratio=0.22857   used:0:00:00

step:  5        prime: 11
LCM=           2,310 [2, 3, 5, 7, 11]
JMP=             480 (12, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 14, 4, 6, 2, 10, 2, 6, 6, 4, 2, 4, 6, 2, 10, 2, 4, 2, 12, 10, 2, 4, 2, 4)
remaining E.-Sieve:  [13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 169, 173, 179, 181, 191, 193, 197, 199, 211]
ratio=0.20779   used:0:00:00

step:  6        prime: 13
LCM=          30,030 [2, 3, 5, 7, 11, 13]
JMP=           5,760 (16, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 14, 4, 6, 2, 10, 2, 6, 6, 4, 6, 6, 2, 10, 2, 4, 2, 12, 12, 4, 2, 4, 6, 2, 10)
remaining E.-Sieve:  [17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211]
ratio=0.19181   used:0:00:00

step:  7        prime: 17
LCM=         510,510 [2, 3, 5, 7, 11, 13, 17]
JMP=          92,160 (18, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 14, 4, 6, 2, 10, 2, 6, 6, 4, 6, 6, 2, 10, 2, 4, 2, 12, 12, 4, 2, 4, 6, 2, 10, 6)
remaining E.-Sieve:  [19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211]
ratio=0.18053   used:0:00:00.015621

step:  8        prime: 19
LCM=       9,699,690 [2, 3, 5, 7, 11, 13, 17, 19]
JMP=       1,658,880 (22, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 14, 4, 6, 2, 10, 2, 6, 6, 4, 6, 6, 2, 10, 2, 4, 2, 12, 12, 4, 2, 4, 6, 2, 10, 6, 6)
remaining E.-Sieve:  [23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211]
ratio=0.17102   used:0:00:00.328047

step:  9        prime: 23
LCM=     223,092,870 [2, 3, 5, 7, 11, 13, 17, 19, 23]
JMP=      36,495,360 (28, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 14, 4, 6, 2, 10, 2, 6, 6, 4, 6, 6, 2, 10, 2, 4, 2, 12, 12, 4, 2, 4, 6, 2, 10, 6, 6, 6)
remaining E.-Sieve:  [29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211]
ratio=0.16359   used:0:00:07.258310

step: 10        prime: 29
LCM=   6,469,693,230 [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
JMP=   1,021,870,080 (30, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2, 4, 14, 4, 6, 2, 10, 2, 6, 6, 4, 6, 6, 2, 10, 2, 4, 2, 12, 12, 4, 2, 4, 6, 2, 10, 6, 6, 6, 2)
remaining E.-Sieve:  [31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211]
ratio=0.15795   used:0:05:09.484354

over all used time -> 0:05:17.148808




#    tStrikes = gen_Strikes(cPrim, LJump)
#    print("\ntStrikes")
#    for i in tStrikes:
#        print(i, end="  ")
#    print()
#
#    tNumbers = gen_Numbers(cLCM, cPrim, LJump)
#    print("\ntNumbers")
#    for n in tNumbers:
#        print(n, end="  ")
#    print()
#
#    tJumpers = gen_Jumpers(cLCM, cPrim, LJump)
#    print("\ntJumpers")
#    for j in tJumpers:
#        print(j, end="  ")
#    print()

#    help(IT.accumulate)
#    help(IT.chain)
#    help(IT.combinations)
#    help(IT.combinations_with_replacement)
#    help(IT.compress)
#    help(IT.count)
#    help(IT.cycle)
#    help(IT.dropwhile)
#    help(IT.filterfalse)
#    help(IT.groupby)
#    help(IT.islice)
#    help(IT.permutations)
#    help(IT.product)
#    help(IT.repeat)
#    help(IT.starmap)
#    help(IT.takewhile)
#    help(IT.tee)
#    help(IT.zip_longest)

"""
