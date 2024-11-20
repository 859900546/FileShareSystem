from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

name2icon = {
    'folder': './res/icon/folder_icon.png',
    'file': './res/icon/file_icon.png',
    'mp4': './res/icon/mp4_icon.png',
    'mp3': './res/icon/mp3_icon.png',
    'jpg': './res/icon/jpg_icon.png',
    'png': './res/icon/jpg_icon.png',
    'gif': './res/icon/jpg_icon.png',
    'text': './res/icon/text_icon.png',
    'txt': './res/icon/txt_icon.png',
    'doc': './res/icon/pdf_icon.png',
    'docx': './res/icon/pdf_icon.png',
    'pdf': './res/icon/pdf_icon.png',
    'zip': './res/icon/zip_icon.png',
    'rar': './res/icon/zip_icon.png',
    'exe': './res/icon/exe_icon.png',
    'py': './res/icon/py_icon.png',
    'cpp': './res/icon/cpp_icon.png',
    'java': './res/icon/java_icon.png',
    'html': './res/icon/h_icon.png',
    'h': './res/icon/h_icon.png',
    'c': './res/icon/cpp_icon.png',
}


class DirectoryItemWidget(QWidget):
    def __init__(self, folder_):
        super().__init__()

        layout = QHBoxLayout()
        self.r_folder = folder_
        # 文件后缀名
        self.file_type = folder_.name.split('.')[-1].lower()
        if self.file_type is None or self.file_type == '':
            self.file_type = 'file'
        icon_label = QLabel('')

        icon_label.setStyleSheet('background-color: transparent;')
        size_x = 30
        size_y = 30
        if self.r_folder.check_file:
            if self.file_type not in name2icon:
                image = QImage(name2icon['file'])
            else:
                image = QImage(name2icon[self.file_type])
                size_x = 30
                size_y = 30

        else:
            image = QImage('./res/icon/folder_icon.png')  # 替换成你想要的图片路径
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(size_x, size_y)
        icon_label.setPixmap(scaled_pixmap)
        icon_label.setFixedSize(size_x, size_y)
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
