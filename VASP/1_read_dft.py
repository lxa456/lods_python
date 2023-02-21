# 需要完成的任务：
# 1.将CONTCAR转成 .xyz文件，统一放在一个文件夹里(xyz_relaxed)
# 2.OUTCAR中需要提取的信息：TOTEN, Max_Force, N_ele
# 3.EIGENVAL中信息：HOMO_DFT、LUMO_DFT、GAP_DFT 
# 4.再从.xyz文件中提取Point_Group，filename 
# 5.需要额外加入的信息：Reference(可以先不弄), user(可以最后统一用sqlite改)
# 最后，将所有信息存在list里，用pandas存在csv文件里，和xyz_relaxed同一目录。

#目录结构：As - DFT
#            L DFT_data - xyz_relaxed - *.xyz
#                       L dft_info.csv

import os
import pandas as pd 


def Vasp2xyz(vasp_path, xyz_dir) -> None:
    f1 = open(vasp_path)
    lines = f1.readlines()
    xyz_filename = lines[0].split()[0]
    lattice_para_x = float(lines[2].split()[0])
    lattice_para_y = float(lines[3].split()[1])
    lattice_para_z = float(lines[4].split()[2])
    atom_species, atom_num = [], []
    [atom_species.append(i) for i in lines[5].split()]
    [atom_num.append(int(i)) for i in lines[6].split()]
    xyz_path = os.path.join(xyz_dir, xyz_filename)
    with open(xyz_path, "w+") as xyz:
        xyz.write(str(sum(atom_num))+"\n\n")
        j = 8 #vasp文件中坐标开始的行数
        for i in range(len(atom_num)):
            for _ in range(atom_num[i]):
                x_xyz = float(lines[j].split()[0])*lattice_para_x
                y_xyz = float(lines[j].split()[1])*lattice_para_y
                z_xyz = float(lines[j].split()[2])*lattice_para_z
                xyz.write('%s %11.9f    %11.9f    %11.9f\n'\
                    %(atom_species[i], x_xyz, y_xyz, z_xyz))
                j+=1


class read_contcar():
    def __init__(self, contcar_path) -> None:
        self.contcar_path = contcar_path
    def filename(self) -> str:
        f1 = open(self.contcar_path)
        lines = f1.readlines()
        xyz_filename = lines[0].split()[0]
        return xyz_filename


class read_outcar():
    def __init__(self, outcar_path) -> None:
        self.outcar_path = outcar_path
    def F_max(self) -> float:
        f1 = open(self.outcar_path)
        lines = f1.readlines()
        for i in range(len(lines)):
            if "TOTAL-FORCE (eV/Angst)" in lines[i]:
                start_line_num = i+2
            elif "total drift:" in lines[i]:
                end_line_num = i-1
        force_list = []
        [force_list.append((float(lines[i].split()[3])**2+\
                                float(lines[i].split()[4])**2+\
                                    float(lines[i].split()[5])**2)**0.5) \
                                        for i in range(start_line_num, end_line_num)]
        max_force = max(force_list)
        return float("%.7f" %max_force)
    def TOTEN(self) -> float:
        f1 = open(self.outcar_path)
        lines = f1.readlines()
        for line in lines:
            if "  free  energy   TOTEN  =" in line:
                total_energy = float(line.split()[-2])
        return total_energy
    def N_ele(self) -> int():
        f1 = open(self.outcar_path)
        lines = f1.readlines()
        for line in lines:
            if "NELECT =  " in line:
                NELECT = int(float(line.split()[2]))
        return NELECT

class read_eigenval():
    def __init__(self, eigenval_path) -> None:
        self.eigenval_path = eigenval_path
    def HOMO(self) -> float:
        f1 = open(self.eigenval_path)
        lines = f1.readlines()
        print(self.eigenval_path)
        for i in range(8, len(lines)):#这里没有考虑分数占据态，可能以后需要修改。
            #print(float(lines[i].split()[2]))
            if lines[i].split()[2] == "1.000000" or lines[i].split()[2] == "0.500000" or float(lines[i].split()[2]) > 0.8:
                homo = float(lines[i].split()[1])
        return homo
    def LUMO(self) -> float:
        f1 = open(self.eigenval_path)
        lines = f1.readlines()
        for i in range(8, len(lines)):
            if lines[i].split()[2] == "0.000000" or float(lines[i].split()[2]) < 0.2:
                lumo = float(lines[i].split()[1])
                return lumo
    def HOMO_LUMO_GAP(self) -> float:
        lumo = self.LUMO()
        homo = self.HOMO()
        return float("%.4f"  %(lumo-homo))


