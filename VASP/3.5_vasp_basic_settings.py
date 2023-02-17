'''
Author: Xueao Li @ DUT
Date: 2022-12-20 15:16:55
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-17 14:40:16
Description: 统一VASP数据的格式。

Copyright (c) 2022 by li xueao 11076446+li-xueao@user.noreply.gitee.com, All Rights Reserved. 
'''

from ase.db import connect
from ase import Atoms
import os, sqlite3


#db1_file = input("Please enter the  first database file name (including the file suffix)")
#db2_file = input("Please enter the second database file name (including the file suffix)")
db_file = "DATABASE.db"
#os.system("ase convert "+db1_file+" "+db2_file+" "+db3_file)
db = connect(db_file)

# metadata 设置
# 修改此处的 ‘default_columns’即可修改网页的默认显示列
# 数据库中没有对应的Keys and Values 时可能会报错。
db.metadata = {
    'title': 'Computational Cluster Database (A subdataset of LODS)',
    'key_descriptions':
        {'Reference': ('Reference', 'DOI',''),\
            'TOTEN':('TOTEN','the DFT total energy (useful for comparing clusters with the same number of atoms)','eV'),\
                 'HOMO_DFT':('HOMO_DFT', 'The energy of highest occupied molecular orbital, calculated with DFT','eV'),\
                     'LUMO_DFT': ('LUMO_DFT', 'The energy of lowest occupied molecular orbital, calculated with DFT', 'eV'),\
                        'GAP_DFT':('GAP_DFT', 'The HOMO-LUMO Gap, calculated with DFT', 'eV'),\
                             'HOMO_GW':('HOMO_GW', 'The energy of highest occupied molecular orbital, calculated with the GW approximation', 'eV'),\
                                 'LUMO_GW':('LUMO_GW', 'The energy of lowest occupied molecular orbital, calculated with the GW approximation', 'eV'),\
                                    'GAP_GW':('GAP_GW','The HOMO-LUMO Gap, calculated with the GW approximation', 'eV'),\
                                        'Relaxed':('Relaxed','Relaxed', ''), \
                                            'Max_Force':("Max_Force", 'Maximum force for structural relaxation','eV/Ang'),\
                                            'N_ele':('N_ele', 'number of valence electrons (included in the calculation)', '')},

        'default_columns': ['id', 'formula','natoms','GAP_GW']}

conn = sqlite3.connect(db_file)
print ("数据库打开成功")

c = conn.cursor()
c.execute('SELECT id from systems')
line_num = len(c.fetchall()) #获取行数

for i in range(1,line_num+1):
    c.execute("UPDATE systems set username = 'Computational condensed matter physics group, Dalian Unverisity of Technology' where ID="+str(i))
    c.execute("UPDATE systems set calculator = 'Vienna Ab initio Simulation Package' where ID="+str(i))

conn.commit()
conn.close()