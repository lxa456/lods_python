## USR方法，判断两个结构的相似度。

import os 
import numpy as np 


class USR:

    def read_xyz(xyz_path):  ##读取.xyz文件，返回struc
        '''读取.xyz文件，返回struc'''
        f1 = open(xyz_path)
        lines = f1.readlines()
        try: ## 有的xyz文件有问题，如单质团簇中的Na
            atom_num = int(lines[0].split()[0])
            coord = np.zeros([atom_num, 3])

            for i in range(atom_num):
                for j in range(3):
                    coord[i][j] = float(lines[i+2].split()[j+1])
        except ValueError:
            atom_num = 0

            for line in lines:
                if len(line.split()) == 4 :
                    try:
                        a = float(lines[atom_num].split()[1])
                        atom_num += 1
                    except:
                        pass

            coord = np.zeros([atom_num, 3])
            n=0
            for line in lines:
                for j in range(3):
                    coord[n][j] = float(lines[n].split()[j+1])   
                n+=1         
        return coord

    def ctd(struc):
        ctd = np.zeros(3)
        atom_num = struc.shape[0]
        sum_x, sum_y, sum_z = 0, 0, 0
        for i in range(atom_num):
            sum_x += float(struc[i][0])
            sum_y += float(struc[i][1])
            sum_z += float(struc[i][2])
        ave_x, ave_y, ave_z = sum_x/atom_num, sum_y/atom_num, sum_z/atom_num
        ctd[0], ctd[1], ctd[2] = ave_x, ave_y, ave_z 
        return ctd

    def distance(position1, position2):
        '''输入两个原子的位置（向量），返回两个原子之间的距离'''
        distance = 0
        for i in range(3):
            distance += (position1[i]-position2[i])**2
        return distance**0.5

    def Farthest_distance(position1, struc):
        '''输入某个原子位置和所有原子位置，返回和它最远的原子的序号'''
        Farthest_distance = 0
        atom_num = struc.shape[0]
        for i in range(atom_num):
            position_i = struc[i]
            res = USR.distance(position1,position_i)
            if res > Farthest_distance:
                Farthest_distance = res
                res_i = i
        return struc[res_i] 
        

    def Nearest_distance(position1, struc):
        '''输入位置和所有原子位置，返回和它最近的原子的序号'''
        Nearest_distance = 10
        atom_num = struc.shape[0]
        for i in range(atom_num):
            position_i = struc[i]
            res = USR.distance(position1,position_i)
            if res < Nearest_distance:
                Nearest_distance = res
                res_i = i
   
        return struc[res_i] 
        

    def distance_list(position1, struc):
        distance_list = [] 
        atom_num = struc.shape[0]
        for i in range(atom_num):
            position_i = struc[i]
            #print('test')
            distance = USR.distance(position1,position_i)
            #print(distance)
            distance_list.append(distance)
            if 0 in distance_list:
                distance_list.remove(0)
        return distance_list


    def var3(x=None):
        mid = np.mean((x - x.mean()) ** 3)
        return abs(mid)      

    def M_vector(path_or_struc):
        if type(path_or_struc) == np.ndarray:
            struc = path_or_struc
        else:
            struc = USR.read_xyz(path_or_struc)

        atom_num = struc.shape[0]

        ctd_position = USR.ctd(struc) ## 分子中心 
        cst_position = USR.Nearest_distance(ctd_position,struc) ## 距离ctd最近的原子
        fct_position = USR.Farthest_distance(ctd_position,struc) ## 距离ctd最远的原子
        ftf_position = USR.Farthest_distance(fct_position,struc) ## 距离fct最远的原子

        #print(ctd_position,cst_position,fct_position,ftf_position)

        miu1_ctd = np.array(USR.distance_list(ctd_position,struc)).mean()
        miu2_ctd = (np.array(USR.distance_list(ctd_position,struc)).var())
        miu3_ctd = USR.var3(np.array(USR.distance_list(ctd_position,struc)))
        #print('ctd')
        #print(USR.distance_list(ctd_position,struc))

        miu1_cst = np.array(USR.distance_list(cst_position,struc)).mean()
        miu2_cst = (np.array(USR.distance_list(cst_position,struc)).var())
        miu3_cst = USR.var3(np.array(USR.distance_list(cst_position,struc))) 

        #print(USR.distance_list(cst_position,struc))
        #print(struc)
        #print(np.array(USR.distance_list(cst_position,struc)))

        miu1_fct = np.array(USR.distance_list(fct_position,struc)).mean()
        miu2_fct = (np.array(USR.distance_list(fct_position,struc)).var())
        miu3_fct = USR.var3(np.array(USR.distance_list(fct_position,struc)))

        miu1_ftf = np.array(USR.distance_list(ftf_position,struc)).mean()
        miu2_ftf = (np.array(USR.distance_list(ftf_position,struc)).var())
        miu3_ftf = USR.var3(np.array(USR.distance_list(ftf_position,struc)))

        M1 = np.array([miu1_ctd,miu2_ctd,miu3_ctd, \
                        miu1_cst,miu2_cst,miu3_cst,\
                        miu1_fct,miu2_fct,miu3_fct, \
                        miu1_ftf,miu2_ftf,miu3_ftf])

        return M1

    def similarity(M1,M2):
        assert M1.shape[0] == 12
        assert M2.shape[0] == 12
        M = 0
        for i in range(12):
            M += abs(M1[i] - M2[i])
        S = 1/(1+M/12)
        return S


if __name__ == '__main__': ## 使用方法
    xyz_path1 = r''
    struc_A = USR.read_xyz(xyz_path1)
    xyz_path2 = r''
    struc_B = USR.read_xyz(xyz_path2)   
    M1 = USR.M_vector(struc_A)
    M2 = USR.M_vector(struc_B)
    print(USR.similarity(M1,M2))
