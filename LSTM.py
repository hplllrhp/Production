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












