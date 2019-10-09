#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:10:43 2019

@author: thausmann
OST has a problem in the sense that it takes very bad guesses just because it couldn't get optimal guesses.
I propose creating a modification which increases the worth of the later Items, according to the variance of the Data know so far 
"""
import numpy
import matplotlib.pyplot as plt

def OptimalStoppingTheorem(List):
    stop=int(len(List)/numpy.e)
    Estimate=max(List[:stop])
    for Entry in List[stop:]:
        if Entry>Estimate:
            return Entry
    return Entry


def avg(List):
    return sum(List)/len(List)

def SD(List):
    return numpy.sqrt(sum([numpy.square(x-avg(List)) for x in List])/len(List))

def SDDistance(List,Element):
    return (Element-avg(List))/SD(List)

def moddedOST(List):
    stop=int(len(List)/numpy.e)
    Estimate=max(List[:stop])
    for i in range(stop,len(List)):
        Entry=List[i]
        NeededSDD=SDDistance(List[:i],Estimate)*(1-(i-stop)/(len(List)-stop))
        if SDDistance(List[:i],Entry)>NeededSDD:
            return Entry
    print('geht das so?')
    return Entry

def StoppingAccuracy(Strat,length):
    Succ=0
    for i in range(1000):
        List=numpy.random.random(length)
        if Strat(List)==max(List):
            Succ+=1
    return Succ/i

List=np.random.random(int(numpy.e*100))

plt.plot(List)
Start=[avg(List) for i in range(100)]
plt.plot(Start+[max(List[:100]) for i in range(100,271)])
plt.plot(Start+[avg(List)+SD(List)*SDDistance(
        List[:i],
        max(List[:100]))
        *(1-(i-100)/170)
        for i in range(100,271)
        ])
plt.ylabel('DataX')
plt.xlabel('log n')

