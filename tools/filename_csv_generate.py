'''
Author: Xueao Li @ DUT
Date: 2023-02-17 15:02:52
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-17 15:44:36
Description: The description of this script.

'''


import os
import pandas as pd


xyz_dir = r"C:\Users\dell\Desktop\xyz\As"
csv_file = os.path.join(xyz_dir, "filename_DOI.csv")
#csv_file = r""

filename_list = []
for root, dirs, files in os.walk(xyz_dir):
    for filename in files:
        if filename.endswith(".xyz"):
            filename_list.append(filename.split(".")[:-1][0])

print(filename_list)
DOI_list = ["TO BE UPDATED ! " for _ in range(len(filename_list))]

filename_data = pd.DataFrame({'filename': filename_list,"Reference":DOI_list})
filename_data.to_csv(csv_file, index=False, sep=',')