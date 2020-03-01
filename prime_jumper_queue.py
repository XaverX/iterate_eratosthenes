# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:17:55 2019

@author: Berthold
"""


# import sys as S
# import math as M
import time as TI
import datetime as DT
import threading as TH
import itertools as IT
import operator as OP
import functools as FT
# import collections as CL
from collections import deque as DQ
from collections import OrderedDict as OD
# import regex as RX


PRIMES = []


def delay(ms):
    TI.sleep(ms / 1000.0)


def timeDiff(TA, TZ=None):
    """
    show me how much time we take
    """
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA


def format_int(i, sep='.'):
    """
    thousand separator
    """
    cyc = IT.cycle(['', '', sep])
    s = str(i)
    last = len(s) - 1
    formatted = [(cyc.__next__() if idx != last else '') + char 
                 for idx, char in enumerate(reversed(s))]
    return ''.join(reversed(formatted))


nextPrime = lambda L: 1 + L[0]


partSumme = lambda L: FT.reduce(OP.add, L, 1)


def ListOf_Strikes(JL):
    p = nextPrime(JL)
    # K = [p * partSumme(L) for L in [JL[0:i+1] for i in range(len(JL))] ]
    # K = [p * partSumme(LL) for LL in [L for L in [JL[0:i+1] for i in range(len(JL))]]]
    # K = [p * partSumme(j, J) for (j, J) in [(i, L[0:i]) for i in range(len(L))]]
    K = DQ([])
    s = 1
    K.append(s * p)
    for i in range(len(JL) - 1):
        s += JL[i]
        K.append(s * p)
    return K


def product_Primes(P):
    return FT.reduce(OP.mul, P, 1)


def length_Jumps(P):
    return FT.reduce(OP.mul, [max(1, x-1) for x in P], 1)


class InvalidPrimeThread(Exception):
    pass


class Prime(TH.Thread):
    THL = TH.Lock()
    AllThreads = OD([])
    __StopSignal = False
    EarlyStart = True
    EarlyLimit = 4
    
    def __init__(self, Prime=0, RunID=0, JL=[], PN=''):
        if (Prime < 1) or (RunID < 0) or (RunID > Prime):
            raise InvalidPrimeThread  # "neither ID nor JL is correct"
        TH.Thread.__init__(self)
        #
        
        # self.THL.acquire()
        # self.THL.release()
        if True:
            self.__PR = Prime  # current prrime
            self.__ID = RunID  # 0 : dispatcher ---  1..p : worker threads
            #
            tn = self.__MakeName(self.__PR, self.__ID)
            self.setName(tn);                     # easy identifier over all threads
            self.AllThreads.setdefault(tn, [self, self.is_alive(), DT.datetime.now(), None, None, 0])
            #
        if RunID == 0:
            self.__dist = product_Primes(PRIMES)      # distances of start points
            self.__size = length_Jumps(PRIMES)        # length of input JumpList
            self.__Jumpers = DQ([])                   # alternativ. bytearray
            PRIMES.append(self.__PR)                  # set the next step of primes
            self.__maxx = product_Primes(PRIMES)      # frame inside  
            self.__outL = length_Jumps(PRIMES)        # assumed length of target list 
            #
            self.__Strikes = set([])  # numbers to be removed
            # self.__Strikes = set(ListOf_Strikes(JL))  # numbers to be removed
            self.__OutList = DQ([])                   # alternativ. bytearray
            self.AddJumpList(JL)     # get the first jumps and include create strikes
            self.__StartCount = 0    # number of already started subthreads
            self.__FinitCount = 0    # number of already ended subthreads
        if RunID >= 1:
            self.__parent = self.AllThreads[PN][0]
            #
            self.__dist = self.__parent.__dist        # distances of start points
            self.__size = self.__parent.__size        # length of input JumpList
            self.__maxx = self.__parent.__maxx        # frame inside  
            self.__Jumpers = DQ([])                   # alternativ. bytearray
            #
            self.__finit = 1 + (self.__ID * self.__dist)
            self.__begin = self.__finit - self.__dist
        print(self)    
    
    def __str__(self):
        print()
        print(self.getName())
        print('prd:', f'{self.__maxx:>16}', ' |  cnt:', f'{self.__size:>16}', sep='', end='')
        if self.__ID == 0: print(' |  out:', f'{self.__outL:>16}', sep='') 
        else: print()
        print(self.__Jumpers)
        if self.__ID == 0: print(self.__Strikes)
        if self.__ID >= 1: print(self.__parent.getName(), self.__begin, self.__finit)
        # return self.getName()
        return ""

    def __MakeName(self, Prime=0, RunID=0):
        return 'X_' + '{:02}'.format(Prime) + '_' + '{:02}'.format(RunID)
        
    def __MakeStrikes(self):
        if (self.__ID != 0) or (len(self.__Jumpers) == 0):
            return
        if len(self.__Jumpers) < min(self.EarlyLimit, self.__size):
            return
        # print('MS:', self.__Jumpers)
        self.THL.acquire()
        self.__Strikes = set(ListOf_Strikes(self.__Jumpers))
        self.THL.release()
    
    def __InitWorkers(self):
        if (self.__ID != 0):
            return
        for i in range(self.__PR):
            Prime(self.__PR, i+1, PN=self.getName())
            if i > 0: continue
            if self.EarlyStart and (i+1 == 1):
                self.__StartWorker(self.__PR, i+1)
                print('ExtraStart')

    def __StartWorker(self, PR=0, ID=0):
        tn = self.__MakeName(PR, ID)
        print('try to start: ', tn)
        T = None
        self.__StartCount += 1
        try:
            T = self.AllThreads[tn][0]
            print(tn, T)
            print(tn, 'alive1', T.is_alive())
            T.start()
            # print(tn, 'ident:', T.T.ident)
            print(tn, 'alive2', T.is_alive())
            delay(2000)
            print(tn, 'alive3', T.is_alive())
            # if T.ident() == 0:
            # if T.ident() > 0:
            T.start()
            print(tn, 'alive4', T.is_alive())
        except:
            print('oops', tn)
            pass

    def AddJumpList(self, JL=[]):
        if (self.__ID != 0):
            return
        if len(self.__Jumpers) + len(JL) > self.__size:
            return
        self.THL.acquire()
        self.__Jumpers.extend(JL)
        self.THL.release()
        # print('JL:', self.__Jumpers)
        if len(self.__Jumpers) >= min(self.EarlyLimit, self.__size):
            self.__MakeStrikes()  # input jumpers complete we can create all strikers

    def EmergencyStop():
        Prime.__StopSignal = True
        delay(1500)
        Prime.THL.acquire()
        Z = [T for T in TH.enumerate() if T.getName().find('X_') == 0]
        Prime.THL.release()
        if len(Z) > 0:
            print('>>> stopping threads: ', end='')
            while len(Z) > 0:
                T = Z.pop()
                print('\t', T.getName(), end='')
                # T._stop()
            else:
                print('\t <<<')

    def run(self):
        X = self.AllThreads[self.getName()]
        X[3] = DT.datetime.now()
        #
        print('RUN', end=': ')
        if self.__ID == 0:
            print('dispatch', self.__PR, self.__ID)
            if len(self.__Jumpers) > min(self.EarlyLimit, self.__size):
                self.__InitWorkers()  # create all sub threads to compute next jump list in partitions
            while self.__StartCount < self.__PR:
                if len(self.__Jumpers) >= self.__size:
                    for i in range(self.__PR):
                        self.__StartWorker(self.__PR, ID=i+1)
                delay(1000)
        elif self.__ID <= self.__PR:
            print('compute', self.__PR, self.__ID)
            delay(1000)
        else:
            print('failure', self.__PR, self.__ID)
        #
        X[4] = DT.datetime.now()


exit
CC = TH.active_count()
if True:
    # PRIMES = []
    # JLX = [1] 
    # PRIMES = [2]
    # JLX = [2] 
    # PRIMES = [2,3]
    # JLX = [4,2] 
    PRIMES = [2,3,5]
    # JLX = [6,4,2,4,2]
    JLX = [6,4,2,4,2,4,6,2]
    print(PRIMES)

    
    X = Prime(nextPrime(JLX),0)
    X.AddJumpList(JLX)
    print('here we are!')
    print(X)

    X.start()
    
    print(PRIMES)
    # print(Prime.AllThreads)
    print()

Prime.EmergencyStop()

#
#
#QQ = "|/-\\"
#qq = 0
#while TH.active_count() > CC:
#    t = ''
#    qq += 1
#    qq %= 4
#    print(' \b\r'.ljust(240, ' '), flush=True, end="") 
#    print(' \b\r', DT.datetime.now(), " : ", QQ[qq], " : ", t, sep="", flush=True, end="") 
#    TI.sleep(0.02)    
#
#
Prime.EmergencyStop()

for Z in Prime.AllThreads.items():
    NN, LL = Z
    runFlag, iTime, sTime, eTime, SleepPhases = LL[1:6]
    print(NN, '\t', runFlag)
    tDiff = eTime - sTime if eTime is not None and sTime is not None else ""
    print(iTime, " : ", sTime, " : ", eTime, " : ", tDiff, " : ", SleepPhases)
