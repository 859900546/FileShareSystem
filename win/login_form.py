from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent

from PyQt5.QtWidgets import QFrame, QMainWindow, QApplication, QMessageBox
#from loguru import logger
from ui.login_form import Ui_Frame as ui_form
from ui.main_ui import MainWindow
from win.register_form import register_form
from Websocket_filesystem import websocket_client
from pointStruct.analysis_data import os_id

class login_form(ui_form, QFrame):
    def __init__(self, parent: QMainWindow = None):
        super(login_form, self).__init__()
        self.setupUi(self)
        self.mysql_pushButton.setText("文件管理系统")
        self.mysql_pushButton.setEnabled(False)
        self.root = parent
        self.root.tray_icon.hide()  # 先隐藏托盘图标
        self.window = None
        # 加载字体
        QtGui.QFontDatabase.addApplicationFont("res/otf/Social Media Circled.otf")

        # 隐藏原始的框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 按钮事件绑定
        self.close_pushButton.clicked.connect(self.close_event)
        self.min_pushButton.clicked.connect(self.showMinimized)

        self.login_pushButton.clicked.connect(self.login_pushButton_event)
        self.forget_password_pushButton.clicked.connect(self.forget_password_pushButton_event)
        self.register_pushButton.clicked.connect(self.register_pushButton_event)

        self.mysql_pushButton.clicked.connect(self.mysql_pushButton_event)

        # 底部按钮
        self.github_pushButton.clicked.connect(self.github_pushButton_event)
        self.phone_pushButton.clicked.connect(self.phone_pushButton_event)
        self.email_pushButton.clicked.connect(self.email_pushButton_event)
        self.t = None
        self.user_name = ""

    # 关闭的逻辑
    def close_event(self):
        #logger.info("关闭登录窗口")
        # 退出应用程序
        QApplication.instance().quit()

    # 数据库
    def mysql_pushButton_event(self):
        return
       # logger.info("数据库窗口")

    # self.mysql_form = mysql_form()
    #  self.mysql_form.show()

    def login_pushButton_event(self):
        #logger.info("用户登录")
        # 登录的逻辑写在这里
        user_name = self.user_name_lineEdit.text()
        password = self.password_lineEdit.text()
        if user_name == "" or password == "":
            QMessageBox.information(self, "错误提示", "请输入用户名密码")
            return
        self.user_name = user_name
        self.t = websocket_client.Login(user_name, password, os_id + "_" + user_name)
        self.t.log.connect(self.login_success)
        self.t.start()

    def login_success(self, log: bool):
        if not log:
            QMessageBox.information(self, "错误提示", "用户名或密码错误")
            return
        self.window = MainWindow()
        self.window.Heartbert.delay = 3
        self.window.init()
        self.window.username = self.user_name

        self.close()
        self.window.show()
        QMessageBox.information(self, f"登录成功", f"欢迎用户：{self.user_name}\n")

    def forget_password_pushButton_event(self):
        #logger.info("忘记密码")
        QMessageBox.information(self, "忘记密码", "请联系管理员admin")

    def register_pushButton_event(self):
        #logger.info("用户注册")
        self.register_form = register_form()
        self.register_form.show()

    def github_pushButton_event(self):
        #logger.info("跳转到github网站")
        QMessageBox.information(self, "GitHub", "859900546")
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/859900546"))

    def phone_pushButton_event(self):
        #logger.info("手机号")
        QMessageBox.information(self, "手机号", "手机号\n1807602575")

    def email_pushButton_event(self):
        #logger.info("邮箱")
        QMessageBox.information(self, "邮箱", "邮箱\n859900546@qq.com")

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        try:
            self._endPos = e.pos() - self._startPos
        except Exception as e:
            return
        self.move(self.pos() + self._endPos)

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
