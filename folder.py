class folder:
    def __init__(self, name="", son_folder=[], father_folder=None, check_file=True, i="", date="", size=0):
        self.name: str = name
        self.son_folder: [] = son_folder  # 子集合
        self.father_folder = father_folder  # 父指针
        self.id = i
        self.check_file = check_file  # 1表示文件，0表示文件夹
        self.date = date
        self.size = size

    def set_son(self, x):
        self.son_folder.append(x)

    def get_id(self):
        if self.father_folder is None:
            return self.id
        else:
            return self.father_folder.get_id() + self.name + '/'
