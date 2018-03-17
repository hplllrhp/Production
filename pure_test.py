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
        self.cpu = []     # property[0]:cpu   property[1]:memory
        self.memory = []
        self.flavor = []        # flavor[0]表示要放的第1种虚拟机的台数，这里用下标直接代替了虚拟机种类，很明显可以flavor.resize(InputNum)

flavor_property = flavor_property()
server_property = server_property()
 
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
            odom = line.split()
            temp_list = list(odom)
            flavor_property.name.append(temp_list[0])
            flavor_property.cpu.append(int(temp_list[1]))
            flavor_property.memory.append(int(int(temp_list[2])/1024))
    return flavor_property
server_property = get_server_property(inputFilePath)
flavor_property = get_flavor_property(inputFilePath)
print(server_property.cpu,flavor_property.cpu)
#print(server_property.property)
#--------------------放置函数开始----------------------
InputNum = 0
i = 0
fn = 0
size = 0
a = []





     