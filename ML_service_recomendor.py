#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 10:10:14 2019

@author: thausmann
ML AWS Service recomendation algorithm
"""
import numpy as np
import matplotlib.pyplot as plt

def char_to_onehot(char):
    """changed functionality to reduce input size"""
    possible_chars = "mlesg" #" aeioubcdfghjklmnpqrstvwxyz"
    onehot = np.zeros(len(possible_chars))
    for i in range(len(possible_chars)):
        if char.lower() == possible_chars[i]:
            
            onehot[i] = 1
            break
    return onehot

def word_to_vector(word):
    vector = np.array([])
    for char in word:
        vector = np.append(vector,char_to_onehot(char))
    return vector

def E(x,y):
    error = 0
    for xi,yi in zip(x,y):
        xi += 10**(-8)
        if xi > 1:
            xi -= 10**(-7)
        error -= np.log((xi)) * (yi) + np.log(1-xi) * (1 - yi)
    return error

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def softmax_P(x):
    y = softmax(x)
    return np.subtract(y,np.square(y))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_P(x):
    omega = sigmoid(x)
    return omega * (1-omega)

def ReLU_P(x):
    return np.where(x > 0, 1,  0.01)

def M(x,params,hist=False):
    a_l=[np.copy(x)]
    for layer in params:
        x = (np.dot(x, layer))
        x = np.where(x > 0, x, x * 0.01)
        a_l.append(np.copy(x))
    if hist:
        return a_l
    return softmax(x)

def vector_to_word(vec):
    possible_chars = "mlesg" #" aeioubcdfghjklmnpqrstvwxyz"
    word = ''
    single_char_space = len(char_to_onehot('a'))
    char_vecs = [vec[i:i+single_char_space] for i in range(0,len(vec),single_char_space)]
    for char_vec in char_vecs:
        word = word + possible_chars[np.argmax(char_vec)]
    return word

def backprop(p_l,a_l,y):
    layers = len(a_l)
    out = softmax(a_l[-1])
    out[out<=0] = out[out<=0]+0.001
    out[out>=1] = out[out>=1]-0.001
    dE_dM = -1/(out) * (y) -1/(1-out) * (1-y)
    dM_da = softmax_P(a_l[-1])
    dp = [0 for layer in range(layers-1)]
    k = dE_dM * dM_da
    for layer in range(layers-2,-1,-1):
        k = k * ReLU_P(np.dot(a_l[layer],p_l[layer]))
        dz_dp = np.column_stack(np.array([k * ai for ai in a_l[layer]])) #this line might be wrong
        dp[layer] = dz_dp
        k = np.dot(p_l[layer],k)
    return dp
    
def T(m):
    return [i.transpose() for i in m]

def train(Points,labels):
    x = np.append(np.square(Points),Points,axis=1)
    Error = []
    alpha = 0.001
    interface_length = len(x[0])
    layer_sizes = [interface_length,16,256,16,2]
    params = np.array([np.random.normal(size=(size1,size2)) for size1,size2 in zip(layer_sizes,layer_sizes[1:])])
    i = 0 
    while len(Error)<2 or Error[-1] > 100:
        if len(Error)>2 and (Error[-1]-Error[-2])**2 < 10**(-6):
            print('stagnating. Taking step')
            for p in range(len(params)):
                params[p] += dp[p] * alpha/len(x)*10
        Error.append(0)
        dp = [np.zeros(params[layer].shape) for layer in range(len(params))]
        for xi,yi in zip(x,labels):
            Error[-1] += E(M(xi,params),yi)
            dp = np.add(dp, T(backprop(params,M(xi,params,hist=True),np.array(yi))))
        for p in range(len(params)):
            params[p] += dp[p] * alpha/len(x)
        i += 1 
        if i%100==0:
            print(Error[-1])
            yield lambda x: M(x,params)[0]
    plt.plot([2*x/(len(Error))-1 for x in range(len(Error))],[2*y/max(Error)-1 for y in Error])
    plt.show()
    print(f'final average error: {Error[-1]/len(Points)} (represents {((Error[0]-Error[-1])/Error[0]*100).__round__(2)}% decrease compared to Initial Error)')
    #return lambda x: M(x,params)[0]
