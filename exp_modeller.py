#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:51:35 2019

@author: thausmann
"""
import numpy as np



def train_model(data):
    m1, m2 = train_exp(data),train_lin(data)
    best_model = compare_r2(m1,m2,data)
    return best_model
    
def train_exp(data):
    a = (data[-1]-data[0])/(np.exp(len(data)-1)-1)
    b = 1
    c = data[0] - a
    model = lambda a,b,c,x: a * np.exp(b*x) + c
    for i in range(1000000):
        da = 0
        db = 0
        dc = 0
        error=0
        for x in range(len(data)):
            error += (model(a,b,c,x)-data[x])**2
            dE = 2 * (model(a,b,c,x)-data[x])
            da += -np.exp(b*x)*dE
            db += -x*np.exp(b*x)*dE
            dc += -dE
        delta = np.multiply([da,db,dc],0.0001/len(data))
        a,b,c=np.add([a,b,c],delta)
        if i%100000==0:
            print(error/len(data))
    return lambda x: model(a,b,c,x)

def train_lin(data):
    pass


def compare_r2(model1,model2,data):
    pass

