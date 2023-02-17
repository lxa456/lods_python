'''
Author: Xueao Li @ DUT
Date: 2023-02-08 17:43:04
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-17 15:01:58
Description: 改CONTCAR第一行的文件名。
'''
import os, sys


def modify_first_line(file_path, new_line):
    '''修改第一行'''
    with open(file_path, 'r') as f:
        lines = f.readlines()

    lines[0] = new_line 

    with open(file_path, 'w') as f:
        f.writelines(lines)

def remove_second_line(file_path):
    '''删除第二行'''
    with open(file_path, 'r') as f:
        lines = f.readlines()

    lines.pop(1)

    with open(file_path, 'w') as f:
        f.writelines(lines)

#current_path = os.path.split( os.path.realpath(sys.argv[0]))[0] #当前目录
path = r"C:\Users\dell\Desktop\团簇数据库_output\binary_dope\Ti1-2Si14-20\DFT"
for root, dirs, files in os.walk(path):
    for filename in files:
        if filename == "CONTCAR":
            f1 = open(os.path.join(root, filename), 'r')
            lines = f1.readlines()
            try:
                name = float(lines[0].replace(".xyz",""))
                name = root.split("\\")[-3]+"-"+lines[0]
            except:
                name = str(lines[0])
            contcar_path = os.path.join(root, filename)
            print(root.split("\\")[-3])
            #print(name)
            #remove_second_line(contcar_path)
            #modify_first_line(contcar_path, name)
            modify_first_line(contcar_path, root.split("\\")[-3]+"-"+name)