# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 11:02:47 2018

@author: Administrator
"""
#打开xml文档
import sys
import glob
import os
import xml.dom.minidom
collapsed_house_count = 0;
landslide_count = 0;
debris_flow_count = 0;
damaged_road_count = 0;

collapsed_house_xml_count = 0;
landslide_xml_count = 0;
debris_flow_xml_count = 0;
damaged_road_xml_count = 0;
file_path = 'E:\\Document\\Personal\\Postgraduate\\post-course\\python\\python_exercise_100\\show-me-the-code\\Annotations\\test'
if(os.path.exists(file_path)):#判断路径是否存在
    #得到该文件夹路径下下的所有xml文件路径  
    f = glob.glob(file_path + '\\*.xml')
    print("该文件夹内总共有%d个XML文件"%len(f))
    for file in f:
        #打开xml文档
        dom = xml.dom.minidom.parse(file)
        #得到文档元素对象
        root = dom.documentElement
        disaster_name = root.getElementsByTagName('name')
        xml_name_list = []
        for i in range(len(disaster_name)):
            if disaster_name[i].firstChild.data == 'collapsed_house':
                collapsed_house_count += 1;
            if disaster_name[i].firstChild.data == 'landslide':
                landslide_count += 1;
            if disaster_name[i].firstChild.data == 'debris_flow':
                debris_flow_count += 1;
            if disaster_name[i].firstChild.data == 'damaged_road':
                damaged_road_count += 1;
            xml_name_list.append(disaster_name[i].firstChild.data)
        if 'collapsed_house' in xml_name_list:
            collapsed_house_xml_count += 1
        if 'landslide' in xml_name_list:
            landslide_xml_count += 1
        if 'debris_flow' in xml_name_list:
            debris_flow_xml_count += 1
        if 'damaged_road' in xml_name_list:
            damaged_road_xml_count += 1
print("%d个XML文件总共有%d个collapsed_house_count特征"%(len(f),collapsed_house_count))
print("%d个XML文件总共有%d个landslide_count特征"%(len(f),landslide_count))
print("%d个XML文件总共有%d个damaged_road_count"%(len(f),damaged_road_count))
print("%d个XML文件总共有%d个debris_flow_count特征"%(len(f),debris_flow_count))

print("在%d个XML文件中具有collapsed_house_count特征特征的总共有%d个"%(len(f),collapsed_house_xml_count))
print("在%d个XML文件中具有landslide_count特征的总共有%d个"%(len(f),landslide_xml_count))
print("在%d个XML文件中具有damaged_road_count特征的总共有%d个"%(len(f),damaged_road_xml_count))
print("在%d个XML文件中具有debris_flow_count特征的总共有%d个"%(len(f),debris_flow_xml_count))

            
    
    
    
    
    
    
    
    
    