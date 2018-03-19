# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 21:34:19 2018

@author: Administrator
"""
#大电脑地址'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\input_data.txt'
#小电脑地址'E:\\coding\\python\\soft_game\\input_data.txt'
#专门用来测试算法
import os
inputFilePath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\input_data.txt'
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
        self.SingleVmFlag = []   #放置开关
class server_property:
    def __init__(self):
        self.cpu = []     # property[0]:cpu
        self.memory = []
        self.flavor = [[0 for i in range(5)] for i in range(1)]        # flavor[0]表示要放的第1种虚拟机的台数，这里用下标直接代替了虚拟机种类，很明显可以flavor.resize(InputNum)
        self.ser_name = []

 
def get_server_property(inputFilePath):
    server_file_array = read_lines(inputFilePath)
    temp_list = server_file_array[0].split()
    server_property.cpu.append(int(temp_list[0]))
    server_property.memory.append(int(temp_list[1]))
    server_property.ser_name.append('server')
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
        
            
       
#--------------------放置函数结束----------------------
flavor_property = flavor_property()
server_property = server_property()
print('1',server_property.cpu,server_property.flavor,server_property.memory,server_property.ser_name)

server_property = get_server_property(inputFilePath)
flavor_property = get_flavor_property(inputFilePath)
print('2',server_property.cpu,server_property.flavor,server_property.memory,server_property.ser_name)

#server_property_static = get_server_property(inputFilePath)
print('3',server_property.cpu,server_property.flavor,server_property.memory,server_property.ser_name)

flavor_property.total = [2, 3, 3, 2, 6]#等于预测出来的数量之后用变量传递
flavor_property.rest = [2, 3, 3, 2, 6]
OptimizeFlag = 0
server_property.ser_num = 0
judge_flag = Judge(len(flavor_property.name))
ToSerNum = 0;#//设置需要配置的服务器，ToSerNum = 0即第1个服务器
fn = 0 #//当前放置优先级最高的虚拟机种类
InputNum = len(flavor_property.name)
print(server_property.cpu,server_property.flavor,server_property.memory,server_property.ser_name)        
 
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
        server_property.cpu.append(56)
        server_property.memory.append(128)
        server_property.ser_name.append('server')
        server_property.flavor.append([0 for i in range(5)])
        for i in range(InputNum):
            flavor_property.SingleVmFlag[i] = 1
        ToSerNum += 1
    else:
        judge_flag = 0
print(server_property.cpu,server_property.flavor,server_property.memory,server_property.ser_name)        
                
                
                



#
#
#     