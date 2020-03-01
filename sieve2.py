# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 00:20:06 2019

sieve on a set

@author: Berthold
"""

primList = []
workSet = set()
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
    minP = 0
    primList.clear()
    workSet.clear()
    print(step, minP, len(workSet))
    primList = [2, 3, 5]

    workSet.clear()
    workSet = workSet.union(set(range(1, maxP+1, 10)))
    workSet = workSet.union(set(range(3, maxP+1, 10)))
#    workSet = workSet.union(set(range(5, maxP+1, 10)))
    workSet = workSet.union(set(range(7, maxP+1, 10)))
    workSet = workSet.union(set(range(9, maxP+1, 10)))
#    workSet.sort()
    workSet.remove(1)
    workSet.difference_update(set(range(3, maxP+1, 3)))
    step = 3
    minP = 5
    print(step, minP, len(workSet))

    while (len(workSet) > 0) and (minP*minP <= maxP):
        step += 1
        minP = min(workSet)
        primList.append(minP)
        workSet.difference_update(set(range(minP, maxP+1, minP)))
        print(step, minP, len(workSet))
    else:
        primList.extend(list(workSet))

    primList.sort()
    print(len(primList))
    print(primList)
