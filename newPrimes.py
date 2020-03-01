# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 20:18:38 2019

@author: Berthold
"""

import datetime as DT
import math as MT


PrimeLoopMax = 17  # 13, 17, 19, 23, 29, 31, 37
PrimeMaxSearch = 10000
WriteToFile = False
fRES = None
fPRM = None
workSet = set()
jumpSet = set()


def GetNumber():
    inVal = "!"
    minP = 100
    maxP = 1000000
    while not inVal.isdigit():
        inVal = input("... bis zu welcher Zahl Primzahlen suchen: ")
        if (inVal == ""):
            inVal = "0"
    inVal = int(inVal)
    if inVal > 0:
        inVal = min(max(minP, inVal), maxP)
    return inVal


def PrintPrimes():
    print()
    i = 0
    for p in primList:
        i += 1
        print("{0:>5}:{1:>12}:{2:>6}:{3:>24}:".format(
                i, p, MT.trunc(MT.sqrt(p)), p*p))


def JumpListGenerator(np, L):
    ts = 1
    td = 0
    tc = 0
    for y in range(np):
        for x in L:
            tc += 1
            ts += x
#            if tc % 25000 == 0: print("\r              \r", ts, end="")
            if ts % np == 0:
                td += x
                continue
#           if ts in NX: td += x; continue
            td += x
            yield td
            td = 0


def JumpSetGenerator(mp, L):
    ts = 1
    while ts <= mp:
        for x in L:
            ts += x
            if ts <= mp:
                yield ts
            else:
                break


def WriteResults(onFile=False):
    print(DT.datetime.now(), DT.datetime.now() - dta)
    print(NP, "::", "PPP:", primProd, primList,
          "\r\nLEN:", len(jumpList),
          "\r\nMAX:", max(jumpList),
          "\r\nRATIO:", "{0:3.3f}".format(100 * len(jumpList) / primProd))
#   on screen and on file
    if onFile:
        fRES.write("{0}::PPP:{1}::\n".format(NP, primProd))
        fRES.write("{0}\n".format(primList))
        fRES.write("LEN:{0}::MAX:{1}\n".format(len(jumpList), max(jumpList)))
        fRES.write("RATIO: {0:3.3f}:\n".format(100 * len(jumpList) / primProd))
        i = 0
        d = 16  # Ausgabebreite 8, 16, 48
        while i < len(jumpList):
            s = repr(jumpList[i:min(i+d, len(jumpList))])
            s = s.replace("[", " ")
            s = s.replace(",", "\t")
            s = s.replace("]", "\t")
            fRES.write("{0}\n".format(s))
            i += d
        fRES.write("\r\n")


try:
    myP = GetNumber()

    workSet.clear()
    workSet = workSet.union(set(range(1, myP+1, 10)))
    workSet = workSet.union(set(range(3, myP+1, 10)))
#    workSet = workSet.union(set(range(5, myP+1, 10)))
    workSet = workSet.union(set(range(7, myP+1, 10)))
    workSet = workSet.union(set(range(9, myP+1, 10)))
#    workSet.sort()
    workSet.remove(1)
    workSet.difference_update(set(range(2, myP+1, 2)))
    workSet.difference_update(set(range(3, myP+1, 3)))
#    workSet.difference_update(set(range(5, myP+1, 5)))
    workSet.difference_update(set(range(7, myP+1, 7)))

    if WriteToFile:
        fRES = open("D:/Berthold/Dokumente/Primes/result1.txt", "w")
        fPRM = open("D:/Berthold/Dokumente/Primes/primes1.txt", "w")

    dta = DT.datetime.now()
    primProd = 1
    NP = 2
    primList = [NP]
    jumpList = [2]
    primProd *= NP
    WriteResults()

    while True:
        NP = 1 + jumpList[0]
        if NP > PrimeLoopMax:
            break

        dta = DT.datetime.now()
        primList.append(NP)
        primProd *= NP
        jumpList = [i for i in JumpListGenerator(NP, jumpList)]
        WriteResults()
        print()

    NP = 1
    while NP <= PrimeMaxSearch:
        for x in jumpList:
            NP += x
    jumpSet = {i for i in JumpSetGenerator(myP, jumpList)}
    workSet.difference_update(jumpSet)

    MP = max(primList)
    MS = MP * MP
#   bis hierhin wurde aus der Sprungliste die Vielfachen
#   kleinerer Primzahlen entfernt

#   weitere Primzahlen hinzufügen mit minimalem Test
    NP = 1
    while NP <= PrimeMaxSearch:
        for x in jumpList:
            NP += x
            b = False
#            if NP <= MP:
#                print("vorhanden:", NP)
#                continue
            if NP > PrimeMaxSearch:
                break
            if NP < MS:
                primList.append(NP)  # sicher Primzahl - bis zum Quadrat
                continue
            b = True
            for z in (z for z in primList
                      if ((z > PrimeLoopMax) and (z * z <= NP))):
                if NP % z == 0:
                    b = False
                    break
            if b:
                primList.append(NP)

    print()
    PrintPrimes()

except IOError:
    pass

finally:
    if fRES:
        fRES.close()
    if fPRM:
        fPRM.close()
