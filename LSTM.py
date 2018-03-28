# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 23:24:32 2018

@author: Administrator
"""
#LSTM
import copy
import random
import math
import numpy as np

random.seed(0)

def sigmoid_np(x):  
    output = 1/(1+np.exp(-x))  
    return output  
print(sigmoid_np(np.array([1,2,3])))

def sigmoid_output_to_derivative_np(output):  
    return output*(1-output)  
print(sigmoid_output_to_derivative_np(np.array([1,2,3])))
# compute sigmoid nonlinearity  
def sigmoid(x): 
    output = []
    temp = 0
    for i in range(len(x[0])):
        temp = 1/(1+math.exp(-x[0][i])) 
        output.append(temp)
    return [output]  
print(sigmoid([[1,2,3]]))
# convert output of sigmoid function to its derivative  
def sigmoid_output_to_derivative(output):  
    lay_output = []
    temp = 0
    for i in range(len(output[0])):
        temp = output[0][i]*(1-output[0][i]) 
        lay_output.append(temp)
    return [lay_output]  
print(sigmoid_output_to_derivative([[1,2,3]]))
def matrixMul2(A, B):
    return [[sum(a * b for a, b in zip(a, b)) for b in zip(*B)] for a in A]
a = [[1]]
b = [[1,2,3]]
c = matrixMul2(a,b)
def creat_matrix(x,y,start=0,step=1):  
     N=[]  
     F=[]  
     for i in range(x):                  #等价于for(i=0,i<x,i++)  
         for j in range(y):              
             F.append(0)  
#             start += step  
         N.append(F)  
         F=[]  
     return N  
 
def random_creat_matrix(x,y,start=0,step=1):  
     N=[]  
     F=[]  
     for i in range(x):                  #等价于for(i=0,i<x,i++)  
         for j in range(y):              
             F.append(random.random())  
#             start += step  
         N.append(F)  
         F=[]  
     return N 

length_flavor = 50
train_x = [i for i in range(1,length_flavor+1)]
train_y = []
for i in range(length_flavor):
    train_y.append(int(2*random.random()))

int2binary = {}  
binary_dim = 8 
# input variables  
alpha = 0.1  
input_dim = 1 
hidden_dim = 16  
output_dim = 1 

# initialize neural network weights  
synapse_0 = random_creat_matrix(input_dim,hidden_dim) 
synapse_1 = random_creat_matrix(hidden_dim,output_dim) 
synapse_h = random_creat_matrix(hidden_dim,hidden_dim)  

synapse_0_update = creat_matrix(len(synapse_0),len(synapse_0[0]))  
synapse_1_update = creat_matrix(len(synapse_1),len(synapse_1[0]))  
synapse_h_update = creat_matrix(len(synapse_h),len(synapse_h[0])) 

# training logic  
for j in range(10):  
    overallError = 0  

    layer_2_deltas = list()  
    layer_1_values = list()  
    layer_1_values.append([0 for i in range(hidden_dim)])  
    
    overallError = 0  
    layer_2_deltas = list()  
    layer_1_values = list()  
    layer_1_values.append([0 for i in range(hidden_dim)])

    train_index = random.randint(0,length_flavor-1)
    print(train_index)
    x = [[train_x[train_index]]]
    y = [[train_y[train_index]]]
    
    layer_1 = sigmoid(matrixMul2(x,synapse_0) + matrixMul2([layer_1_values[-1]],synapse_h))  
    layer_2 = sigmoid(matrixMul2(layer_1,synapse_1))  
    
    layer_2_error = y - layer_2
    layer_2_deltas.append((layer_2_error)*sigmoid_output_to_derivative(layer_2))  
    overallError += abs(layer_2_error[0])  

a = [[1,2,3]]
b = [[2,1,3]]
print(a - b)

