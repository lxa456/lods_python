'''
Author: Xueao Li @ DUT
Date: 2022-12-20 15:16:55
LastEditors: Xueao Li @ DUT
LastEditTime: 2022-12-20 17:25:39
Description: 合并两个数据库。重点是统一ase database数据的格式。

Copyright (c) 2022 by li xueao 11076446+li-xueao@user.noreply.gitee.com, All Rights Reserved. 
'''

from ase.db import connect
from ase import Atoms
import os, sqlite3


db1_file = input("Please enter the  first database file name (including the file suffix)")
db2_file = input("Please enter the second database file name (including the file suffix)")
db3_file = "DATABASE.db"
os.system("ase convert "+db1_file+" "+db2_file+" "+db3_file)
db = connect(db3_file)
# metadata 设置
# 修改此处的 ‘default_columns’即可修改网页的默认显示列
#db.metadata = {'title': 'Computational Cluster Database (A subdataset of LODS)','key_descriptions':\
#    {'Reference': ('Reference', 'DOI',''),\
#        'TOTEN':('TOTEN','the DFT total energy (useful for comparing clusters with the same number of atoms)',\
#            'eV'), 'HOMO_DFT':('HOMO_DFT', 'Highest occupied state calculated with DFT',''),\
#                 'LUMO_DFT': ('LUMO_DFT', 'Lowest unoccupied state calculated with DFT', ''),\
#                     'GAP_DFT':('GAP_DFT', 'HOMO-LUMO Gap calculated with DFT', ''),\
#                          'HOMO_GW':('HOMO_GW', 'Highest occupied state calculated with GW', ''),\
#                               'LUMO_GW':('LUMO_GW', 'Lowest unoccupied state calculated with GW', ''),\
#                                   'GAP_GW':('GAP_GW','HOMO-LUMO Gap calculated with GW', ''),\
#                                       'Relaxed':('Relaxed','Relaxed', ''),\
#                                            'N_ele':('N_ele', 'number of valence electrons (included in the calculation)', ''),\
#                                                 'Max_Force':("Max_Force", 'the maximum force experienced by each atom (eV/Ang)','eV/Ang'),\
#                                                     'Reference':'DOI', 'HOMO_GW':'Highest occupied state calculated with GW'},\
#                                                         'default_columns': ['id', 'formula', 'calculator','mass','natoms','Point_Group']}

#db.metadata = {'default_columns': ['id', 'formula', 'calculator','mass','natoms','Point_Group']}


#db.metadata = {
#    'title': 'Computational Cluster Database (A subdataset of LODS)',
#    'key_descriptions':
#        {'Reference': ('Reference', 'DOI',''),'TOTEN':('TOTEN','the DFT total energy (useful for comparing clusters with the same number of atoms)','eV'), 'HOMO_DFT':('HOMO_DFT', 'Highest occupied state calculated with DFT','eV'), 'LUMO_DFT': ('LUMO_DFT', 'Lowest unoccupied state calculated with DFT', 'eV'),'GAP_DFT':('GAP_DFT', 'HOMO-LUMO Gap calculated with DFT', 'eV'), 'HOMO_GW':('HOMO_GW', 'Highest occupied state calculated with GW', 'eV'), 'LUMO_GW':('LUMO_GW', 'Lowest unoccupied state calculated with GW', 'eV'),'GAP_GW':('GAP_GW','HOMO-LUMO Gap calculated with GW', 'eV'),'Relaxed':('Relaxed','Relaxed', ''), 'N_ele':('N_ele', 'number of valence electrons (included in the calculation)', '')},
#
#        'default_columns': ['id', 'formula', 'calculator','Point_Group','Reference']}


conn = sqlite3.connect(db3_file)
print ("数据库打开成功")

c = conn.cursor()
c.execute('SELECT id from systems')
line_num = len(c.fetchall()) #获取行数

for i in range(1,line_num+1):
    c.execute("UPDATE systems set username = 'Computational condensed matter physics group, Dalian Unverisity of Technology' where ID="+str(i))
    c.execute("UPDATE systems set calculator = 'vasp' where ID="+str(i))

conn.commit()
conn.close()