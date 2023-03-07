'''
Author: Xueao Li @ DUT
Date: 2023-02-28 15:07:18
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-28 19:44:38
Description: The description of this script.

'''
from ase.db import connect
import os
from shutil import move
from ase import Atoms
from USR import USR  
from structure_similarity import *


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
    
    #print(xyz_path_list)
    for i in range(len(xyz_path_list)-1):
        for j in range(i+1, len(xyz_path_list)):
            M1 = USR.M_vector(xyz_path_list[i])
            M2 = USR.M_vector(xyz_path_list[j])
            print(USR.similarity(M1,M2))
            print(xyz_path_list[i], xyz_path_list[j])
            #print(xyz_path_list[i], xyz_path_list[j])
                #print(filename)
                #print(similarity(xyz_path, db_path))
    #similarity()


dupli_dir = all_formula_list("DATABASE.db")
make_dupli_dir(dupli_dir=dupli_dir)
move_xyz(db_path="DATABASE.db", dupli_dir=dupli_dir)
#dir_similarity(r"C:\Users\dell\Desktop\团簇数据库_output\lods_python\tools\de-duplication\Cd16Te16")