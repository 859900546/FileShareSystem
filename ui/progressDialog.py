from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QProgressBar, QVBoxLayout, QLabel, QDialog


class ProgressDialog(QDialog):
    def __init__(self, name: str, type_: str = "上传"):
        super().__init__()
        self.name = name
        self.type_ = type_
        self.setWindowTitle(f"{self.name} -{type_}进度")
        self.setFixedSize(400, 100)

        # 创建布局
        layout = QVBoxLayout(self)

        # 创建进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # 创建状态标签
        self.status_label = QLabel(f"正在{type_}...", self)
        layout.addWidget(self.status_label)

        # 创建图标
        image = QImage('./res/mainicon/folder_icon_1.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

    def update_progress(self, value: float):
        self.progress_bar.setValue(int(value * 100))
        if value < 0.0:
            self.status_label.setText(f"{self.type_}失败！")
            QTimer.singleShot(1000, self.close)  # 延时关闭对话框
        if value >= 1.0:
            self.status_label.setText(f"{self.type_}完成！")
            QTimer.singleShot(1000, self.close)  # 延时关闭对话框
