'''
Author: Xueao Li @ DUT
Date: 2023-10-23 19:24:43
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-10-23 20:10:21
Description: The description of this script.

'''
'''
Author: Xueao Li @ DUT
Date: 2023-10-23 19:24:43
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-10-23 19:41:53
Description: The description of this script.

'''
import os
from ase.io import dmol, xyz
from FormatsToXyz import FormatsConversion

car_path = r"C:\Users\dell\Desktop\团簇数据库_output\lods_python\VASP\step0\TransTest\Sn9_a.car"
xyz_path = r"C:\Users\dell\Desktop\团簇数据库_output\lods_python\VASP\step0\TransTest\Sn9_a.xyz"

f_xyz = open(xyz_path, "w+")
atoms = dmol.read_dmol_car(car_path)
filename = os.path.basename(car_path)
xyz.write_xyz(f_xyz, [atoms], comment="%s %s" %(filename, atoms.symbols))
#FormatsConversion.CarToXyz(car_path, xyz_path)