# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:52:26 2018

@author: Administrator
"""
#注意两台电脑的文件的路径不一样，所以需要注意区分
#inputFilePath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\input_data.txt'
#ecsDataPath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\train_data.txt'
#resultFilePath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\output_data.txt'

#用来更方便精心观察变量调试使用
import sys
import os

def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\n" % item)

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
    

def cal_mean(readings):
    """
    Function to calculate the mean value of the input readings
    :param readings:
    :return:
    """
    readings_total = sum(readings)
    number_of_readings = len(readings)
    mean = readings_total / float(number_of_readings)
    return mean


def cal_variance(readings):
    """
    Calculating the variance of the readings
    :param readings:
    :return:
    """

    # To calculate the variance we need the mean value
    # Calculating the mean value from the cal_mean function
    readings_mean = cal_mean(readings)
    # mean difference squared readings
    mean_difference_squared_readings = [pow((reading - readings_mean), 2) for reading in readings]
    variance = sum(mean_difference_squared_readings)
    return variance / float(len(readings) - 1)


def cal_covariance(readings_1, readings_2):
    """
    Calculate the covariance between two different list of readings
    :param readings_1:
    :param readings_2:
    :return:
    """
    readings_1_mean = cal_mean(readings_1)
    readings_2_mean = cal_mean(readings_2)
    readings_size = len(readings_1)
    covariance = 0.0
    for i in range(readings_size):
        covariance += (readings_1[i] - readings_1_mean) * (readings_2[i] - readings_2_mean)
    return covariance / float(readings_size - 1)


def cal_simple_linear_regression_coefficients(x_readings, y_readings):
    """
    Calculating the simple linear regression coefficients (B0, B1)
    :param x_readings:
    :param y_readings:
    :return:
    """
    # Coefficient B1 = covariance of x_readings and y_readings divided by variance of x_readings
    # Directly calling the implemented covariance and the variance functions
    # To calculate the coefficient B1
    b1 = cal_covariance(x_readings, y_readings) / float(cal_variance(x_readings))

    # Coefficient B0 = mean of y_readings - ( B1 * the mean of the x_readings )
    b0 = cal_mean(y_readings) - (b1 * cal_mean(x_readings))
    return b0, b1


def predict_target_value(x, b0, b1):
    """
    Calculating the target (y) value using the input x and the coefficients b0, b1
    :param x:
    :param b0:
    :param b1:
    :return:
    """
    return b0 + b1 * x


def cal_rmse(actual_readings, predicted_readings):
    """
    Calculating the root mean square error
    :param actual_readings:
    :param predicted_readings:
    :return:
    """
    square_error_total = 0.0
    total_readings = len(actual_readings)
    for i in xrange(0, total_readings):
        error = predicted_readings[i] - actual_readings[i]
        square_error_total += pow(error, 2)
    rmse = square_error_total / float(total_readings)
    return rmse


def simple_linear_regression(dataset):
    """
    Implementing the simple linear regression without using any python library
    :param dataset:
    :return:
    """

    # Get the dataset header names
    # Calculating the mean of the square feet and the price readings
    data_date_predict = [[0 for i in range(51,58)] for i in range(len(dataset)+1)]
    data_date_predict[0][:] = range(51,58)
    for i in range(len(dataset)):
        square_feet_mean = cal_mean(range(1,50))
        price_mean = cal_mean(dataset[i][1:50])
        square_feet_variance = cal_variance(range(1,50))
#        price_variance = cal_variance(dataset[i][1:50])
        
        # Calculating the regression
        covariance_of_price_and_square_feet = cal_covariance(range(1,50),dataset[0][1:50])
        w1 = covariance_of_price_and_square_feet / float(square_feet_variance)
    
        w0 = price_mean - (w1 * square_feet_mean)
    
        # Predictions
        for j in range(len(data_date_predict[0][:])):
            data_date_predict[i+1][j] = w0 + w1 * data_date_predict[0][j]
            if data_date_predict[i+1][j]<0:
               data_date_predict[i+1][j] = 0
    return data_date_predict
class flavor_property:
    def __init__(self):
        self.name = []          # 虚拟机类型
        self.total = predicted_data          # 
        self.rest = predicted_data
        self.cpu = []      # property[0]:cpu
        self.memory = []
        self.SingleVmFlag = []   #放置开关
class server_property:
    def __init__(self):
        self.cpu = [int(server_info[0])]     # property[0]:cpu
        self.memory = [int(server_info[0])]
        self.flavor = [[0 for i in range(5)] for i in range(1)]        # flavor[0]表示要放的第1种虚拟机的台数，这里用下标直接代替了虚拟机种类，很明显可以flavor.resize(InputNum)
        self.ser_name = ['server']

def get_server_property(inputFilePath):
    server_file_array = read_lines(inputFilePath)
    temp_list = server_file_array[0].split()
    return temp_list

def get_flavor_property(inputFilePath):
    flavor_file_array = read_lines(inputFilePath)
    for line in flavor_file_array:
        if 'flavor' in line:
            temp = line.split()
            temp_list = list(temp)
            flavor_property.name.append(temp_list[0])
            flavor_property.cpu.append(int(temp_list[1]))
            flavor_property.memory.append(int(int(temp_list[2])/1024))
            flavor_property.SingleVmFlag.append(1)
    return flavor_property

#print(server_property.property)
#--------------------放置函数开始----------------------
def JudgeRest(InputNum,ToSerNum):
    flag = 0
    for i in range(InputNum):
        if(flavor_property.rest[i] != 0 and flavor_property.SingleVmFlag[i] != 0):
            if(server_property.cpu[ToSerNum] >= flavor_property.cpu[i] and server_property.memory[ToSerNum] >= flavor_property.memory[i]):
               flag = 1
               break
    return flag

def SelectFlavorToSet(InputNum,i):
    fn = 0
    size = 0
    a = []    #//存储还没分配完的虚拟机的类型标号，后续就是在这里面筛选
    for j in range(InputNum):
        if(flavor_property.rest[j] != 0 and flavor_property.SingleVmFlag[j] != 0):
            a.append(j)
    size = len(a)
    fn = a[0]
    for k in range(1,size):
        if(i == 0):
            if(flavor_property.cpu[a[k]] > flavor_property.cpu[fn]):
                fn = a[k]
            elif(flavor_property.cpu[a[k]] < flavor_property.cpu[fn]):
                fn = fn
            else:
                if(flavor_property.memory[a[k]] > flavor_property.memory[fn]):
                    fn = a[k]
                else:
                    fn = fn
        else:
            if(flavor_property.memory[a[k]] > flavor_property.memory[fn]):
                fn = a[k]
            elif(flavor_property.memory[a[k]] < flavor_property.memory[fn]):
                fn = fn
            else:
                if(flavor_property.cpu[a[k]] > flavor_property.cpu[fn]):
                    fn = a[k]
                else:
                    fn = fn
    return fn

def Judge(InputNum):
    flag = 1
    num = 0
    for i in range(InputNum):
        if(flavor_property.rest[i] == 0):
            num += 1
    if(num == InputNum):
        flag = 0
    return flag
        
# Do your work from here#
to_predict_list = []
date_flag = 1
inputFilePath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\input_data.txt'
ecsDataPath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\train_data.txt'
resultFilePath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\output_data.txt'
ecs_lines = read_lines(ecsDataPath)
input_lines = read_lines(inputFilePath)
    

flavor_property = flavor_property()
server_property = server_property()
server_info = get_server_property(inputFilePath)
flavor_property = get_flavor_property(inputFilePath)
date_table = [[0 for i in range(51)] for i in range(len(flavor_property.name))]
for i in range(len(flavor_property.name)):
    date_table[i][0] = flavor_property.name[i]  
for line1 in ecs_lines: 
        odom1 = line1.split() 
        Train_list2 = list(odom1)
        for i in range(len(flavor_property.name)):
            if flavor_property.name[i] in Train_list2: 
                if Train_list2[2][5:7] == '01':
                    date_flag = int(Train_list2[2][8:10])
                if Train_list2[2][5:7] == '02':
                    date_flag = int(Train_list2[2][8:10]) + 31
                date_table[i][date_flag] += 1                 
data_date_predict = simple_linear_regression(date_table)
predicted_data = []#存放最后的预测结果
for i in range(1,len(data_date_predict)):
    predicted_data.append(sum(data_date_predict[i][:]))
for count in range(len(predicted_data)):#将预测结果圆整，只要数据大于整数部分就加一
    predicted_data[count] = int(predicted_data[count])+1
print(predicted_data)
OptimizeFlag = 0
server_property.ser_num = 0
judge_flag = Judge(len(flavor_property.name))
ToSerNum = 0;#//设置需要配置的服务器，ToSerNum = 0即第1个服务器
fn = 0 #//当前放置优先级最高的虚拟机种类
InputNum = len(flavor_property.name)
while (judge_flag):
    flag = 1#//设置能否配置的标志位，因为是还未配置的虚拟机，所以一开始是可以配置的
    server_property.flavor[ToSerNum][:] = [0 for i in range(5)]
    while(flag):
        fn = SelectFlavorToSet(InputNum,OptimizeFlag)
        for i in range(flavor_property.rest[fn]):
            if(flavor_property.cpu[fn] <= server_property.cpu[ToSerNum] and flavor_property.memory[fn] <= server_property.memory[ToSerNum]):
                server_property.flavor[ToSerNum][fn] += 1
                flavor_property.rest[fn] -= 1
                server_property.cpu[ToSerNum] -= flavor_property.cpu[fn]
                server_property.memory[ToSerNum] -= flavor_property.memory[fn]
            else:
                flavor_property.SingleVmFlag[fn] = 0#//标志该虚拟机在该服务器上不能再放置
                break; #//内存没超，但服务器剩余的CPU数已经不能再放这种了虚拟机了，就跳出循环
        #进入到下面这个if的情况：1)该虚拟机已经放置完  2)该虚拟机已不能再该台服务器上放置
        if(JudgeRest(InputNum,ToSerNum) == 0):
            flag = 0
    if(Judge(InputNum) != 0):#判断一下，是不是所有虚拟机都配置完了，如果不是，那就新开一台物理服务器 
        server_property.cpu.append(int(server_info[0]))
        server_property.memory.append(int(server_info[1]))
        server_property.ser_name.append('server')
        server_property.flavor.append([0 for i in range(5)])
        for i in range(InputNum):
            flavor_property.SingleVmFlag[i] = 1
        ToSerNum += 1
    else:
        judge_flag = 0
print(server_property.cpu,server_property.flavor,server_property.memory,server_property.ser_name)        
if ecs_lines is None:
    print('ecs information is none')
if input_lines is None:
    print('input file information is none')
    
for item in ecs_lines:
    values = item.split()
    uuid = values[0]
    flavorName = values[1]
    createTime = values[2]

for item in input_lines:
    print("index of input data")

