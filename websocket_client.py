import os
import sys
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import websocket
from analysis_data import *

ip = '127.0.0.1'

try:
    ws = websocket.WebSocket()
    ws.connect("ws://127.0.0.1:8608")
except:
    pass


class send(QThread):
    def __init__(self, m):
        self.message = m

    def run(self):
        ws.send(self.message)


class loop_connect(QThread):
    log: pyqtSignal = pyqtSignal(bool)
    s = 0

    def run(self):
        while True:
            try:
                ws.send(',')
                self.log.emit(True)
                print("心跳检测正常：", get_date())
            except websocket.WebSocketConnectionClosedException:
                print("WebSocket 连接已关闭")
                self.log.emit(False)
                ws.connect("ws://127.0.0.1:8608")
            except Exception as e:
                print("WebSocket 连接异常：", e)
                self.log.emit(False)
                ws.connect("ws://127.0.0.1:8608")
            time.sleep(self.s)


class recv(QThread):
    data_sent = pyqtSignal(str)

    def __init__(self, m):
        self.message = m

    def run(self):
        s = ws.recv()
        self.data_sent(s)  # 发送信号


class Get_folder(QThread):
    new_data = pyqtSignal(str)

    def run(self):
        #  ws.connect("ws://112.74.184.16:8608")
        try:
            ws.send(f'GETfolder:,{os_id}')
            s = ws.recv()
            self.new_data.emit(s)
        except:
            pass


class Post_folder(QThread):
    message = None
    log = pyqtSignal(bool)

    def run(self):
        # ws.connect("ws://112.74.184.16:8608")
        if self.message is None:
            return
        try:
            ws.send(f'POSTfolder:,{os_id}')
            s = ws.recv()
            if s == "Post:start":
                ws.send(self.message)  # 发送数据
                self.log.emit(True)
            else:
                print(s, 'ft')
                self.log.emit(False)
        except:
            pass


class Get_file(QThread):
    new_data = pyqtSignal(str)

    def __init__(self, name):
        self.file_name = name

    def run(self):
        if not ws.connected:
            ws.connect("ws://112.74.184.16:8608")
        ws.send('GETfile:' + self.file_name)
        s = ws.recv()
        self.new_data.emit(s)


class Post_file(QThread):
    send_progress = pyqtSignal(float)
    log = pyqtSignal(bool)

    def __init__(self, AbsolutePath, RelativePath):
        super().__init__()
        self.file = AbsolutePath
        self.RelativePath = RelativePath
        self.total_chunks = 0
        self.chunk_size = 0
        self.file_size = 0

    def run(self):
        self.chunk_size = 1024 * 1024  # 每次发送 1MB
        self.file_size = os.path.getsize(self.file)
        self.total_chunks = (self.file_size + self.chunk_size - 1) // self.chunk_size  # 总共的分块数
        ws.send(f'POSTfile:,{self.total_chunks},{self.RelativePath}')
        s = ws.recv()
        if s == "Post:startfile":
            webss = websocket.WebSocket()  # 发送数据端口
            try:
                webss.connect("ws://127.0.0.1:8609")  # 发送数据端口
            except:
                return
            self.send_file(self.file, webss)  # 发送数据
        else:
            self.log.emit(False)

    def send_file(self, file_path, webs):
        with open(file_path, 'rb') as f:
            start_time = time.time()  # 记录开始时间
            print(self.total_chunks, self.chunk_size, self.file_size)
            for chunk_num in range(self.total_chunks):
                data: bytes = f.read(self.chunk_size)
                #  print(type(data), data.decode('utf-8'))
                webs.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
                # 计算进度
                progress = (chunk_num + 1) / self.total_chunks * 100
                elapsed_time = time.time() - start_time
                estimated_time_left = (elapsed_time / (chunk_num + 1)) * (self.total_chunks - (chunk_num + 1))

                self.send_progress.emit(progress)  # 发送进度信号

                # 显示进度 sys.stdout.write( f"\rSending chunk {chunk_num + 1}/{self.total_chunks} ({progress:.2f}%) -
                # Estimated time left: {estimated_time_left:.2f}s") sys.stdout.flush()
            webs.close()
            print("\nFile transfer complete.")


class create_file(QThread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        ws.send(f'CREfile:,{self.name}')
        s = ws.recv()
        print(s)


class delete_file(QThread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        ws.send(f'DELfile:,{self.name}')
        s = ws.recv()
        print(s)


def get_file_serverName(Relative_path: str):
    name = Relative_path.replace('\\', '@0@')
    name = name.replace('/', '@0@')
    return name
# test = Post_file(r"D:\Desktop\test.pdf")
# test.start()
# test.wait()
