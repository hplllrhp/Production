# -*- coding: utf-8 -*-
import re
import math
import copy
import numpy as np
from matplotlib import pyplot as plt
from sklearn import linear_model
from sklearn.neural_network import MLPRegressor

# =============================================================================
# Number of days of every month
# =============================================================================
Month = dict()
Month[1] = 31
Month[2] = 30
Month[3] = 31
Month[4] = 30
Month[5] = 31
Month[6] = 30
Month[7] = 31
Month[8] = 31
Month[9] = 30
Month[10] = 31
Month[11] = 30
Month[12] = 31

INPUT = './input_5flavors_cpu_7days.txt.'
TEST = './TestData_2015.2.20_2015.2.27.txt'
TRAIN = 'TrainData_2015.1.1_2015.2.19.txt'

H = 24
N = 7
TOTAL_FLAVOR = 15

global SamplePS
SampleVM = list()
global DimToBeOptimized
global HistoryTime_Begin
global PredictTime_Begin
global PredictTime_End
global FlavorNum

# =============================================================================
# physical server class definition
# =============================================================================
class PhysicalServer:
    
    def __init__(self, cpu, mem, sto):
        self.cpu = cpu
        self.rest_cpu = cpu
        self.mem = mem
        self.rest_mem = mem
        self.sto = sto
        self.rest_sto = sto
        self.vm = []
    
    def addVm(self, vm):
        self.vm.append(vm)
        self.rest_cpu -= vm.cpu
        self.rest_mem -= vm.mem
        self.rest_sto -= vm.sto
        
    def rmVm(self, num):
        self.rest_cpu += self.vm[num].cpu
        self.rest_mem += self.vm[num].mem
        self.rest_sto += self.vm[num].sto
        del self.vm[num]
        
    def state(self):
        print('Total CPU: ' + str(self.cpu) + '\n' +
              'Used CPU: ' + str(self.cpu - self.rest_cpu) + '\n' +
              'Rest CPU: ' + str(self.rest_cpu) +'\n')
        print('Total memory: ' + str(self.mem) + '\n' +
              'Used memory: ' + str(self.mem - self.rest_mem) + '\n' +
              'Rest memory: ' + str(self.rest_mem) + '\n')
        print('Total storage: ' + str(self.sto) + '\n' +
              'Used storage: ' + str(self.sto - self.rest_sto) + '\n' +
              'Rest storage: ' + str(self.rest_sto) + '\n')
        print('Total virtual machine: ' + str(len(self.vm)) + '\n' +
              'List: ')
        for i in range(len(self.vm)):
            print('  VM ' + str(i) + ': ')
            self.vm[i].state()
        print('\n')
        
   
# =============================================================================
# virtual machine class definition
# =============================================================================
class VirtualMachine:
    
    def __init__(self, num, cpu, mem):
        self.num = num
        self.cpu = cpu
        self.mem = mem
    
    def state(self):
        print('Flavor' + str(self.num) + ': \n'
              '    CPU: ' + str(self.cpu) + '\n' +
              '    Memory: ' + str(self.mem) + '\n')
        
        
# =============================================================================
# Convert time into value
# =============================================================================
def time2val(time):
    
    #yyyy = time[0:4]
    mm = time[5:7]
    dd = time[8:10]
    hh = time[11:13]
    
    # Convertion
    #yyyy *= 365 * 24
    mm = int(mm)
    dd = int(dd)
    hh = int(hh)
    
    # To value
    value = 0
    mm -= 1
    for i in range(0, mm):
        value += Month[i+1] * 24
    value += (dd-1) * 24 + hh
    
    return int(value / H)
        

