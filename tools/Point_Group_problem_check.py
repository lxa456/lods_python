'''
Author: Xueao Li @ DUT
Date: 2023-02-11 10:34:27
LastEditors: Xueao Li @ DUT
LastEditTime: 2023-02-17 15:00:32
Description: 计算点群时偶尔有bug，用此脚本查验。
'''
def PointGroup(xyz_path) -> str:
        import pymatgen.core as mg
        from pymatgen.symmetry.analyzer import PointGroupAnalyzer
        try:
            structure = mg.Molecule.from_file(xyz_path)
            finder = PointGroupAnalyzer(structure)
            print(xyz_path, finder.get_pointgroup())
            
            
            return finder.get_pointgroup()
        except:
            print(xyz_path)

path = r"C:\Users\dell\Desktop\团簇数据库_output\binary_dope\MAu12-Du\DFT_data\xyz_relaxed"

#PointGroup(r"C:\Users\dell\Desktop\团簇数据库_output\binary_dope\MAu12-Du\DFT_data\xyz_relaxed\Ir@Au12.xyz")
import os , time
for root, dirs, files in os.walk(path):
    for filename in files:
        if filename.endswith(".xyz"):
            PointGroup(os.path.join(root,filename))
            time.sleep(0.5)