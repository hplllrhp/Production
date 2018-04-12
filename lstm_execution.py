import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
from lstm_class_object import LSTMPopulation
import random
import math

class Array:
    """实现__getitem__，支持序列获取元素、Slice等特性"""

    def __init__(self, lst):
        self.__coll = lst

    def __repr__(self):
        """显示列表"""

        return '{!r}'.format(self.__coll)

    def __getitem__(self, key):
        """获取元素"""
        slice1, slice2 = key
        row1 = slice1.start
        row2 = slice1.stop
        col1 = slice2.start
        col2 = slice2.stop
        return [self.__coll[r][col1:col2] for r in range(row1, row2)]
#------进行了数据预处理----------------
def normalise(signal):
    mu = np.mean(signal)#对矩阵所有元素求均值
    variance = np.mean((signal - mu)**2)#求方差
    signal_normalised = (signal - mu)/(np.sqrt(variance + 1e-8))#归一化
    print('mu',mu,'variance',variance,'sp',np.sqrt(variance + 1e-8))
    return signal_normalised
#a = np.array([[1,2,3,4]])
#print(normalise(a)) 
def creat_zero_matrix(x,y,start=0,step=1):  
     N=[]  
     F=[]  
     for i in range(x):                  #等价于for(i=0,i<x,i++)  
         for j in range(y):              
             F.append(0)  
#             start += step  
         N.append(F)  
         F=[]  
     return N  
 
def creat_random_matrix(x,y,start=0,step=1):  
     N=[]  
     F=[]  
     for i in range(x):                  #等价于for(i=0,i<x,i++)  
         for j in range(y):              
             F.append(2*random.random()-1)  
#             start += step  
         N.append(F)  
         F=[]  
     return N
 
def matrix_divi_single(x,y):
    temp = creat_zero_matrix(len(x),len(x[0]))
    for i in range(len(x)):
        for j in range(len(x[0])):
            temp[i][j] = x[i][j] / y
    return temp

def matrix_trans(matrix):
    return [[row[col] for row in matrix] for col in range(len(matrix[0]))]


#------进行了数据预处理----------------
original_flavor_data = np.loadtxt(open("E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\origin_code\\draw_data.csv","rb"), delimiter=",", skiprows=0)  
flavor_1 = original_flavor_data[4]
#t_range = np.linspace(0,100,1000)#从0到100中间间隔为0.1
#原始数据为sin和cos的函数值相加
#train_df_roc_signal_unnormalised = np.sin(2*np.pi*300*t_range) + 0.5*np.sin(2*np.pi*t_range)
#train_df_roc_signal_unnormalised = np.random.rand(1000)
#train_df_roc_signal_unnormalised = np.array([i for i in range(0,151)]).T
#每个元素值加上约1.5
train_df_roc_signal_unnormalised = flavor_1
temp = train_df_roc_signal_unnormalised - min(train_df_roc_signal_unnormalised)
#每个元素值除约3.0
train_df_roc_signal = (temp)/max(temp)
plt.figure(1)
plt.plot(train_df_roc_signal[0:149])

seq_len = 7#队列长度72
input_size = 1#输入大小
hidden_size_a = 21#隐藏大小
output_size = 1#输出大小
learning_rate = 2e-3#学习率0.001
n, p = 0, 0#
np.random.seed(0)
#随机生成在标准正态分布附近的一个权值矩阵W_out
#W_out = np.random.randn(output_size, hidden_size_a) / np.sqrt(output_size)
W_out = matrix_divi_single(creat_random_matrix(output_size, hidden_size_a),math.sqrt(output_size))
lstm_a = LSTMPopulation(input_size, hidden_size_a)#将两个参数输入初始化LSTM模型
#signal = np.zeros((seq_len,1))
#target = np.zeros((seq_len,output_size))
#mW_out = np.zeros_like(W_out)
signal = creat_zero_matrix(seq_len,1)
target = creat_zero_matrix(seq_len,output_size)#72*1的矩阵
mW_out = creat_zero_matrix(len(W_out),len(W_out[0]))#mW
j=0
k=0
#循环训练
for i in range(500):
    #如何j+72+1大于train_df_roc_signal长度，则重置j和网络lstm_a
    if j+seq_len+output_size >= len(train_df_roc_signal):
        j=0
        lstm_a.reset_states()
    #signal第一列等于训练数据的j:j+seq_len
