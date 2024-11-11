import os
import shutil
import sys
import threading
import time
from copy import deepcopy
from functools import partial
from queue import Queue

from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QImage, QDragEnterEvent, QDropEvent, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidgetItem, QMessageBox, \
    QMenu, QAction, QLineEdit, QDialogButtonBox, QVBoxLayout, QDialog, QListWidget, QShortcut

from pointStruct import analysis_data
from ui.DirectoryItemWidget import DirectoryItemWidget
from pointStruct.analysis_data import *
from ui import uio, progressDialog
# import mouse
from Websocket_filesystem import websocket_client
import requests


class MainWindow(QMainWindow):
    download_file_signal = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.txt_path = 'test2.txt'
        self.ui = uio.Ui_FileManagerWindow()
        self.ui.setupUi(self)
        self.root_folder = None
        self.menu = None

        #        self.mouse_.start()  # 开始
        #        self.mouse_.value_changed.connect(self.listen_mouse)
        self.menu_2 = None
        self.selected_items = None
        self.action1 = None
        self.action2 = None
        self.action3 = None
        self.action6 = None
        self.action4 = None
        self.action5 = None
        self.action7 = None
        self.action8 = None
        self.copy_list = []

        self.post_file_urls: Queue = Queue()
        self.delete_file_urls: Queue = Queue()
        self.sticker_file_urls: Queue = Queue()

        self.is_shear = False
        self.sort_type = 1  # 排序规则
        self.isreverse = False  # 是否从大到小
        self.t = None
        self.tt = None
        self.progress_dialog = None
        self.root_path = 'static\\files'

        self.download_file_signal.connect(self.download_file_signal_slot)

        # 启用拖拽功能
        self.setAcceptDrops(True)
        self.ui.fileListWidget.value_changed.connect(self.listen_mouse)
        # 热键
        self.shortcut_copy = QShortcut(QKeySequence("Ctrl+C"), self)
        self.shortcut_copy.activated.connect(self.folder_copy)

        # 设置热键：Ctrl+V
        self.shortcut_paste = QShortcut(QKeySequence("Ctrl+V"), self)
        self.shortcut_paste.activated.connect(self.folder_stick)

        # 设置热键: DEL
        self.shortcut_delete = QShortcut(QKeySequence("Del"), self)
        self.shortcut_delete.activated.connect(self.delete_f)

    # self.download_file_signal.connect(self.download_file_signal_slot)

    #        self.websock = websocket_client.websock()

    def init(self):

        self.recv_folder()
        self.ui.lineEdit.setReadOnly(True)

        self.ui.fileListWidget.itemDoubleClicked.connect(self.onClicked)  # 为表项绑定槽函数
        self.ui.fileListWidget.setSelectionMode(QListWidget.MultiSelection)  # 设置listwidget选择模式为多选
        self.ui.fileListWidget.itemSelectionChanged.connect(self.on_selection_changed)  # 绑定选择变化事件

        # 名称
        self.ui.pushButton.setStyleSheet("background-color: transparent;text-align: left;")
        self.ui.pushButton.setText('名称 ')
        # 修改时间
        self.ui.pushButton_2.setStyleSheet("background-color: transparent;text-align: left;")
        self.ui.pushButton_2.setText('修改时间 ')
        # 类型
        self.ui.pushButton_6.setStyleSheet("background-color: transparent;text-align: left;")
        self.ui.pushButton_6.setText('类型 ')
        # 大小
        self.ui.pushButton_7.setStyleSheet("background-color: transparent;text-align: left;")
        self.ui.pushButton_7.setText('大小 ')

        self.ui.pushButton.clicked.connect(partial(self.update_sortype, 1))
        self.ui.pushButton_2.clicked.connect(partial(self.update_sortype, 2))
        self.ui.pushButton_7.clicked.connect(partial(self.update_sortype, 3))

        self.ui.pushButton_4.clicked.connect(self.recv_folder)  # 刷新
        self.ui.pushButton_4.setText('')
        self.ui.pushButton_4.setStyleSheet('background-color: rgba(255, 255, 255, 100)')
        image = QImage('rec/icon/flush_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(25, 25)
        icon = QIcon(scaled_pixmap)
        self.ui.pushButton_4.setIcon(icon)
        self.ui.pushButton_4.setIconSize(pixmap.size())

        self.ui.pushButton_5.clicked.connect(self.button_return)
        self.ui.pushButton_5.setText('')
        self.ui.pushButton_5.setStyleSheet('background-color: rgba(255, 255, 255, 100);')
        image = QImage('rec/icon/return_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(25, 25)
        icon = QIcon(scaled_pixmap)
        self.ui.pushButton_5.setIcon(icon)
        self.ui.pushButton_5.setIconSize(pixmap.size())

        self.ui.pushButton_3.setText('')
        self.ui.pushButton_3.setStyleSheet('background-color: rgba(255, 255, 255, 100);')
        image = QImage('rec/icon/menu_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(25, 25)
        icon = QIcon(scaled_pixmap)
        self.ui.pushButton_3.setIcon(icon)
        self.ui.pushButton_3.setIconSize(pixmap.size())

        image = QImage('rec/icon/folder_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(25, 25)
        icon = QIcon(scaled_pixmap)
        self.setWindowTitle(f'文件管理系统   用户：{os_id}')
        self.setWindowIcon(icon)
        # 菜单栏
        self.menu = QMenu(self)
        image = QImage('rec/icon/new_file.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        action1 = QAction(icon, "新建文件", self)
        image = QImage('rec/icon/folder_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        action2 = QAction(icon, "新建文件夹", self)
        action3 = QAction("...", self)
        action1.triggered.connect(partial(self.new_built, 1))
        action2.triggered.connect(partial(self.new_built, 0))
        self.menu.addAction(action1)
        self.menu.addAction(action2)
        self.menu.addAction(action3)
        self.ui.pushButton_3.clicked.connect(self.toggle_menu)

        # 右键菜单栏
        self.menu_2 = QMenu(self)
        image = QImage('rec/icon/new_file.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        self.action1 = QAction(icon, "新建文件", self)
        image = QImage('rec/icon/folder_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        self.action2 = QAction(icon, "新建文件夹", self)
        image = QImage('rec/icon/delete_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        self.action3 = QAction(icon, "删除", self)
        self.action4 = QAction("复制", self)
        self.action5 = QAction("粘贴", self)
        self.action6 = QAction("剪切", self)
        self.action5.setEnabled(False)  # 不可点击
        self.action7 = QAction("重命名", self)

        image = QImage('rec/icon/flush_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        self.action8 = QAction(icon, "刷新", self)

        self.action1.triggered.connect(partial(self.new_built, 1))
        self.action2.triggered.connect(partial(self.new_built, 0))
        self.action3.triggered.connect(self.delete_f)

        self.action4.triggered.connect(self.folder_copy)
        self.action5.triggered.connect(self.folder_stick)
        self.action6.triggered.connect(self.folder_shear)
        self.action7.triggered.connect(self.re_name)
        self.action8.triggered.connect(self.recv_folder)  # 刷新

        self.menu_2.addAction(self.action1)
        self.menu_2.addAction(self.action2)
        self.menu_2.addAction(self.action3)
        self.menu_2.addAction(self.action4)
        self.menu_2.addAction(self.action5)
        self.menu_2.addAction(self.action6)
        self.menu_2.addAction(self.action7)
        self.menu_2.addAction(self.action8)

        # self.ui.fileListWidget.value_changed.connect(self.listen_mouse)

    # self.menu_2.removeAction(action7)  # 移出操作
    # self.ui.pushButton_3.clicked.connect(self.toggle_menu)

    # self.menu.aboutToHide.connect(self.ui.pushButton_3.setChecked)

    # 界面刷新
    def populateList(self):
        # self.write_folder()  # 更新文件位置
        self.ui.fileListWidget.clear()  # 清除目录
        QApplication.processEvents()  # 刷新界面
        time.sleep(0.05)  # 过渡动画
        self.ui.lineEdit.setText(self.root_folder.get_id())
        if self.sort_type == 1:
            temp = sorted(self.root_folder.son_folder, key=lambda x: (x.check_file, x.name), reverse=self.isreverse)
        elif self.sort_type == 2:
            temp = sorted(self.root_folder.son_folder, key=lambda x: (x.check_file, x.date), reverse=self.isreverse)
        elif self.sort_type == 3:
            temp = sorted(self.root_folder.son_folder, key=lambda x: (x.check_file, x.size), reverse=self.isreverse)
        for i in temp:  # 遍历子目录
            # while (i.name, i.check_file) in book:  # 去重
            #     i.name = i.name + "(1)"
            # book.add((i.name, i.check_file))
            item_widget = DirectoryItemWidget(i)  # 列表对应的布局对象
            item = QListWidgetItem(self.ui.fileListWidget)
            item.setSizeHint(item_widget.sizeHint())
            self.ui.fileListWidget.addItem(item)
            self.ui.fileListWidget.setItemWidget(item, item_widget)

        if not len(self.root_folder.son_folder):
            item = QListWidgetItem(self.ui.fileListWidget)
            # item.setSizeHint(item_widget.sizeHint())
            item.setText('当前目录为空')
            image = QImage('rec/icon/file_icon_2.png')  # 替换成你想要的图片路径
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(50, 50)
            icon = QIcon(scaled_pixmap)
            item.setIcon(icon)
            # item.setFixedSize(30, 30)
            self.ui.fileListWidget.addItem(item)

        # self.ui.fileListWidget.itemClicked.connect(self.onClicked)

    # 列表点击
    def onClicked(self, item)   ->None:
        # Here you can access the widget and its contents
        widget = self.ui.fileListWidget.itemWidget(item)
        if widget is None:
            QMessageBox.warning(self, "警告", "空目录")
            return

        path = self.get_relative_path(widget.r_folder)  # 获取相对路径

        if widget.r_folder.check_file == 1:
            print(path)
            if not os.path.exists(path):
                name = self.get_file_servername(widget.r_folder)  # 获取文件名
                reply = QMessageBox.question(self, '确认', '文件不存在，是否下载？', QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
                if reply == QMessageBox.Yes:
                    threading.Thread(target=self.download_file, args=(name,)).start()
                else:
                    return
            else:
                threading.Thread(target=os.startfile, args=(path,)).start()  # 打开文件
            # QMessageBox.warning(self, "警告", "现在还不能打开文件")
            return
        # print(widget.r_folder.name)
        self.root_folder = widget.r_folder  # 更新root
        self.populateList()  # 显示目录
        # QMessageBox.information(self, "Directory Clicked", "You clicked on a directory.")

    # 返回按钮
    def button_return(self):
        if self.root_folder.father_folder is None:
            return
        self.root_folder = self.root_folder.father_folder
        self.populateList()
        # self.recv_folder()  # 获取最新

    # 菜单监听
    def toggle_menu(self):
        if self.menu.isVisible():
            self.menu.close()
        else:
            self.menu.popup(self.mapToGlobal(self.ui.pushButton_3.rect().bottomLeft()))

    # 创建文件夹
    def new_folder(self, name: str) -> folder.folder or None:
        # if self.check_operatre():
        #     return -1
        return new_folder(self.root_folder, name, 0, date=get_date())
        #  self.send_folder()  # 发送最新结构
        # self.populateList()

    # 创建文件
    def new_file(self, name: str, size: int = 0, date: str = get_date()) -> folder.folder or None:
        # if self.check_operatre():
        #     return -1
        return new_folder(self.root_folder, name, 1, size=size, date=date)
        #  self.send_folder()  # 发送最新结构
        # self.populateList()

    # 删除操作触发控制事件
    def delete_f(self):
        # if self.check_operatre():  # 判断这次操作可行性
        #     return -1
        self.selected_items = self.ui.fileListWidget.selectedItems()

        if len(self.selected_items) > 1:
            reply = QMessageBox.question(self, '确认', '确定要删除吗?', QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                pass
            else:
                return
        for item in self.selected_items:
            if self.ui.fileListWidget.itemWidget(item).r_folder.check_file == 0:  # 文件夹
                self.get_file_urls(self.ui.fileListWidget.itemWidget(item).r_folder, self.delete_file_urls)
            else:
                self.delete_file_urls.put(self.ui.fileListWidget.itemWidget(item).r_folder)

        self.delete_file_slot(True)
        # self.populateList()

    def get_file_urls(self, root_: folder.folder, Qurls: Queue) -> None:
        if root_.check_file == 1:
            Qurls.put(root_)
        else:
            if root_.father_folder is None or len(root_.son_folder) == 0:
                return
            for i in root_.son_folder:
                if i.check_file == 1:
                    Qurls.put(i)
                else:
                    self.get_file_urls(i, Qurls)
        return None

    def delete_file_slot(self, log: bool)->None:
        print(log)
        if self.delete_file_urls.empty():
            self.send_folder()  # 发送最新结构
            return
        pointer = self.delete_file_urls.get()

        if pointer.check_file == 1:
            self.delete_file(pointer)
        else:
            self.delete_folder(pointer)

        time.sleep(0.1)

    def delete_file(self, pointer: folder.folder):
        try:
            os.remove(self.get_relative_path(pointer))
        except Exception as e:
            print(e)
        del_file_name = self.get_file_servername(pointer)  # 获取文件名
        self.tt = websocket_client.delete_file(del_file_name)
        self.tt.log.connect(self.delete_file_slot)
        self.tt.start()
        analysis_data.delete_folder(pointer)

    # 输入框
    def get_name(self, flag, old_messge=""):
        input_dialog = QDialog(self)
        input_dialog.setWindowTitle("输入框")

        layout = QVBoxLayout(input_dialog)

        label = QLabel(f"请输入{'文件' if flag else '文件夹'}名称:", input_dialog)
        layout.addWidget(label)

        line_edit = QLineEdit(input_dialog)
        line_edit.setText(old_messge)
        layout.addWidget(line_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
                                      input_dialog)
        layout.addWidget(button_box)

        button_box.accepted.connect(input_dialog.accept)
        button_box.rejected.connect(input_dialog.reject)

        if input_dialog.exec() == QDialog.DialogCode.Accepted:
            input_value = line_edit.text()
            return input_value

    # 创建文件夹或文件
    def new_built(self, flag:str)  ->None:
        input_value = self.get_name(flag)
        if input_value is None or not len(input_value):
            return
        list_ = ['/', '?', ',', ':']
        for i in list_:
            if input_value.count(i):
                return
        book = set()
        # 判重名
        for i in self.root_folder.son_folder:  # 遍历子目录
            book.add((i.name, i.check_file))
        while (input_value, flag) in book:
            input_value += "(1)"
        del book
        if not flag:
            self.new_folder(input_value)
        else:
            self.new_file(input_value)

        self.send_folder()  # 发送最新结构

        # self.populateList()  # 刷新界面

    # def write_folder(self):
    #     write_folder_structure(self.txt_path)

    def on_selection_changed(self):
        if len(self.ui.fileListWidget.selectedItems()) == 0:  # 检查是否取消了所有选择
            self.ui.fileListWidget.clearSelection()  # 清除选择

    # 监听鼠标事件
    def listen_mouse(self, value:int, x, y) -> None:
        # 0,1 分别代表左键按下和弹起、2,3分别代表右键
        windowsize = self.pos()
        xxyy = QPoint(x + 20, y + windowsize.y() - 20)
        # windowsize = self.size()
        if value == 0:
            self.ui.fileListWidget.clearSelection()
        elif value == 1:
            pass
            # self.ui.fileListWidget.clearSelection()
        if value == 2:
            pass
        elif value == 3:
            self.selected_items = self.ui.fileListWidget.selectedItems()
            if not len(self.selected_items):
                self.menu_2.removeAction(self.action3)
                self.menu_2.removeAction(self.action4)
                self.menu_2.removeAction(self.action5)
                self.menu_2.removeAction(self.action6)
                self.menu_2.removeAction(self.action7)
            else:
                self.menu_2.addAction(self.action3)
                self.menu_2.addAction(self.action4)
                self.menu_2.addAction(self.action5)
                self.menu_2.addAction(self.action6)
                self.menu_2.addAction(self.action7)
            if len(self.copy_list):
                self.menu_2.addAction(self.action5)  # 显示粘贴按钮
            if self.menu_2.isVisible():
                self.menu_2.close()
            else:
                self.menu_2.popup(self.mapToGlobal(xxyy))
        return
    # 复制
    def folder_copy(self):
        self.selected_items = self.ui.fileListWidget.selectedItems()
        self.copy_list.clear()
        for item in self.selected_items:
            widget = self.ui.fileListWidget.itemWidget(item)
            self.copy_list.append(widget.r_folder)
        self.action5.setEnabled(True)

    # 剪切
    def folder_shear(self):
        self.copy_list.clear()
        for item in self.selected_items:
            widget = self.ui.fileListWidget.itemWidget(item)
            self.copy_list.append(widget.r_folder)
        self.is_shear = True
        self.action5.setEnabled(True)

    # 粘贴
    def folder_stick(self):
        print('粘贴')
        if self.copy_list is None or not len(self.copy_list):
            return
        for i in self.copy_list:
            # 判重名
            input_value = deepcopy(i.name)
            after_cnt = 0
            # 分离文件名和后缀
            if i.check_file:
                for j in range(0, len(input_value)):
                    if input_value[j] == '.':
                        after_cnt = j
            print(after_cnt)
            flag = i.check_file
            book = set()
            for ii in self.root_folder.son_folder:  # 遍历子目录
                book.add((ii.name, ii.check_file))
            while (input_value, flag) in book:
                input_value = input_value[:after_cnt] + "(1)" + input_value[after_cnt:]
            del book
            # i.name = input_value
            if i.check_file:
                self.sticker_file_urls.put((i, input_value))
            else:
                # self.new_folder(i.name)
                f = deepcopy(i)
                f.name = input_value
                f.father_folder = self.root_folder
                self.root_folder.son_folder.append(f)

                #  获取粘贴队列
                self.get_file_urls(f, self.sticker_file_urls)

            if self.is_shear:
                delete_folder(i)  # 删除原来位置的
                os.remove(self.get_relative_path(i))  # 删除原文件

        self.sticker_file_slot(True)
        self.action5.setEnabled(False)  # 复制完成
        self.is_shear = False  # 重置剪切状态
        self.copy_list = []
        # self.populateList()

    def sticker_file_slot(self, log:bool) ->  None:
        print(log)
        if self.sticker_file_urls.empty():
            self.send_folder()
            return

        file_url = self.sticker_file_urls.get()
        if type(file_url) == tuple:
            orc_point = file_url[0]
            dest_name = file_url[1]
        else:
            orc_point = file_url
            dest_name = file_url.name

        Relative_path = self.get_relative_path(orc_point)  # 获取文件在本地的原路径
        dest_path = self.get_relative_path(self.root_folder) + '\\' + dest_name  # 目标文件在本地的路径
        # 确保目标目录存在，如果没有则创建
        dest_dir = os.path.dirname(Relative_path)  # 获取目标文件路径的目录部分
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)  # 创建目标文件夹及其父文件夹
        try:
            shutil.copy(Relative_path, dest_path)  # 复制文件到目标目录
        except Exception as e:
            print(e)
        self.new_file(dest_name, size=orc_point.size, date=orc_point.date)

        self.t = websocket_client.copy_file(self.get_file_servername(orc_point),
                                            self.get_file_servername(self.root_folder))
        self.t.log.connect(self.sticker_file_slot)
        self.t.start()
        time.sleep(0.05)

    # 重命名
    def re_name(self):
        if len(self.selected_items) != 1:
            return
        for item in self.selected_items:
            widget = self.ui.fileListWidget.itemWidget(item)
            s = self.get_name(widget.r_folder.check_file, old_messge=widget.r_folder.name)
            if s is None:
                return
            book = set()
            # 判重名
            for i in self.root_folder.son_folder:  # 遍历子目录
                book.add((i.name, i.check_file))
            while (s, widget.r_folder.check_file) in book:
                s += "(1)"
            widget.r_folder.name = s
            widget.r_folder.date = get_date()
        self.send_folder()
        # self.populateList()

        # 刷新

    def update_sortype(self, sort_type:int) -> None :
        if self.sort_type == sort_type:
            self.isreverse = not self.isreverse
        self.sort_type = sort_type
        if self.sort_type == 1:
            self.ui.pushButton.setText(self.ui.pushButton.text()[:-1] + ("^" if self.isreverse else " "))
            self.ui.pushButton_7.setText('大小 ')
            self.ui.pushButton_2.setText('修改时间 ')
        elif self.sort_type == 2:
            self.ui.pushButton_2.setText(self.ui.pushButton_2.text()[:-1] + ("^" if self.isreverse else " "))
            self.ui.pushButton.setText('名称 ')
            self.ui.pushButton_7.setText('大小 ')
        else:
            self.ui.pushButton_7.setText(self.ui.pushButton_7.text()[:-1] + ("^" if self.isreverse else " "))
            self.ui.pushButton.setText('名称 ')
            self.ui.pushButton_2.setText('修改时间 ')
        self.populateList()  # 刷布局
        return
    # 获取文件夹结构的回调函数
    def Get_folder(self, data:str) -> None:
        if data is None or not len(data) or data[0] != '/':
            return
        path = []
        old_folder = ""
        if self.root_folder is not None:
            old_folder = self.root_folder.get_id()
            path = old_folder.split('/')
        self.root_folder = str_read_folder_structure(data)
        for i in path:
            if i is None or not len(i):
                continue
            for j in self.root_folder.son_folder:
                if i == j.name:
                    self.root_folder = j
                    break
        from pointStruct.analysis_data import root
        if old_folder != self.root_folder.get_id():
            self.root_folder = root
        self.populateList()

    # 提交修改后的文件夹的回调函数
    def Post_folder(self, log:bool) -> None:
        if log:
            self.ui.label_5.setText('True')
            self.ui.label_5.setStyleSheet('color:rgb(0,200,0)')
        else:
            self.ui.label_5.setText('False')
            self.ui.label_5.setStyleSheet('color:rgb(200,0,0)')

        self.recv_folder()  # 获取最新数据
        # self.populateList()
        return

    # 获取文件的回调函数
    def Get_file(self, data):
        pass

    # 提交文件的回调函数
    def Post_file(self, Absolute_path:str, Relative_path:str) -> None:
        self.progress_dialog = progressDialog.ProgressDialog()
        self.progress_dialog.show()
        self.t = websocket_client.Post_file(Absolute_path, Relative_path)
        self.t.send_progress.connect(self.progress_dialog.update_progress)
        self.t.log.connect(self.Post_file_slot)
        self.t.start()
        return
    def Post_file_slot(self, log:bool) -> None:
        print(log)
        if self.post_file_urls.empty():
            self.send_folder()
            return
        file_url = self.post_file_urls.get()
        file_path = file_url.toLocalFile()  # 获取第一个文件的本地路径
        if os.path.isdir(file_path):
            QMessageBox.warning(self, "警告", "请不要上传文件夹！")
            return
        # 获取文件大小，以KB为单位
        file_size = max(1024, os.path.getsize(file_path))
        t = self.new_file(os.path.basename(file_path), size=int(file_size / 1024))
        dest_path = self.get_relative_path(t)  # 获取文件在服务器上的路径
        print(dest_path)
        # 确保目标目录存在，如果没有则创建
        dest_dir = os.path.dirname(dest_path)  # 获取目标文件路径的目录部分
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)  # 创建目标文件夹及其父文件夹
        shutil.copy(file_path, dest_path)

        print(t.get_id()[:-1])
        self.Post_file(file_path, t.get_id()[:-1])  # 绝对路径，相对路径
        time.sleep(0.05)

    # 拖拽进入事件
    def dragEnterEvent(self, event: QDragEnterEvent) ->None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    # 放下文件事件
    def dropEvent(self, event: QDropEvent) -> None:
        # 获取拖入的文件路径
        file_urls = event.mimeData().urls()
        file_path = file_urls[0].toLocalFile()  # 获取第一个文件的本地路径
        # 判断是否为文件夹
        if os.path.isdir(file_path):
            QMessageBox.warning(self, "警告", "请不要上传文件夹！")
            return
        if file_urls:
            # 提示是否上传
            reply = QMessageBox.question(self, '确认', '是否上传文件？', QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                for file_url in file_urls:
                    self.post_file_urls.put(file_url)

                self.Post_file_slot(True)
            else:
                return
            # 判断是否为文件夹
        else:
            return
        # 判断是否为文件夹

    # 读取文件夹
    def recv_folder(self):
        self.t = websocket_client.Get_folder()
        self.t.new_data.connect(self.Get_folder)
        self.t.start()

    # 发送文件夹结构
    def send_folder(self):

        data = str_write_folder_structure()
        time.sleep(0.001)  # 玄学
        self.tt = websocket_client.Post_folder()
        self.tt.message = data
        self.tt.log.connect(self.Post_folder)
        self.tt.start()

    def check_operatre(self):
        old_id = self.root_folder.get_id()
        self.recv_folder()  # 获取最新层次结构
        time.sleep(0.001)
        if old_id != self.root_folder.get_id():
            return -1  # 更新失败
        return 0

    def download_file(self, file_name:str) -> bool:
        path = file_name.replace('@0@', '\\')
        with requests.get(f"http://172.17.251.208:6618/static/files/{file_name}", stream=True) as response:
            if response.status_code == 200:
                with open(f'static\\files{path}', 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):  # 按块读取文件
                        file.write(chunk)
                self.download_file_signal.emit(True, os.path.basename(path))
                return True
            else:
                self.download_file_signal.emit(False, os.path.basename(path))
                return False

    def download_file_signal_slot(self, status: bool, file_name: str) -> None:
        if status:
            QMessageBox.information(self, "下载成功", f" {file_name} 下载成功")
        else:
            QMessageBox.warning(self, "下载失败", f" {file_name} 下载失败")
        return

    def get_file_servername(self, folder_: folder.folder) -> str:  # 获取文件在服务器上的名称
        return websocket_client.get_file_serverName(folder_.get_id()[:-1])

    def get_relative_path(self, folder_: folder.folder) ->str:  # 获取文件本地相对路径
        return self.root_path + folder_.get_id()[:-1].replace('/', '\\')

    # def mousePressEvent(self, event: QMouseEvent):
    #     print(f"Mouse pressed at: {event.pos()}")
    #     if event.button() == Qt.LeftButton:  # 如果点击的是鼠标左键
    #         print(f"Mouse clicked at: ({event.x()}, {event.y()})")
    #
    # def mouseReleaseEvent(self, event: QMouseEvent):
    #     print(f"Mouse Released at: {event.pos()}")
    #
    # def mouseMoveEvent(self, event: QMouseEvent):
    #     print(f"Mouse moved to: {event.pos()}")


temp = 0


def heartbert_check(log):
    global temp
    if log:
        window.ui.label_5.setText('H:' + str(temp))
        temp += 1
        temp %= 10
        window.ui.label_5.setStyleSheet('color:rgb(0,200,0)')
    else:
        window.ui.label_5.setText('W:' + str(temp))
        temp += 1
        temp %= 10
        window.ui.label_5.setStyleSheet('color:rgb(200,0,0)')


if __name__ == "__main__":
    with open('config.ini', 'r') as f:
        ip = f.readline().strip()
    websocket_client.ip = ip
    websocket_client.start_ws()
    print(websocket_client.ip)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.init()
    window.show()
    x = websocket_client.loop_connect()

    x.s = 2
    x.log.connect(heartbert_check)
    x.start()
    sys.exit(app.exec_())

# 剩余工作：
# 1. 优化界面
# 2. 处理客户端本地文件删除
# 4. 客户端本地文件结构修改，同步文件大小，文件创建者，修改时间等信息
# 3. 服务端将PCB映射到mysql数据库，并提供查询功能
# 5. bug处理
# 6. github测试
