import time
from random import seed
from random import random
import math
import sys
sys.setrecursionlimit(10000)
# first and last options for the pivot of quicksort raise the needed recursion limit


def bubblesort(v):
    v = v.copy()
    for i in range(len(v)-1, 1, -1):
        for j in range(i):
            if v[j] > v[i]:
                v[j], v[i] = v[i], v[j]

    return v


def countsort(v):
    res = []
    fr = [0] * (max(v)+1) if v != [] else []
    for i in v:
        fr[i] += 1
    for i, n in enumerate(fr):
        if n > 0:
            while n > 0:
                res += [i]
                n -= 1
    return res


def merge(v1, v2):
    v = []
    i = j = 0
    while i < len(v1) and j < len(v2):
        if v1[i] < v2[j]:
            v.append(v1[i])
            i += 1
        else:
            v.append(v2[j])
            j += 1
    if i == len(v1):
        v += v2[j:]
    elif j == len(v2):
        v += v1[i:]
    return v


def mergesort(v):
    if len(v) < 2:
        return v
    return merge(mergesort(v[:len(v)//2]), mergesort(v[len(v)//2:]))


def radixsortMSD(v, start, base=10):
    newv = []
    if start == 0:
        for i in range(base):
            for n in v:
                if i == n % base:
                    newv.append(n)
        return newv
    for i in range(base):
        part = []
        for n in v:
            if i == (n // base ** start) % base:
                part.append(n)
        newv += radixsortMSD(part, start-1, base)
    return newv


def radixsortLSD(v, start, maxlen, base=10):
    newv = []
    if start == maxlen:
        for i in range(base):
            for n in v:
                if i == n % base:
                    newv.append(n)
        return newv
    for i in range(base):
        part = []
        for n in v:
            if i == (n // base ** start) % base:
                part.append(n)
        newv = merge(newv, radixsortLSD(part, start + 1, maxlen, base))
    return newv


def quicksort(v, select):
    if len(v) < 2:
        return v
    lt = []
    eq = []
    gt = []
    pivot = select(v)
    for n in v:
        if n != v[0]:
            break
    else:
        return v
    for n in v:
        if n < pivot:
            lt.append(n)
        elif n == pivot:
            eq.append(n)
        else:
            gt.append(n)
    lt = quicksort(lt, select)
    eq = quicksort(eq, select)
    gt = quicksort(gt, select)
    return lt + eq + gt


def median(v):
    if len(v) <= 5:
        return mergesort(v)[len(v)//2]
    subl = [mergesort(v[i:i+5]) for i in range(0, len(v), 5)]
    newmed = [sl[len(sl)//2] for sl in subl]
    return median(newmed)


def verify(v, res):
    if len(v) != len(res):
        return [False, f'Error: different lengths: v of length {len(v)} and res of length {len(res)}']
    v.sort()
    for i in range(len(v)):
        if v[i] != res[i]:
            return [False, f'Error: different values: {v[i]} and {res[i]} at position {i}']
    return [True]


def printResult(f, v, res, dur):
    start = time.time()
    sorted(v)
    dur2 = time.time() - start
    f.write(f'Result of sorting:\n{res}\n')
    ver = verify(v, res)
    f.write(f'Result is valid and took {dur} to finish, with a difference of {dur - dur2} to the "sorted" function\n\n' if ver[0] else str(ver[1]) + '\n')


seed(time.time())
try:
    tests = []
    sorts = []
    with open('input.txt', 'r') as f:
        # number of tests
        n = int(f.readline())
        tests = [[int(j) for j in f.readline().split()] for i in range(n)]
        # number of sorts
        s = int(f.readline())
        sorts = [f.readline().split() for i in range(s)]

    with open('output.txt', 'w') as f:
        for t in tests:
            v = [int(random() * t[0]) for i in range(t[1])]
            f.write(f'Initial list:\n{str(v)}\n\n')
            for s in sorts:
                start = 0  # to have it available in the larger scope
                res = []
                if s[0] == 'bubblesort':
                    f.write('Bubblesort:\n')
                    start = time.time()
                    res = bubblesort(v)
                elif s[0] == 'countsort':
                    f.write('Countsort:\n')
                    start = time.time()
                    res = countsort(v)
                elif s[0] == 'mergesort':
                    f.write('Mergesort:\n')
                    start = time.time()
                    res = mergesort(v)
                elif s[0] == 'radixsortMSD':
                    f.write('Radixsort MSD:\n')
                    maxim = max(v) if v != [] else 'err'
                    start = time.time()
                    if maxim == 'err':
                        res = []
                    else:
                        res = radixsortMSD(v, math.ceil(math.log(maxim, int(s[2]))) if maxim != 0 else 0, base=int(s[2]))\
                            if 'base' in s else radixsortMSD(v, math.ceil(math.log(maxim, 10)) if maxim != 0 else 0, base=10)
                elif s[0] == 'radixsortLSD':
                    f.write('Radixsort LSD:\n')
                    maxim = max(v) if v != [] else 'err'
                    start = time.time()
                    if maxim == 'err':
                        res = []
                    else:
                        res = radixsortLSD(v, 0, math.ceil(math.log(maxim, int(s[2]))) if maxim != 0 else 0, base=int(s[2]))\
                            if 'base' in s else radixsortLSD(v, 0, math.ceil(math.log(maxim, 10)) if maxim != 0 else 0, base=10)
                elif s[0] == 'quicksort':
                    f.write('Quicksort:\n')
                    start = time.time()
                    if s[1] == 'median':
                        res = quicksort(v, median)
                    elif s[1] == 'first':
                        res = quicksort(v, lambda x: x[0])
                    elif s[1] == 'last':
                        res = quicksort(v, lambda x: x[-1])
                    elif s[1] == 'middle':
                        res = quicksort(v, lambda x: x[len(x)//2])
                    elif s[1] == 'random':
                        res = quicksort(v, lambda x: x[round(random()*(len(x)-1))])
                    else:
                        raise Exception(f'Undefined quicksort parameter\n')
                else:
                    raise Exception(f'Undefined sort name in input file\n')
                dur = time.time() - start
                printResult(f, v, res, dur)
            f.write('--------------------------------------------------\n\n')
except Exception as e:
    with open('output.txt', 'w') as f:
        f.write(str(e))
