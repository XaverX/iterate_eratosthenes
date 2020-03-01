# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:30:00 2019

ASPI
alternate search of primes based on iteration

@author: Berthold Braun
"""
import sys
import datetime as DT
#   import copy as CC
#   import json as JSON
from collections import deque
#   https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-queues

#   Abbruch bei ...
BreakOnMax = 1_500_000_000
MaxStepping = 11
MaxPrim = 17
#   aktuelle Position
stepping = 0
#   Startwerte
kgV = 1
primList = []
psqrList = []
pkgvList = []
jumpList = deque([1])
#   jumpList = [1]
jumpCount = {}
theStrikes = deque([])
#   theStrikes = []
currentP = 1


#   zur Kontrolle Ausgabe der aktuellen Position der Berechnung
def WhereWeAre(T0=None, *T):
    if T0 is None:
        T0 = DT.datetime.now()
    print('###', stepping, currentP, "---", T0)
    TT = list(T)
    print("{:>20}".format(kgV), primList)
    print("{:>20}".format(len(jumpList)), "[", end="")
    for i in range(min(len(jumpList), 18)):
        print(jumpList[i], end=", ")
    print("...]")
    print("{:2.3f}".format(100 * len(jumpList) / kgV), "  ", end="")
    TX = T0
    while len(TT) > 0:
        print(TT[0] - T0, "  ", end="")
        T0 = TT.pop(0)
    if (T0 != TX):
        print(T0 - TX, end="")
    print("\n")
    sys.stdout.flush()


def GetNextPrim(L):
    return 1 + L[0]  # nächste Primzahl: 1 + first(List)


def GetStrikeList(p, v, L):
    yield p
    #    Liste erzeugen über die Vielfachen der aktuellen Primzahl
    #    inklusive der grade gefundenen Primzahl selbst 1*p
    k = 1
    for i in L:
        k += i
        # wenn Rahmen überschritten, zusätzliches nachrückendes Queue-Element
        # if k * p > v: break  # nicht mehr benötigt wenn zusätzliches Element
        yield k * p
    return None


def GetTS(TT):
    # for tt in TT:
    #     yield tt
    while len(TT) > 0:
        xx = TT.popleft()
        yield xx
    return None


def GetTL(LL):
    # for ll in LL:
    #     yield ll
    while len(LL) > 0:
        xx = LL.popleft()
        yield xx
    return None


def GetNJ(LL, TT):
    cmpStrikes = GetTS(TT)
    nextJumper = GetTL(LL)
    CPS = next(cmpStrikes)
    sumJLE = 1
    while len(LL) > 0:
        JLE = next(nextJumper)
        sumJLE += JLE
        if sumJLE >= CPS:  # we found a striker
            NJE = next(nextJumper)  # get next jumper
            sumJLE += NJE  # add to running sum
            JLE += NJE  # correct the new jumper
            CPS = next(cmpStrikes)  # get next striker to compare
        yield JLE
        continue
    return None


#   Erzeugung der nächsten Iteration der Sprungliste
def GetNextJumps(LL, TT):
    JJ = deque([])  # empty queue for jumpList-elements
    # DD = {}  # empty/prefilled dictionary for counting the jumpList-elements
    DD = dict.fromkeys([i for i in range(2, 2 * LL[0], 2)], 0)
    for ll in GetNJ(LL, TT):
        DD[ll] = DD.get(ll, 0) + 1  # counting the jumpList-elements
        JJ.append(ll)
    return JJ, DD


def PartedString(J, rs=480, sp="\t", lf="\n"):
    # rs :: 1, 2, 8, 48, 480, 5760
    # rs = product of 1, 2, 4, 6, 10, (p-1), ... MaxLineLength
    # J Queue in jumpList-elements
    OutputLine = ""
    ElementInLine = 0
    CurLineNumber = 0
    MaxLineLength = min(len(J), rs)
    while True:
        for jj in J:
            ElementInLine += 1
            # create a line of some jumpList-elements
            OutputLine += "\t{}".format(jj)
            if ElementInLine >= MaxLineLength:
                yield OutputLine.lstrip(sp) + lf
                OutputLine = ""
                ElementInLine = 0
                CurLineNumber += 1
                if (  # False or
                        (CurLineNumber >= 4) or  # break after third line
                        (CurLineNumber*MaxLineLength >= len(J))):
                    if (CurLineNumber*MaxLineLength < len(J)):
                        OutputLine = "not all values ... has to be continued"
                        yield OutputLine + lf
                    return None


def WriteJumpers(p, s, P, v, C, J):
    try:
        fobj = open("prime_jumps__{:02}.txt".format(p), "w")
        # write stepping, current prime, primeList-elements
        fobj.write(">>> {:2}: {:4}\n".format(s, p))
        fobj.write("{}\n".format(P))
        # write length of jumpList and product of primes = kgV
        fobj.write("{:16} : {:21}\n".format(len(J), v))
        fobj.write("---\n")
        for jj in sorted(C.keys()):
            fobj.write("{:3}: {:11} \n".format(jj, C.get(jj)))
        fobj.write("+++\n")
        # write first n lines of jumpList-elements
        for t in PartedString(J):
            fobj.write("{}".format(t))
        fobj.write("***\n")
        with open("prime_jumps__{:02}.dat".format(p), "wb") as fbin:
            for i in J:
                fbin.write(i.to_bytes(1, byteorder='big', signed=True))
    finally:
        if fobj:
            fobj.close()


def AddToPrimes(p, k):
    primList.append(p)
    psqrList.append(p*p)
    pkgvList.append(k)


print('Los geht es!')
WhereWeAre()
dta = DT.datetime.now()
while True:
    dt0 = DT.datetime.now()
    stepping += 1
    currentP = GetNextPrim(jumpList)
    kgV *= currentP
    if (  # False or
            (kgV > BreakOnMax) or
            (currentP > MaxPrim) or
            (stepping > MaxStepping)):
        break
    theStrikes.clear()
    for pp in (GetStrikeList(currentP, kgV, jumpList)):
        theStrikes.append(pp)
    AddToPrimes(currentP, kgV)

    dt1 = DT.datetime.now()
    jumpList *= currentP
    jumpList, jumpCount = GetNextJumps(jumpList, theStrikes)

    dt2 = DT.datetime.now()
    WriteJumpers(currentP, stepping,
                 primList, kgV,
                 jumpCount, jumpList)

    dt3 = DT.datetime.now()
    WhereWeAre(dt0, dt1, dt2, dt3)

dtx = DT.datetime.now()
print(dta, "\n", dtx-dta)
print('Primes: ({})'.format(len(primList)))
print(primList)
print('Jumpers: ({}), first={}, max={}'.format(
        len(jumpList), jumpList[0], max(jumpList)))
print([jumpList[i] for i in range(min(24, len(jumpList)))])
print("\n")
sys.stdout.flush()
jumpList = [1]
jumpCount = {}
for i in range(len(primList)):
    print("{:3} {:4} {:5} {:12}".format(
            1+i, primList[i], psqrList[i], pkgvList[i]))
print("\n")
