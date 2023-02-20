## 一步到位，生成vasp结构优化所有的输入文件。
## 需要改的参数：xyz文件夹路径，是否带电，赝势文件不需要改（shell脚本里有）

from FormatsToXyz import FormatsConversion
import shutil 
from incar_generate import write_incar
import os
from potcar_generate import *


def mymovefile(srcfile,dstpath,newname):    #src=source, dst=destination
                        # 移动函数
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(srcfile)             # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)                       # 创建路径
        shutil.move(srcfile, os.path.join(dstpath,newname))          # 移动文件
        print ("move %s -> %s"%(srcfile, dstpath + "\\"+newname))

########输入刚生成的.vasp文件的路径，创建等量的文件夹##########
def mymkdir(path):
    lenth = 0
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.vasp'):
                lenth += 1
    for i in range(1,lenth+1):
        new_dir = path + '\\'+str(i).rjust(2,'0')
        os.mkdir(new_dir)

ion_num =  0     ##需要修改，不带电则设置为0, 阴离子anion(-)填正数，阳离子cation(+)填负数。
xyz_data_dir = r'C:\Users\dell\Desktop\ClusterDB_Second_Edition\团簇组装体系\Co6Se8[C60]2'  


##使用USR筛选后的结构文件夹
vasp_optfile_dir = xyz_data_dir.replace("ClusterDB_Second_Edition","团簇数据库_input")
incar_path = r'C:\Users\dell\Desktop\lxa_python\INCAR_opt' ##incar参考文件

if not os.path.exists(vasp_optfile_dir):
    os.makedirs(vasp_optfile_dir)


vasp_path_list = []
for root, dirs, files in os.walk(xyz_data_dir):
    for filename in files:
        if filename.endswith(".xyz"):
            xyz_path = os.path.join(root, filename)
            vasp_path = xyz_path.replace("ClusterDB_Second_Edition","团簇数据库_input")
            vasp_path = os.path.join(vasp_optfile_dir,filename[:-3]+"vasp")
            vasp_path_list.append(vasp_path)## 方便后续文件的移动
            FormatsConversion.XyzToVasp(xyz_path,vasp_path) ##先放在大的文件夹下，后续再创建

mymkdir(vasp_optfile_dir) ##创建文件夹

n = 1
for vaspPath in vasp_path_list: ##将incar和poscar放到数字文件夹中
    num_dir = os.path.join(vasp_optfile_dir,str(n).rjust(2,'0'))
    poscar_path = os.path.join(num_dir,"POSCAR")
    new_incar_path = os.path.join(num_dir,"INCAR")
    mymovefile(vaspPath, num_dir,"POSCAR")
    write_incar(incar_path,new_incar_path,poscar_path,ion_num) ##若ion_num=0,则不写incar？
    n += 1
    species_list = read_species_from_poscar(poscar_path)
    print("POTCAR包含元素: ",species_list)
    potcar_path = os.path.join(num_dir,"POTCAR")
    gen_potcar(species_list, potcar_path)
