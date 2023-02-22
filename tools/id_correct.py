'''
Author: Xueao Li @ DUT
Date: 2023-02-22 16:50:20
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-22 17:27:20
Description: db.delete()删除数据导致序号不对,用本脚本改正序号ID。

'''

from ase.db import connect
import os
import sqlite3
from shutil import copy

def id_list(db_path):
    id_list = []
    db = connect(db_path)
    for row in db.select():
        id_list.append(row.id)
    return id_list


current_path = os.path.dirname(os.path.abspath(__file__))
file_1 = os.path.join(current_path, 'DATABASE_2022_02_22.db')
new_db = os.path.join(current_path, "DATABASE_NEW.db")
copy(file_1, new_db)


ID_list  = id_list(new_db)
#print(len(id_list(new_db)))

conn1 = sqlite3.connect(new_db)
c1 = conn1.cursor()
c1.execute('SELECT id from systems')

for index, value in enumerate(ID_list):
    c1.execute("UPDATE systems set ID=%s" %(index+1)+" where ID=%s" %value)
    c1.execute("UPDATE keys set id=%s" %(index+1)+" where id=%s" %value)
    c1.execute("UPDATE species set id=%s" %(index+1)+" where id=%s" %value)
    c1.execute("UPDATE text_key_values set id=%s" %(index+1)+" where id=%s" %value)
    c1.execute("UPDATE number_key_values set id=%s" %(index+1)+" where id=%s" %value)

conn1.commit()
#row_num1 = len(c1.fetchall()) 
#print(row_num1)
conn1.close()
print("修改完毕")