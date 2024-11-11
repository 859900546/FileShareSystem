from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QProgressBar, QVBoxLayout, QLabel, QDialog


class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("上传进度")
        self.setFixedSize(400, 100)

        # 创建布局
        layout = QVBoxLayout(self)

        # 创建进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        # 创建状态标签
        self.status_label = QLabel("正在上传...", self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def update_progress(self, value):
        self.progress_bar.setValue(int(value * 100))
        if value >= 1.0:
            self.status_label.setText("上传完成！")
            QTimer.singleShot(1000, self.close)  # 延时关闭对话框
