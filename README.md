## 背景

LODS(Low-Dimensional Systems)数据库管理脚本

#### Keys and Description

ASE database 默认Keys

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

需要更新的Key

| Keys           | Description                                                  | data type |
| -------------- | ------------------------------------------------------------ | --------- |
| filename       | original filename                                            | string    |
| Functional     | Functional type                                              | string    |
| TOTEN          | the DFT total energy (useful for comparing clusters with the same number of atoms) | float     |
| GAP_DFT        | The HOMO-LUMO Gap, calculated with DFT                       | float     |
| HOMO_DFT       | The energy of highest occupied molecular orbital, calculated with DFT | float     |
| LUMO_DFT       | The energy of lowest unoccupied molecular orbital, calculated with DFT | float     |
| Max_Force      | Maximum force for structural relaxation                      | float     |
| Point_Group    | Point Group                                                  | string    |
| GAP_GW         | The HOMO-LUMO Gap, calculated with the GW approximation      | float     |
| HOMO_GW        | The energy of highest occupied molecular orbital, calculated with the GW approximation | float     |
| LUMO_GW        | The energy of lowest unoccupied molecular orbital, calculated with the GW approximation | float     |
| Reference      | DOI                                                          | string    |
| N_ele          | number of valence electrons (included in the calculation)    | integer   |
| Dimensionality | The Representation of Materials on a Spatial Scale           | string    |
| Composition    | Composition units of non cluster materials(if the Dimensionality is 0D-assembled) |           |

特殊 Key-value pairs : Similarity

| Keys               | Description                                                  | data type |
| ------------------ | ------------------------------------------------------------ | --------- |
| similar_id_list    | The ID list of the structure similar to this structure       | int       |
| similar_value_list | The similarity list of the similar structure calculated by USR method | float     |

## 批量结构优化（VASP）

#### step 1. 预处理：统一文件格式，去重

​	FormatToXyz.py  # 将 *.mol, *.cif, *.msi, *.xsd 等格式文件转换为 *.xyz 格式

​	输入：结构文件文件夹路径 		输出： xyz 格式文件文件夹路径

​	DB_deduplication.py  # 使用 USR 初步筛选出与当前数据库中相同化学式团簇的相似度 < 0.95 的结构

#### step 2. 生成 VASP 输入文件

​	vasp_opt.py  # 根据 *.xyz 文件信息，生成对应的INCAR、KPOINTS、POSCAR（要扩胞 10 Angstrom）、POTCAR

​	输入：xyz 格式文件文件夹路径	输出： VASP 输入文件（每种结构文件对应一个文件夹）

#### step 3. 上传至超算并批量提交作业

​	使用 Shell 脚本批量提交即可，运行完毕后 使用 tools/finish_vasp.py 检查是否正常结束作业，对于不正常作业要人工检查。

## 使用方法(VASP)

#### step 0. 使用前准备

- DFT 计算结果文件夹，里面包含多个 DFT 输出，如 OUTCAR、EIGENVAL 等

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

- read_dft.py # 提取所有 DFT 输出的有效信息

- 处理后：

- Ag - DFT

     └── DFT_data──  xyz_relaxed──  *.xyz

  ​            └──dft_info.csv

#### step 2. 筛选

当前优化的结构可能与数据库已有的结构重复，使用USR方法筛选出重复度 > 0.94 的结构。

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

- 合并 DFT_data_screen/xyz_relaxed 文件夹中的 xyz 文件到 .db 中，再将 dft_data_not_exist.csv 更新到 .db 中。
- update_db.py  # 输入： xyz_relaxed 路径， dft_data_not_exist.csv 路径      输出：.db 数据库文件 



#### step 3.5. 基本设置

- 修改 username 和 calculator 等默认参数

- vasp_basic_setting.py


#### step 4. 合并*.db文件+后处理

​	把 *.db 和 DATABASE.db 放在同一文件夹下，合并到一个新的数据库中。

- convert.py  # 输入： *.db 和 DATABASE.db 的路径	输出： 合并后的新 .db 文件

  

#### step 5. 相似度数据更新

​	由于每次更新会导致序号问题或新加入的相似结构问题，在每次增删数据后要进行相似度数据更新，保留相似度 > 0.8 的相关数据；

​	update_similarity.py # 输入： *.db 文件路径

#### step 5. check + upload

- ase db -w DATABASE.db # 检查数据
- 上传至远端服务器，Flask Web app 自动更新网站上的数据

##### 备注：只更新keys and values 可参考GW中的update_key_values.py

## 作者

Xueao Li @ DLUT

LODS_DLUT@163.com

