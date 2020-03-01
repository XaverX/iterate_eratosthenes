# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 17:26:13 2019

@author: Berthold
"""


# import sys
import time as TI
import datetime as DT
import itertools as IT
import threading as TH
import operator as OP
import functools as FT


PRIMES = []
MAXPRIME = 17
# = ...,13,17,19,23,29,31,37,...
MAXCOUNT = 480 # 480, 5_760, 92_160, 1_658_880 
# = 1*2*4*6*10*12*16*18 products of all p-1
THREADS = {}


def timeDiff(TA, TZ=None):
    """
    show me how much time we take
    """
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA
    # print('-'.rjust(60, '-'), flush=True)


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


nextPrim = lambda L: 1 + L[0]


def product_Primes(P):
    return FT.reduce(OP.mul, P, 1)


def length_Jumps(P):
    return FT.reduce(OP.mul, [max(1, x-1) for x in P], 1)


class InvalidPrimeThread(Exception):
    pass


class Prime(TH.Thread):
    THL = TH.Lock()
#    __ID = 0  # this thread handles prime = ID
#    __NN = ""
#    __prdP = 0  # product of primes until ID
#    __lenI = 0  # assumed length of bytearray in+out
#    __lenO = 0
#    __posI = 0  # working position in bytearray
#    __posO = 0
#    __outX = 0
#    __JL_I = bytearray([])
#    __JL_O = []
#    __NX = None  # next thread object to fill up with jumpers
#    __break = False  # flag for emergency stop
#    __follower = False  # flag for created next prime object

    def __init__(self, ID=0):  # , JL=[]
        if (ID <= 0):
            raise InvalidPrimeThread  # "neither ID nor JL is correct"
        TH.Thread.__init__(self)
        #
        self.THL.acquire()
        if True:
            self.__ID = ID
            self.__NN = "X_" + format_int(self.__ID)
            self.setName(self.__NN)
            self.__lenI = length_Jumps(PRIMES)
            # self.__JL_I = bytearray(self.__lenI)
            self.__JL_I = bytearray([])
            PRIMES.append(self.__ID)
            self.__prdP = product_Primes(PRIMES)
            self.__lenO = length_Jumps(PRIMES)
            self.__JL_O = []
            self.__posI = 0  # working position in bytearray
            self.__posO = 0
            self.__outX = 0
            self.__NX = None  # next thread object to fill up with jumpers
            self.__break = False  # flag for emergency stop
            self.__follower = False  # flag for created next prime object
            THREADS.setdefault(self.__NN, [self, DT.datetime.now(), None, None])
        self.THL.release()
        # print(self.__ID, 'ii')
        # print(self)

    def setBreak(self):
        """
        set stop signal
        """
        self.__break = True
        
    def addList(self, L):
        """
        put a couple of values to input jumper list
        """
        if (len(L) == 0) or (self.__posI + len(L) > self.__lenI):
            return False
        self.THL.acquire()
        
        self.__JL_I.extend(bytearray(L))
        self.__posI += len(L)
        
#        for b in L:
#            self.__JL_I[self.__posI] = b
#            self.__posI += 1
        self.THL.release()
        return True
            
    def addValue(self, v):
        """
        put a single value to input jumper list
        """
        if v <= 0 or self.__posI >= self.__lenI:
            return False
        L = [v]
        return self.addList(L)

    def __str__(self):
        CRLF = "\n"
        s = "\r\n< " + format_int(self.__ID) + " >" + CRLF
        s += " : " + format_int(self.__prdP)
        s += " : " + format_int(len(self.__JL_I)) + " : " + format_int(self.__posI)
        s += " : " + format_int(len(self.__JL_O)) + " : " + format_int(self.__posO) + " : " + format_int(self.__outX) + CRLF
#        t = ""
#        for w in self.__JL_I:
#            if len(t) == 0:
#                t += "("
#            else:
#                t += ","
#            t += format_int(w)
#        if len(t) > 0:
#            t += ")"
#        s += t
#        t = ""
#        for w in self.__JL_O:
#            if len(t) == 0:
#                t += "("
#            else:
#                t += ","
#            t += format_int(w)
#        if len(t) > 0:
#            t += ")"
#        s += t
        return s

    def __gen_Strikes(self):
        """
        generate the multiples of current prime
        this are the numbers where successive jumpers will be summarized
        """
        t = 1
        yield t * self.__ID
        for i in range(self.__lenI):
            if self.__break:
                break
            while i >= self.__posI:
                if self.__break:
                    break
                print("\t\b\r", self.__ID, i, 'S sleeping ', end="\b\r", flush=True)
                TI.sleep(0.0166 * self.__ID)
            k = self.__JL_I[i]
            t += k
            yield t * self.__ID
            if t > self.__prdP:
                break

    def __setTimes(self, key, ST, ET):
        if key is None:
            return
        self.THL.acquire()
        Z = THREADS[key]
        T, iTime, sTime, eTime = Z
        # print("\n  <<<:", key, iTime, ":: S ", sTime, ">", ST, ":: E ", eTime, ">", ET, ":>>>  ")
        if ST is not None:
            sTime = ST
        if ET is not None:
            eTime = ET
        Z = [T, iTime, sTime, eTime]
        THREADS[key] = Z
        self.THL.release()

    def __sendJumpers(self):
        L = []
        #
        self.THL.acquire()
        L = self.__JL_O[self.__outX:self.__posO]
        # self.__JL_O.clear()
        self.THL.release()
        #
        self.__NX.addList(L)
        if self.__outX == 0:
            if self.__NX.__ID <= MAXPRIME:
                self.__NX.start()
        self.__outX += len(L)            
        L.clear()

    def __gen_Jumpers(self):
        self.__setTimes(self.__NN, DT.datetime.now(), None)
        S = self.__gen_Strikes()
        s = next(S)
        t = 1
        j = 0
        n = 0
        for k in range(self.__ID):
            for i in range(self.__lenI):
                while i >= self.__posI:
                    if self.__break:
                        break
                    print("\t\b\r", self.__ID, i, 'J sleeping ', end="\b\r", flush=True)
                    TI.sleep(0.0166)
                #
                j = n  # if last round met a striker > 0
                j += self.__JL_I[i]  # add the difference to jump
                t += self.__JL_I[i]
                TI.sleep(0.0000001)
                #
                if t == s:
                    n = j
                    s = next(S)
                    continue
                n = 0
                #
                self.THL.acquire()
                self.__JL_O.append(j)
                self.__posO += 1
                self.THL.release()
                #
                if not self.__follower:
                    self.__follower = True
                    self.__NX = Prime(ID=nextPrim([j]))
                    TI.sleep(0.2)
                    self.__sendJumpers()
                    TI.sleep(0.3)
                #
                if self.__posO % MAXCOUNT == 0:
                    self.__sendJumpers()
        else:
            self.__sendJumpers()
        TI.sleep(0.3)
        self.__setTimes(self.__NN, None, DT.datetime.now())
        # print(self)
        
    def getWhere(self):
        self.THL.acquire()
        return self.__JL_O[-1]
        self.THL.release()
    
    def run(self):
        self.__gen_Jumpers()


CC = TH.active_count()

PRIMES = []
print("PRIMES", PRIMES)

H = Prime(ID=1)
H.addList([1])
H.start()

QQ = "|/-\\"
qq = 0
while TH.active_count() > CC:
    qq += 1
    qq %= 4
    print(' \b\r'.ljust(240, ' '), flush=True, end="") 
    Prime.THL.acquire()
    t = " (" + format_int(TH.active_count()) + ") "
    for Z in THREADS.items():
        NN, ZZ = Z
        T, iTime, sTime, eTime = ZZ
        if eTime is not None:
            continue
        if sTime is None:
            continue
        # print(NN, end=" : ", flush=True)
        if t > "":
            t += ":  "
        t += "<" + NN + "> "
        # t += (NN + " (" + format_int(T.getWhere()) + ")")
    Prime.THL.release()
    print(' \b\r', DT.datetime.now(), " : ", QQ[qq], " : ", t, sep="", flush=True, end="") 
    TI.sleep(0.02)    
print()

#while TH.active_count() > CC:
#    print('-'.rjust(60, '-'), flush=True)
#    print(DT.datetime.now())
#    for T in TH.enumerate():
#        print(T.getName(), T.ident, T.name)
#    print()
#    TI.sleep(1)    

print()
print("PRIMES", PRIMES)

for Z in THREADS.items():
    NN, ZZ = Z
    T, iTime, sTime, eTime = ZZ
    print(NN)
    tDiff = eTime - sTime if eTime is not None and sTime is not None else ""
    print(iTime, " : ", sTime, " : ", eTime, " : ", tDiff)
