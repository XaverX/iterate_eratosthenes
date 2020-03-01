# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:30:00 2019

ASPI
alternate search of prims based on iteration

@author: Berthold Braun
"""


BreakOnMax = 10000000000
MaxStepping = 11
MaxPrim = 13
stepping = 0
kgV = 1
primList = []
jumpList = [1]
currentP = 1


def GetNextPrim(L):
    return 1 + L[0]


def GetStrikeList(p, v, L):
    k = 1
    yield k * p
    for i in L:
        k += i
        if k * p > v:
            break
        yield k * p
    return None


def WhereWeAre():
    print()
    print(stepping, currentP)
    print(kgV, primList)
#    print(len(jumpList), max(jumpList), jumpList)
#    print(len(jumpList), max(jumpList))


print('Los geht es!')
WhereWeAre()
while True:
    stepping += 1
    currentP = GetNextPrim(jumpList)
    primList.append(currentP)
    kgV *= currentP
    if (
            stepping >= MaxStepping) or (
            currentP >= MaxPrim) or (
            kgV >= BreakOnMax):
        break
    theStrikes = [pp for pp in (GetStrikeList(currentP, kgV, jumpList))]

    WhereWeAre()
    jumpList *= currentP

    # Startwert für Summation und Zusammenfassung der Elemente der Sprungliste
    k = 1
    # Positionsmarker
    p = -1

    for i in jumpList:
        p += 1
        if i == 0:
            continue
        k += i
        if k in theStrikes:
            t = jumpList.pop(p + 1)
            jumpList[p] += t
            k += t

print()
print('Primes:')
print(primList)
