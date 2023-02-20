# coding=utf-8

import numpy as np
import os 
import xml
from shutil import copy


class FormatsConversion:

    def CarToXyz(car_path, xyz_path):
        '''.car文件转换为.xyz文件'''
        f1 = open(car_path)
        lines = f1.readlines()
        with open(xyz_path , 'w+') as xyz:
            n = 0
            for line in lines:
                if len(line.split()) == 9:
                    n += 1
            xyz.write(str(n) + '\n')
            for line in lines:
                if len(line.split()) == 9:
                    coord_x = float(line.split()[1])
                    coord_y = float(line.split()[2])
                    coord_z = float(line.split()[3])
                    atom_name = line.split()[-2]
                    xyz.write("\n%s  %9.9f   %9.9f   %9.9f"%(atom_name,coord_x,coord_y,coord_z))

    def XsdToXyz(xsd_path, xyz_path):
        '''.xsd文件转换为.xyz文件'''
        xmldom = xml.dom.minidom.parse(xsd_path)  #读取文件路径
        xmlroot = xmldom.documentElement  # xml的第一个根节点
        Atom3d = xmlroot.getElementsByTagName('Atom3d')  # 操作的是Atom3d节点，这里getElementByTag可以操作xml中所有节点tag，
                                                            #不论是子节点还是根节点，还是子子节点...
        a=[]
        for node in Atom3d:  # 遍历Atom3d节点下内容
            atom_name_with_number = node.getAttribute('Name')
            atom_name =  ''.join(filter(str.isalpha, atom_name_with_number)) #保留字符串中的字母
            if atom_name != 'As':
                atom_name = node.getAttribute('Components')
            coord = node.getAttribute('XYZ')
            b = atom_name,coord
            b_list = list(b)
            if atom_name != '':
                a.append(b_list)
        data = np.array(a)

        with open(xyz_path , 'w+') as xyz:
            xyz.write(str(len(data)))
            xyz.write("\n")
            for line in data:
                atom_name = line[0]
                coord = line[1].split(',')
                coord_x = float(coord[0])
                coord_y = float(coord[1])
                coord_z = float(coord[2])
                xyz.write("\n%s  %9.9f   %9.9f   %9.9f"%(atom_name,coord_x,coord_y,coord_z))

    def MolToXyz(mol_path, xyz_path):
        '''.mol文件转换为.xyz文件'''
        f1 = open(mol_path)
        lines = f1.readlines()
        atom_num = lines[3].split()[0]
        with open(xyz_path , 'w+') as xyz:
            xyz.write(str(atom_num)+'\n')
            for i in range(4, int(atom_num)+4):
                atom_name = lines[i].split()[3]
                coord_x = float(lines[i].split()[0])
                coord_y = float(lines[i].split()[1])
                coord_z = float(lines[i].split()[2])
                xyz.write("\n%s  %9.9f   %9.9f   %9.9f"%(atom_name,coord_x,coord_y,coord_z))

    def MsiToXyz(msi_path, xyz_path):
        '''.msi文件转换为.xyz文件'''
        f1 = open(msi_path)
        lines = f1.readlines()
        atom_name = []
        coord_x, coord_y, coord_z = [],[],[]
        #for i in range(len(lines)):
        #    if 'ACL' in lines[i]:
        #        atom_name.append(lines[i].split()[-1][:-2])
        #    if 'XYZ' in lines[i]:
        #        coord_x.append(float(lines[i].split()[3][1:]))
        #        coord_y.append(float(lines[i].split()[4]))
        #        coord_z.append(float(lines[i].split()[5][:-2]))

        
        test = 0
        for i in range(len(lines)):

            if 'ACL' in lines[i]:
                atom_name.append(lines[i].split()[-1][:-2])

                for j in range(i, i+5):
                    if 'XYZ' in lines[j].split() :
                        coord_x.append(float(lines[j].split()[3][1:]))
                        coord_y.append(float(lines[j].split()[4]))
                        coord_z.append(float(lines[j].split()[5][:-2])) 
                        test = 123#说明存在XYZ
                if test != 123:
                    print("test")
                    coord_x.append(float(0))
                    coord_y.append(float(0))
                    coord_z.append(float(0))   
            test = 0
                              

        with open(xyz_path , 'w+') as xyz:
            atom_num = len(atom_name)
            #print(atom_num)
            xyz.write(str(atom_num)+'\n')
            try:
                for i in range(atom_num):
                    xyz.write("\n%s  %9.9f   %9.9f   %9.9f"%(atom_name[i],coord_x[i],coord_y[i],coord_z[i]))
            except:
                print(msi_path)
                print('msi源文件有问题')
                xyz.write('msi源文件有问题')
    
    def CifToXyz(cif_path, xyz_path):
        '''.cif文件转换为.xyz文件'''
        f1 = open(cif_path)
        lines = f1.readlines()
        atom_name, coord_x, coord_y, coord_z = [],[],[],[]
        for line in lines:
            if len(line.split()) == 2:   ## 这里默认坐标轴之间垂直，有待修正!!
                if line.split()[0] == '_cell_length_a':
                    cell_length_x = line.split()[1]
                elif line.split()[0] == '_cell_length_b':
                    cell_length_y = line.split()[1]
                elif line.split()[0] == '_cell_length_c':
                    cell_length_z = line.split()[1]
                

            elif len(line.split()) == 8:
                atom_name.append(line.split()[-1])
                coord_x.append(float(line.split()[-6])*float(cell_length_x))
                coord_y.append(float(line.split()[-5])*float(cell_length_y))
                coord_z.append(float(line.split()[-4])*float(cell_length_z))
        with open(xyz_path , 'w+') as xyz:
            xyz.write(str(len(atom_name))+'\n')
            for i in range(len(atom_name)):
                xyz.write("\n%s  %9.9f   %9.9f   %9.9f"%(atom_name[i],coord_x[i],coord_y[i],coord_z[i]))

    def DelteErrorCodes(path): ## 暂时没想到好办法，先用穷举法。
        '''部分xsd文件中有乱码，调用本函数删除乱码。'''
        with open(path,'r+',encoding="utf-8") as filetxt:
            lines = filetxt.readlines()
            filetxt.seek(0)
            for line in lines:
                if "�" in line:
                    lines="".join(lines).replace("�",'1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
                if '' in line:
                    lines="".join(lines).replace('','1')
            filetxt.write("".join(lines))

    def XyzToVasp(xyz_path, vasp_path):
        f1 = open(xyz_path)
        lines = f1.readlines()
        element_list ,element_num,element_order = [], [], []
        #coord_x, coord_y, coord_z = [], [], []
        atom_num = int(lines[0].split()[0])
        coord = np.zeros([atom_num,3])
        n, m = 0, 0
        for line in lines:
            if len(line.split()) == 4 and n > 1:
                if line.split()[0] not in element_list:
                    element_list.append(line.split()[0])
                    element_num.append(0)
                #else:
                #    element_num[-1] += 1
                element_order.append(line.split()[0])
                for i in range(3):
                    coord[m][i] = float(line.split()[i+1])
                m += 1
            n += 1

        for ele in element_order:
            for index in range(len(element_list)):
                #print(ele, element_list[index])
                if ele == element_list[index]:
                    element_num[index] += 1

        _r = 20 ## 扩胞的大小
        max = np.amax(coord, axis=0)
        min = np.amin(coord, axis=0)
        boundary = max-min
        max_boundary = np.max(boundary)
        for i in range(3):
            if boundary[i] == 0:
                boundary[i] = max_boundary
        xr, yr, zr = max[0]-min[0]+_r, max[1]-min[1]+_r, max[2]-min[2]+_r
        x_centroid, y_centroid, z_centroid = np.average(coord[:,0])/boundary[0], np.average(coord[:,1])/boundary[1], np.average(coord[:,2])/boundary[2]
        x_move , y_move , z_move = 0.5 - x_centroid , 0.5 - y_centroid , 0.5 - z_centroid 

        with open(vasp_path, 'w+') as f2:
            f2.write(xyz_path.split('\\')[-1] + '\n')
            f2.write('1.0' + '\n')
            f2.write('       %15.9f        %15.9f        %15.9f\n'%(xr,0,0))
            f2.write('       %15.9f        %15.9f        %15.9f\n'%(0,yr,0))
            f2.write('       %15.9f        %15.9f        %15.9f\n'%(0,0,zr))
            for i in range(len(element_num)):
                f2.write("   "+str(element_list[i]))
            f2.write('\n')
            for i in range(len(element_num)):
                f2.write('   '+str(element_num[i]))
            f2.write('\nCartesian\n')
            for i in element_list:
                for j in range(len(element_order)):
                    if i == element_order[j]:
                        f2.write('     %s         %s         %s\n' 
                        %((float(coord[j][0])/boundary[0]+x_move)*(max[0]-min[0])+xr/2,\
                            (float(coord[j][1])/boundary[1]+y_move)*(max[1]-min[1])+yr/2,\
                                (float(coord[j][2])/boundary[2]+z_move)*(max[2]-min[2])+zr/2))
            

    def Xyz_repair(xyz_path):
        f1 = open(xyz_path)        
        pass


    def XyzToGjf(xyz_path, gjf_path): ## gauss
        f1 = open(xyz_path)
        lines = f1.readlines()
        atom_name, coord_x, coord_y, coord_z = [],[],[],[]
        for line in lines:
            if len(line.split()) == 4:
                atom_name.append(line.split()[0])
                coord_x.append(line.split()[1])
                coord_y.append(line.split()[2])
                coord_z.append(line.split()[3])
        with open(gjf_path, 'w+') as gjf:
            gjf.write('%nprocshared=32\n')
            gjf.write('%mem=128GB\n')
            gjf.write('#p  opt b3lyp/6-311+G(d,p) em=gd3\n\n')
            filename = xyz_path.split('\\')[-1]
            gjf.write(filename + '\n\n')
            gjf.write('1    1\n')
            for i in range(len(atom_name)):
                gjf.write("\n%s  %9.9f   %9.9f   %9.9f"%(atom_name[i],coord_x[i],coord_y[i],coord_z[i]))



if __name__=="__main__":
    ###  将含有各种格式文件的数据库文件夹统一转换为xyz形式，放在另一个文件夹中。
    db_path = r'C:\Users\dell\Desktop\团簇数据库\团簇组装体系\Na6Pb'
    db_xyz_path = r'C:\Users\dell\Desktop\团簇数据库_xyz\团簇组装体系\Na6Pb'  

    for root, dirs, files in os.walk(db_path):
        for filename in files:

            if filename.endswith('.xsd'): # 只匹配后缀名为'.xsd'的文件
                xsd_path = os.path.join(root, filename)
                xyz_path = root.replace(db_path,db_xyz_path)
                if not os.path.exists(xyz_path):
                    os.makedirs(xyz_path)
                xyz_file = os.path.join(xyz_path, filename.split('.')[-2]+'.xyz')
                try:
                    FormatsConversion.XsdToXyz(xsd_path, xyz_file)
                except:
                    try:
                        FormatsConversion.DelteErrorCodes(xsd_path)
                        FormatsConversion.XsdToXyz(xsd_path, xyz_file)
                    except:
                        print("xsd文件有错误！")
                        pass

            elif filename.endswith('.mol'): # 只匹配后缀名为'.mol'的文件
                mol_path = os.path.join(root, filename)
                xyz_path = root.replace(db_path,db_xyz_path)
                if not os.path.exists(xyz_path):
                    os.makedirs(xyz_path)
                xyz_file = os.path.join(xyz_path, filename.split('.')[-2]+'.xyz')
                FormatsConversion.MolToXyz(mol_path, xyz_file)

            elif filename.endswith('.car'): # 只匹配后缀名为'.car'的文件
                car_path = os.path.join(root, filename)
                xyz_path = root.replace(db_path,db_xyz_path)
                if not os.path.exists(xyz_path):
                    os.makedirs(xyz_path)
                xyz_file = os.path.join(xyz_path, filename.split('.')[-2]+'.xyz')
                FormatsConversion.CarToXyz(car_path, xyz_file)

            elif filename.endswith('.msi'): # 只匹配后缀名为'.msi'的文件
                msi_path = os.path.join(root, filename)
                xyz_path = root.replace(db_path,db_xyz_path)
                if not os.path.exists(xyz_path):
                    os.makedirs(xyz_path)
                xyz_file = os.path.join(xyz_path, filename.split('.')[-2]+'.xyz')
                FormatsConversion.MsiToXyz(msi_path, xyz_file)

            elif filename.endswith('.cif'): # 只匹配后缀名为'.cif'的文件
                cif_path = os.path.join(root, filename)
                xyz_path = root.replace(db_path,db_xyz_path)
                if not os.path.exists(xyz_path):
                    os.makedirs(xyz_path)
                xyz_file = os.path.join(xyz_path, filename.split('.')[-2]+'.xyz')
                FormatsConversion.CifToXyz(cif_path, xyz_file)

            else: ## 将原有.xyz文件和.pdf复制到新文件夹中
                source_path = os.path.join(root, filename)
                xyz_path = root.replace(db_path,db_xyz_path)
                if not os.path.exists(xyz_path):
                    os.makedirs(xyz_path)
                copy(source_path, os.path.join(xyz_path, filename))

            


