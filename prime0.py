# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:30:00 2019
ASPI
alternate search of prims based on iteration
@author: Berthold Braun
"""

BreakOnMax = 1000000
MaxStepping = 9
MaxPrim = 13
stepping = 0
currentP = 1
kgV = 1
primList = []
jumpList = [1]


def GetNextPrim(L):
    return 1 + L[0]


def GetNextStrike(p, v, L):
    k = 1
    yield k * p
    for i in L:
        k += i
        if k * p > v:
            break
        yield k * p
    return None


while True:
    stepping += 1
    currentP = GetNextPrim(jumpList)
    primList.append(currentP)
    kgV *= currentP

    if (stepping >= MaxStepping) or (currentP >= MaxPrim) or (kgV >= BreakOnMax):
        break

    theStrikes = [pp for pp in (GetNextStrike(currentP, kgV, jumpList))]
    jumpList *= currentP

    k = 1
    p = -1
    for i in jumpList:
        p += 1
        k += i
        if k in theStrikes:
            t = jumpList.pop(p + 1)
            jumpList[p] += t
            k += t


r = 24
print()
print('Primes:', len(primList))
print(primList)
print('JumpList:', len(jumpList))
# print(jumpList[0:r], '...', jumpList[len(jumpList)-r-1:len(jumpList)])
print(jumpList)
jumpList.reverse()
print(jumpList[1:])
