# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:52:26 2018

@author: Administrator
"""

#用来更方便精心观察变量调试使用# coding=utf-8
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

# Do your work from here#
inputFilePath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\input_data.txt'
ecsDataPath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\train_data.txt'
resultFilePath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\soft_game\\output_data.txt'
ecs_infor_array = read_lines(ecsDataPath)
input_file_array = read_lines(inputFilePath)
ecs_lines = ecs_infor_array
input_lines = input_file_array

result = []
if ecs_lines is None:
    print('ecs information is none')
if input_lines is None:
    print('input file information is none')
    
#    for index, item in ecs_lines:
#        values = item.split(" ")
#        uuid = values[0]
#        flavorName = values[1]
#        createTime = values[2]
#
#    for index, item in input_lines:
#        print("index of input data")

