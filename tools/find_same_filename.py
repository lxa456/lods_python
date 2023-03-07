'''
Author: Xueao Li @ DUT
Date: 2023-03-07 09:58:00
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-03-07 15:03:22
Description: 删掉同名Row。

'''
from ase.db import connect


def delete_row(db_path,id_list):
    from shutil import copy
    new_db = "DATABASE_NEW.db"
    copy(db_path,new_db)
    print("Created New File:",str(new_db))
    db = connect(new_db)
    print("Deleted Row:",str(id_list))
    db.delete(ids=id_list)


def same_file_list(db_path):
    db = connect(db_path)
    filename_list = []
    for row in db.select():
        filename_list.append(row.filename)
    from collections import Counter   #引入Counter
    b = dict(Counter(filename_list))
    same_filename_list = [key for key,value in b.items()if value > 1]
    return same_filename_list


def filename_2_id(filename_list, db_path):
    db = connect(db_path)
    id_list = []
    for filename in filename_list:
        for row in db.select(filename=filename):
            id = row.id
        id_list.append(id)
    return id_list


if __name__ == "__main__":
    db_path = "DATABASE.db"
    same_filename_list = same_file_list(db_path=db_path)
    id_list = filename_2_id(same_filename_list,db_path)
    delete_row(db_path=db_path, id_list=id_list)