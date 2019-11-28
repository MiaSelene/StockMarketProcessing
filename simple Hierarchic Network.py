#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 12:48:45 2019

@author: thausmann
simple Hierarchic Network
"""
import numpy as np
def feed(ER,hir):
    v = ER
    a = 1 if hir[0]['v']>t else 0
    v *= (1-a)

    
current_state = next_state
next_state = compute_step(current_state)


class state():
    def __init__(self,layers):
        self.layers = layers
        self.layer_a = [np.zeros(layer) for layer in layers]
        self.layer_v = [np.zeros(layer) for layer in layers]
        self.param_p = [np.random.normal(layer1,layer2) for layer1,layer2 in zip(layers,layers[1:])]
        self.param_t = [np.random.normal(layer) for layer in layers]
    
    def compute_step(self):
        layer_a = []
        layer_v = []
        param_p = np.copy(self.param_p)
        param_t = np.copy(self.param_t)
        for layer_index in range(len(self.layers)-1):
            layer_v[layer_index+1] = np.dot(self.layer_a[layer_index] , self.p[layer_index])
            for index in range(self.layers[layer_index+1]):
                if layer_v[layer_index+1][index] > param_t[layer_index+1]:
                    layer_v[layer_index+1][index] = 0
                    layer_a[layer_index+1][index] = 1
                    #param_p[layer_index] increase the corresponding row by some small value times the activation of the last layer
                    param_t[layer_index+1][index] -= 0.01
                    