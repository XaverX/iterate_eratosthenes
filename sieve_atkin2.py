# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 22:00:00 2019
Prime_Sieve_Atkin Standard
@author: Berthold
"""

#   maxSearch = 1000000000
maxSearch = 1000
primList = [2, 3, 5]
workSet = set()


try:
    workSet.clear()
#   prepare the numbers to be checked for prime
    workSet = workSet.union(set(range(1, maxSearch+1, 10)))
    workSet = workSet.union(set(range(3, maxSearch+1, 10)))
#    workSet = workSet.union(set(range(5, maxSearch+1, 10)))
    workSet = workSet.union(set(range(7, maxSearch+1, 10)))
    workSet = workSet.union(set(range(9, maxSearch+1, 10)))

#   we begin with known primes 2,3,5
#   workSet should be cleared from multiples and nonprime 1
    workSet.remove(1)
#    workSet.difference_update(set(range(2, maxSearch+1, 2)))
    workSet.difference_update(set(range(3, maxSearch+1, 3)))
#    workSet.difference_update(set(range(5, maxSearch+1, 5)))

    currentMin = 1
#    while ((currentMin * currentMin) <= maxSearch):
    while (currentMin <= maxSearch):
        n = 0
        if currentMin in workSet:
            pass
#            workSet.difference_update(
#                    set(range(currentMin, maxSearch+1, currentMin)))
            checkModul = currentMin % 60
            if checkModul in [1, 13, 17, 29, 37, 41, 49, 53]:
                atkinValue = 4 * n
                print("A", currentMin)
                primList.append(currentMin)
            elif checkModul in [7, 19, 31, 43]:
                print("B", currentMin)
                primList.append(currentMin)
            elif checkModul in [11, 23, 47, 59]:
                print("C", currentMin)
                primList.append(currentMin)
            else:
                print("oops", currentMin)
        if (len(workSet) == 0):
            break
        currentMin += 1
    else:
        pass
#        primList.extend(workSet)
        primList.sort()
        print(primList)


except IOError:
    pass


finally:
    pass
