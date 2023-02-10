'''
Author: Xueao Li @ DUT
Date: 2023-02-10 21:22:34
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-10 21:23:19
Description: 通过OUTCAR批量检查vasp有没有计算完成。

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''

import os 
not_converged  = list()

input_dir = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(input_dir):
    for filename in files:
        if filename.endswith('OUTCAR'):
            outcar_path = os.path.join(root, filename)
            f1 = open (outcar_path)
            line = f1.readlines()
            for i in range(1,9):
                if line[-i] != '\n':
                    vol = str(line[-i].split()[0])
                    break

            if vol == "Voluntary":
                print(root.split("/")[-1], "converged")
                print("  Time used (sec) "+line[-11].split()[-1])
            else:
                print(root.split("/")[-1], " is not converged")
                not_converged.append(root.split('/')[-1])

print(not_converged)
