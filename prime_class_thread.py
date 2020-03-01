# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 21:30:32 2019

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
from collections import namedtuple as NT
# import regex as RX


PRIMES = []
MAXPRIME = 29


def showThreading(M=None):
    print(DT.datetime.now(), flush=True)
    PrimeBase.THL.acquire()
    for Z in PrimeBase.AllThreads.values():
        if M is not None:
            if Z.Prime != M: continue
        print(f'{Z.Prime:>4}{Z.RunID:>4}{str(Z.alive):>7}{Z.PauseCnt:>9}{Z.WhereItIs:>13}', end='', flush=True)
        if Z.FinitTime is not None and Z.StartTime is not None:
            tDiff = Z.FinitTime - Z.StartTime
        elif Z.ReadyTime is not None and Z.StartTime is not None:
            tDiff = Z.ReadyTime - Z.StartTime
        else:
            tDiff = None
        if Z.RunID == 0:
            print(" : ",  formDT(Z.InitTime, 'HMS3'), 
                  " : ", formDT(Z.StartTime, 'HMS3'), 
                  " : ", formDT(Z.FinitTime, 'HMS3'), 
                  " : ", formDT(tDiff, 'delta3'), flush=True)
        else:
            print(" : ",  formDT(Z.InitTime, 'HMS3'), 
                  " : ", formDT(Z.StartTime, 'HMS3'), 
                  " : ", formDT(Z.ReadyTime, 'HMS3'), 
                  " : ", formDT(tDiff, 'delta6'), flush=True)
    PrimeBase.THL.release()
    print(flush=True)


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


def formDT(T, datefmt=None):
    if T is None: return str(None)
    if datefmt == 'delta6':
        s = f'{T.seconds:>7}.{T.microseconds:06}'
    elif datefmt == 'delta3':
        s = f'{T.seconds//60:>4}:{T.seconds%60:02}.{T.microseconds//1000:03}'
    elif datefmt == 'HMS3':
        s = T.strftime('%H:%M:%S.%f')
    elif datefmt == 'TS':
        s = T.strftime('%Y%m%d%H%M%S')
    elif datefmt == 'D':
        s = T.strftime('%d.%m.%Y')
    elif datefmt == 'T':
        s = T.strftime('%H:%M:%S')
    elif datefmt == 'DT':
        s = T.strftime('%d.%m.%Y %H:%M:%S')
    else:
        s = T.strftime('%Y-%m-%d %H:%M:%S')
    return s


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
    """
    beginning with 1 and than adding all differences
    multiplied with current prime 
    this and following difference will be added
    this are the numbers where we should do something
    in sieve of Eratosthenes this are the numbers which will be erased
    """
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
    """
    multiply the until here known primes - 2*3*5*...
    this gives the range where list differences will be repeated 
    """
    return FT.reduce(OP.mul, P, 1)


def length_Jumps(P):
    """
    formula that shows us the expected size of array of differences
    length = (2-1)*(3-1)*(5-1)*(7-1)*.. = product over all (p-1)
    """
    return FT.reduce(OP.mul, [max(1, x-1) for x in P], 1)


class InvalidPrimeThread(Exception):
    pass

#   --- Base start

class PrimeBase(TH.Thread):
    THL = TH.Lock()
    AllThreads = OD([])
    _StopSignal = False
    EarlyLimit = 8  # we need at minimum at least 8 elements in Jumpers
    
    def __init__(self, Prime=0, RunID=0):
        TH.Thread.__init__(self)
        PrimeBase.THL.acquire()
        if True:
            self._PR = Prime  # current prrime
            self._ID = RunID  # 0 : dispatcher ---  1..p : worker threads
            # print('init thread: ', Prime, RunID, flush=True)
            #
            tn = self._MakeName(Prime, RunID)
            self.setName(tn);                     # easy identifier over all threads
            #
            nt = NT('Info', ['Prime', 'RunID', 
                             'TObject', 'Alive', 'I_AmReady', 'PauseCnt', 'WhereItIs', 
                             'InitTime', 'StartTime', 'ReadyTime', 'FinitTime'])
            nt.Prime = Prime  # current prrime
            nt.RunID = RunID  # 0 : dispatcher ---  1..p : worker threads
            nt.TObject = self
            nt.alive = self.is_alive()
            nt.I_AmReady = False
            nt.InitTime = DT.datetime.now()
            nt.StartTime = None
            nt.ReadyTime = None
            nt.FinitTime = None
            nt.PauseCnt = 0  # counter for thread sleep phases
            nt.WhereItIs = 0
            #
            self.AllThreads.setdefault(tn, nt)
        PrimeBase.THL.release()
    #
    def _MakeName(self, Prime=0, RunID=0):
        return 'X_' + '{:02}'.format(Prime) + '_' + '{:02}'.format(RunID)
        # 'X_' to find the thread by name
    #
    def EmergencyStop():
        PrimeBase._StopSignal = True
        delay(3000)
        PrimeBase.THL.acquire()
        Z = [T for T in TH.enumerate() if T.getName().find('X_') == 0 and T.is_alive()]
        PrimeBase.THL.release()
        if len(Z) > 0:
            print('>>> stopping threads: ', end='', flush=True)
            while len(Z) > 0:
                T = Z.pop()
                print('\t', T.getName(), end='', flush=True)
                if T.is_alive():
                    pass  # T._stop()
            else:  # while
                print('\t <<<', flush=True)
    #
    def __str__(self):
        return self.getName()

