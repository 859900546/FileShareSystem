from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


class DirectoryItemWidget(QWidget):
    def __init__(self, folder_):
        super().__init__()

        layout = QHBoxLayout()
        self.r_folder = folder_
        icon_label = QLabel('')

        icon_label.setStyleSheet('background-color: transparent;')
        if self.r_folder.check_file:
            image = QImage('rec/file_icon.png')
        else:
            image = QImage('rec/folder_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(30, 30)
        icon_label.setPixmap(scaled_pixmap)
        icon_label.setFixedSize(30, 30)
        # icon = QIcon(scaled_pixmap)
        # icon_label.setIcon(icon)
        # icon_label.setIconSize(pixmap.size())

        name_label = QLabel(folder_.name)
        mod_date_label = QLabel(folder_.date)
        type_label = QLabel("文件" if folder_.check_file else "文件夹")
        size_label = QLabel('')
        if folder_.check_file:
            size_label = QLabel(f'{folder_.size}KB')
        # Set alignment to ensure proper column alignment
        icon_label.setAlignment(Qt.AlignLeft)
        name_label.setAlignment(Qt.AlignLeft)
        mod_date_label.setAlignment(Qt.AlignLeft)
        type_label.setAlignment(Qt.AlignLeft)
        size_label.setAlignment(Qt.AlignLeft)

        # Add widgets to the layout with stretch factors
        layout.addWidget(icon_label, 1)
        layout.addWidget(name_label, 1)
        layout.addWidget(mod_date_label, 1)
        layout.addWidget(type_label, 1)
        layout.addWidget(size_label, 1)

        self.setLayout(layout)
