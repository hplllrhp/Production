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
a = [[1,2,3]]
b = 0.1
print(matrix_mul_single(a,b)) 
def abs_matrix(x):
    for i in range(len(x)):
        for j in range(len(x[0])):
            x[i][j] = abs(x[i][j])
    return x

def matrix_trans(matrix):
    return [[row[col] for row in matrix] for col in range(len(matrix[0]))]

length_flavor = 10
train_x = [1,2,3,4,5,6,7,8,9,10]
train_y = [2,4,6,8,10,12,14,16,18,20]
#for i in range(length_flavor):
#    train_y.append(int(2*random.random()))
# input variables  
alpha = 1
input_dim = 1 
hidden_dim = 8 
output_dim = 1 

# initialize neural network weights  
synapse_0 = random_creat_matrix(input_dim,hidden_dim) 
synapse_1 = random_creat_matrix(hidden_dim,output_dim) 
synapse_h = random_creat_matrix(hidden_dim,hidden_dim)  

synapse_0_update = creat_matrix(len(synapse_0),len(synapse_0[0]))  
synapse_1_update = creat_matrix(len(synapse_1),len(synapse_1[0]))  
synapse_h_update = creat_matrix(len(synapse_h),len(synapse_h[0])) 
count = 10
# training logic 
for j in range(1000):
    overallError = 0  
    layer_2_deltas = list()  
    layer_1_values = list()  
    layer_1_values.append([[0 for i in range(hidden_dim)]])
    for train_index in range(length_flavor):   
#        train_index = random.randint(0,length_flavor-1)
        x = [[train_x[train_index]]]
        y = [[train_y[train_index]]]
        
        layer_1 = sigmoid(matrix_add(matrixMul2(x,synapse_0),matrixMul2(layer_1_values[-1],synapse_h)))  
        layer_2 = sigmoid(matrixMul2(layer_1,synapse_1))
#        if(j % 100 == 0):
#            print("layer_1:" , str(layer_1))
#            print("synapse_1:" , str(synapse_1))
#            print('sig',matrixMul2(layer_1,synapse_1))
        layer_2_error = matrix_sub(sigmoid(y),sigmoid(layer_2))
        layer_2_deltas.append(matrix_mul(layer_2_error,sigmoid_output_to_derivative(layer_2)))  
#        if(count >= 0):
#            count = count - 1
#            print('x',x)
#            print('y',y)
#            print('layer_1',layer_1)
#            print('layer_2',layer_2)
#            print('layer_2_error',layer_2_error)
#            print('layer_2_deltas[-1][-1]',layer_2_deltas[-1][-1])
        overallError += abs(layer_2_error[0][0])  
        days = x
        z = layer_2[0][0]
        layer_1_values.append(copy.deepcopy(layer_1))
    future_layer_1_delta = [[0 for i in range(hidden_dim)]]
    for back_index in range(length_flavor-1,-1,-1):  
        x = [[train_x[back_index]]]
        layer_1 = layer_1_values[back_index]
        prev_layer_1 = layer_1_values[back_index - 1]
        layer_2_delta = layer_2_deltas[back_index]
#        layer_1_delta = matrix_mul((matrixMul2(future_layer_1_delta,matrix_trans(synapse_h)) + matrixMul2(layer_2_delta,matrix_trans(synapse_1))),sigmoid_output_to_derivative(layer_1))
        m1 = matrixMul2(future_layer_1_delta,matrix_trans(synapse_h))    
        m2 = matrixMul2(layer_2_delta,matrix_trans(synapse_1))
        m3 = sigmoid_output_to_derivative(layer_1)
        m4 = matrix_add(m1,m2)
        layer_1_delta = matrix_mul(m4,m3)
         
        synapse_1_update = matrix_add(synapse_1_update,matrixMul2(matrix_trans(layer_1),layer_2_delta))
        synapse_h_update = matrix_add(synapse_h_update,matrixMul2(matrix_trans(prev_layer_1),layer_1_delta))
        synapse_0_update = matrix_add(synapse_0_update,matrixMul2(matrix_trans(x),layer_1_delta))
        future_layer_1_delta = layer_1_delta
#        if(j % 100 == 0):
#            print('layer_2_delta',layer_2_delta)
    synapse_0 = matrix_add(synapse_0,matrix_mul_single(synapse_0_update,alpha))
    synapse_1 = matrix_add(synapse_1,matrix_mul_single(synapse_1_update,alpha))
    synapse_h = matrix_add(synapse_h,matrix_mul_single(synapse_h_update,alpha))
    synapse_0_update = creat_matrix(len(synapse_0),len(synapse_0[0]))  
    synapse_1_update = creat_matrix(len(synapse_1),len(synapse_1[0]))  
    synapse_h_update = creat_matrix(len(synapse_h),len(synapse_h[0])) 
    if(j % 100 == 0):
        print('j',j)
        print("Error:" , str(overallError))
        print('index:',str(train_index))
        print('days:',  str(days))
        print("True:" , str(y))   
        print("Pred:" , str(z))
        print( "------------" )
print(matrixMul2(layer_1,synapse_1))  


   
         

