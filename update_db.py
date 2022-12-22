'''
Author: Xueao Li @ DUT
Date: 2022-12-13 20:20:48
LastEditors: Xueao Li @ DUT
LastEditTime: 2022-12-20 14:59:15
Description: 本脚本面向Linux系统。

Copyright (c) 2022 by li xueao 11076446+li-xueao@user.noreply.gitee.com, All Rights Reserved. 
'''
from ase.db import connect
from ase import Atoms
import os, sys, sqlite3, csv
import pandas as pd

#db = connect("DATABASE.db")
#update_csv = r'C:\Users\dell\Desktop\团簇数据库_output\simple\Ag\DFT_data\dft_info.csv'
update_csv = "dft_info.csv"
##f2 = pd.read_csv(update_csv,header=0)
#print(f2.head(1))
#print(f2["filename"])
#print(f2.head())
#f3 = pd.read_csv(update_csv,header=1)
current_path = os.path.split( os.path.realpath(sys.argv[0]))[0] #当前目录

db_filename = "Ag.db"
## *.db文件中的所有key
db_key = ["filename", "GAP_DFT","HOMO_DFT","LUMO_DFT","Point_Group"\
    ,"TOTEN","GAP_GW","HOMO_GW","LUMO_GW","Point_Group", "N_ele", "Max_Force"]

## pd.read_csv 没玩明白，先手动读csv
f1 = open(update_csv)
lines1 = f1.readlines()
## all KEY in csv file
key_list = [] 
[key_list.append(lines1[0].strip().split(",")[i]) for i in range(len(lines1[0].split(",")))]
## all VALUE of filename KEY in csv file
filename_list = []
[filename_list.append(lines1[i].strip().split(",")[0]) for i in range(1, len(lines1))]


## step 1. 按照csv中filename的顺序来convert所有*.xyz 文件成 .db
xyz_path_list = []
for name in filename_list:
    for root, dirs, files in os.walk(current_path):
        for filename in files:
            if filename == name+".xyz" :
                xyz_path = os.path.join(root, filename)
                xyz_path_list.append(xyz_path)

#print(xyz_path_list)

convert_cmd = ''
for i in xyz_path_list:
    convert_cmd+=i+" "
#print(convert_cmd)

#os.system("ase convert "+convert_cmd+db_filename)

db = connect(db_filename)
## step 2. 按row.id更新db中的keys and values
#for row in db.select():
    

def index(list, value) -> int:
    """输入list和它包含的元素，
    返回该元素的序号（当然是从0开始）"""
    assert value in list, "value不在list中！"
    i = 0
    for index in list:
        if index == value:
            return i
        else:
            i+=1

#[x.append(i[0])  for i in data]
#print(key_list)

def update_Sequential(db_file, key, value_list):
    db = connect(db_file)
    for row in db.select():
        db.update(row.id, )
## csv文件中的第一行是key。
## 检查key是否在 db_key 中。

for row in db.select():
    for key in key_list:
        if key in db_key:
            if key == "TOTEN":
                N_column = index(key_list, "TOTEN") # KEY在csv文件的列数
                TOTEN = str(lines1[row.id].split(',')[N_column])+" eV"
                db.update(row.id, TOTEN=TOTEN)
            if key == "filename":
                N_column = index(key_list, "filename") # KEY在csv文件的列数
                filename = str(lines1[row.id].split(',')[N_column])
                db.update(row.id, filename=filename)
            if key == "Max_Force":
                N_column = index(key_list, "Max_Force") # KEY在csv文件的列数
                Max_Force = float(lines1[row.id].split(',')[N_column])
                db.update(row.id, Max_Force=Max_Force)
            if key == "N_ele":
                N_column = index(key_list, "N_ele") # KEY在csv文件的列数
                N_ele = int(lines1[row.id].split(',')[N_column])
                db.update(row.id, N_ele=N_ele)
            if key == "HOMO_DFT":
                N_column = index(key_list, "HOMO_DFT") # KEY在csv文件的列数
                HOMO_DFT = float(lines1[row.id].split(',')[N_column])
                db.update(row.id, HOMO_DFT=HOMO_DFT)
            if key == "GAP_DFT":
                N_column = index(key_list, "GAP_DFT") # KEY在csv文件的列数
                GAP_DFT = float(lines1[row.id].split(',')[N_column])
                db.update(row.id, GAP_DFT=GAP_DFT)
            if key == "Point_Group":
                N_column = index(key_list, "Point_Group") # KEY在csv文件的列数
                Point_Group = str(lines1[row.id].split(',')[N_column])
                db.update(row.id, Point_Group=Point_Group)
        else:
            print(key,"not in db_key! Please check the KEY in csv file!!!")