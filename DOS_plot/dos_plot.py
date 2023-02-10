# step 1. prepare cmd.in 
# step 2. run vaspkit
# step 3. plot DOS + eigenval 
# step 4. save


import matplotlib.pyplot as plt
import subprocess
import os, sys


def read_eigenval(eigenval_path):
    ''''读取EIGENVAL中的基本信息，为执行vaspkit做准备'''
    f1 = open(eigenval_path)
    lines = f1.readlines()
    energy = []
    for line in lines :
        if len(line.split()) == 3 and float(line.split()[-1]) <= 1.0000:
            energy.append(float(line.split()[1]))

    import math
    max_energy = str(math.ceil(max(energy)))
    min_energy = str(math.ceil(min(energy))-1)
    cmd_path = eigenval_path.replace("EIGENVAL","cmd.in")
    with open(cmd_path,"w+") as cmd:
        cmd.write("117\n")
        cmd.write("1\n")
        cmd.write(min_energy+"  "+max_energy+"  2000  0.15""\n")


def run_vaspkit():
    directories = []
    output = subprocess.run(["ls", "-F"], stdout=subprocess.PIPE, text=True)
    for line in output.stdout.split("\n"):
        if line.endswith("/"):
            directories.append(line.rstrip("/"))

    for directory in directories:
        os.chdir(directory)
        os.system("vaspkit < cmd.in")
        os.chdir("..")


def dos_plot(dos_path):
    '''根据vaspkit生成的TDOS.dat文件画图'''
    f1 = open(dos_path,"r")
    lines = f1.readlines()
    energy, dos = [], []
    for i in range(2,len(lines)):
        energy.append(float(lines[i].split()[0]))
        dos.append(float(lines[i].split()[1]))
    plt.plot(energy ,dos,c="#00809d")


def eigenval_plot(eigenval_path,feimi_energy_path):
    '''根据EIGENVAL文件，在DOS图中画出竖直线。还要根据费米能级调整。'''
    f1 = open(eigenval_path,'r')
    lines = f1.readlines()
    energy = []
    for line in lines :
        if len(line.split()) == 3 and float(line.split()[-1]) <= 1.0000:
            energy.append(float(line.split()[1]))
    
    f2 = open(feimi_energy_path,"r")
    lines2 = f2.readlines()
    fermi = float(lines2[1].split()[0])
    for i in energy:
        plt.axvline(x = i-fermi,ymin=0,ymax=0.15,linestyle='-',lw=0.3, c="#b30b00")


def png_name(poscar_path):
    f1 = open(poscar_path)
    lines = f1.readlines()
    name = lines[0].split()[0]
    if ".xyz" in name:
        name1 = name.replace('.xyz','')
    return name1


#左上角化学式
def vasp_formula(vasp_path):
    f1 = open(vasp_path)
    lines = f1.readlines()
    atom, num = [],[]
    for i in range(len(lines[5].split())):
        atom.append(lines[5].split()[i])
        num.append(int(lines[6].split()[i]))

    formula = ''
    for j in range(len(atom)):
        formula += atom[j]+"$_\mathrm{"+str(num[j])+'}$'
    return formula


def save_png(text,save_path):
    plt.text(0.05, 0.90,s=text,fontdict={'family' : 'Arial', 'size':18}, transform=plt.gca().transAxes)
    plt.axvline(x=0,ymin=0,ymax=1,linestyle='--',c="#a6a6a6")
    plt.xlabel("Energy (eV)",fontsize=15)
    plt.ylabel("Density of States (ev$^{-1}$)",fontsize=15)
    plt.ylim(bottom=0)
    plt.savefig(save_path,dpi=300,bbox_inches='tight')
    plt.cla()
    

if __name__=="__main__":
    current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
    
    save_dir = os.path.join(current_path,"DOS_images")
    if not os.path.exists(save_dir):
          os.makedirs(save_dir)      

    for root, dirs, files in os.walk(current_path):
        for filename in files:
            if filename == "EIGENVAL":
                eigenval = os.path.join(root,filename)
                # step 1.
                read_eigenval(eigenval_path=eigenval)

    # step 2.
    run_vaspkit()

    #step 3.
    for root, dirs, files in os.walk(current_path):
        for filename in files:
            if filename == "EIGENVAL":
                eigenval = os.path.join(root,filename)
                poscar = os.path.join(root,"POSCAR")
                dos_dat = os.path.join(root,"TDOS.dat")
                fermi_energy = os.path.join(root,"FERMI_ENERGY")
                dos_plot(dos_path=dos_dat)
                eigenval_plot(eigenval_path=eigenval, feimi_energy_path=fermi_energy)
                text = vasp_formula(vasp_path=poscar)
                # step 4.
                png = png_name(poscar_path=poscar)
                save_png(text=text,save_path=os.path.join(save_dir,png))
