'''
Author: Xueao Li @ DUT
Date: 2023-02-21 20:27:22
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-21 20:33:30
Description: 指定xyz文件夹和输出文件夹，生成全部的NanoGW输入文件。
'''


import os
import math
from shutil import copy

###########（1种原子）输入Type_num函数，依次输出Atom_Type, Local_component, Nv  ########
def cluster_information(type_num_function):
    Atom_Type = type_num_function[1]
    type1_num = type_num_function[2]
    if Atom_Type in ['As', 'Ge', 'P', 'Si']:
        Local_component = 'p'
    elif Atom_Type in ['B', 'N', 'H', 'O', 'Li', 'Ga', 'C']:
        Local_component = 's'
    if Atom_Type in ['H', 'O', 'Li']:
        valence_electron_num = 1
    elif Atom_Type in ['B', 'Ga']:
        valence_electron_num = 3
    elif Atom_Type in ['Ge', 'Si', 'C']:
        valence_electron_num = 4
    elif Atom_Type in ['As', 'N', 'P']:
        valence_electron_num = 5
    elif Atom_Type in ['O']:
        valence_electron_num = 6
    Nv = type1_num*valence_electron_num/2
    return Atom_Type, Local_component, Nv

#########输入Nv，依次输出num_isdf_points，state_num，max_number_states################
def parameter(Nv):
    Nv = float(Nv)
    Nc = 8*float(Nv)
    num_isdf_points_out = 20 * math.sqrt((Nv+Nc)*Nv)
    max_number_states = 9*Nv
    states_num = int(30 + 9*Nv) #parsec.in 文件中的
    num_isdf_points = int(num_isdf_points_out)
    return str(num_isdf_points),str(states_num), str(int(max_number_states))

########输出xyz文件的Boundary_Sphere_Radius##############
def Boundary_Sphere_Radius(xyz_path):
    final_distance = []
    f1 = open(xyz_path)
    line_read = f1.readlines()
    distance_list = []
    distance = 0
    for i in range(2,len(line_read)):
        for j in range(i+1, len(line_read)):
            xi, yi, zi = float(line_read[i].split()[1]), float(line_read[i].split()[2]),float(line_read[i].split()[3])
            xj, yj, zj = float(line_read[j].split()[1]), float(line_read[j].split()[2]),float(line_read[j].split()[3])
            distance = math.sqrt((xi-xj)**2+ (yi-yj)**2+ (zi-zj)**2)/0.529177
            distance_list.append(distance)
            distance = 0
    final_distance = int((max(distance_list)/2)*1.5)+8 ##乘1.5是为了A换算Bohr，本身计算的半径偏大所以乘的1.5，再在半径基础上+8
    return str(final_distance)

########输入刚生成的.in文件的路径，创建等量的文件夹##########
def mkdir(path):
    lenth = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.in_pa'):
                lenth += 1
    for i in range(1,lenth+1):
        new_dir = path + '\\'+str(i).rjust(2,'0')
        os.mkdir(new_dir)

#######依次输入.in文件的末尾，路径，以及新名字##
def fenpei(endswith, path, newname):
    file_path_list = []
    file_num = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(endswith):
                file_num += 1
                file_path = os.path.join(root, filename)
                file_path_list.append(file_path)
                #filename_list.append(filename)
    for i in range(1,file_num+1):
        new_dir = path +'\\'+ str(i).rjust(2,'0')
        copy(file_path_list[i-1], new_dir+'\\' + newname)

########输入xyz文件的路径，依次输出原子类型数量，原子类型#####
def Type_num(xyz_path):
    f5 = open(xyz_path)
    line = f5.readlines()
    type1 = line[2].split()[0]
    type1_num, type2_num = 0 , 0
    for i in range(2,len(line)):
        if line[i].split()[0] != type1:
            type2_num += 1
            type2 = line[i].split()[0]
        else :
            type1_num += 1
    if type2_num == 0:
        return 1, type1, type1_num
    else:
        return 2, type1, type1_num, type2, type2_num
       
###########（2种原子）输入Type_num函数，依次输出Local_component1,Local_component2, Nv#####
def cluster_information2(type_num_function):
    Atom1_Type, Atom2_Type = type_num_function[1], type_num_function[3]
    type1_num, type2_num = type_num_function[2], type_num_function[4]
    if Atom1_Type in ['As', 'Ge', 'P', 'Si']:
        Local_component1 = 'p'
    elif Atom1_Type in ['B', 'N', 'H', 'O', 'Li', 'Ga', 'C']:
        Local_component1 = 's'
    if Atom1_Type in ['H', 'O']:
        valence_electron_num1 = 1
    elif Atom1_Type in ['B', 'Ga']:
        valence_electron_num1 = 3
    elif Atom1_Type in ['Ge', 'Si', 'C']:
        valence_electron_num1 = 4
    elif Atom1_Type in ['As', 'N', 'P']:
        valence_electron_num1 = 5
    elif Atom1_Type in ['O']:
        valence_electron_num1 = 6

    if Atom2_Type in ['As', 'Ge', 'P', 'Si']:
        Local_component2 = 'p'
    elif Atom2_Type in ['B', 'N', 'H', 'O', 'Li', 'Ga', 'C']:
        Local_component2 = 's'
    if Atom2_Type in ['H', 'O']:
        valence_electron_num2 = 1
    elif Atom2_Type in ['B', 'Ga']:
        valence_electron_num2 = 3
    elif Atom2_Type in ['Ge', 'Si', 'C']:
        valence_electron_num2 = 4
    elif Atom2_Type in ['As', 'N', 'P']:
        valence_electron_num2 = 5
    elif Atom2_Type in ['O']:
        valence_electron_num2 = 6

    Nv = (type1_num*valence_electron_num1 + type2_num*valence_electron_num2)/2
    return Local_component1,Local_component2, Nv


