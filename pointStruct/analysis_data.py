import uuid
from datetime import datetime
import platform
import folder

root = folder.folder()


def get_machine_code():
    board_serial = platform.machine()
    # 获取设备标识符
    device_id = uuid.getnode()

    # 拼接机器码
    machine_code = f"{board_serial}-{device_id}"
    return machine_code


os_id = get_machine_code()


# 读取
def read_folder_structure(file_path, indent_size=2):
    global root

    def parse_subfolders(lines, indent, f_folder):
        f_subfolder = []
        while lines:
            line = lines.pop(0)
            line = line.strip('\n')
            if line:
                subfolder_indent = line.count(" " * indent_size)  # 两个空格表示缩进,获取缩进数量以判断层次关系
                # print(subfolder_indent, indent)
                if subfolder_indent == indent:
                    subfolder_name = line.lstrip(" -")  # 右截取
                    subfolder = folder.folder()
                    temp = subfolder_name.split(',')
                    subfolder.name = temp[0]  # name
                    subfolder.check_file = False if temp[1] == '0' else True
                    subfolder.id = f_folder.id + subfolder.name + '/'
                    subfolder.father_folder = f_folder  # 父目录
                    subfolder.date = temp[2]
                    subfolder.size = temp[3]
                    subfolder.son_folder = parse_subfolders(lines, indent + 1, subfolder)  # 继续递归
                    f_subfolder.append(subfolder)  # 将当前子文件夹加入到父文件夹中
                elif subfolder_indent < indent:  # 进入叔叔层
                    lines.insert(0, line)  # 将读取的行重新放回列表
                    break
        return f_subfolder

    with open(file_path, "r") as file:
        liness = file.readlines()
        print(type(liness))
    x = folder.folder(i=liness.pop(0).strip())
    x.name = 'root'
    x.check_file = -1
    folder_structure = parse_subfolders(liness, 0, x)  # 开始递归
    x.son_folder = folder_structure
    root = x  # 保存当前根
    return x


def str_read_folder_structure(liness, indent_size=2):
    global root
    delete_root()  # 删除root

    def parse_subfolders(lines, indent, f_folder):
        f_subfolder = []
        while lines:
            line = lines.pop(0)
            line = line.strip('\n')
            if line:
                subfolder_indent = line.count(" " * indent_size)  # 两个空格表示缩进,获取缩进数量以判断层次关系
                # print(subfolder_indent, indent)
                if subfolder_indent == indent:
                    subfolder_name = line.lstrip(" -")  # 右截取
                    subfolder = folder.folder()
                    temp = subfolder_name.split(',')
                    subfolder.name = temp[0]  # name
                    subfolder.check_file = False if temp[1] == '0' else True
                    subfolder.id = f_folder.id + subfolder.name + '/'
                    subfolder.father_folder = f_folder  # 父目录
                    subfolder.date = temp[2]
                    subfolder.size = temp[3]
                    try:
                        subfolder.builder = temp[4]
                    except Exception as e:
                        print(e)
                        subfolder.builder = "system"
                    subfolder.son_folder = parse_subfolders(lines, indent + 1, subfolder)  # 继续递归
                    f_subfolder.append(subfolder)  # 将当前子文件夹加入到父文件夹中
                elif subfolder_indent < indent:  # 进入叔叔层
                    lines.insert(0, line)  # 将读取的行重新放回列表
                    break
        return f_subfolder

    liness = liness.split("\n")
    # print('111', type(liness))
    # print(liness.pop(0).strip())
    root = folder.folder(i=liness.pop(0).strip())
    root.name = 'root'
    root.check_file = -1
    folder_structure = parse_subfolders(liness, 0, root)  # 开始递归
    root.son_folder = folder_structure
    # root = deepcopy(x)
    return root


# 写入
def write_folder_structure(file_path):
    def start(folder_, indent=-2):
        if folder_.check_file == -1:
            s = folder_.id
        else:
            s = " " * indent + "- " + folder_.name + "," + (
                "1" if folder_.check_file else "0") + "," + folder_.date + "," + \
                str(folder_.size) + "," + folder_.builder
            # print(" " * indent + "- " + folder_.name + " " + (
            #     "文件" if folder_.check_file else "文件夹") + "," + "路径：" + folder_.id)
        f.write(s + '\n')
        for child in folder_.son_folder:
            start(child, indent + 2)

    with open(file_path, 'w') as f:
        start(root)


ss = ""


def str_write_folder_structure(file_path='test2.txt'):
    global ss
    ss = ""

    def start(folder_, indent=-2):
        global ss
        if folder_.check_file == -1:
            s = folder_.id
        else:
            s = " " * indent + "- " + folder_.name + "," + (
                "1" if folder_.check_file else "0") + "," + folder_.date + "," + \
                str(folder_.size) + "," + folder_.builder
            # print(" " * indent + "- " + folder_.name + " " + (
            #     "文件" if folder_.check_file else "文件夹") + "," + "路径：" + folder_.id)
        # f.write(s + '\n')
        ss += s + '\n'
        for child in folder_.son_folder:
            start(child, indent + 2)

    # with open(file_path, 'w') as f:
    start(root)
    return ss


# 删除全部
def delete_root():
    def start(folder_):
        if not len(folder_.son_folder):
            return
        for child in folder_.son_folder:
            start(child)
            folder_.son_folder.remove(child)  # 移出叶子结点
            del child  # 删除子结点

    if root is None:
        return
    start(root)  # 开始递归


# 新建子结点
def new_folder(f_folder: folder.folder, name: str, check_file: int, size: int = 0, date: str = "") -> folder.folder or int:
    if f_folder is None:
        return -1
    temp = folder.folder(name=name, check_file=check_file, father_folder=f_folder, son_folder=[], date=date,
                         size=size)
    # print(len(temp.son_folder))
    f_folder.set_son(temp)
    return temp
    # print(len(temp.son_folder), len(f_folder.son_folder))
    # 有阿飘~~~~~~~~~~~~~~~~~~~~~~
    # temp.son_folder = []  # 不知何原因
    # 阿飘~~~~~~~~~~~~~~~~~~~~~~~~~


def delete_folder(n_folder):
    # for i in n_folder.son_folder:
    #
    n_folder.father_folder.son_folder.remove(n_folder)
    del n_folder  # 删除


def get_date():
    return str(datetime.now())[:19]