# =============================================================================
# Read data from given txt
# =============================================================================
def readData():
    
    global SamplePS
    global SampleVM
    global DimToBeOptimized
    global HistoryTime_Begin
    global PredictTime_Begin
    global PredictTime_End
    global FlavorNum
    
    # Read input file
    nowBlock = 0
    FlavorNum = 0
    flavorList = []
    f = open(INPUT, 'r+', encoding='utf-8')
    for line in f:
        if line is not '\n':
            if nowBlock == 0:
                Space_1 = line.find(' ')
                Space_2 = line.find(' ', Space_1+1)
                CPU = int(line[0:Space_1])
                MEM = int(line[Space_1:Space_2])
                STO = int(line[Space_2:])
                SamplePS = PhysicalServer(CPU, MEM, STO)
                SamplePS.state()
                nowBlock += 1
            else:
                if nowBlock == 1:
                    FlavorNum = int(line)
                    for i in range(FlavorNum):
                        line = f.readline()
                        Space_1 = line.find(' ')
                        Space_2 = line.find(' ', Space_1+1)
                        Space_3 = line.find('\n', Space_2+1)
                        NUM = int(line[6:Space_1])
                        CPU = int(line[Space_1:Space_2])
                        MEM = int(line[Space_2:Space_3])
                        tempVM = VirtualMachine(NUM, CPU, MEM)
                        SampleVM.append(tempVM)
                        flavorList.append(NUM)
                        tempVM.state()
                    nowBlock += 1
                else:
                    if nowBlock == 2:
                        DimToBeOptimized = line.replace('\n', '')
                        print('The dimension to be optimized is: ' + DimToBeOptimized)
                        nowBlock += 1
                    else:
                        if nowBlock == 3:
                            PredictTime_Begin = line.replace('\n', '')
                            PredictTime_End = f.readline().replace('\n', '')
                            print('Predict time begin at: ' + PredictTime_Begin)
                            print('Predict time end at: ' + PredictTime_End)
                            print('\n')
            
    
    # Read the beginning time
    line = open(TRAIN, encoding='utf-8').readline()
    Space_1 = line.find('\t')
    Space_2 = line.find('\t', Space_1+1)
    HistoryTime_Begin = line[Space_2+1:].replace('\n', '')
    
    historyData = [[0]for i in range(TOTAL_FLAVOR)]
    for i in range(TOTAL_FLAVOR):
        for j in range(time2val(HistoryTime_Begin), time2val(PredictTime_Begin) - 1):
            historyData[i].append(0)
            
    futureData = [[0]for i in range(TOTAL_FLAVOR)]
    for i in range(TOTAL_FLAVOR):
        for j in range(time2val(PredictTime_Begin), time2val(PredictTime_End) - 1):
            futureData[i].append(0)
            
    # Read history data
    for line in open(TRAIN, encoding='utf-8'):
        Space_1 = line.find('\t')
        Space_2 = line.find('\t', Space_1+1)
        tempFlavor = int(line[Space_1+7:Space_2])
        tempTime = line[Space_2+1:].replace('\n', '')
        if tempTime is not None:
            value = time2val(tempTime)
            if tempFlavor <= TOTAL_FLAVOR:
                historyData[tempFlavor-1][value] += 1
            else:
                None
#                print('Flavor data error.\n')
#                print('Now flavor: ' + str(tempFlavor))
        else:
            print('Time data error.\n')
            
                
    # Print history data
    print('History data: ')
    print('Total diffs: ' + str(len(historyData[0])))
    for i in range(TOTAL_FLAVOR):
        print('Flavor' + str(i+1) + ': (Total: ' + str(sum(historyData[i])) + ')\n' + str(historyData[i]) + '\n')
        
    # Read test data
    for line in open(TEST, encoding='utf-8'):
        Space_1 = line.find('\t')
        Space_2 = line.find('\t', Space_1+1)
        tempFlavor = int(line[Space_1+7:Space_2])
        tempTime = line[Space_2+1:].replace('\n', '')
        if tempTime is not None:
            value = time2val(tempTime) - time2val(PredictTime_Begin) - 1
            if tempFlavor <= TOTAL_FLAVOR:
                futureData[tempFlavor-1][value] += 1
            else:
                None
#                print('Flavor data error.\n')
#                print('Now flavor: ' + str(tempFlavor))
        else:
            print('Time data error.\n')
            
                
    # Print history data
    print('Future data: ')
    print('Total diffs: ' + str(len(futureData[0])))
    for i in range(TOTAL_FLAVOR):
        print('Flavor' + str(i+1) + ': (Total: ' + str(sum(futureData[i])) + ')\n' + str(futureData[i]) + '\n')
#    plt.plot(historyData[2])
    return historyData, futureData

# =============================================================================
# 差分数据
# =============================================================================
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i-interval]
        diff.append(value)
    return diff

