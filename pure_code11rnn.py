# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 22:01:39 2018

@author: Administrator
"""
import numpy as np
import random
import math
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
a = [[1.5]]
b = [[1,2.5,3.5]]
c = matrixMul2(a,b)
print(c)
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
             F.append(2*random.random()-1)  
#             start += step  
         N.append(F)  
         F=[]  
     return N 
def matrix_add(x,y):
    temp = creat_matrix(len(x),len(x[0]))
    for i in range(len(x)):
        for j in range(len(x[0])):
            temp[i][j] = x[i][j] + y[i][j]
    return temp

def matrix_sub(x,y):
    temp = creat_matrix(len(x),len(x[0]))
    for i in range(len(x)):
        for j in range(len(x[0])):
            temp[i][j] = x[i][j] - y[i][j]
    return temp

def matrix_mul(x,y):
    temp = creat_matrix(len(x),len(x[0]))
    for i in range(len(x)):
        for j in range(len(x[0])):
            temp[i][j] = x[i][j] * y[i][j]
    return temp

def matrix_mul_single(x,y):
    temp = creat_matrix(len(x),len(x[0]))
    for i in range(len(x)):
        for j in range(len(x[0])):
            temp[i][j] = x[i][j] * y
    return temp
#a = [[1,2,3]]
#b = 0.1
#print(matrix_mul_single(a,b)) 
def abs_matrix(x):
    for i in range(len(x)):
        for j in range(len(x[0])):
            x[i][j] = abs(x[i][j])
    return x

def matrix_trans(matrix):
    return [[row[col] for row in matrix] for col in range(len(matrix[0]))]


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
random.seed(1)

# initialize weights randomly with mean 0
#syn0 = 2*np.random.random((1,1)) - 1
syn0 = random_creat_matrix(3,6)
syn1 = random_creat_matrix(6,3)
for j in range(1):
#    random_x = random.randint(4,45)*0.1
    x = [[1,2,3]]
    y = [[0.1,0.2,0.3]]
    for iter in range(1000):
        # forward propagation
        l0 = x
#        l1 = nonlin(np.dot(l0,syn0))
        l1 = sigmoid(matrixMul2(l0,syn0))
        l2 = sigmoid(matrixMul2(l1,syn1))
    #    print('syn0','\n',syn0,'\n','np.dot(l0,syn0)',np.dot(l0,syn0),'\n','l1',l1,'\n')
        # how much did we miss?
        l2_error = matrix_sub(y,l2)
        l2_delta = matrix_mul(l2_error,sigmoid_output_to_derivative(l2))
        
        l1_error = matrixMul2(l2_delta,matrix_trans(syn1))
        # multiply how much we missed by the 
        # slope of the sigmoid at the values in l1
        l1_delta = matrix_mul(l1_error,sigmoid_output_to_derivative(l1))
    #    print('l1_error',l1_error,'\n','l1del',nonlin(l1,True),'\n','l1_delta',l1_delta,'\n')
        # update weights
        syn0 = matrix_add(syn0,matrixMul2(matrix_trans(l0),l1_delta))
        syn1 = matrix_add(syn1,matrixMul2(matrix_trans(l1),l2_delta))
    #    print('np.dot',np.dot(l0.T,l1_delta),'\n','syn0','\n',syn0,'\n')
    if(j%10 == 0):
        print("Output After Training:----------------------")
        print('x',x,'y',y,'predict',l2)
sigmoid(matrixMul2([[2,3,4]],syn1))   

