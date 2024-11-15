import os
import time
import requests
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import websocket
from pointStruct.analysis_data import *

try:
    with open('./config.ini', 'r') as f:
        ip = f.readline().strip()
except:
    ip = '127.0.0.1'
timeout: int = 200
ws = websocket.WebSocket()


def start_ws():
    try:
        ws.connect(f"ws://{ip}:8608", timeout=timeout)
    except:
        pass


class send(QThread):
    def __init__(self, m: str) -> None:
        self.message = m
        return

    def run(self):
        try:
            ws.send(self.message)
        except:
            pass


class loop_connect(QThread):
    log: pyqtSignal = pyqtSignal(bool)
    delay = 0

    def run(self):
        while True:
            try:
                ws.send(',')
                self.log.emit(True)
            # print("心跳检测正常：", get_date())
            except websocket.WebSocketConnectionClosedException:
                print("WebSocket 连接已关闭")
                self.log.emit(False)
                try:
                    ws.connect(f"ws://{ip}:8608", timeout=timeout)
                except:
                    pass
            except Exception as e:
                # print("WebSocket 连接异常：", e)
                self.log.emit(False)
                try:
                    ws.connect(f"ws://{ip}:8608", timeout=timeout)
                except Exception as e:
                    print(e)
            time.sleep(self.delay)


class recv(QThread):
    data_sent = pyqtSignal(str)

    def __init__(self, m: str) -> None:
        self.message = m
        return

    def run(self):
        try:
            s = ws.recv()
            self.data_sent(s)  # 发送信号
        except:
            pass


class Get_folder(QThread):
    new_data = pyqtSignal(str)

    def run(self):
        #  ws.connect(f"ws://{ip}:8608")
        try:
            if not ws.connected:
                start_ws()
            ws.send(f'GETfolder:,{os_id}')
            s = ws.recv()
            self.new_data.emit(s)
        except:
            pass


class Post_folder(QThread):
    message = None
    log = pyqtSignal(bool)

    def run(self):
        # ws.connect(f"ws://{ip}:8608")
        if self.message is None:
            return
        cnt = 0
        while cnt < 10:
            try:
                ws.send(f'POSTfolder:,{os_id}')
                s = ws.recv()
                if s == "Post:start":
                    ws.send(self.message)  # 发送数据
                    print('push成功')
                    self.log.emit(True)
                    break
                else:
                    print(s, 'FT')
                    ws.close()
                    time.sleep(0.1)
                    ws.connect(f"ws://{ip}:8608", timeout=timeout)
                    self.log.emit(False)
                    cnt += 1
            except Exception as e:
                print(e)
                if e == "WebSocket connection is closed":
                    start_ws()
                cnt += 1
                pass


class Get_file(QThread):
    new_data = pyqtSignal(str)

    def __init__(self, name: str) -> None:
        self.file_name = name
        return

    def run(self):
        if not ws.connected:
            start_ws()
        try:
            ws.send(f'GETfile:{self.file_name},{os_id}')
            s = ws.recv()
            self.new_data.emit(s)
        except Exception as e:
            print(e)


class Post_file(QThread):
    send_progress = pyqtSignal(float)
    log = pyqtSignal(bool)

    def __init__(self, AbsolutePath: str, RelativePath: str) -> None:
        super().__init__()
        self.file = AbsolutePath
        self.RelativePath = RelativePath
        self.total_chunks = 0
        self.chunk_size = 0
        self.file_size = 0
        return

    def run(self):
        self.chunk_size = 1024 * 1024  # 每次发送 1MB
        self.file_size = os.path.getsize(self.file)
        self.total_chunks = (self.file_size + self.chunk_size - 1) // self.chunk_size  # 总共的分块数
        if not ws.connected:
            start_ws()
        try:
            ws.send(f'POSTfile:,{self.total_chunks},{self.RelativePath},{os_id}')
            s = ws.recv()
        except Exception as e:
            print(e)
            self.log.emit(False)
            return
        if s == "Post:startfile":
            webss = websocket.WebSocket()  # 发送数据端口
            try:
                webss.connect(f"ws://{ip}:8609")  # 发送数据端口
            except:
                self.log.emit(False)
                return
            self.send_file(self.file, webss)  # 发送数据
            self.log.emit(True)
        else:
            self.log.emit(False)

    def send_file(self, file_path: str, webs: websocket) -> None:
        with open(file_path, 'rb') as f:
            for chunk_num in range(self.total_chunks):
                data: bytes = f.read(self.chunk_size)
                #  print(type(data), data.decode('utf-8'))
                try:
                    webs.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
                except Exception as e:
                    print(e, '167')
                # 计算进度
                progress = (chunk_num + 1) / self.total_chunks
                self.send_progress.emit(progress)  # 发送进度信号
                # 显示进度 sys.stdout.write( f"\rSending chunk {chunk_num + 1}/{self.total_chunks} ({progress:.2f}%) -
                # Estimated time left: {estimated_time_left:.2f}s") sys.stdout.flush()
            self.send_progress.emit(1.0)  # 发送进度信号
            webs.close()
        return