#    signal[:,0] = train_df_roc_signal[j:j+seq_len]
    for i in range(seq_len):
        signal[i][0] = train_df_roc_signal[i+j]
#    signal[:,0]  = train_df_roc_signal[j:j+seq_len]
    #target第一列等于训练数据的j+1:j+1+seq_len
    for i in range(seq_len):
         target[i][0] = train_df_roc_signal[j+1+i]
#    target[:,0] = train_df_roc_signal[j+1:j+1+seq_len]
    #对signal也就是训练数据的j:j+seq_len进行训练
    lstm_a.forward(signal)
    #获取隐藏层输出值
    lstm_a_hidden_out = lstm_a.get_hidden_output() 
    #输出值等于矩阵相乘
#    output = lstm_a_hidden_out.dot(W_out.T)
    output = lstm_a_hidden_out.dot(matrix_trans(W_out))
    #获取误差
    error = output - target
    #用误差点乘lstm_a_hidden_out得到dW_out
    dW_out = (error).T.dot(lstm_a_hidden_out) 
    #损失 = 输出减去目标的平方的平均值
    loss = np.mean(np.square(output - target))
    #dh_out = 误差点乘权值矩阵
    dh_out = (error).dot(W_out)
    #对dh_out进行反向传播
    lstm_a.backward(dh_out)
    #对lstm_a进行训练网络
    lstm_a.train_network(learning_rate)
#感觉下面的代码加不加都行，因为结果都一样
#    for param, dparam, mem in zip([W_out],
#                              [dW_out],
#                              [mW_out]):
#        mem += dparam * dparam
#        param += -learning_rate * dparam / np.sqrt(mem + 1e-8)
#    
    print (k, loss)
    k += 1
    j += 1

# Testing phase
for ll in range(1):
    #下标是400+ll*100
    index = 0
    #画图长度是240
    plot_len = 150
    #可能是间隔12
    next_vals = 14
    #创建矩阵
    sample_signal = np.zeros((plot_len,1))
    #sample_signal的第一列赋值为train_df_roc_signal的index:index+plot_len的值
    sample_signal[:,0] = train_df_roc_signal[index:index+plot_len]
    #画图的点比上面的多了next_vals
    sample_signal_plotting = train_df_roc_signal[index:index + plot_len + next_vals] 
    #把示例放进去训练
    dd = lstm_a.sample_network(sample_signal, W_out, next_vals)
    #得到示例的输出
    sampled_output = dd.dot(matrix_trans(W_out))
#    y_out = dd.dot(W_out.T)
#    sampled_output = 1.0 / (1.0 + np.exp(-y_out))

    plt.figure(2)
    #画出sampled_output
    plt.plot(sampled_output[:,0])
    plt.hold(True)
    #画出预测与真实值的对比图，红色是真实值
    plt.plot(sample_signal_plotting[:], 'r')
    plt.title('Prediction vs Actual Signal')
    
    #画出plot_len:plot_len+next_vals长度下预测真实对比图
    plt.figure(3)
    plt.plot(sampled_output[plot_len:plot_len+next_vals,0])
    plt.hold(True)
    plt.plot(sample_signal_plotting[plot_len:plot_len+next_vals], 'r')
    plt.title('Prediction Mode - Blue (Prediction), Red (Actual)')
    plt.hold(False)
    plt.show()
print('sum ori',sum(train_df_roc_signal_unnormalised),'sum sin',sum(train_df_roc_signal),'max',max(train_df_roc_signal_unnormalised),'sum predit[]',sum(sampled_output),'sum pridit-next',sum(sampled_output[150:150+next_vals,0]),sampled_output[150:150+next_vals,0])
print('mean ori',np.mean(train_df_roc_signal_unnormalised),'np.mean_signal',np.mean(train_df_roc_signal),'np.mean output',np.mean(sampled_output[0:150,0]))

