# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 23:12:57 2018

@author: Administrator
"""

#对txt进行处理，统计出flavor1到5出现过的数量
to_predict_list = []
with open('input_data.txt', 'r') as f:  
    data = f.readlines()  #txt中所有字符串读入data  
    for line in data: 
        if 'flavor' in line:
            odom = line.split()
            list1 = list(odom)
            to_predict_list.append(list1[0])
date_table = [ [0 for i in range(51)] for i in range(len(to_predict_list))] 
for i in range(len(to_predict_list)):
    date_table[i][0] = to_predict_list[i]
date_count = 0
date_flag = 1
date_flag_new = 1
Train_list_samedate = []
#先找出有几个需要检测的flavor，len函数，然后在条件句中
with open('Train_Data.txt', 'r') as f1:  
    data = f1.readlines()  #txt中所有字符串读入data  
    for line1 in data: 
        odom1 = line1.split() 
        Train_list2 = list(odom1)
        for i in range(len(to_predict_list)):
            if to_predict_list[i] in Train_list2: 
                if Train_list2[2][5:7] == '01':
                    date_flag = int(Train_list2[2][8:10])
                if Train_list2[2][5:7] == '02':
                    date_flag = int(Train_list2[2][8:10]) + 30
                date_table[i][date_flag] += 1 
          
print(len(date_table))            
            
            
#        if date_flag == date_flag_new:
#            Train_list_samedate.append(Train_list2)
#            print('same')
#        if date_flag != date_flag_new:
#            print('notsame')
#            for i in range(len(to_predict_list)):
#                date_count = str(Train_list_samedate).count(to_predict_list[i])
#                date_table[i][date_flag_new] = date_count
#            for i in range(len(to_predict_list)):
#                date_count = str(Train_list2).count(to_predict_list[i])
#                date_table[i][date_flag] = date_count
#        date_flag_new = date_flag
#        Train_list_samedate = []
#        
        
        
        
        
        
        