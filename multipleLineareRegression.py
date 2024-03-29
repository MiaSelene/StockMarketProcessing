#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 14:50:01 2019

@author: thausmann
"""
import numpy as np
import matplotlib.pyplot as plt



def MultipleLineareRegression(x,yhat,alpha,acc):
    """nimmt eine Liste aus Inputvektoren x und outputvektoren y und bestimmt die Lineare Transformation die mit dem lokal geringsten Fehler mue+Mx=y erfuellt"""
    new=[float('inf')]
    M=np.random.standard_normal((len(yhat[0]),len(x[0])))
    mue=[sum([vec[i] for vec in yhat])/len(yhat) for i in range(len(yhat[0]))] #errechnet Mittelwertsvektor
    yhat = np.subtract(yhat,mue) #normiert outputs so das ihr Durchschnitt=0
    while True:
        dM=np.zeros((len(yhat[0]),len(x[0]))) #initialisiert Fehlermatrix mit 0
        for vec,Target in zip(x,yhat):        #Schleife ueber alle Datenpunkte (x,y)
            y=np.array(np.dot(M,vec))         #errechnet Modeloutput aus x
            Error=np.array([np.subtract(Target,y)*2 for Element in vec]).transpose() #Matrix in den Dimensionen von M mit eintraegen 2(y_i-y_i^), kopiert fuer j=1,2,...,n
            Error=np.multiply(Error,[vec for Element in Target])                  # Multpliziere Matrix mit x_j so das die eintraege jetzt e_ij=2(y_i-y_i^)*x_j sind, die Ableitung der Fehlerfunktion fuer m_ij 
            dM=np.add(dM,Error)  #lokalen Fehler zur Fehlermatrix addieren
        M=np.add(M,dM*alpha/len(yhat))  #nach allen Daten das Modell um den Durchschnitt der lokalen Fehler mal alpha veraendern
        new.append(sum([(TargetE-yE)**2 for TargetE,yE in zip(Target,y)])) #letzten Fehler zum Graphen hinzufuegen
        
        if new[-1]<(10**(-acc)): #wenn der Fehler klein genug ist, abbrechen und Modell zurueckgeben
            print('Training finished after {0} iterations.'.format(len(new)))
            plt.plot(new[1:])
            plt.show()
            print('Returning Model y(x)=mue+Mx')
            return lambda x: np.dot(M,x)+mue
        elif ((new[-1]-new[-2])**2)<(10**(-2*acc)*alpha):
            print('no linear representation of Dataset. Stagnation')
            plt.plot(new[1:])
            plt.show()
            print('Returning Model y(x)=mue+Mx with Remaining Error {0}'.format(np.round(new[-1],2)))
            return lambda x: np.dot(M,x)+mue
