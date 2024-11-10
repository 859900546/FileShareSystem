from PyQt5.QtCore import QThread, pyqtSignal
from pynput.mouse import Listener
import pynput
import pygetwindow as gw
mouse = pynput.mouse.Controller()


class MyThread(QThread):
    value_changed = pyqtSignal(int, int, int)  # 信号

    def change_value(self, new_value, xx, y):
        self.value_changed.emit(new_value, xx, y)  # 发射带参数的信号

    def run(self):
        self.mo()

    def mo(self):
        with Listener(on_click=self.mouse_click) as listener:
            listener.join()

    def mouse_click(self, xx, y, button, pressed):
        # print(x,y)
        if pressed and button == pynput.mouse.Button.left:
            self.change_value(0, xx, y)
        elif not pressed and button == pynput.mouse.Button.left:
            self.change_value(1, xx, y)
        if pressed and button == pynput.mouse.Button.right:
            self.change_value(2, xx, y)
        elif not pressed and button == pynput.mouse.Button.right:
            self.change_value(3, xx, y)
        if not pressed and button == pynput.mouse.Button.x1:
            pass
        if not pressed and button == pynput.mouse.Button.x2:
            pass

    def is_mouse_in_window(self,window_title,mouse_x,mouse_y):
        # 获取窗口位置和大小
        window = gw.getWindowsWithTitle(window_title)[0]  # 获取特定标题的窗口
        window_rect = (window.left, window.top, window.right, window.bottom)
        # 判断鼠标是否在窗口内
        if window_rect[0] <= mouse_x <= window_rect[2] and window_rect[1] <= mouse_y <= window_rect[3]:
            return True
        return False
# x = MyThread()
# x.start()
