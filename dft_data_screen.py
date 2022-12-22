'''
Author: Xueao Li @ DUT
Date: 2022-12-21 17:02:55
LastEditors: Xueao Li @ DUT
LastEditTime: 2022-12-22 14:56:04
Description: The description of this script.

Copyright (c) 2022 by li xueao 11076446+li-xueao@user.noreply.gitee.com, All Rights Reserved. 
'''


from USR import USR
import os
from structure_similarity import *
from shutil import copy
import pandas as pd  ##将数据保存为csv文件


## DATABASE.db 路径
db_path = r"C:\Users\dell\Desktop\database_backups\DATABASE_backup\2022_6_4\DATABASE.db" 

## 相似度的上限，超过该值即判定为重复结构。
similarity_value = 0.90

dft_data_dir = r"C:\Users\dell\Desktop\团簇数据库_output\simple\Ag\DFT_data"
dft_data_screen_dir = dft_data_dir.replace("DFT_data","DFT_data_screen")
dft_data_csv = os.path.join(dft_data_dir,"dft_info.csv")

## 将所有相似性信息存在similarity.csv中
similarity_csv = os.path.join(dft_data_screen_dir,"similarity.csv")
## 将所有重复的结构的dft信息存在dft_data_exist.csv中
dft_data_exist_csv = os.path.join(dft_data_screen_dir, "dft_data_exist.csv")
## 将所有新的结构的dft信息存在dft_data_not_exist.csv中
dft_data_not_exist_csv = os.path.join(dft_data_screen_dir, "dft_data_not_exist.csv")

if not os.path.exists(dft_data_screen_dir):
    os.makedirs(dft_data_screen_dir)

## 存储所有相似度的数值
similarity_list = []
## 存储所有xyz文件的文件名
filename_list = []

def extract_row(csv_file: str, list: list, new_csv: str) -> None: 
    '''把csv_file中特定行放到另一个csv文件中'''
    f1 = open(csv_file, "r")
    lines = f1.readlines()
    with open(new_csv, "w+") as new:
        new.write(lines[0])
        for i in list:
            new.write(lines[int(i)])
    

def filename_index(csv_file: str, filename: str) -> int:
    '''输入csv文件路径和filename，返回filename所在的行数'''
    f1 = open(csv_file, "r")
    lines = f1.readlines()
    for i in range(len(lines)):
        if lines[i].split(",")[0] == filename:
            return i


exist_xyz_index_list = []
not_exist_xyz_index_list = []

## 遍历dft_data下所有*.xyz
for root, dirs, files in os.walk(dft_data_dir):
    for filename in files:
        if filename.endswith(".xyz"):
            xyz_path = os.path.join(root, filename)
            ## 该xyz文件在DATABASE.db中相同化学式结构的相似度
            _similarity = similarity(xyz_path,db_path)
            filename_list.append(filename[:-4])

            ## 重复的数据放在xyz_relaxed_existed中
            if type(_similarity) == float and _similarity > similarity_value: 
                xyz_relaxed_existed_path = os.path.join(dft_data_screen_dir, "xyz_relaxed_existed", filename)
                if not os.path.exists(os.path.join(dft_data_screen_dir, "xyz_relaxed_existed")):
                    os.makedirs(os.path.join(dft_data_screen_dir, "xyz_relaxed_existed"))

                copy(xyz_path, xyz_relaxed_existed_path)
                exist_xyz_index_list.append(filename_index(dft_data_csv,filename[:-4]))

            elif type(_similarity) == float and _similarity < similarity_value :
                xyz_relaxed_not_existed_path = os.path.join(dft_data_screen_dir, "xyz_relaxed", filename)
                if not os.path.exists(os.path.join(dft_data_screen_dir, "xyz_relaxed")):
                    os.makedirs(os.path.join(dft_data_screen_dir, "xyz_relaxed"))
                copy(xyz_path, xyz_relaxed_not_existed_path)
                similarity_list.append(str(_similarity)+' (Exist but not satisfied!)')
                not_exist_xyz_index_list.append(filename_index(dft_data_csv,filename[:-4]))
                
            elif type(_similarity) == str :
                xyz_relaxed_not_existed_path = os.path.join(dft_data_screen_dir, "xyz_relaxed", filename)
                if not os.path.exists(os.path.join(dft_data_screen_dir, "xyz_relaxed")):
                    os.makedirs(os.path.join(dft_data_screen_dir, "xyz_relaxed"))
                copy(xyz_path, xyz_relaxed_not_existed_path)
                similarity_list.append('Not Exist!')
                not_exist_xyz_index_list.append(filename_index(dft_data_csv,filename[:-4]))


## 保存相似度信息
similarity_data = pd.DataFrame({'filename': filename_list, 'similarity':similarity_list})
similarity_data.to_csv(similarity_csv, index=False, sep=',')

## 将dft_data.csv分开为dft_data_existed.csv和dft_data_not_existed.csv保存
extract_row(dft_data_csv,exist_xyz_index_list,dft_data_exist_csv)
extract_row(dft_data_csv,not_exist_xyz_index_list,dft_data_not_exist_csv)