##有的团簇体系带电，INCAR里的NELECT是由原子数决定，用本脚本生成特定NELECT的INCAR。

periodic_table = {'H':1, 'He':2,'Hf':4, 'Li':1, 'Be':2, 'B':3, 'C':4, 'N':5, 'O':6, 'F':7, 'Ne':8, 'Na':1, 'Mg':2, 'Al':3, 'Si':4, 'P':5, 'S':6, 'Cl':7, 'Ar':8,
                  'K':1, 'Ca':2, 'Sc':3, 'Ti':4, 'V':5, 'Cr':6, 'Mn':7, 'Fe':8, 'Co':9, 'Ni':10, 'Cu':11, 'Zn':12, 'Ga':3, 'Ge':4, 'As':5, 'Se':6, 'Br':7, 
                  'Kr':8, 'Rb':1, 'Sr':2, 'Y':3, 'Zr':4, 'Nb':5, 'Mo':6, 'Te':7, 'Ru':8, 'Rh':9, 'Pd':10, 'Ag':11, 'Cd':12, 'In':3, 'Sn':4, 'Sb':5, 'Te':6, 
                  'I':7, 'Xe':8, 'Cs':1, 'Ba':2, 'La':3, 'Ce':4, 'Pr':5, 'Nd':6, 'Pm':7, 'Sm':8, 'Eu':9, 'Gd':10, 'Tb':11, 'Dy':12, 'Ho':13, 'Er':14, 'Tm':15, 
                   'W':8,'Au':11}
##  元素对应的价电子个数。


def Nelect(poscar_path):

    f1 = open(poscar_path)
    lines = f1.readlines()
    element_list = []
    element_num_list = []
    Nelect = 0
    for i in range(len(lines[5].split())):
        element_list.append(lines[5].split()[i])
        element_num_list.append(int(lines[6].split()[i]))
    for i in range(len(element_list)):
        Nelect += periodic_table[element_list[i]]*element_num_list[i]

    return Nelect

def write_incar(incar_path, new_incar_path, poscar_path,ion):
    '''依次输入incar参考文件路径，生成incar的路径，poscar路径，带电量。
    python脚本中执行了本函数后，要注意提交任务的shell脚本是否会覆盖INCAR'''
    f1 = open(incar_path)
    lines1 = f1.readlines()
    with open(new_incar_path,'w+') as f2:
        n = 0
        for line in lines1:
            n += 1
            if n != 16:
                f2.write(line)
            elif ion == 0:
                pass
            else:
                f2.write("\n   NELECT  = "+str(Nelect(poscar_path)+ion)+"\n\n")



if __name__=="__main__":

    vasp_path = r'C:\Users\dell\Desktop\C60_ML\7-14\mg2c60\ML_c60.vasp'
    incar_path = r'C:\Users\dell\Desktop\lxa_python\INCAR' ##incar参考文件
    new_incar_path = r'C:\Users\dell\Desktop\lxa_python\INCAR_test'
    print(Nelect(vasp_path))

    write_incar(incar_path,new_incar_path,vasp_path,-1)