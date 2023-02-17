'''
Author: Xueao Li @ DUT
Date: 2023-02-14 10:44:18
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-17 14:33:20
Description: 提取GW输出文件信息到gw_information.csv
'''
import os
import pandas as pd 
import numpy as np 
from shutil import copy

current_path = os.path.dirname(os.path.abspath(__file__))#当前路径
gw_path = r"C:\Users\dell\Desktop\GW信息汇总\GW_update\GaAs"
csv_path = os.path.join(gw_path, 'gw_information.csv')


def read_filename(parsecin_path):
    f1 = open(parsecin_path)
    lines = f1.readlines()
    filename = lines[0].replace("#","").replace(".xyz","").replace("\n","")
    return filename


def homolumo(sigma_path):
    f1 = open(sigma_path)
    line = f1.readlines()
    HOMO = float(line[4].split()[-1])
    LUMO = float(line[5].split()[-1])
    return HOMO,LUMO

filename_list, homo_list, lumo_list, gap_list = [], [], [],[]

for root,dirs,files in os.walk(gw_path):
    for filename in files:
        if filename == "parsec.in":
            parsec_in_path = os.path.join(root, filename)
            filename_list.append(read_filename(parsec_in_path))
        elif filename == "sigma_001_0000":
            sigma_path = os.path.join(root, filename)
            homo_list.append(homolumo(sigma_path)[0])
            lumo_list.append(homolumo(sigma_path)[1])
            gap_list.append("%.3f" %(homolumo(sigma_path)[1]-homolumo(sigma_path)[0]))


print(filename_list, homo_list, lumo_list, gap_list)
print(len(filename_list), len(homo_list), len(lumo_list), len(gap_list))

#字典中的key值即为csv中列名
dataframe = pd.DataFrame({'filename': filename_list, 'HOMO_GW':homo_list,\
     'LUMO_GW':lumo_list,'GAP_GW':gap_list})
#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe.to_csv(csv_path, index=False, sep=',')

