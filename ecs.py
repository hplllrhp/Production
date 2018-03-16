# coding=utf-8
import sys
import os
import predictor
print('safenot')
def main():
    print('main function begin.')
    if len(sys.argv) != 4:
        print('parameter is incorrect!')
        print('Usage: python esc.py ecsDataPath inputFilePath resultFilePath')
#        exit(1)
    # Read the input files
    inputFilePath = 'D:\\installation manual\\Ubuntu14_04\\share_file\\FAQV3.5\\sdk\\sdk\\sdk-python\\src\\ecs\\input_data.txt'
    ecsDataPath = 'D:\\installation manual\\Ubuntu14_04\\share_file\\FAQV3.5\\sdk\\sdk\\sdk-python\\src\\ecs\\train_data.txt'
    resultFilePath = 'D:\\installation manual\\Ubuntu14_04\\share_file\\FAQV3.5\\sdk\\sdk\\sdk-python\\src\\ecs\\output_data.txt'
    ecs_infor_array = read_lines(ecsDataPath)
    input_file_array = read_lines(inputFilePath)
    # implementation the function predictVm
    predic_result = predictor.predict_vm(ecs_infor_array, input_file_array)
    # write the result to output file
    if len(predic_result) != 0:
        write_result(predic_result, resultFilePath)
    else:
        predic_result.append("NA")
        write_result(predic_result, resultFilePath)
    print('main function end.')


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


if __name__ == "__main__":
    main()
