# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 22:09:40 2019

@author: Berthold
"""


# import sys
import datetime as DT
import itertools as IT
# import operator as OP
# import functools as FT


MAXPRIME = 29
XCONTROL = 10_000_000
ZCONTROL = 1_000_000

PPRIME = 1
PRIMES = []
K = bytearray([1])
J = bytearray([])


nextPrim = lambda L: 1 + L[0]


def timeDiff(TA, TZ=None):
    """
    show me how much time we take
    """
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA
    # print('-'.rjust(60, '-'), flush=True)


def format_int(i, sep='.'):
    """
    thousand separator
    """
    cyc = IT.cycle(['', '', sep])
    s = str(i)
    last = len(s) - 1
    formatted = [(cyc.__next__() if idx != last else '') + char 
                 for idx, char in enumerate(reversed(s))]
    return ''.join(reversed(formatted))


def gen_Strikes():
    """
    get the numbers to be removed from JumpList - as like in E-sieve
    """
    t = 1
    p = nextPrim(K)
    yield t*p
    for k in K:
        t += k
        if t > PPRIME:
            break
        yield t*p


def check_Symmetry():
    """
    remove or ignore last element
    compare list from start against from end
    """
    d = 0
    for i, x in enumerate(J[0:len(J)-1]):
        if i // ZCONTROL != d:
            d = i // ZCONTROL
            print(f'~{format_int(d):>9}', end=' # ', flush=True)
        yield i, x, J[-2-i]


T0 = DT.datetime.now()
TK = DT.timedelta(0)
while True:
    TA = DT.datetime.now()
    print(">>> ", flush=True)
    #
    p = nextPrim(K)
    PRIMES.append(p)
    print(">>> ", PRIMES)
    PPRIME *= p
    S = gen_Strikes()
    s = next(S)
    J.clear()
    #
    t = 1
    n = 0
    d = 0
    print(flush=True)
    for i in range(p):
        for k in K:
            j = k + n
            t += k
            if t // XCONTROL != d:
                d = t // XCONTROL
                print(f'~{format_int(d):>9}', end=' # ', flush=True)
            if t == s:
                n = k
                s = next(S)
                continue
            n = 0
            J.append(j)
    print(flush=True)
    #
    print(flush=True)
    lstSymmetry = [(i, x, y) for (i, x, y) in check_Symmetry() if x != y]
    for t in lstSymmetry:
        i, x, y = t
        print(i, x, y)
    print(flush=True)
    #
    K = J.copy()
    print(f"{format_int(len(K)):>30}", flush=True)
    print(f"{format_int(PPRIME):>30}", flush=True)
    TZ = DT.datetime.now()
    TD = TZ - TA
    if TK > DT.timedelta(0):
        TL = TD // TK
    else:
        TL = 1
    TK = TD
    print(f"{TL:30}")
    print(f"used time -> {timeDiff(TA)}", flush=True)
    #
    if p >= MAXPRIME:
        break
print()
print(f"over all: -> {timeDiff(T0)}", flush=True)
print(flush=True)
