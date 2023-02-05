## 背景

LODS(Low-Dimensional Systems)数据库管理脚本

#### Keys and Description

ASE database 自带

| Keys       | Desciption                         | data type        |
| ---------- | ---------------------------------- | ---------------- |
| formula    | Chemical formula                   | string           |
| natoms     | Number of atoms                    | integer          |
| unique_id  | Random(unique) ID                  | string           |
| id         | Unique row ID                      | intger           |
| mass       | Sum of atomic masses in unit celll | float            |
| relaxed    | relaxed                            | bool             |
| pbc        | Periodic boundary conditions       | [bool bool bool] |
| ctime      | Age                                | float            |
| user       | Username                           | string           |
| calculator | ASE-calculator name                | string           |
| charge     | Net charge in unit cell            | float            |

需要添加的

| Keys        | Desciption                                                   | data type |
| ----------- | ------------------------------------------------------------ | --------- |
| filename    | original filename                                            | string    |
| Functional  | Functional type                                              | string    |
| TOTEN       | the DFT total energy (useful for comparing clusters with the same number of atoms) | float     |
| GAP_DFT     | HOMO-LUMO Gap calculated with DFT                            | float     |
| HOMO_DFT    | Highest occupied state calculated with DFT                   | float     |
| LUMO_DFT    | Lowest unoccupied state calculated with DFT                  | float     |
| Max_Force   | The maximum force on the atom                                | float     |
| Point_Group | Point Group                                                  | string    |
| GAP_GW      | HOMO-LUMO Gap calculated with GW                             | float     |
| HOMO_GW     | Highest occupied state calculated with GW                    | float     |
| LUMO_GW     | Lowest unoccupied state calculated with GW                   | float     |
| Reference   | DOI                                                          | string    |
| N_ele       | number of valence electrons (included in the calculation)    | integer   |



## 使用方法

#### step 0. 使用前准备

- DFT计算结果文件夹，里面包含多个DFT输出，如OUTCAR、EIGENVAL等

- pip install -r ./requirements.txt

- 初始目录结构示例：

  DFT

  ├── Ag

  │   ├── 01

  │   │   ├── OUTCAR

  │   │   └── *

  │   ├── 02

  │   │   ├── OUTCAR

  │   │   └── *

#### step 1. 处理DFT输出文件

- ​	read_dft.py

- 处理后：

- Ag - DFT

     └── DFT_data──  xyz_relaxed──  *.xyz

  ​            └──dft_info.csv

#### step 2. 筛选

新数据可能与现有数据有重复，使用USR方法筛选。

- dft_dir_screen.py

- 处理后：

- Ag

  ├── DFT

  ├── DFT_data

  ​    └── xyz_relaxed

  └── DFT_data_screen

  ​    └── xyz_relaxed

  ​        ├── similarity.csv

  ​        ├── dft_data_not_exist.csv

  ​        └── dft_data_exist.csv

  

#### step 3. 将该批数据合并为*.db

- update_db.py

  

#### step 4. 合并*.db文件+后处理

- db_merge.py

  

#### step 5. check + upload

- 

## 作者

Xueao Li @ DLUT

LODS_DLUT@163.com

