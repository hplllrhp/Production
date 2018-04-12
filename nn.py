# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 22:01:39 2018

@author: Administrator
"""
import numpy as np
import random
# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))
    
# input dataset
#X = np.array([[0,0,1]])
    
# output dataset            
#y = np.array([[1]]).T

# seed random numbers to make calculation
# deterministic (just a good practice)
np.random.seed(1)

# initialize weights randomly with mean 0
syn0 = 2*np.random.random((1,1)) - 1
for j in range(100):
    x = np.array([[random.randint(4,45)*0.1]])
    y = 0.2*x
    for iter in range(1000):
        # forward propagation
        l0 = x
        l1 = nonlin(np.dot(l0,syn0))
    #    print('syn0','\n',syn0,'\n','np.dot(l0,syn0)',np.dot(l0,syn0),'\n','l1',l1,'\n')
        # how much did we miss?
        l1_error = y - l1
        # multiply how much we missed by the 
        # slope of the sigmoid at the values in l1
        l1_delta = l1_error * nonlin(l1,True)
    #    print('l1_error',l1_error,'\n','l1del',nonlin(l1,True),'\n','l1_delta',l1_delta,'\n')
        # update weights
        syn0 += np.dot(l0.T,l1_delta)
    #    print('np.dot',np.dot(l0.T,l1_delta),'\n','syn0','\n',syn0,'\n')
    if(j%10 == 0):
        print("Output After Training:----------------------")
        print('x',x,'y',y,'predict',l1)
        print(l1_error)