# =============================================================================
# Sigmoid变换
# =============================================================================
def sigmoid(value):
    
    return (1.0 / (1 + math.exp(-value)))

def listSigmoid(dataset):
    sig = list()
    for i in range(len(dataset)):
        if dataset[i] is not 0:
            value = sigmoid(dataset[i])
            sig.append(value)
        else:
            sig.append(0)
    return sig
 
# =============================================================================
# Sigmoid反变换
# =============================================================================
def asigmoid(value):
    return -math.log((1.0 / value) - 1)

def listAsigmoid(dataset):
    sig = list()
    for i in range(len(dataset)):
        if dataset[i] is not 0:
            value = asigmoid(dataset[i])
            sig.append(value)
        else:
            sig.append(0)
    return sig

# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':


    historyData, futureData = readData()
    
    # 以七天为单位加和
    historyData_copy = copy.deepcopy(historyData)
    for i in range(TOTAL_FLAVOR):
        for j in range(N-1, len(historyData[i])):
            historyData[i][j] = sum(historyData_copy[i][j-N+1:j])
    print('History data: ')
    print('Total diffs: ' + str(len(historyData[0])))
    for i in range(TOTAL_FLAVOR):
        print('Flavor' + str(i+1) + ': (Total: ' + str(sum(historyData[i])) + ')\n' + str(historyData[i]) + '\n')
        
    # 抽取特征矩阵
    x = [[]for i in range(TOTAL_FLAVOR)]
    y = [[]for i in range(TOTAL_FLAVOR)]
    for i in range(TOTAL_FLAVOR):
        for j in range(N-1, len(historyData[i])-N):
            x[i].append(historyData[i][j+1:j+N])
            y[i].append(historyData[i][j+N])
            
    # 高斯核局部加权
#    for i in range(TOTAL_FLAVOR):
#        for j in range(len(x[i])):
#            for k in range(len(x[i][j])):
#                p = 0.0046
#                w = math.exp(- math.pow(x[i][j][k] - x[i][j][-1], 2) / 2 * p)
#                x[i][j][k] = w * x[i][j][k]
                
# 追加
#    for i in range(TOTAL_FLAVOR):
#        for j in range(len(x[i])):
#            x[i][j].append(x[i][j][-1] * x[i][j][-1])
#            x[i][j].append(1)
#            for k in range(len(x[i][j])):
#                x[i][j].append(sigmoid(x[i][j][k]))
    
    # LSE拟合
    lse_clf = []
    for i in range(TOTAL_FLAVOR):
        lse_clf.append(linear_model.LinearRegression())
        lse_clf[i].fit(x[i][:], y[i][:])
        
    # Neural network拟合
    nn_clf = []
    for i in range(TOTAL_FLAVOR):
        nn_clf.append(MLPRegressor(solver='sgd',
                           alpha=1e-5,
                           hidden_layer_sizes=(2, 5),
                           random_state=0))
        nn_clf[i].fit(x[i][:], y[i][:])
        
    # 预测
    for i in range(TOTAL_FLAVOR):
        for j in range(N):
            historyData[i].append(lse_clf[i].predict(x[i][-1:])[0])
            x[i].append(historyData[i][-N:-1])
        
    for i in range(TOTAL_FLAVOR):
        print('Flavor' + str(i+1) + ':')
        print('Prediction: ' + str(historyData[i][-7]) + '\nActual: ' + str(y[i][-7]) + '\n')
        
    print(np.array(historyData))
    
#    MODE = 'score'
#    MODE = 'graphical'
    
#    for i in range(TOTAL_FLAVOR):
#        
#        if MODE is 'graphical':
#            y_predict.append(lse_clf[i].predict(x[i]))
#            plt.figure(i)
#            plt.plot(y_predict[i])
#            plt.plot(finalData[i][N-1:time_split])
#            
#        else:
#            sum_1 += math.pow((y_predict[i] - y[i][-t]), 2)
#            sum_2 += math.pow((y_predict[i]), 2)
#            sum_3 += math.pow(y[i][-t], 2)
#        
#    
#    score_1 = (1 - math.sqrt(sum_1 / FlavorNum) / (math.sqrt(sum_2 / FlavorNum) + math.sqrt(sum_3 / FlavorNum)))
#    print(score_1)