#   --- Base finit

#   --- Dispatch start

class PrimeDispatch(PrimeBase):
    """
    holds the current prime and some common values for all worker child threads
    collects after running childs the new jumper list
    """
    #
    def __init__(self, Prime=0, RunID=0, JL=[]):
        if (Prime < 1) or (Prime > MAXPRIME) or (RunID != 0):
            raise InvalidPrimeThread  # out of range
        PrimeBase.__init__(self, Prime, RunID)
        PrimeBase.THL.acquire()
        if True:  # only for a good block visibility
            # PRIMES has still in values
            self._dist = product_Primes(PRIMES)   # distances of start points
            self._size = length_Jumps(PRIMES)     # length of input JumpList
            self._Jumpers = DQ([])                # alternatively use a bytearray
            self._Strikes = set([])               # numbers to be removed
            PRIMES.append(Prime)                  # set the next step of primes
            print(PRIMES, flush=True)
            # PRIMES changed for out values
            self.__maxx = product_Primes(PRIMES)  # size of frame inside  
            self.__outL = length_Jumps(PRIMES)    # assumed length of target list 
            self._OutList = OD([])
            # self.__OutList = DQ([])               # alternatively use a bytearray
            #
        PrimeBase.THL.release()
        if len(JL) > 0:
            self.AddJumpList(JL)     # get the first jumps and include create strikes
    #
    def __str__(self):
        t = PrimeBase.__str__(self)
        print(t, flush=True)
        print(self._Jumpers, flush=True)
        print(self._Strikes, flush=True)
        return t
    #   
    def __MakeStrikes(self):
        if (len(self._Jumpers) == 0):
            return
        if len(self._Jumpers) < min(PrimeBase.EarlyLimit, self._size):
            return
        # print('MS:', self._Jumpers, flush=True)
        self.THL.acquire()
        self._Strikes = set(ListOf_Strikes(self._Jumpers))
        self.THL.release()
    #
    def AddJumpList(self, JL=[]):
        if len(JL) == 0: return
        if len(self._Jumpers) + len(JL) > self._size:
            return
        if True:
            self.THL.acquire()
            self._Jumpers.extend(JL)
            self.THL.release()
        if len(self._Jumpers) >= self._size:
            self.__MakeStrikes()  # input jumpers complete we can create all strikers
        if len(self._Jumpers) <= 48:
            print('JL:', self._PR, self._ID, list(self._Jumpers), flush=True)
        else:
            print('JL:', self._PR, self._ID, list(self._Jumpers)[:21], '...', list(self._Jumpers)[-21:], flush=True)
    #
    def __InitWorkers(self):
        for i in range(self._PR):
            if PrimeBase._StopSignal: break
            tn = self._MakeName(self._PR, i+1)
            self._OutList.setdefault(tn , [])
            PrimeWorker(self._PR, i+1, self)
    #
    def __StartWorker(self, PR=0, ID=0):
        tn = self._MakeName(PR, ID)
        try:
            X = PrimeBase.AllThreads[tn]
            T = X.TObject
            if T.ident is None: T.start()
        except:
            print('problems starting thread: ', tn, flush=True)
    #
    def run(self):
        X = self.AllThreads[self.getName()]
        X.StartTime = DT.datetime.now()
        print('Thread started:', self._PR, flush=True)
        #
        while len(self._Jumpers) < min(PrimeBase.EarlyLimit, self._size):
            if PrimeBase._StopSignal: break
            print(self.getName(), 'wait for jumpers before init childs', flush=True)
            delay(self._PR); X.PauseCnt += 1
        self.__InitWorkers()  # create all sub threads to compute next jump list in partitions
        delay(10*self._PR)
        while len(self._Jumpers) < self._size:
            if PrimeBase._StopSignal: break
            print(self.getName(), 'wait for jumpers after init childs', flush=True)
            delay(self._PR); X.PauseCnt += 1
        for i in range(self._PR):
            if PrimeBase._StopSignal: break
            # print(self.getName(), 'start workers b', self._PR, i+1, flush=True)
            self.__StartWorker(self._PR, ID=i+1)
            delay(3)
        pNextJumps = 1
        pN = None
        np = 0
        zBreak = False
        # now let it run and wait for results
        while not zBreak:
            if PrimeBase._StopSignal: break
            zBreak = True
            PrimeBase.THL.acquire()
            print('get thread list', flush=True)
            ZZ = [Z for Z in PrimeBase.AllThreads.values() if Z.Prime == self._PR and Z.RunID > 0]
            PrimeBase.THL.release()
            for Z in ZZ:
                zBreak &= Z.I_AmReady
                print('$$: ', Z.Prime, Z.RunID, Z.I_AmReady, Z.WhereItIs, flush=True)
            # Korrektur für kleine Primzahlen, kurze Jumplisten zusammenziehen
            if zBreak and self._size < PrimeBase.EarlyLimit:
                tn1 = self._MakeName(self._PR, 1)
                for i in range(2, self._PR+1):
                    tni = self._MakeName(self._PR, i)
                    self._OutList[tn1].extend(self._OutList[tni])
                    self._OutList[tni].clear()
            # Startvorbereitungen für nächste Primzahl vorbereiten
            tn = self._MakeName(self._PR, 1)
            if len(self._OutList[tn]) > 0: np = nextPrime(self._OutList[tn])
            if (pN is None) and (1 < np <= MAXPRIME):
                print('create new thread: ', np, flush=True)
                pN = PrimeDispatch(np, 0)
            
            if pN: 
                for Z in ZZ:
                    if (Z.RunID == pNextJumps) and Z.I_AmReady: 
                        tn = self._MakeName(Z.Prime, Z.RunID)
                        print('working ...', self._PR, pNextJumps, '-->', np, flush=True)
                        pN.AddJumpList(self._OutList[tn])
                        pNextJumps += 1
            
            print('just before start ...done:', self._PR, pNextJumps-1, '-->', np, flush=True)
            if (pN is not None) and (pNextJumps > self._PR):
                print('start new thread: ', np, flush=True)
                pN.start()

        while True:
            if PrimeBase._StopSignal: break
            zi = 0; za = 0; zz = 0
            for Z in PrimeBase.AllThreads.values():
                if Z.Prime == self._PR and Z.RunID > 0:
                    if Z.InitTime is not None: zi += 1
                    if Z.StartTime is not None: za += 1
                    if Z.ReadyTime is not None: zz += 1
            if zi == 0: break
            if za == zz: break        
            delay(10*self._PR); X.PauseCnt += 1
        #
        X.FinitTime = DT.datetime.now()
        print(self.getName(), 'run finished', flush=True)
    
