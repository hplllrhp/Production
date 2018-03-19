result = [5, 'flavor1 2', 'flavor2 3', 'flavor3 3', 'flavor4 2', 'flavor5 6']
with open('C:\\Users\\Administrator\\Desktop\\result.txt', 'w') as output_file:
        for item in result:
            output_file.write("%s\n" % item)