class download_file(QThread):
    progress = pyqtSignal(float)

    def __init__(self, pointer: folder.folder) -> None:
        super().__init__()
        self.server_name = get_file_serverName(pointer.get_id()[:-1])
        self.name = pointer.get_id()[:-1].replace('/', '\\')
        self.root_path = 'static\\files'
        self.file_size: int = int(pointer.size) * 1024
        # self.file_size = pointer.size
        return

    def run(self):
        path = self.root_path + self.name
        print(self.server_name)
        dest_dir = os.path.dirname(path)  # 获取目标文件路径的目录部分
        chunk_size: int = 1024  # 每次下载 1MB
        total_size: int = 0
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)  # 创建目标文件夹及其父文件夹
        with requests.get(f"http://172.17.251.208:6618/static/files/{self.server_name}", stream=True) as response:
            if response.status_code == 200:
                self.progress.emit(0.01)  # 发送进度信号
                with open(path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=chunk_size):  # 按块读取文件
                        total_size += chunk_size
                        self.progress.emit(total_size / self.file_size)  # 发送进度信号
                        file.write(chunk)
                self.progress.emit(1.0)  # 发送进度信号
            else:
                self.progress.emit(-1.0)  # 发送进度信号


class create_file(QThread):

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        return

    def run(self):
        if not ws.connected:
            start_ws()
        try:
            ws.send(f'CREfile:,{self.name},{os_id}')
            s = ws.recv()
            print(s)
        except Exception as e:
            print(e)


class delete_file(QThread):
    log = pyqtSignal(bool)
    progress = pyqtSignal(float)

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        return

    def run(self):
        if not ws.connected:
            start_ws()
        try:
            ws.send(f'DELfile:,{self.name},{os_id}')
            s = ws.recv()
            print(s)
            self.log.emit(True)
            self.progress.emit(1.0)
        except Exception as e:
            print(e)
            self.log.emit(False)
            self.progress.emit(1.0)


class copy_file(QThread):
    log = pyqtSignal(bool)

    def __init__(self, path: str, dest_path: str) -> None:
        super().__init__()
        self.name = get_file_serverName(path)
        self.new_name = get_file_serverName(dest_path)
        return

    def run(self):
        if not ws.connected:
            start_ws()
        try:
            ws.send(f'COPYfile:,{self.name},{self.new_name},{os_id}')
            s = ws.recv()
            print(s)
            self.log.emit(True)
        except Exception as e:
            print(e)
            self.log.emit(False)


class rename_file(QThread):
    log = pyqtSignal(bool)

    def __init__(self, path: str, new_name: str) -> None:
        super().__init__()
        self.name = get_file_serverName(path)
        self.new_name = new_name
        return

    def run(self):
        if not ws.connected:
            start_ws()
        try:
            ws.send(f'RENfile:,{self.name},{self.new_name},{os_id}')
            s = ws.recv()
            print(s)
            self.log.emit(True)
        except Exception as e:
            print(e)
            self.log.emit(False)


def get_file_serverName(Relative_path: str) -> str:
    name = Relative_path.replace('\\', '@0@')
    name = name.replace('/', '@0@')
    return name
# test = Post_file(r"D:\Desktop\test.pdf")
# test.start()
# test.wait()
