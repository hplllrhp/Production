# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 23:24:32 2018

@author: Administrator
"""
#LSTM
import copy
import random
import math

random.seed(0)
# compute sigmoid nonlinearity  
def sigmoid(x):  
    output = 1/(1+math.exp(-x))  
    return output   
# convert output of sigmoid function to its derivative  
def sigmoid_output_to_derivative(output):  
    return output*(1-output)  
def matrixMul2(A, B):
    return [[sum(a * b for a, b in zip(a, b)) for b in zip(*B)] for a in A]

int2binary = {}  
binary_dim = 8 

# input variables  
alpha = 0.1  
input_dim = 1 
hidden_dim = 8  
output_dim = 1 

# initialize neural network weights  
synapse_0 = random.random((input_dim,hidden_dim)) 
synapse_1 = random.random((hidden_dim,output_dim)) 
synapse_h = random.random((hidden_dim,hidden_dim))  

synapse_0_update = zeros_like(synapse_0)  
synapse_1_update = zeros_like(synapse_1)  
synapse_h_update = zeros_like(synapse_h) 












