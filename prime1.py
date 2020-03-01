# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""
import sys
import datetime as DT
import functools as FT
import itertools as IT
import operand as OP

MAX_PRIME = 17

#   prime = 3
#   frame = 6
#   PP = [2,3]
#   LL = [4,2]

prime = 5
frame = 30
PP = [2, 3, 5]
LL = [6, 4, 2, 4, 2, 4, 6, 2]


def HowLong(DTA, DTZ=DT.datetime.now()):
    print(DTZ - DTA)
    print()
    sys.stdout.flush()


def NextPrim(L):
    return 1 + L[0]


def NextFrame(L, P):
    return NextPrim(L) * FT.reduce(lambda x, y: x*y, P, 1)


def NextS(L):
    yield map(lambda a, b=1: (a+b, b), L)


def NextStriker(L):
    m = NextPrim(L)
    t = 1
    yield (t*m)
    for l in L:
        t += l
        yield (t*m)


def NextElement(L):
    t = len(L)
    for i in L:
        t -= 1
        yield i, t


def NextJumper(L, P):
    m = NextPrim(L)
    f = NextFrame(L, P)
    k = NextStriker(L)
    kk = next(k)
    t = 1
    u = NextElement(L)
    for i in range(m):
        while True:
            if t > f:
                break
            uX = next(u)
            uu = uX[0]
            if uX[1] <= 0:
                u = NextElement(L)
            t += uu
            if t == kk:
                kk = next(k)
                uX = next(u)
                if uX[1] <= 0:
                    u = NextElement(L)
                uu += uX[0]
                t += uX[0]
            yield uu


TA = DT.datetime.now()
print(TA)
print(prime, PP)
print(frame, LL)

while True:
    T0 = DT.datetime.now()
    prime = NextPrim(LL)
    frame = NextFrame(LL, PP)
    print(prime)
    print(frame)
#    KK = list(NextStriker(LL))
#    print(KK)

    LL = list(NextJumper(LL, PP))
    PP.append(prime)
    HowLong(T0, DT.datetime.now())

    if prime >= MAX_PRIME:
        break

print()
print(prime, PP)
print(frame, len(LL))
TZ = DT.datetime.now()
HowLong(TA, TZ)
