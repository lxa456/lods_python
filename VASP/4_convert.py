'''
Author: Xueao Li @ DUT
Date: 2023-02-10 17:08:12
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-17 11:22:16
Description: 合并本文件夹下的db文件到DATABASE.db中。
'''
##合并两个ase数据库
import sqlite3
from select import select
import os 

current_path = os.path.dirname(os.path.abspath(__file__))
file_1 = os.path.join(current_path, 'DATABASE.db')
#database_convert = input("输入被合并的文件名(带后缀)")

def db_name_list():
    filename_list = list()
    for root, dirs ,files in os.walk(current_path):
        for filename in files:
            if filename.endswith('.db'):
                filename_list.append(filename)
    filename_list.remove("DATABASE.db")
    #filename_list.remove("Ag.db")
    filename_list.sort()
    return filename_list

for database_convert in db_name_list() :
    file_2 = os.path.join(current_path, database_convert)
    #file_1 = r'C:\\Users\\dell\\Desktop\\sqlite3_test\\convert\\As.db'
    #file_2 = r'C:\\Users\\dell\\Desktop\\sqlite3_test\\convert\\B.db'
    conn1 = sqlite3.connect(file_1)##合并到此数据库（DATABASE）
    conn2 = sqlite3.connect(file_2)##被合并的数据库
    #print('数据库连接成功')
    print(database_convert)
    c1 = conn1.cursor()
    c2 = conn2.cursor()
    c1.execute('SELECT id from systems')
    row_num1 = len(c1.fetchall()) #获取DATABASE的行数
    c2.execute('SELECT id from systems')
    row_num2 = len(c2.fetchall()) #获取被合并的行数
    print('初始db的行数为'+str(row_num1), '被合并db的行数为'+str(row_num2))
    ##修改需要合并数据库的id,目前number_text_value有待完善
    for i in range(1,row_num2+1):
    #    print(i)
        #一个笨方法，目的是防止表中的主键冲突（一个表中不能存在两个相同的主键），例如：需要添加的表的第一个 id是23，
        #它会与自己表中id=23的内容冲突，所以先将第一个id设置成101，第二个id设置成102... ，下面再将他们改    回23，24...
        c2.execute("UPDATE systems set ID="+str(10000+i)+" where ID="+str(i))
        c2.execute("UPDATE keys set id="+str(10000+i)+" where id="+str(i))
        c2.execute("UPDATE species set id="+str(10000+i)+" where id="+str(i))
        c2.execute("UPDATE text_key_values set id="+str(10000+i)+" where id="+str(i))
        c2.execute("UPDATE number_key_values set id="+str(10000+i)+" where id="+str(i))
    conn2.commit()
    
    for j in range(1,row_num2+1):
        c2.execute("UPDATE systems set ID="+str(row_num1+j)+" where ID="+str(10000+j))
        c2.execute("UPDATE keys set id="+str(row_num1+j)+" where id="+str(10000+j))
        c2.execute("UPDATE species set id="+str(row_num1+j)+" where id="+str(10000+j))
        c2.execute("UPDATE text_key_values set id="+str(row_num1+j)+" where id="+str(10000+j))
        c2.execute("UPDATE number_key_values set id="+str(row_num1+j)+" where id="+str(10000 +j))

    conn2.commit()
    conn2.close()

    c1.execute("attach '"+str(file_2)+"' as SecondaryDB")##连接被合并的数据库
    #c.execute("attach 'C:/Users/dell/Desktop/sqlite3_test/convert/B.db' as SecondaryDB")
    c1.execute('insert into systems select * from SecondaryDB.systems')
    c1.execute('insert into species select * from SecondaryDB.species')
    c1.execute('insert into keys select * from SecondaryDB.keys')
    c1.execute('insert into text_key_values select * from SecondaryDB.text_key_values')
    c1.execute('insert into number_key_values select * from SecondaryDB.number_key_values')

    conn1.commit()
    c1.execute('detach SecondaryDB')#取消连接
    conn1.close()
    print("修改完毕")
