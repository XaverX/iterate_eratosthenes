# -*- coding: utf-8 -*-

import datetime as DT

"""
    sieve of eratosthenes
    an alternative implementation
    not by striking out the multiples of a prime number
    instead find the differences of still residing numbers
    computed in an iterative way
"""

"""
iter_cnts = 3
curr_prim = 5
jump_list = [6,4,2,4,2,4,6,2]
prim_prod = 30
prim_list = [2,3,5]
jumps_cnt = len(jump_list)
"""

#   preparation

iter_cnts = 0
iter_maxc = 5
max_number = 10000000000
s = "\r" + " "*80
#   iteration step current and maximum
#   maximum number to be checked after iteration and finding differences

curr_prim = 1
jump_list = [1]
prim_prod = 1
prim_list = []
jumps_cnt = len(jump_list)
mult_list = [0]
# - curr_prim - the prime number we are actual working on
# - jump_list - the current builded list if differences
# - prim_prod - the product of falready found prime numbers
# - prim_list - list of currently found prime numbers
# - jumps_cnt - current size of jump_list
# - mult_list - multiples of current prime

###############################################################################
#   start of generating the list of differences
#   called jump_list inside a frame of numbers given by prim_prod
###############################################################################

while (iter_cnts < iter_maxc):
    print("\n")
    iter_cnts += 1
    dta = DT.datetime.now()
    print(dta)
#   we are in next iteration
    curr_prim = 1 + jump_list[0]
    prim_list.append(curr_prim)
    prim_prod *= curr_prim
#   get the next prime number = allways give by 1 plus first difference
#   add it ot list and compute product of all found primes

    print(iter_cnts, " :: ", curr_prim)
    print(prim_prod, " <= ", prim_list)

    mult_list.clear()
    mult_list.append(curr_prim)
#   prepare list of multiples and put current prime into it

    k_sum = 1
    p_pos = -1
#   starting point to add the differences from jump_list
#   position of current used difference for summarizing and striking out
    while (k_sum < prim_prod):
        for p in jump_list:
            k_sum += p
            mult_list.append(k_sum * curr_prim)
        del mult_list[-1]
        print("mult_list: ", mult_list, len(mult_list))
#   finding the multiples of current prime
#   based on the numbers of last frame
#   delete the last one - we are to far = out of frame
        k_sum = 1
        jump_list *= curr_prim
        print(DT.datetime.now(), DT.datetime.now() - dta)
#   on the new = current prime we have to run
#   across old jump_list n times
#   to reach the end of frame = prim_prod

        print(".", end="")
        for p in jump_list:
            k_sum += p
            p_pos += 1
#   find the current remaining naumbers in sieve by adding the differences
#   remember the position of current jump_list element
#   for summarizing and striking out
            if ((p_pos % 1000) == 0):
                if ((p_pos // 1000) % 5) == 0:
                    print(s, "\r.", k_sum, p_pos, id(jump_list), end="")
                elif ((p_pos // 1000) % 5) == 1:
                    print(s, "\r/", k_sum, p_pos, id(jump_list), end="")
                elif ((p_pos // 1000) % 5) == 2:
                    print(s, "\r_", k_sum, p_pos, id(jump_list), end="")
                elif ((p_pos // 1000) % 5) == 3:
                    print(s, "\r\\", k_sum, p_pos, id(jump_list), end="")
                elif ((p_pos // 1000) % 5) == 4:
                    print(s, "\rI", k_sum, p_pos, id(jump_list), end="")

            if k_sum in mult_list:
                d = jump_list[p_pos + 1]
#   we matched a multiple - than get the next difference
#                print(k_sum, " in ", mult_list)
                k_sum += d
                jump_list[p_pos] += d
                jump_list[p_pos + 1] = 0
#   and add it to current sum counter and difference
#   set the element which was added to zero - it is now in the sum
#   so we will not recompute on next step and reposition on this next iteration
#            elif k_sum < prim_prod:
#                pass
#                print (k_sum)
        print("\r                                            \r", end="")

    print(DT.datetime.now(), DT.datetime.now() - dta)
    print(len(jump_list), jump_list.count(0))
    while 0 in jump_list:
        jump_list.remove(0)
#   reduce the jump_list - all the zeros will be deleted here

    jumps_cnt = len(jump_list)
    print("jump_list => ", len(jump_list))
    print("{0:3.2f}".format(100 * len(jump_list) / prim_prod))
    print(DT.datetime.now(), DT.datetime.now() - dta)

print("ZZZ")





