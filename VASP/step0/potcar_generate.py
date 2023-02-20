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

 
def merge(file_list, file1):
    with open(file1, 'w+', encoding='utf-8') as f1 :
        for file in file_list:
            f2 = open(file,'r', encoding='utf-8')
            for i in f2:
                f1.write(i)
 

def gen_potcar(species_list, target_path):##根据元素类型的list，生成对应的potcar
    potcar_dir = r"C:\Users\dell\Desktop\团簇数据库_input\POTCAR"
    potcar_list = []
    for species in species_list:
        potcar_path = os.path.join(potcar_dir,"POTCAR-"+species)

        potcar_list.append(potcar_path)
    merge(potcar_list, target_path)
        

#poscar_test = r'C:\Users\dell\Desktop\团簇数据库_input\合金_掺杂团簇\Ag-Au\17\POSCAR'
#print(read_species_from_poscar(poscar_test))

#current_path = os.path.dirname(os.path.abspath(__file__))#当前路径

#for root, dirs, files in os.walk(current_path):
#    for filename in files:
#        if filename == "POSCAR":
#            poscar_path = os.path.join(root, filename)
#            species_list = read_species_from_poscar(poscar_path)
#            target_path = root
#            print(target_path)
#            gen_potcar(species_list, target_path)