class read_xyz():
    def __init__(self,xyz_path) -> None:
        self.xyz_path = xyz_path
    def PointGroup(self) -> str:
        import pymatgen.core as mg
        from pymatgen.symmetry.analyzer import PointGroupAnalyzer
        try:
            structure = mg.Molecule.from_file(self.xyz_path)
            finder = PointGroupAnalyzer(structure)
            #print(self.xyz_path, finder.get_pointgroup())
            
            
            return finder.get_pointgroup()
        except:
            print(self.xyz_path)
    def Filename(self) -> str:
        filename = self.xyz_path.split('\\')[-1]
        return filename.split(".")[0]

def cut_path(dirname1, n) -> str: 
    '''剪切路径，如：
    dirname1:"C:\\Users\\dell\\Desktop\\团簇数据库_output\\simple\\Ag\\DFT\\Ag7-20-\\13\\CONTCAR",
    n = 2.  
    return : C:\\Users\\dell\\Desktop\\团簇数据库_output\\simple\\Ag\\DFT\\Ag7-20-
    '''
    head = ''
    for index,value in enumerate(dirname1.split("\\")):
        if index < len(dirname1.split("\\"))-n-1:
            head = head + value +"\\"
        elif index == len(dirname1.split("\\"))-n-1:
            head = head+value
    return head

if __name__ == '__main__':

    ## 先CONTCAR -> *.xyz
    dft_output_path = r"C:\Users\dell\Desktop\团簇数据库_output\binary_dope\4_missing\Mo_at_B10-24\DFT"
    dft_data = dft_output_path.replace("DFT", "DFT_data")
    for root, dirs, files in os.walk(dft_output_path):
        for filename in files:
            if filename == "CONTCAR":
                contcar_path = os.path.join(root, filename)
                xyz_dir = os.path.join(cut_path(contcar_path,2).replace("DFT","DFT_data"), "xyz_relaxed")
                if not os.path.exists(xyz_dir):
                    os.makedirs(xyz_dir)
                print(root)
                Vasp2xyz(vasp_path=contcar_path,xyz_dir=xyz_dir)


    ## OUTCAR & EIGENVAL & CONTCAR(filename)
    max_force, n_ele, total_energy = [],[],[]
    homo, lumo, gap = [],[],[]
    filename_list, point_group_list = [],[]
    for root, dirs, files in os.walk(dft_output_path):
        for filename in files:
            if filename == "OUTCAR":
                outcar_path = os.path.join(root, filename)
                outcar = read_outcar(outcar_path)
                max_force.append(outcar.F_max())
                n_ele.append(outcar.N_ele())
                total_energy.append(outcar.TOTEN())
            if filename == "EIGENVAL":
                eigenval_path = os.path.join(root, filename)
                eigenval = read_eigenval(eigenval_path)
                homo.append(eigenval.HOMO())
                gap.append(eigenval.HOMO_LUMO_GAP())
                lumo.append(eigenval.LUMO())
            if filename == "CONTCAR":
                contcar_path = os.path.join(root, filename)
                contcar = read_contcar(contcar_path)
                xyz_path = os.path.join(cut_path(contcar_path,2).replace("DFT","DFT_data"), "xyz_relaxed",contcar.filename())
                xyz = read_xyz(xyz_path)
                point_group = xyz.PointGroup()
                point_group_list.append(point_group)
                filename_list.append(contcar.filename().split(".")[0])
    csv_path = os.path.join(dft_data, "dft_info.csv")
    # 所有信息汇总：filename, max_force, n_ele, total_energy, \
    # homo(DFT), lumo(DFT), gap(DFT), point_group
    # 有些默认信息还没加：functional:PBE
    Functional_list = ["PBE" for _ in range(len(filename_list))]

    cluster_data = pd.DataFrame({"filename":filename_list, \
        "Max_Force":max_force, "N_ele":n_ele, "TOTEN":total_energy,\
            "HOMO_DFT":homo,"LUMO_DFT":lumo,"GAP_DFT":gap,\
                "Point_Group": point_group_list,\
                "Functional": Functional_list}) #formula_list, atom_num_list, bandgap_list均为list
    cluster_data.to_csv(csv_path, index=False, sep=',') #写入以csv_path为路径的csv文件里
