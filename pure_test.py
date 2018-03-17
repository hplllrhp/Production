# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 21:34:19 2018

@author: Administrator
"""

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
        self.name = ''          # 虚拟机类型
        self.total = 0          # 
        self.rest = 0
        self.property = []      # property[0]:cpu   property[1]:memory
        self.SingleVmFlag = 1   #放置开关
class server_property:
    def __init__(self):
        self.property = ''      # property[0]:cpu   property[1]:memory
        self.flavor = []        # flavor[0]表示要放的第1种虚拟机的台数，这里用下标直接代替了虚拟机种类，很明显可以flavor.resize(InputNum)

flavor_property = flavor_property()
server_property = server_property()
 
def get_server_property(inputFilePath):
    server_file_array = read_lines(inputFilePath)
    temp_list = server_file_array[0].split()
    return temp_list
server_property.property = get_server_property(inputFilePath)
#print(server_property.property[0])
print(server_property.property)






     