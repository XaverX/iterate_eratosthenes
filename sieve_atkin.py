# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 13:03:32 2019
Prime_Sieve_Atkin
@author: Berthold
"""

#   maxSearch = 1000000000
maxSearch = 900
primList = [2, 3, 5]
AtkinList = [1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59]


def Atkin31(p):
    for x in range(1, p // 2, 1):
        if (4 * x * x) > p:
            break
        for y in range(1, p // 2, 2):
            a = 4 * x * x + y * y
            if a > p:
                break
            if a == p:
                yield p
    return 0


def Atkin32(p):
    for x in range(1, p // 2, 2):
        if (3 * x * x) > p:
            break
        for y in range(2, p // 2, 2):
            a = 3 * x * x + y * y
            if a > p:
                break
            if a == p:
                yield p
    return 0


def Atkin33(p):
    for x in range(2, p, 1):
        if (3 * x * x) < p:
            continue
        for y in range(x - 1, 0, -2):
            a = 3 * x * x - y * y
            if a > p:
                break
            if a == p:
                yield p
    return 0


try:
    i = 0
    while True:
        for j in AtkinList:
            currentMin = i * 60 + j
            n = 0
            if (currentMin <= maxSearch):
                if j in [1, 13, 17, 29, 37, 41, 49, 53]:
                    for k in Atkin31(currentMin):
                        if k == currentMin:
                            n += 1
                    else:
                        if n % 2 == 1:
                            print("A", currentMin)
                            primList.append(currentMin)
                elif j in [7, 19, 31, 43]:
                    for k in Atkin32(currentMin):
                        if k == currentMin:
                            n += 1
                    else:
                        if n % 2 == 1:
                            print("B", currentMin)
                            primList.append(currentMin)
                elif j in [11, 23, 47, 59]:
                    for k in Atkin33(currentMin):
                        if k == currentMin:
                            n += 1
                    else:
                        if n % 2 == 1:
                            print("C", currentMin)
                            primList.append(currentMin)
            if currentMin >= maxSearch:
                break
        if currentMin >= maxSearch:
            break
        i += 1


except IOError:
    pass


finally:
    pass
    print(primList)
    print(len(primList))
