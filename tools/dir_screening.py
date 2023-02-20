'''
Author: Xueao Li @ DUT
Date: 2023-02-04 22:09:52
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-20 15:49:38
Description: The description of this script.

'''
## 筛选文件夹，文件夹里存放xyz文件夹，把从中的xyz文件筛选出来放到另一个文件夹。
## 本脚本用来提前筛选出结构相似的结构，减少不必要的计算量。

from ase.db import connect
from ase.atoms import Atoms
from USR import USR
import os
from structure_similarity import *
from shutil import copy
import pandas as pd  ##将数据保存为csv文件


dir_path = r'C:\Users\dell\Desktop\团簇数据库_xyz\团簇组装体系'
db_path = r'C:\Users\dell\Desktop\USR_test\USR\DATABASE.db'
new_dir = r'C:\Users\dell\Desktop\ClusterDB_Second_Edition\团簇组装体系'
csv_path = os.path.join(new_dir,"similarity.csv")

if not os.path.exists(new_dir):
    os.makedirs(new_dir)

filename_list = []
_similarity_list = []
formula_list = []

for root,dirs,files in os.walk(dir_path):
    for filename in files:
        if filename.endswith('.xyz'):
            xyz_path = os.path.join(root,filename)
            print(xyz_path)
            _similarity = similarity(xyz_path,db_path)
            filename_list.append(filename[:-3])
            new_xyz_path = xyz_path.replace(dir_path,new_dir)

            if not os.path.exists(root.replace(dir_path,new_dir)):
                os.makedirs(root.replace(dir_path,new_dir))

            if  type(_similarity) == str :
                _similarity_list.append('Not Exist!')
                formula_list.append(formula(xyz_path))
                copy(xyz_path, new_xyz_path)
            elif _similarity <= 0.90 :
                _similarity_list.append(str(_similarity)+' (Exist but not satisfied!)')
                formula_list.append(formula(xyz_path))
            else:
                _similarity_list.append(_similarity)
                formula_list.append(formula(xyz_path))
        else:
            source_path = os.path.join(root, filename)
            new_path = root.replace(dir_path,new_dir)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            copy(source_path, new_path)

            

#print(formula_list)
#print(filename_list)       
#print(_similarity_list)
#
similarity_data = pd.DataFrame({'Filename': filename_list, 'Formula': formula_list,\
    'similarity':_similarity_list})
similarity_data.to_csv(csv_path, index=False, sep=',')




            


