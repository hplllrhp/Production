import copy
import os
import csv
import matplotlib.pyplot as plt
#tate_table = [['flavor1', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], ['flavor2', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2], ['flavor3', 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0], ['flavor4', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ['flavor5', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 3, 0, 1, 3, 0, 0, 1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0]]
#temg_tate_table = copy.deepcopy(tate_table)
#for i in range(len(tate_table)):
#    for j in range(1,len(tate_table[0])):
#        temg_tate_table[i][j] = sum(tate_table[i][1:j+1])
#print('temg_tate_table',temg_tate_table,'tate_table',tate_table)

#去掉数组中的异常值，原理是在正态分布的假设下，区域 \mu\pm 3\sigma 包含了99.7% 的数据，
#如果某个值距离分布的均值 \mu 超过了 3\sigma，那么这个值就可以被简单的标记为一个异常点（outlier）。
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
    return variance / float(len(readings))

list2 = [0,0,0,1,2,0,0,0,0,0,0,0,0,0,1,0,0,2,0,0,12,0,0,0,1,0,1,0,0,0,0,0]
list3 = [[0,0,0,1,2,0,0,0,0,0,0,0,0,0,1,0,0,2,0,0,12,0,0,0,1,0,1,0,0,0,0,0],[0,0,0,1,2,0,0,0,0,0,0,0,0,0,1,0,0,2,0,0,12,0,0,0,1,0,1,0,0,0,0,0]]

def excluding_outliers(input_list):
    mean = cal_mean(input_list)
    variance = pow((cal_variance(input_list)),0.5)
    for i in range(len(input_list)):
        if ((input_list[i]-mean)>3*variance) or ((mean - input_list[i])>3*variance):
            input_list[i] = mean
    output_list = copy.deepcopy(input_list)
    print(output_list)
    return output_list



def excluding_data_table(input_table):
    for i in range(len(input_table)):
        mean = cal_mean(input_table[i][:])
        variance = pow((cal_variance(input_table[i][:])),0.5)
        for j in range(len(input_table[i])):
            if ((input_table[i][j]-mean)>3*variance) or ((mean - input_table[i][j])>3*variance):
                input_table[i][j] = mean
    output_table = copy.deepcopy(input_table)
    return output_table

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
    
def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        i = 1;
        output_file.write('days   number\n')
        for item in array:
            output_file.write('%s  ' %i)
            output_file.write("%s\n" %item) 
            i += 1
def write_csv(input_arry,outpuFilePath):
    with open(outpuFilePath,'w') as f:
        f_csv = csv.writer(f)
        #先写入columns_name
        f_csv.writerow(['days','number'])
        #写入多行用writerows
        for i in range(len(input_arry)):
            f_csv.writerow([i+1,input_arry[i]])
        
file_path = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\origin_code\\LSTM_F1_150.txt'
outpuFilePath = 'E:\\Document\\Personal\\Postgraduate\\game\\huawei_soft\\huawei\\ecs\\origin_code\\LSTM_F1_150.csv'
lines = read_lines(file_path)
templine = lines[0].split(',')
for i in range(len(templine)):
    templine[i] = float(templine[i]) 
#    templine[i] += 1
print(templine)
write_csv(templine,outpuFilePath)







