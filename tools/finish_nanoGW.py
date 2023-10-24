'''
Author: Xueao Li @ DUT
Date: 2023-02-10 21:22:34
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-04-09 16:08:18
Description: 通过OUTCAR批量检查PARSEC or NanoGW有没有计算完成。

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''

import os 
not_converged  = list()

input_dir = os.path.dirname(os.path.abspath(__file__))

def check_parsec(parsec_out):
    if os.path.exists(parsec_out):
        print("parsec.out exists!")
        f1 = open(parsec_out, "r")
        lines = f1.readlines()
        print(lines[-10])
    else:
        print("parsec.out does not exist!")
    

def check_sigma(sigma_out):
    if os.path.exists(sigma_out):
        print("sigma.out exists!")
        f1 = open(sigma_out, "r")
        
    else:
        print("sigma.out does not exist!")
    pass

for root, dirs, files in os.walk(input_dir):
    for filename in files:
        if filename == "parsec.in":
            print("******************")
            print(root)
            parsec_out = os.path.join(root, filename.replace("in", "out"))
            check_parsec(parsec_out)
            sigma_out = os.path.join(root, filename.replace("parsec.in", "sigma.out"))            
            check_sigma(sigma_out)

#for root, dirs, files in os.walk(input_dir):
#    for filename in files:
#        if filename.endswith('OUTCAR'):
#            outcar_path = os.path.join(root, filename)
#            f1 = open (outcar_path)
#            line = f1.readlines()
#            for i in range(1,9):
#                if line[-i] != '\n':
#                    vol = str(line[-i].split()[0])
#                    break
#
#            if vol == "Voluntary":
#                print(root.split("/")[-1], "converged")
#                print("  Time used (sec) "+line[-11].split()[-1])
#            else:
#                print(root.split("/")[-1], " is not converged")
#                not_converged.append(root.split('/')[-1])
#
#print(not_converged)
