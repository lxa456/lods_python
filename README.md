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
| Reference   | DOI                                                          | float     |
| N_ele       | number of valence electrons (included in the calculation)    | integer   |



## 使用方法

## 作者

Xueao Li @ DLUT

LODS_DLUT@163.com