#atom = 'B'####修改原子类型####
#dir_path = r'C:\Users\dell\Desktop\mag\occupation_num_test\xyz_mag\\' +atom+ r'\\no_mag\\0-20'#xyz文件的路径
dir_path = r"The path of xyz dir"
#out_path = r'C:\Users\dell\Desktop\GW_replace_test\0-20_no_mag\\' +atom #输出的GW输入文件的路径
out_path = r'The path of GW input files'  #输出的GW输入文件的路径

if not os.path.exists(out_path):
    os.mkdir(out_path)

parsec_path = open(r"The path of parsec.in_ref","r")#参考的输入文件路径
parsec_content = parsec_path.readlines()
rgwbs_path = open(r'The path of rgwbs.in_ref','r')#参考的输入文件路径
rgwbs_content = rgwbs_path.readlines()

for root, dirs, files in os.walk(dir_path):
    for filename in files:
        if filename.endswith('.xyz'):
            xyz_path = os.path.join(root, filename)
            f3 = open(xyz_path)
            file_name = xyz_path.split("\\")[-1]
            xyz_content = f3.readlines()
            B_S_R = Boundary_Sphere_Radius(xyz_path)
            
            if Type_num(xyz_path)[0] == 1:
                cluster_infor = cluster_information(Type_num(xyz_path))
                print(cluster_information(Type_num(xyz_path))[-1])
                all_parameter = parameter(cluster_information(Type_num(xyz_path))[-1])
            elif Type_num(xyz_path)[0] == 2:
                cluster_infor = cluster_information2(Type_num(xyz_path))
                print(cluster_information2(Type_num(xyz_path))[-1])
                all_parameter = parameter(cluster_information2(Type_num(xyz_path))[-1])
            with open(out_path+'\\'+'shunxu.txt',"a+") as f4:
                f4.write(filename+'\n')

            with open(out_path+'\\'+file_name[0:-4]+'.in_pa',"w+") as f2:
                f2.write('#'+file_name+'\n')
                f2.write('Boundary_Sphere_Radius: '+ B_S_R +'\n')

                for i in range(2,6):
                    f2.write(str(parsec_content[i]))
                
                f2.write('States_Num: '+ all_parameter[1]+'\n')
                
                for i in range(7,11):
                    f2.write(str(parsec_content[i]))
                
                f2.write('Atom_Types_Num: '+str(Type_num(xyz_path)[0]) +'\n')
                if Type_num(xyz_path)[0] == 1:
                    f2.write('Atom_Type: '+ Type_num(xyz_path)[1]+'\n')
                    f2.write('Local_component: '+ cluster_infor[1]+ '\n'+'\n')
                    f2.write('begin Atom_Coord'+ '\n')

                    for i in range(2,len(xyz_content)):
                        xyz = xyz_content[i]
                        f2.write('    '+str(xyz.split()[1])+'    '+str(xyz.split()[2])+'    '+str(xyz.split()[3]) + '\n')
                    f2.write('end Atom_Coord')
                if Type_num(xyz_path)[0] == 2:
                    f2.write('Atom_Type: '+ str(Type_num(xyz_path)[1])+'\n')
                    f2.write('Local_component: '+ cluster_infor[0]+ '\n'+'\n')
                    f2.write('begin Atom_Coord'+ '\n')
                    for i in range(2, len(xyz_content)):
                        if xyz_content[i].split()[0] == Type_num(xyz_path)[1]:
                            xyz = xyz_content[i]
                            f2.write('    '+str(xyz.split()[1])+'    '+str(xyz.split()[2])+'    '+str(xyz.split()[3]) + '\n')
                    f2.write('end Atom_Coord'+'\n\n')

                    f2.write('Atom_Type: '+ str(Type_num(xyz_path)[3])+'\n')
                    f2.write('Local_component: '+ cluster_infor[1]+ '\n'+'\n')
                    f2.write('begin Atom_Coord'+ '\n')
                    for i in range(2, len(xyz_content)):
                        if xyz_content[i].split()[0] == Type_num(xyz_path)[3]:
                            xyz = xyz_content[i]
                            f2.write('    '+str(xyz.split()[1])+'    '+str(xyz.split()[2])+'    '+str(xyz.split()[3]) + '\n')
                    f2.write('end Atom_Coord')

            HOMO = math.ceil(float(cluster_infor[-1]))
            LUMO = HOMO + 1
            with open(out_path+'\\'+file_name[0:-4]+'.in_rg',"w+") as f3:
                f3.write('distribute_representations  1'+'\n')
                for i in range(1, 9):
                    if i != 3:
                        f3.write(rgwbs_content[i])
                    else:
                        f3.write('distribute_wavefunctions 96'+'\n')
                        
                f3.write('num_isdf_points  '+ all_parameter[0]+'\n')
                for i in range(10,13):
                    f3.write(rgwbs_content[i])
                f3.write('range 1 '+ '%s' %HOMO+'\n')
                for i in range(14,16):
                    f3.write(rgwbs_content[i])
                f3.write('range '+'%s'%LUMO+' '+all_parameter[-1]+'\n')
                for i in range(17,19):
                    f3.write(rgwbs_content[i])     
                f3.write('max_number_states  '+ all_parameter[-1]+'\n')
                for i in range(20,25):
                    f3.write(rgwbs_content[i])
                f3.write('range '+ '%s' %HOMO+' '+'%s'%LUMO+'\n')
                f3.write('end diag')


mkdir(out_path)
fenpei('.in_pa', out_path, 'parsec.in')
fenpei('.in_rg', out_path, 'rgwbs.in')