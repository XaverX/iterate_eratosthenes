# -*- coding: utf-8 -*-
"""
Created on Thu Jan 09 16:00:00 2020
@author: Berthold Braun

computing some prime numbers - saving into a file
using distances from sieve of Eratosthenes - from file computed before
for a reduced amount of to be checked numbers
to check if prime
a) using division until sqare root
b) using Atkin wheel
c) ...

TODO
try the following changes ...
* use MP.pool instead of self created processes
        stored in a list
        starting and joining by pool-commands
* exchange of numbers between main and workers
        in 2 single threads
        create, store in ordered result list and send
        recieve, compute the differences and save to file
* recieve numbers from workers to main
        in a couple of queues one for each worker
        managed dictionary instead queue
        unmanged list or dict
* implementation of other checking methods (Atkin, ...)

"""


import sys
import os as OS
import getopt as GO
# import regex as RX
# import math as M
import time as TI
import datetime as DT
import itertools as IT
import operator as OP
import functools as FT
#
import numpy as NP
# import numba as NA
#
# import csv
# import collections as CL
from collections import deque as DQ
# from collections import OrderedDict as OD
from collections import namedtuple as NT
#
# import json
# import xml
# import threading as TH
import multiprocessing as MP
# import mmap as MM
#
import cProfile
import pstats
import io


MAXNUM = 1_000_000
NEWLIN = 100
NCORES = 0  # 0 non parallel execution
MCORES = max(1, MP.cpu_count() - 2)  # maximum number of wanted processes
MCORES = 60  # maximum number of wanted processes

#
JPfile = 'start_jumpers.csv'
PPfile = 'CheckedPrimes.csv'
startP = [2, 3, 5]
startJ = [6, 4, 2, 4, 2, 4, 6, 2]
#
pInfo = NT('T', ['P', 'Q', 'R'])
Aprime = DQ([])
Xprime = DQ([])
Ajumps = bytearray([])
DTYPE = 'int8'  # check dtype on greater MAXNUM = difference between primes
Pjumps = NP.array([], dtype=DTYPE)


