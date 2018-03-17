# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 21:34:19 2018

@author: Administrator
"""
#大电脑地址'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\input_data.txt'
#小电脑地址'E:\\coding\\python\\soft_game\\input_data.txt'
#专门用来测试算法
import os
inputFilePath = 'E:\\coding\\python\\soft_game\\input_data.txt'
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
    
class flavor_property:
    def __init__(self):
        self.name = []          # 虚拟机类型
        self.total = []          # 
        self.rest = []
        self.cpu = []      # property[0]:cpu
        self.memory = []
        self.SingleVmFlag = 1   #放置开关
class server_property:
    def __init__(self):
        self.cpu = []     # property[0]:cpu
        self.memory = []
        self.flavor = []        # flavor[0]表示要放的第1种虚拟机的台数，这里用下标直接代替了虚拟机种类，很明显可以flavor.resize(InputNum)


 
def get_server_property(inputFilePath):
    server_file_array = read_lines(inputFilePath)
    temp_list = server_file_array[0].split()
    server_property.cpu.append(int(temp_list[0]))
    server_property.memory.append(int(temp_list[1]))
    return server_property

def get_flavor_property(inputFilePath):
    flavor_file_array = read_lines(inputFilePath)
    for line in flavor_file_array:
        if 'flavor' in line:
            temp = line.split()
            temp_list = list(temp)
            flavor_property.name.append(temp_list[0])
            flavor_property.cpu.append(int(temp_list[1]))
            flavor_property.memory.append(int(int(temp_list[2])/1024))
    return flavor_property

#print(server_property.property)
#--------------------放置函数开始----------------------
def JudgeRest(InputNum):
    flag = 0
    for i in range(InputNum):
        if(flavor_property.rest[i] != 0 and flavor_property.SingleVmFlag != 0):
            if(server_property.cpu[0] >= flavor_property.cpu[i] and server_property.memory[0] >= flavor_property.memory[i]):
               flag = 1
               break
    print(server_property.cpu,flavor_property.total[i])
    return flag

def SelectFlavorToSet(InputNum,i):
    fn = 0
    size = 0
    a = []    #//存储还没分配完的虚拟机的类型标号，后续就是在这里面筛选
    for j in range(InputNum):
        if(flavor_property.rest[j] != 0 and flavor_property.SingleVmFlag != 0):
            a.append(j)
    size = len(a)
    for k in range(size):
        if(i == 0):
            if(flavor_property.cpu[a[k]] > flavor_property.cpu[a[k]-1]):
                fn = a[k]
            elif(flavor_property.cpu[a[k]] < flavor_property.cpu[a[k]-1]):
                fn = a[k-1]
            else:
                fn = flavor_property.memory[a[k]] > flavor_property.memory[a[k -1]] ? a[k] : a[k-1] 
    print()
    
#--------------------放置函数结束----------------------
flavor_property = flavor_property()
server_property = server_property()
server_property = get_server_property(inputFilePath)
flavor_property = get_flavor_property(inputFilePath)
flavor_property.total = [2, 3, 3, 2, 6]#等于预测出来的数量之后用变量传递
flavor_property.rest = [0,0,0,0,0]
flag = JudgeRest(4)



     