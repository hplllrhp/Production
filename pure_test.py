# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 21:34:19 2018

@author: Administrator
"""

#专门用来测试算法
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
        