#   --- Dispatch finit

#   --- Worker start

class PrimeWorker(PrimeBase):
    """
    computes a part of new differnces called by dispatcher
    """
    #
    def __init__(self, Prime=0, RunID=0, PT=None):
        if (Prime < 1) or (RunID < 1) or (RunID > Prime) or (PT is None):
            raise InvalidPrimeThread  # this is somehwere not correct"
        PrimeBase.__init__(self, Prime, RunID)
        # self.__outList = DQ([])                # alternatively use a bytearray
        PrimeBase.THL.acquire()
        self.__PT = PT
        self.__finit = (RunID * PT._dist) + 1
        self.__start = self.__finit - PT._dist
        PrimeBase.THL.release()
    #
    def __str__(self):
        t = PrimeBase.__str__(self)
        return t
    #
    def run(self):
        X = self.AllThreads[self.getName()]
        X.StartTime = DT.datetime.now()
        #
        s_old = 0
        k = self.__start
        if k in self.__PT._Strikes:
            s_old = 2
        for s_lst in self.__PT._Jumpers:
            if PrimeBase._StopSignal: break
            X.WhereItIs += 1
            n = s_lst
            n += s_old
            k += s_lst
            if k in self.__PT._Strikes:
                s_old = s_lst
                continue
            s_old = 0
            # self.__outList.append(n)
            self.__PT._OutList[self.getName()].append(n)
        # print('!!: ', self.getName(), self._PR, self._ID, self.__start, self.__finit, self.__PT._OutList[self.getName()], flush= True)
        X.I_AmReady = True
        X.ReadyTime = DT.datetime.now()

#   --- Worker finit

#   --- main ---

PRIMES = [2]
JLX = [2] 
# PRIMES = [2,3]
# JLX = [4,2] 
# PRIMES = [2,3,5]
# JLX = [6,4,2,4,2,4,6,2]
print(PRIMES)
print(JLX)

print('... es geht los!', nextPrime(JLX), MAXPRIME)
X = PrimeDispatch(nextPrime(JLX),0)
X.AddJumpList(JLX)
# print(X)
X.start()
    

# rimeBase.EmergencyStop()

while True:
    M = max(PRIMES)
    if M >= MAXPRIME: break
    print(M, '\t', PRIMES, flush=True)
    showThreading(M)
    delay(5000)
#    c = input('Abbruch?')
#    if (c == "C"):
#        break
#    if (c != ""):
#        delay(1000)
#        continue
    
showThreading()
