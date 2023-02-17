'''
Author: Xueao Li @ DUT
Date: 2023-02-11 14:57:31
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-12 09:46:10
Description: The description of this script.

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''


import os

path = r"C:\Users\dell\Desktop\团簇数据库_output\reopt分子团簇\(H2O)30-48"


for root, dirs, files in os.walk(path):
    for filename in files:
        if filename.endswith(".out"):
            #print(filename.replace("@","_at_"))
            old_name = os.path.join(root, filename)
            #new_name = os.path.join(root, root.split("\\")[-1]+"_"+filename)
            #os.rename(old_name, new_name)
            #print(root.split("\\")[-1])
            #print(new_name)
            new_name = os.path.join(root, filename.replace("@","_at_"))
            os.rename(old_name, new_name)
            