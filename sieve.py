# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 19:28:27 2019

sieve eratosthenmes

@author: Berthold
"""

primList = []
workList = []
maxP = "1"
step = 0

while maxP != "":
    maxP = input("... bis zu welcher Zahl Primzahlen suchen: ")
    if (maxP == ""):
        break
    for c in maxP:
        if c not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            maxP = 0
            break
        else:
            maxP = int(maxP)
    if maxP <= 0:
        break
    maxP = max(100, maxP)

    step = 0
    primList.clear()
    primList = [2, 5]

    workList.clear()
    workList.extend(list(range(1, maxP+1, 10)))
    workList.extend(list(range(3, maxP+1, 10)))
#    workList.extend(list(range(5, maxP+1, 10)))
    workList.extend(list(range(7, maxP+1, 10)))
    workList.extend(list(range(9, maxP+1, 10)))
    workList.sort()
    workList.remove(1)

    minP = 1

    while (len(workList) > 0):
        step += 1
        minP = workList[0]
        primList.append(minP)
        for w in list(range(minP, maxP+1, minP)):
            if w in workList:
                workList.remove(w)

    primList.sort()
    print(primList)