def profile(fnc):
    """
    decorator for profiling
    """
    def DoIt(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return DoIt


def fInt(i, sep='.'):
    """
    thousand separator
    """
    cyc = IT.cycle(['', '', sep])
    s = str(i)
    last = len(s) - 1
    formatted = [(cyc.__next__() if idx != last else '') + char
                 for idx, char in enumerate(reversed(s))]
    return ''.join(reversed(formatted))


def delay(ms):
    """
    stop working for some milli seconds
    """
    TI.sleep(ms / 1000.0)


def timeDiff(TA, TZ=None):
    """
    show me how much time we take
    """
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA


def SetRange(v, low, up):
    if v < low:
        return low
    if v > up:
        return up
    return v


def SetValue(v, L):
    if len(L) == 0:
        return 1
    if v < min(L):
        return min(L)
    if v > max(L):
        return max(L)
    for x in L[::-1]:
        if x <= v:
            return x


def known_primes(L):
    D = DQ([])
    for (p, q, r) in [(x, x*x, x % 60) for x in L]:
        E = pInfo(p, q, r)
        D.append(E)
    return D


def make_jumpers(fn, pp, jp):
    try:
        read_primes = 0
        read_jumpers = 0
        p = []
        j = []
        with open(fn, 'rt') as ff:
            for tt in ff:
                tt = tt.strip()
                if tt == '':
                    continue
                zz = ''
                if tt[0] == '#':
                    zz = tt.split(sep='\t')[-1].lower()
                    if zz == 'reset':
                        read_primes = 0
                        read_jumpers = 0
                    if zz == 'primes':
                        read_primes += 1
                        # read_jumpers = 0
                    if zz == 'jumpers':
                        read_jumpers += 1
                        read_primes = 2
                    continue
                if read_primes == 1:
                    p.extend(list([int(x) for x in tt.split(sep='\t')]))
                if read_jumpers == 1:
                    j.extend(list([int(x) for x in tt.split(sep='\t')]))
    except (FileNotFoundError, PermissionError):
        p = pp
        j = jp
    finally:
        return p, j


def write_primes(fn, lf):
    # write primes into file - recomputed by distances - in blocks of NEWLIN
    p = 1
    x = 1
    s = f'{MAXNUM}'
    s = 1 + len(s)
    with open(fn, 'wt') as ff:
        ff.write(f'max={fInt(MAXNUM)}')
        for z in Pjumps:
            p += z
            if p >= x:
                ff.write('\n')
                # ff.flush()
            else:
                ff.write('\t')
            while p >= x:
                x += lf
            ff.write(f'{p:>{s}}')
        ff.write('\n')


def gen_print_dot():
    # set a distance how often we say we are still computing
    # get length of a number
    s = f'{MAXNUM}'
    s = len(s)
    DOT = round(MAXNUM, s) // 100
    if DOT > 1_000_000: DOT = 1_000_000
    if DOT < 100: DOT = 100
    d = -1
    while True:
        p = (yield)
        if p <= 0:
            break
        dd = p // DOT
        if dd > d:
            d = dd
            print('.', sep='', end='')
    return None


def use_print_dot():
    while True:
        yield from gen_print_dot()
    return None


def gen_prime_jump():
    # store the primes into an array by their difference
    global Pjumps
    d0 = 0
    s = 1
    tt = []
    while True:
        p = (yield)
        # signal to shutdown the generator
        if p <= 0:
            break
        # get the difference between primes
        if p > 1:
            d = p - s
            if d > d0:
                d0 = d
                print(' ', d0, ' ', sep='', end='')
            tt.append(d)
            s = p
        # signal at end = 1 or a handful is ready to collect them
        if p == 1 or len(tt) >= 32:
            ta = NP.array(tt, dtype=DTYPE)
            Pjumps = NP.concatenate((Pjumps, ta))
            tt = []
    return None


def gen_jumps():
    # generate the next possible prime to check
    # endless repeating the distances from E.-sieve-remainders
    x = 1
    for i in IT.cycle(Ajumps):
        x += i
        yield x
    return None


def use_prime_jump():
    while True:
        yield from gen_prime_jump()
    return None


def check_composed(n):
    # divide number by list of computed primes until the square-root-rule
    # here we do not need first primes becuase we use E.sieve-jumps
    for E in Xprime:
        p, q, r = E
        if q > n:
            return False
        if n % p == 0:
            return True


def MP_check_composed(nm, mpS, mpC, mpQ, mpR):
    prior = 0
    ospid = OS.getpid()
    mpR.put_nowait((ospid, 'Init', nm))
    #
    SQ = list([(p, q) for (p, q) in mpS])
    mpR.put_nowait((len(SQ), 'List', nm))
    #
    while (mpQ.qsize() == 0) or (mpQ.empty()):
        delay(10)
        continue
    cmdQ = mpQ.get_nowait()
    mpR.put_nowait((cmdQ, 'Comm', nm))
    #
    mpR.put_nowait((0, 'Wait', nm))
    while mpC.qsize() > 0:
        delay(10)
        continue
    while True:
        if not mpC.empty():
            break
        n = prior
        try:
            n = mpQ.get_nowait()
        # except MP.Empty as e:
        #    continue
        except Exception as e:
            E = str(e.__class__)
            E = E.upper()
            # <class '_queue.Empty'>
            if E.find('EMPTY') >= 0:
                continue
            else:
                mpR.put_nowait((0, 'Error', nm,
                                e.__class__(), e.__repr__(), e.__cause__))
                delay(10)
                continue
        if n <= 1:
            continue
        if n == prior:
            continue
            prior = n
        for (p, q) in SQ:
            if q > n:
                mpR.put_nowait((n, False, nm))  # n is prime
                break
            if n % p == 0:
                mpR.put_nowait((n, True, nm))  # n is composed
                break
        else:
            mpQ.task_done()


def read_worker(mpR, nm):
    print(nm, end=': ', flush=True)
    for i in range(4):
        while mpR.empty():
            delay(10)
        else:
            a = mpR.get_nowait()
            print(a[1], f'{a[0]:>6}  ', sep=':', end=' ', flush=True)
            mpR.task_done()
    print()


def iterate_primes():
    print_dot = use_print_dot()
    # show running dots while still excuting
    next(print_dot)
    prime_jump = use_prime_jump()
    # get numbers which will be possible prime without already striked out ones
    next(prime_jump)
    #
    # for the first primes we also get the distances for later file report
    for p in Aprime:
        prime_jump.send(p)
    #
    # the border until we will store the square of a prime
    m2 = 10000
    while m2*m2 < MAXNUM: m2 += 10000
    while m2*m2 > MAXNUM: m2 -= 1000
    while m2*m2 < MAXNUM: m2 += 100
    while m2*m2 > MAXNUM: m2 -= 10
    m1 = (m2 // 20)
    m2 += m1
    #
    J = gen_jumps()
    p = next(J)
    print_dot.send(p)
    p2 = p * p
    #
    # til the square of highest known prime all chosen numbers are prime
    while p < p2:
        prime_jump.send(p)
        E = pInfo(p, p * p, p % 60)
        Xprime.append(E)
        p = next(J)
    #
    # no multiprocessing
    while True:
        # get next number which could be a prime
        p = next(J)
        print_dot.send(p)
        # test the number - prime or not prime that's the question
        if check_composed(p):
            continue  # no prime than get next number
        prime_jump.send(p)  # yeah its a prime - store it
        # store the prime's square (+ Atkin residuum = 60 for later use)
        if p <= m2:
            E = pInfo(p, p * p, p % 60)
            Xprime.append(E)
        # we should stop looping if maximum test number reached
        if p >= MAXNUM:
            break
        # on multiprocessing we still get the squares with single core
        if NCORES >= 1 and p > m2:
            break
    # execution on n cpu-cores
    ProcList = []
    if NCORES >= 1:
        print()
        mng = MP.Manager()
        mpQ = mng.Queue()  # input for next number to check for is_prime
        mpR = mng.Queue()  # output results tuple(num, bool, worker)
        mpC = mng.Queue()  # input to send stop signal - detect by not empty
        mpS = mng.list()   # list of known primes and their squares
        for E in Xprime:
            p, p2, _ = E
            mpS.append((p, p2))
        # prepare processes
        try:
            for k in range(NCORES):
                pName = f'PY_{k:02}'
                # print(pName)
                MWP = MP.Process(target=MP_check_composed,
                                 args=(pName, mpS, mpC, mpQ, mpR),
                                 name=pName)
                ProcList.append(MWP)
            # ? runs also without indentation : p>max or proclist is empty
            mpC.put_nowait('WAIT')
            delay(10)
            for MWP in ProcList:
                mpQ.put_nowait(MWP.name)
                MWP.start()
                read_worker(mpR, MWP.name)
            mpC.get_nowait()
            delay(10)
            #
            while True:
                while (not mpR.empty()) or (mpR.qsize() > 0):
                    a = None
                    a = mpR.get_nowait()
                    # print('<<< recv: ', a, ' (', mpR.qsize(), ')', sep='', flush=True)
                    if (p < MAXNUM) and (mpQ.qsize() < (5 * NCORES)):
                        break
                while (p < MAXNUM) and mpQ.qsize() < (20 * NCORES):
                    p = next(J)
                    print_dot.send(p)
                    mpQ.put_nowait(p)
                    # print('>>> send: ', p, ' (', mpQ.qsize(), ')', sep='', flush=True)
                    if mpR.qsize() > (3 * NCORES):
                        break
                if (p >= MAXNUM) and mpQ.empty() and mpR.empty():
                    break
        #
        except Exception as e:
            print(e)
        #
        finally:
            mpC.put_nowait('STOP')
            delay(100)
            for MWP in ProcList:
                MWP.join()
                if MWP.is_alive():
                    MWP.terminate()
                MWP.close()
            mpC.get_nowait()
            mpC.task_done()

    #
    # signaling the end
    print_dot.send(0)
    prime_jump.send(1)
    prime_jump.send(0)


# @profile
def DoAllTheStuff():
    global Aprime, Xprime, Ajumps
    # get prepared numbers as remaining distances after E.-sieving
    pp, jj = make_jumpers(JPfile, startP, startJ)
    # store the first primes in extra array - we do not need them for jumping
    Aprime.extend(pp)
    Ajumps = bytearray(jj)
    print(fInt(MAXNUM), fInt(NEWLIN), JPfile, PPfile)
    iterate_primes()
    write_primes(PPfile, NEWLIN)
    print('\n', pp, sep='', end='')
    print(' ... for more primes up to', fInt(MAXNUM),
          'see file:', PPfile, sep=' ')


def usage():
    print(f'compute the primes til a given number - default {MAXNUM}')
    print('known commands are:')
    print('\t-h --help              :: shows this message')
    print('\t-j --jumpers <in_file> :: distances in sieve until known prime')
    print('\t-p --primes <out_file> :: computed primes until giben maximum')
    print('\t-m --maxnum <nnnnnnnn> :: number where to stop computation')
    print('\t-l --linelen <nn>      :: number of primes in a line')
    print('\t-c --cpunodes <##>     :: if >0 try to use this number of cores')
    print('\t-a --algorithm <##> ')


if __name__ == "__main__":
    try:
        opts, args = GO.getopt(sys.argv[1:], 'hj:p:l:m:a:c:', [
                     'help', 'jumpers', 'primes',
                     'linelen', 'maxnum',
                     'algorithm', 'cpunodes'])
    except GO.GetoptError as err:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(255)
    #
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            break
        elif o in ("-j", "--jumpers"):
            JPfile = a
        elif o in ("-p", "--primes"):
            PPfile = a
        elif o in ("-m", "--maxnum"):
            MAXNUM = SetRange(int(a), 1_000, 1_000_000_000)
        elif o in ("-l", "--linelen"):
            NEWLIN = SetValue(int(a), [1, 10, 20, 50, 100, 200, 500, 1000])
        elif o in ("-c", "--cpunodes"):
            NCORES = SetRange(int(a), 0, MCORES)
        elif o in ("-a", "--algorithm"):
            pass
        else:
            assert False, "unhandled option"
            break
    else:
        print('DoAllTheStuff')
        ta = TI.time()
        DoAllTheStuff()
        tz = TI.time()
        print(f'time used: {(tz-ta)*1000/1000:>12.3f}')
