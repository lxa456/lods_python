'''
Author: Xueao Li @ DUT
Date: 2023-02-04 22:09:52
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-28 19:13:13
Description: The description of this script.

'''
## 检测输入的.xyz文件在DATABASE文件中相同元素和数量的团簇的相似度。

from ase.db import connect
from ase.atoms import Atoms
from USR import USR
import os


def formula(xyz_path):
    f1 = open(xyz_path)
    lines = f1.readlines()
    atom_species = []
    atom_num = []
    for line in lines:
        if len(line.split()) == 4:
            if line.split()[0] not in atom_species:
                atom_species.append(line.split()[0])
                atom_num.append(0)
            atom_num[-1] += 1
    formula = ''
    for i in range(len(atom_num)):
        formula += atom_species[i]+str(atom_num[i])
    return formula    

def similarity(xyz_path, db_path):    
    db = connect(db_path)
    A = None

    try: ##筛选单原子团簇
        M1 = USR.M_vector(xyz_path)
    except UnboundLocalError :
        for atoms in db.select(formula = formula(xyz_path)):
            A = atoms.toatoms(add_additional_information=False)
            struc_A = A.get_positions()
        if A != None:
            return 1
        else:
            return "this structure not in database now!"
    except:
        return "xyz file problem!!"

    similarity_list = []
    for atoms in db.select(formula = formula(xyz_path)):
        A = atoms.toatoms(add_additional_information=False)
        #print(A)
        struc_A = A.get_positions()
        M2 = USR.M_vector(struc_A)
        similarity_list.append(USR.similarity(M1,M2))
        #print(M1)
        #print(M2)
        #print(USR.similarity(M1,M2))
    if A == None: #or M2 == None:
        return "this structure not in database now!"
    else:
        return max(similarity_list) #返回最大相似度的值。





if __name__ == '__main__':
    db = connect('DATABASE.db')
    #similarity(xyz_path)
    xyz_path1 = r''
    xyz_path2 = r''
    M1 = USR.M_vector(xyz_path1)
    M2 = USR.M_vector(xyz_path2)
    #print(M1)
    print(USR.similarity(M1,M2))
    #xyz_path = r'/home/lxa/structure/26_sorted00.xyz'
    #xyz_path = r'/home/lxa/structure/Ga7As7.xyz'

