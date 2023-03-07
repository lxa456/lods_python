'''
Author: Xueao Li @ DUT
Date: 2023-02-28 15:07:18
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-03-07 15:09:20
Description: 使用USR方法过滤数据库中的重复结构。不太好用，有待更新。
'''
from ase.db import connect
import os
from shutil import move
from ase import Atoms
from USR import USR  
from structure_similarity import *
import numpy as np


def all_formula_list(db_path):
    '''读取database中的相同化学式的结构'''
    formula_list = []
    dupli_list = []
    db = connect(db_path)
    for row in db.select():
        if row.formula not in formula_list:
            formula_list.append(row.formula)
        elif row.formula in formula_list and row.formula not in dupli_list:
            dupli_list.append(row.formula)
    return dupli_list


def make_dupli_dir(dupli_dir):
    """创建以化学式为名的文件夹"""
    for dir in dupli_dir:
        if not os.path.exists(os.path.join("de-duplication", dir)):
            os.makedirs(os.path.join("de-duplication", dir))


def move_xyz(db_path, dupli_dir):
    """把相同化学式的xyz文件放到对应的文件夹里"""
    db = connect(db_path)
    for row in db.select():
        if row.formula in dupli_dir:
            print(row.formula)
            atoms = row.toatoms()
            Atoms.write(atoms, filename = str(row.id)+"_"+row.filename+".xyz", format="xyz")
            move(str(row.id)+"_"+row.filename+".xyz", os.path.join("de-duplication", row.formula,str(row.id)+"_"+row.filename+".xyz"))
        

def dir_similarity(xyz_dir):
    """检查文件夹内文件的相似性，大于0.9视为相同结构"""

    xyz_path_list = []
    for root, dirs, files in os.walk(xyz_dir):
        for filename in files:
            if filename.endswith(".xyz"):
                xyz_path = os.path.join(root, filename)
                xyz_path_list.append(xyz_path)
    
    dupli_list = []

    for i in range(len(xyz_path_list)-1):
        for j in range(i+1, len(xyz_path_list)):
            M1 = USR.M_vector(xyz_path_list[i])
            M2 = USR.M_vector(xyz_path_list[j])
            if USR.similarity(M1,M2) > 0.95:
                #print(USR.similarity(M1,M2))
                xyz_pair = np.zeros(2)
                xyz_pair[0] = int(xyz_path_list[i].split("\\")[-1].split("_")[0])
                xyz_pair[1] = int(xyz_path_list[j].split("\\")[-1].split("_")[0])
                dupli_list.append(xyz_pair)
    dupli_list = np.array(dupli_list)
    return dupli_list


def delete_duplicate_row(db_path,dupli_list):
    from shutil import copy
    new_db = "DATABASE_NEW.db"
    copy(db_path,new_db)
    db = connect(new_db)
    delete_id_list = []
    for pair in dupli_list:
        id_1, id_2 = int(pair[0]), int(pair[1])
        if id_1 not in delete_id_list and id_2 not in delete_id_list:

            for row in db.select(id=id_1):
                N_ele_1 = row.N_ele

            for row in db.select(id=id_2):
                N_ele_2 = row.N_ele

            if N_ele_1 == N_ele_2:
                delete_id_list.append(max(id_1, id_2))
    db.delete(ids=delete_id_list)
    print(delete_id_list)


#dupli_list = np.array([[4720,4803],[4778,4779]])

#delete_duplicate_row("DATABASE.db", dupli_list)

if __name__ == "__main__":


    dupli_dir = all_formula_list("DATABASE.db")
    for dir in dupli_dir:
        xyz_dir = os.path.join("de-duplication", dir)
        dupli_list = dir_similarity(xyz_dir=xyz_dir)
        print(xyz_dir)
        print(dupli_list)
        #print(xyz_dir)


#make_dupli_dir(dupli_dir=dupli_dir)
#move_xyz(db_path="DATABASE.db", dupli_dir=dupli_dir)
#dir_similarity(r"C:\Users\dell\Desktop\团簇数据库_output\lods_python\tools\de-duplication\Cd16Te16")