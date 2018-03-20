import copy
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
list3 = [[1,2,3],[4,5,6]]
def excluding_outliers(input_list):
    mean = cal_mean(input_list)
    variance = pow((cal_variance(input_list)),0.5)
    for i in range(len(input_list)):
        if ((input_list[i]-mean)>3*variance) or ((mean - input_list[i])>3*variance):
            input_list[i] = mean
    output_list = copy.deepcopy(input_list)
    print(output_list)
    return output_list

print(excluding_outliers(list3))






