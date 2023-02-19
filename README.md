## 背景

LODS(Low-Dimensional Systems)数据库管理脚本

#### Keys and Description

ASE database 自带

| Keys       | Description                        | data type          |
| ---------- | ---------------------------------- | ------------------ |
| formula    | Chemical formula                   | string             |
| natoms     | Number of atoms                    | integer            |
| unique_id  | Random(unique) ID                  | string             |
| id         | Unique row ID                      | intger             |
| mass       | Sum of atomic masses in unit celll | float              |
| relaxed    | relaxed                            | bool               |
| pbc        | Periodic boundary conditions       | [bool, bool, bool] |
| ctime      | Age                                | float              |
| user       | Username                           | string             |
| calculator | ASE-calculator name                | string             |
| charge     | Net charge in unit cell            | float              |

需要添加的

| Keys        | Description                                                  | data type |
| ----------- | ------------------------------------------------------------ | --------- |
| filename    | original filename                                            | string    |
| Functional  | Functional type                                              | string    |
| TOTEN       | the DFT total energy (useful for comparing clusters with the same number of atoms) | float     |
| GAP_DFT     | The HOMO-LUMO Gap, calculated with DFT                       | float     |
| HOMO_DFT    | The energy of highest occupied molecular orbital, calculated with DFT | float     |
| LUMO_DFT    | The energy of lowest unoccupied molecular orbital, calculated with DFT | float     |
| Max_Force   | Maximum force for structural relaxation                      | float     |
| Point_Group | Point Group                                                  | string    |
| GAP_GW      | The HOMO-LUMO Gap, calculated with the GW approximation      | float     |
| HOMO_GW     | The energy of highest occupied molecular orbital, calculated with the GW approximation | float     |
| LUMO_GW     | The energy of lowest unoccupied molecular orbital, calculated with the GW approximation | float     |
| Reference   | DOI                                                          | string    |
| N_ele       | number of valence electrons (included in the calculation)    | integer   |



## 使用方法(VASP)

#### step 0. 使用前准备

- DFT计算结果文件夹，里面包含多个DFT输出，如OUTCAR、EIGENVAL等

- pip install -r ./requirements.txt

- 初始目录结构举例：

  DFT

  ├── Ag

  │   ├── 01

  │   │   ├── OUTCAR

  │   │   └── *

  │   ├── 02

  │   │   ├── OUTCAR

  │   │   └── *

#### step 1. 处理DFT输出文件

- read_dft.py

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

- 合并xyz_relaxed 中的xyz文件到*.db中，再将dft_data_not_exist.csv更新到*.db中。
- update_db.py



#### step 3.5. 基本设置

修改username 和 calculator.

vasp_basic_setting.py

#### step 4. 合并*.db文件+后处理

​	把*.db和DATABASE.db放在同一文件夹下，合并到一个新的数据库中。

- convert.py

  

#### step 5. check + upload

- ase db -w DATABASE.db

  

##### 备注：只更新keys and values 可参考GW中的update_key_values.py

## 作者

Xueao Li @ DLUT

LODS_DLUT@163.com

