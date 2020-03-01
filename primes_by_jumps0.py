# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 20:49:03 2019

@author: Berthold
"""


# import sys
import datetime as DT
import itertools as IT
import operator as OP
import functools as FT


#    SHOW_PROGRESS = True
SHOW_REMAINING = False
MAX_NUMBER = 10_000_000
MAX_PRIME = 19  # 11, 13, 17, 19, 23, 29, 31
P = []
#   P = [2]
#   P = [2, 3]
#   P = [2, 3, 5]
L = (1, )
#   L = (2, )
#   L = (4, 2)
#   L = (6, 4, 2, 4, 2, 4, 6, 2)
C = IT.count(start=len(P))
_ = next(C)


def timeDiff(TA, TZ=None):
    if TZ is None:
        TZ = DT.datetime.now()
    return TZ - TA
    print('-'.rjust(80, '-'), flush=True)


def next_Prim(L):
    return 1 + L[0]


def gen_Numbers(f, L):
    t = 1
    while True:
        for k in L:
            t += k
            yield t
            if (f <= 0):
                continue
            if (t >= f):
                return None


def gen_Strikes(L):
    p = next_Prim(L)
    t = 1
    yield t*p
    for k in L:
        t += k
        yield t*p


def gen_Jumpers(L):
    ta = 1
    tz = ta
    p = next_Prim(L)
    S = gen_Strikes(L)
    s = next(S)
#    ma = 0
#    mz = ma
    for i in range(p):
        for k in L:
            tz += k
#            if SHOW_PROGRESS:
#                mz = (tz >> 20)
#                if (mz > ma):
#                    print(f'\r{tz:15,}\r', end="", flush=True)
#                    ma = mz
            if tz == s:
                s = next(S)
                continue
            yield tz - ta
            ta = tz


print('\n')
T0 = DT.datetime.now()
print('-'.rjust(80, '-'), flush=True)
print(T0, '\n', flush=True)

while True:
    # break
    TA = DT.datetime.now()
    p = next_Prim(L)
    P.append(p)
    LCM = FT.reduce(OP.mul, P)
    print(f'{next(C)})  p:={p:02} -> P:=', P,
          f'   LCM:={LCM:,}',
          sep="", flush=True)

    L = tuple(j for j in gen_Jumpers(L))
    LEN = len(L)
    QUT = LEN / LCM

    print(f'\rL:=', L[0:min(8, len(L))],
          f'   LEN:={LEN:,}',
          f'   QUT:={QUT:4.6f}',
          sep="", flush=True)
    if SHOW_REMAINING:
        N = gen_Numbers(max(1000, 3*p*p), L)
        print(f"remaining E.-Sieve:  {list(n for n in N)}")

    print(f"{timeDiff(TA)}", flush=True)
    print('-'.rjust(20, '-'), flush=True)
    if p >= MAX_PRIME:
        break
print(f"used time P1 -> {timeDiff(T0)}", flush=True)

T1 = DT.datetime.now()
P1 = P
p = next_Prim(L)
P2 = [p for p in gen_Numbers(p*p, L)]
pp = P2.pop()
QQ = [p*p for p in P2]

CCC = len(P1) + len(P2)  # Anzahl gefundener Primzahlen
ZZZ = len(P1)  # gefunden plus Zahlen im Iterator erzeugt
VVV = 0  # Anzahl Divisionen
LLL = 0  # aktuelle Lauflänge
SUM = 0
NPR = 0
UUU = {}  # Lauflängen dictionary

X = gen_Numbers(0, L)
while True:
    x = next(X)
    ZZZ += 1
    if x < pp:
        continue
    prime_found = True
    LLL = 0
    for p, q in zip(P2, QQ):
        if q > x:
            break
        LLL += 1
        VVV += 1
        if x % p == 0:
            prime_found = False
            NPR += 1
            break
    UUU[LLL] = UUU.get(LLL, 0) + 1
    if prime_found:
        CCC += 1
        P2.append(x)
        QQ.append(x*x)
    if x > MAX_NUMBER:
        break
print(f"used time P2 -> {timeDiff(T1)}", flush=True)

K = sorted(UUU.keys())
for i, k in enumerate(K):
    v = UUU.get(k)
    SUM += k*v
    # print(f'{k:4}-->{v:7}  ', end="")
    # if (i + 1) % 5 == 0:
    #     print()

print(f"\n\r{CCC:12,}  {NPR:12,}  {ZZZ:12,}  {VVV:12,}  {SUM:12,}")
# print(P1 + P2)
print(f"over all used time -> {timeDiff(T0)}", flush=True)
print('-'.rjust(80, '-'), '\n', flush=True)

#    --------------------------------------------------------------------------------
#    2019-05-05 13:22:08.699101
#    1)  p:=02 -> P:=[2]   LCM:=2
#    L:=(2,)   LEN:=1   QUT:=0.500000
#    remaining E.-Sieve:  [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 219, 221, 223, 225, 227, 229, 231, 233, 235, 237, 239, 241, 243, 245, 247, 249, 251, 253, 255, 257, 259, 261, 263, 265, 267, 269, 271, 273, 275, 277, 279, 281, 283, 285, 287, 289, 291, 293, 295, 297, 299, 301, 303, 305, 307, 309, 311, 313, 315, 317, 319, 321, 323, 325, 327, 329, 331, 333, 335, 337, 339, 341, 343, 345, 347, 349, 351, 353, 355, 357, 359, 361, 363, 365, 367, 369, 371, 373, 375, 377, 379, 381, 383, 385, 387, 389, 391, 393, 395, 397, 399, 401, 403, 405, 407, 409, 411, 413, 415, 417, 419, 421, 423, 425, 427, 429, 431, 433, 435, 437, 439, 441, 443, 445, 447, 449, 451, 453, 455, 457, 459, 461, 463, 465, 467, 469, 471, 473, 475, 477, 479, 481, 483, 485, 487, 489, 491, 493, 495, 497, 499, 501, 503, 505, 507, 509, 511, 513, 515, 517, 519, 521, 523, 525, 527, 529, 531, 533, 535, 537, 539, 541, 543, 545, 547, 549, 551, 553, 555, 557, 559, 561, 563, 565, 567, 569, 571, 573, 575, 577, 579, 581, 583, 585, 587, 589, 591, 593, 595, 597, 599, 601, 603, 605, 607, 609, 611, 613, 615, 617, 619, 621, 623, 625, 627, 629, 631, 633, 635, 637, 639, 641, 643, 645, 647, 649, 651, 653, 655, 657, 659, 661, 663, 665, 667, 669, 671, 673, 675, 677, 679, 681, 683, 685, 687, 689, 691, 693, 695, 697, 699, 701, 703, 705, 707, 709, 711, 713, 715, 717, 719, 721, 723, 725, 727, 729, 731, 733, 735, 737, 739, 741, 743, 745, 747, 749, 751, 753, 755, 757, 759, 761, 763, 765, 767, 769, 771, 773, 775, 777, 779, 781, 783, 785, 787, 789, 791, 793, 795, 797, 799, 801, 803, 805, 807, 809, 811, 813, 815, 817, 819, 821, 823, 825, 827, 829, 831, 833, 835, 837, 839, 841, 843, 845, 847, 849, 851, 853, 855, 857, 859, 861, 863, 865, 867, 869, 871, 873, 875, 877, 879, 881, 883, 885, 887, 889, 891, 893, 895, 897, 899, 901, 903, 905, 907, 909, 911, 913, 915, 917, 919, 921, 923, 925, 927, 929, 931, 933, 935, 937, 939, 941, 943, 945, 947, 949, 951, 953, 955, 957, 959, 961, 963, 965, 967, 969, 971, 973, 975, 977, 979, 981, 983, 985, 987, 989, 991, 993, 995, 997, 999, 1001]
#    0:00:00
#    --------------------
#    2)  p:=03 -> P:=[2, 3]   LCM:=6
#    L:=(4, 2)   LEN:=2   QUT:=0.333333
#    remaining E.-Sieve:  [5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, 37, 41, 43, 47, 49, 53, 55, 59, 61, 65, 67, 71, 73, 77, 79, 83, 85, 89, 91, 95, 97, 101, 103, 107, 109, 113, 115, 119, 121, 125, 127, 131, 133, 137, 139, 143, 145, 149, 151, 155, 157, 161, 163, 167, 169, 173, 175, 179, 181, 185, 187, 191, 193, 197, 199, 203, 205, 209, 211, 215, 217, 221, 223, 227, 229, 233, 235, 239, 241, 245, 247, 251, 253, 257, 259, 263, 265, 269, 271, 275, 277, 281, 283, 287, 289, 293, 295, 299, 301, 305, 307, 311, 313, 317, 319, 323, 325, 329, 331, 335, 337, 341, 343, 347, 349, 353, 355, 359, 361, 365, 367, 371, 373, 377, 379, 383, 385, 389, 391, 395, 397, 401, 403, 407, 409, 413, 415, 419, 421, 425, 427, 431, 433, 437, 439, 443, 445, 449, 451, 455, 457, 461, 463, 467, 469, 473, 475, 479, 481, 485, 487, 491, 493, 497, 499, 503, 505, 509, 511, 515, 517, 521, 523, 527, 529, 533, 535, 539, 541, 545, 547, 551, 553, 557, 559, 563, 565, 569, 571, 575, 577, 581, 583, 587, 589, 593, 595, 599, 601, 605, 607, 611, 613, 617, 619, 623, 625, 629, 631, 635, 637, 641, 643, 647, 649, 653, 655, 659, 661, 665, 667, 671, 673, 677, 679, 683, 685, 689, 691, 695, 697, 701, 703, 707, 709, 713, 715, 719, 721, 725, 727, 731, 733, 737, 739, 743, 745, 749, 751, 755, 757, 761, 763, 767, 769, 773, 775, 779, 781, 785, 787, 791, 793, 797, 799, 803, 805, 809, 811, 815, 817, 821, 823, 827, 829, 833, 835, 839, 841, 845, 847, 851, 853, 857, 859, 863, 865, 869, 871, 875, 877, 881, 883, 887, 889, 893, 895, 899, 901, 905, 907, 911, 913, 917, 919, 923, 925, 929, 931, 935, 937, 941, 943, 947, 949, 953, 955, 959, 961, 965, 967, 971, 973, 977, 979, 983, 985, 989, 991, 995, 997, 1001]
#    0:00:00
#    --------------------
#    3)  p:=05 -> P:=[2, 3, 5]   LCM:=30
#    L:=(6, 4, 2, 4, 2, 4, 6, 2)   LEN:=8   QUT:=0.266667
#    remaining E.-Sieve:  [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49, 53, 59, 61, 67, 71, 73, 77, 79, 83, 89, 91, 97, 101, 103, 107, 109, 113, 119, 121, 127, 131, 133, 137, 139, 143, 149, 151, 157, 161, 163, 167, 169, 173, 179, 181, 187, 191, 193, 197, 199, 203, 209, 211, 217, 221, 223, 227, 229, 233, 239, 241, 247, 251, 253, 257, 259, 263, 269, 271, 277, 281, 283, 287, 289, 293, 299, 301, 307, 311, 313, 317, 319, 323, 329, 331, 337, 341, 343, 347, 349, 353, 359, 361, 367, 371, 373, 377, 379, 383, 389, 391, 397, 401, 403, 407, 409, 413, 419, 421, 427, 431, 433, 437, 439, 443, 449, 451, 457, 461, 463, 467, 469, 473, 479, 481, 487, 491, 493, 497, 499, 503, 509, 511, 517, 521, 523, 527, 529, 533, 539, 541, 547, 551, 553, 557, 559, 563, 569, 571, 577, 581, 583, 587, 589, 593, 599, 601, 607, 611, 613, 617, 619, 623, 629, 631, 637, 641, 643, 647, 649, 653, 659, 661, 667, 671, 673, 677, 679, 683, 689, 691, 697, 701, 703, 707, 709, 713, 719, 721, 727, 731, 733, 737, 739, 743, 749, 751, 757, 761, 763, 767, 769, 773, 779, 781, 787, 791, 793, 797, 799, 803, 809, 811, 817, 821, 823, 827, 829, 833, 839, 841, 847, 851, 853, 857, 859, 863, 869, 871, 877, 881, 883, 887, 889, 893, 899, 901, 907, 911, 913, 917, 919, 923, 929, 931, 937, 941, 943, 947, 949, 953, 959, 961, 967, 971, 973, 977, 979, 983, 989, 991, 997, 1001]
#    0:00:00
#    --------------------
#    4)  p:=07 -> P:=[2, 3, 5, 7]   LCM:=210
#    L:=(10, 2, 4, 2, 4, 6, 2, 6)   LEN:=48   QUT:=0.228571
#    remaining E.-Sieve:  [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 121, 127, 131, 137, 139, 143, 149, 151, 157, 163, 167, 169, 173, 179, 181, 187, 191, 193, 197, 199, 209, 211, 221, 223, 227, 229, 233, 239, 241, 247, 251, 253, 257, 263, 269, 271, 277, 281, 283, 289, 293, 299, 307, 311, 313, 317, 319, 323, 331, 337, 341, 347, 349, 353, 359, 361, 367, 373, 377, 379, 383, 389, 391, 397, 401, 403, 407, 409, 419, 421, 431, 433, 437, 439, 443, 449, 451, 457, 461, 463, 467, 473, 479, 481, 487, 491, 493, 499, 503, 509, 517, 521, 523, 527, 529, 533, 541, 547, 551, 557, 559, 563, 569, 571, 577, 583, 587, 589, 593, 599, 601, 607, 611, 613, 617, 619, 629, 631, 641, 643, 647, 649, 653, 659, 661, 667, 671, 673, 677, 683, 689, 691, 697, 701, 703, 709, 713, 719, 727, 731, 733, 737, 739, 743, 751, 757, 761, 767, 769, 773, 779, 781, 787, 793, 797, 799, 803, 809, 811, 817, 821, 823, 827, 829, 839, 841, 851, 853, 857, 859, 863, 869, 871, 877, 881, 883, 887, 893, 899, 901, 907, 911, 913, 919, 923, 929, 937, 941, 943, 947, 949, 953, 961, 967, 971, 977, 979, 983, 989, 991, 997, 1003]
#    0:00:00
#    --------------------
#    5)  p:=11 -> P:=[2, 3, 5, 7, 11]   LCM:=2,310
#    L:=(12, 4, 2, 4, 6, 2, 6, 4)   LEN:=480   QUT:=0.207792
#    remaining E.-Sieve:  [13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 169, 173, 179, 181, 191, 193, 197, 199, 211, 221, 223, 227, 229, 233, 239, 241, 247, 251, 257, 263, 269, 271, 277, 281, 283, 289, 293, 299, 307, 311, 313, 317, 323, 331, 337, 347, 349, 353, 359, 361, 367, 373, 377, 379, 383, 389, 391, 397, 401, 403, 409, 419, 421, 431, 433, 437, 439, 443, 449, 457, 461, 463, 467, 479, 481, 487, 491, 493, 499, 503, 509, 521, 523, 527, 529, 533, 541, 547, 551, 557, 559, 563, 569, 571, 577, 587, 589, 593, 599, 601, 607, 611, 613, 617, 619, 629, 631, 641, 643, 647, 653, 659, 661, 667, 673, 677, 683, 689, 691, 697, 701, 703, 709, 713, 719, 727, 731, 733, 739, 743, 751, 757, 761, 767, 769, 773, 779, 787, 793, 797, 799, 809, 811, 817, 821, 823, 827, 829, 839, 841, 851, 853, 857, 859, 863, 871, 877, 881, 883, 887, 893, 899, 901, 907, 911, 919, 923, 929, 937, 941, 943, 947, 949, 953, 961, 967, 971, 977, 983, 989, 991, 997, 1003]
#    0:00:00
#    --------------------
#    6)  p:=13 -> P:=[2, 3, 5, 7, 11, 13]   LCM:=30,030
#    L:=(16, 2, 4, 6, 2, 6, 4, 2)   LEN:=5,760   QUT:=0.191808
#    remaining E.-Sieve:  [17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 289, 293, 307, 311, 313, 317, 323, 331, 337, 347, 349, 353, 359, 361, 367, 373, 379, 383, 389, 391, 397, 401, 409, 419, 421, 431, 433, 437, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 493, 499, 503, 509, 521, 523, 527, 529, 541, 547, 551, 557, 563, 569, 571, 577, 587, 589, 593, 599, 601, 607, 613, 617, 619, 629, 631, 641, 643, 647, 653, 659, 661, 667, 673, 677, 683, 691, 697, 701, 703, 709, 713, 719, 727, 731, 733, 739, 743, 751, 757, 761, 769, 773, 779, 787, 797, 799, 809, 811, 817, 821, 823, 827, 829, 839, 841, 851, 853, 857, 859, 863, 877, 881, 883, 887, 893, 899, 901, 907, 911, 919, 929, 937, 941, 943, 947, 953, 961, 967, 971, 977, 983, 989, 991, 997, 1003]
#    0:00:00.015604
#    --------------------
#    7)  p:=17 -> P:=[2, 3, 5, 7, 11, 13, 17]   LCM:=510,510
#    L:=(18, 4, 6, 2, 6, 4, 2, 4)   LEN:=92,160   QUT:=0.180525
#    remaining E.-Sieve:  [19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 361, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 437, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 529, 541, 547, 551, 557, 563, 569, 571, 577, 587, 589, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 667, 673, 677, 683, 691, 701, 703, 709, 713, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 779, 787, 797, 809, 811, 817, 821, 823, 827, 829, 839, 841, 851, 853, 857, 859, 863, 877, 881, 883, 887, 893, 899, 907, 911, 919, 929, 937, 941, 943, 947, 953, 961, 967, 971, 977, 983, 989, 991, 997, 1007]
#    0:00:00.015643
#    --------------------
#    8)  p:=19 -> P:=[2, 3, 5, 7, 11, 13, 17, 19]   LCM:=9,699,690
#    L:=(22, 6, 2, 6, 4, 2, 4, 6)   LEN:=1,658,880   QUT:=0.171024
#    remaining E.-Sieve:  [23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 529, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 667, 673, 677, 683, 691, 701, 709, 713, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 841, 851, 853, 857, 859, 863, 877, 881, 883, 887, 899, 907, 911, 919, 929, 937, 941, 943, 947, 953, 961, 967, 971, 977, 983, 989, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1073, 1081, 1087]
#    0:00:00.265541
#    --------------------
#    9)  p:=23 -> P:=[2, 3, 5, 7, 11, 13, 17, 19, 23]   LCM:=223,092,870
#    L:=(28, 2, 6, 4, 2, 4, 6, 6)   LEN:=36,495,360   QUT:=0.163588
#    remaining E.-Sieve:  [29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 841, 853, 857, 859, 863, 877, 881, 883, 887, 899, 907, 911, 919, 929, 937, 941, 947, 953, 961, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1073, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1147, 1151, 1153, 1163, 1171, 1181, 1187, 1189, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1247, 1249, 1259, 1271, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1333, 1361, 1363, 1367, 1369, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1457, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1517, 1523, 1531, 1537, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1591]
#    0:00:05.556797
#    --------------------
#    10)  p:=29 -> P:=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]   LCM:=6,469,693,230
#    L:=(30, 6, 4, 2, 4, 6, 6, 2)   LEN:=1,021,870,080   QUT:=0.157947
#    remaining E.-Sieve:  [31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 961, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1147, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1271, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1333, 1361, 1367, 1369, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1457, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1517, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1591, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1643, 1657, 1663, 1667, 1669, 1681, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1739, 1741, 1747, 1753, 1759, 1763, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1829, 1831, 1847, 1849, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1891, 1901, 1907, 1913, 1927, 1931, 1933, 1949, 1951, 1961, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2021, 2027, 2029, 2039, 2053, 2063, 2069, 2077, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2173, 2179, 2183, 2201, 2203, 2207, 2209, 2213, 2221, 2237, 2239, 2243, 2251, 2257, 2263, 2267, 2269, 2273, 2279, 2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2419, 2423, 2437, 2441, 2447, 2449, 2459, 2467, 2473, 2477, 2479, 2491, 2501, 2503, 2521, 2531]
#    0:04:06.939166
#    --------------------
#    over all used time -> 0:04:12.792751
#    --------------------------------------------------------------------------------
