import pcbnew
import os
import shutil
import zipfile
import datetime

# 工程目录下Gerber和钻孔文件的存放位置
path_out = "out"
# 下单用的文件的位置
path_final = "out/final"

# 用于检查文件是否为Gerber文件以判断是否进行替换操作
file_filter = ('.gbl','.gbs','.gbp','.gbo','.gm1','gm13',
               '.gtl','.gts','.gtp','.gto','.drl','.G1',
               '.G2','.gko')

jlc_header="""G04 Layer: BottomSilkscreenLayer*
G04 EasyEDA v6.5.25, 2023-03-20 21:11:36*
**********************************至少这一行要换成自己的************************************
G04 Gerber Generator version 0.2*
G04 Scale: 100 percent, Rotated: No, Reflected: No *
G04 Dimensions in millimeters  *
G04 leading zeros omitted , absolute positions ,3 integer and 6 decimal *\n"""

# 两张对应表，分别根据结尾和文件名来判断该给什么生成的文件什么名称
replace_list_end = [('.gbl',"Gerber_BottomLayer.GBL"),
                    ('.gko',"Gerber_BoardOutlineLayer.GKO"),
                    ('.gbp',"Gerber_BottomPasteMaskLayer.GBP"),
                    ('.gbo',"Gerber_BottomSilkscreenLayer.GBO"),
                    ('.gbs',"Gerber_BottomSolderMaskLayer.GBS"),
                    ('.gtl',"Gerber_TopLayer.GTL"),
                    ('.gtp',"Gerber_TopPasteMaskLayer.GTP"),
                    ('.gto',"Gerber_TopSilkscreenLayer.GTO"),
                    ('.gts',"Gerber_TopSolderMaskLayer.GTS"),
                    ('.gd1',"Drill_Through.GD1"),
                    ('.gm1',"Gerber_MechanicalLayer1.GM1"),
                    ('.gm13',"Gerber_MechanicalLayer13.GM13")]

replace_list_contain = [('_PCB-PTH', "Drill_PTH_Through.DRL"),
                        ('_PCB-NPTH', "Drill_NPTH_Through.DRL"),
                        ('-PTH', "Drill_PTH_Through.DRL"),
                        ('-NPTH', "Drill_NPTH_Through.DRL"),
                        ('_PCB-In1_Cu', "Gerber_InnerLayer1.G1"),
                        ('_PCB-In2_Cu', "Gerber_InnerLayer2.G2"),
                        ('_PCB-Edge_Cuts', "Gerber_BoardOutlineLayer.GKO")]

def zipFolder(folder_path, output_path):
    """
    压缩指定路径下的文件夹
    :param folder_path: 要压缩的文件夹路径
    :param output_path: 压缩文件的输出路径
    """
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip.write(file_path, os.path.relpath(file_path, folder_path))

# 读取Gerber文件和钻孔文件，修改名称并给Gerber文件内容添加识别头后写入到输出文件夹
def fileTransform(filename, path_out):
    # 按行读取文件内容
    lines = open(filename).readlines()

    # 检查文件类型并给新文件取好相应的名称，写入识别头和原来的文件内容
    hit_flag = 0

    for replace_couple in replace_list_end:
        if filename.endswith(replace_couple[0]):
            file_new = open(path_out + '/' + replace_couple[1], 'w')
            hit_flag = 1
            break

    if hit_flag == 0:
        for replace_couple in replace_list_contain:
            if filename.find(replace_couple[0]) != -1:
                file_new = open(path_out + '/' + replace_couple[1], 'w')
                hit_flag = 1
                break

    if hit_flag == 1:
        hit_flag = 0

        file_new.write(jlc_header)

        for line in lines:
            file_new.write(line)

        file_new.close()

def pathInit(path_out):
    # 检查下目录是否存在，没有就创建
    folder_out = os.path.exists(path_out)
    if not folder_out:
        os.makedirs(path_out)
        print("Folder %s created!" % path_out)
    else:
        print("Folder \"%s\" already exists!" % path_out)

    # 清空目录
    for files in os.listdir(path_out):
        path = os.path.join(path_out, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

    print("Folder \"%s\" clean!" % path_out)

class GiveMeFreePCB(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Give me free PCB!"
        self.category = "A descriptive category name"
        self.description = "A description of the plugin"
        self.show_toolbar_button = True # Optional, defaults to False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png') # Optional

    # 关于路径，写的是处理工程目录下out目录里的文件，
    def Run(self):
        # 获取当前工程路径
        path_workdir = os.environ.get('KIPRJMOD')

        # 把工程根目录设为工作目录
        os.chdir(path_workdir)

        path_out_abs = os.path.join(os.getcwd(), path_out)

        pathInit(os.path.join(path_workdir, path_final))

        file_count = 0

        path_files = os.listdir(os.path.join(os.getcwd(), path_out))

        # 遍历out目录下的文件，识别类型并进行相应的处理
        for p in path_files:
            if(os.path.isfile(os.path.join(path_out_abs, p))):
                if(p.endswith(file_filter)):
                    print("Gerber file %s found." % p)
                    fileTransform(os.path.join(path_out_abs, p), os.path.join(os.getcwd(), path_final))
                    file_count += 1

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        board = pcbnew.GetBoard()
        project_name = os.path.splitext(os.path.basename(board.GetFileName()))[0]

        zipFolder(path_out_abs + '/' + "final", path_out_abs + '/' + "out_" + project_name + '-' + timestamp + ".zip")

        # 打开资源管理器
        os.system("explorer.exe %s" % path_out_abs) 作者：ngHackerX86 https://www.bilibili.com/read/cv22773523/ 出处：bilibili