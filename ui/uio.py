# -*- coding: utf-8 -*-

# Form implementation generated from reading ui files 'uio.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this files will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal


class Ui_FileManagerWindow(object):
    def setupUi(self, FileManagerWindow):
        FileManagerWindow.setObjectName("FileManagerWindow")
        FileManagerWindow.resize(883, 737)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FileManagerWindow.sizePolicy().hasHeightForWidth())
        FileManagerWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(FileManagerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(9, -1, -1, -1)
        self.horizontalLayout_2.setSpacing(15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton_3.setMaximumSize(QtCore.QSize(60, 35))
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setMinimumSize(QtCore.QSize(80, 0))
        self.pushButton_5.setMaximumSize(QtCore.QSize(100, 35))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setMinimumSize(QtCore.QSize(40, 30))
        self.pushButton_4.setMaximumSize(QtCore.QSize(40, 30))
        self.pushButton_4.setSizeIncrement(QtCore.QSize(3, 0))
        self.pushButton_4.setStyleSheet("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setMinimumSize(QtCore.QSize(35, 0))
        self.label_5.setMaximumSize(QtCore.QSize(35, 16777215))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMouseTracking(False)
        self.pushButton.setTabletTracking(False)
        self.pushButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout.addWidget(self.pushButton_7)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.fileListWidget = QListWidget_2(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileListWidget.sizePolicy().hasHeightForWidth())
        self.fileListWidget.setSizePolicy(sizePolicy)
        self.fileListWidget.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(9)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.fileListWidget.setFont(font)
        self.fileListWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.fileListWidget.setResizeMode(QtWidgets.QListView.Fixed)
        self.fileListWidget.setObjectName("fileListWidget")
        self.verticalLayout_2.addWidget(self.fileListWidget)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        FileManagerWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(FileManagerWindow)
        QtCore.QMetaObject.connectSlotsByName(FileManagerWindow)

    def retranslateUi(self, FileManagerWindow):
        _translate = QtCore.QCoreApplication.translate
        FileManagerWindow.setWindowTitle(_translate("FileManagerWindow", "File Manager"))
        self.pushButton_3.setText(_translate("FileManagerWindow", "☰"))
        self.pushButton_5.setText(_translate("FileManagerWindow", "back"))
        self.pushButton_4.setText(_translate("FileManagerWindow", "flushed"))
        self.pushButton.setText(_translate("FileManagerWindow", "名称"))
        self.pushButton_2.setText(_translate("FileManagerWindow", "修改日期"))
        self.pushButton_6.setText(_translate("FileManagerWindow", "类型"))
        self.pushButton_7.setText(_translate("FileManagerWindow", "大小"))


class QListWidget_2(QtWidgets.QListWidget):
    value_changed = pyqtSignal(int, int, int)  # 信号

    def __init__(self, parent=None):
        super(QListWidget_2, self).__init__(parent)

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if event.button() == Qt.LeftButton:
            self.value_changed.emit(0, x, y)
        elif event.button() == Qt.RightButton:
            self.value_changed.emit(2, x, y)
        super(QListWidget_2, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if event.button() == Qt.LeftButton:
            self.value_changed.emit(1, x, y)
        elif event.button() == Qt.RightButton:
            self.value_changed.emit(3, x, y)
        super(QListWidget_2, self).mouseReleaseEvent(event)
