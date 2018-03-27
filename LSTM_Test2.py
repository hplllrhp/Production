# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 11:19:32 2018

@author: Administrator
"""
import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print( 'file not exist: '+ file_path) 
        return None 
#导入存储在csv文件中的数据
#data_test = read_lines('LSTM_F1_150.csv')
#print(data_test)
        
dataframe = read_csv('LSTM_F1_150.csv',engine='python',header = 0)
dataset = dataframe.values
#print('dataframe',dataframe,'dataset',dataset)
#fig = plt.figure(facecolor='white')
#ax = fig.add_subplot(111)
#ax.plot(dataset, label='True Data')
#plt.show()

print(dataset[0][1])

# X is the number of passengers at a given time (t) and Y is the number of passengers at the next time (t + 1).
# convert an array of values into a dataset matrix
def create_dataset(dataset,look_back = 1):
    data_x, data_y = []
    for i in range(len(dataset) - look_back -1):
        a = dataset[i:(i+look_back),0]
        data_x.appen(a)
        data_y.appen(dataset[])
# fix random seed for reproducibility
numpy.random.seed(7)









