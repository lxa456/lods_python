'''
Author: Xueao Li @ DUT
Date: 2023-02-10 21:18:52
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-10 21:25:37
Description: 根据各个文件夹中的POSCAR，批量生成对应的POTCAR（linux执行） 
                批量计算多组分材料时很有用。
'''
import os
from shutil import copy

def read_species_from_poscar(path)-> list:##读取poscar，输出元素类型的list
    f1 = open(path)
    lines = f1.readlines()
    species_list = []
    for species in lines[5].split():
        #print(species)
        species_list.append(species)
    return species_list

def gen_potcar(species_list, target_path):##根据元素类型的list，生成对应的potcar
    current_path = os.path.dirname(os.path.abspath(__file__))
    cat_shell = str()
    for species in species_list:
        potcar_path = os.path.join(current_path,"POTCAR-"+species)
        cat_shell += potcar_path+" "
        #potcar_list.append("POTCAR-"+species)
    os.system("cat "+cat_shell+"> "+os.path.join(target_path,"POTCAR"))
        

current_path = os.path.dirname(os.path.abspath(__file__))#当前路径

for root, dirs, files in os.walk(current_path):
    for filename in files:
        if filename == "POSCAR":
            poscar_path = os.path.join(root, filename)
            species_list = read_species_from_poscar(poscar_path)
            target_path = root
            print(target_path)
            gen_potcar(species_list, target_path)
