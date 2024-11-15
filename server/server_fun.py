import asyncio
import os
import shutil
import time

from websockets import ConnectionClosed

mutex = 1
data_path = 'data.txt'
with open(data_path, "r", encoding='gbk') as f:
    data = f.readlines()
max_time = 10

# 根目录
root_path = r'D:\文档\个人兴趣类\我的项目\JS study\static\files'


async def handle_postfile(websocket, file_name: str, file_size):
    # 发送启动文件传输的消息
    await asyncio.wait_for(websocket.send('Post:startfile'), timeout=10)
    name = get_server_file_name(file_name)
    print(name)
    try:
        async for chunk in websocket:
            if isinstance(chunk, bytes):
                with open(root_path + '\\' + name, "ab") as f:
                    f.write(chunk)  # 按块保存文件
            else:
                print("Received non-file data:", chunk)

        # 文件传输完成，保存到磁盘
        print("File saved successfully.")
    except ConnectionClosed as e:
        print(f"Connection closed unexpectedly: {e}")
    # 如果需要，可以进行额外的处理，如记录日志等
    finally:
        await websocket.close()  # 在finally块中确保连接关闭


async def handle_postfolder(websocket):
    global mutex, data, max_time, data_path
    p_start = time.time()
    while not mutex:
        if time.time() - p_start >= max_time:
            await asyncio.wait_for(websocket.send('Post:timeout'), timeout=10)
            mutex = 1  # nb的1
            return
        time.sleep(0.01)
        pass
    mutex = 0
    await asyncio.wait_for(websocket.send('Post:start'), timeout=10)  # 设置超时时间为10秒  前为标识符后为消息
    #  await websocket.send(data)
    x = await asyncio.wait_for(websocket.recv(), timeout=10)
    # data = message[4:]
    data = check_data(x)  # 检查data完整性
    mutex = 1
    # await websocket.send('0,ok')  # 前为标识符后为消息
    with open(data_path, "w") as ff:
        ff.writelines(data)
    # nows = "log/" + message[1] + str(datetime.now())[:19].replace(':', '--') + ".txt"
    # with open(nows, "w") as ff:
    #     ff.writelines(data)


async def handle_getfolder(websocket):
    await asyncio.wait_for(websocket.send(data), timeout=10)


async def handle_deletefile(websocket, file_name: str):
    file_path = root_path + '\\' + file_name
    code_str = 200
    try:
        os.remove(file_path)
    except Exception as e:
        code_str = 404
        print(f"Error occurred while deleting file: {e}")
    try:
        await asyncio.wait_for(websocket.send(f'DEL,{file_name}:{code_str}'), timeout=10)
    except asyncio.TimeoutError:
        print("Timeout while sending message to client.")


async def handle_createfile(websocket, file_name: str):
    file_path = root_path + '\\' + file_name
    try:
        with open(file_path, "w") as ff:
            ff.write("")
    except Exception as e:
        print(f"Error occurred while creating file: {e}")
    try:
        await asyncio.wait_for(websocket.send(f'CREATE,{file_name}:ok'), timeout=10)
    except asyncio.TimeoutError:
        print("Timeout while sending message to client.")


async def handle_copyfile(websocket, orc_file_name: str, dest_file_name: str):
    orc_file_name = get_server_file_name(orc_file_name)
    dest_file_name = get_server_file_name(dest_file_name)
    try:
        shutil.copyfile(root_path + '\\' + orc_file_name, root_path + '\\' + dest_file_name)
    except Exception as e:
        print(f"Error occurred while copying file: {e}")
    try:
        await asyncio.wait_for(websocket.send(f'COPY,{orc_file_name},{dest_file_name}:ok'), timeout=10)
    except asyncio.TimeoutError:
        print("Timeout while sending message to client.")


async def handle_renamefile(websocket, orc_file_name: str, dest_file_name: str):
    orc_file_name = get_server_file_name(orc_file_name)
    dest_file_name = get_server_file_name(dest_file_name)
    try:
        os.rename(root_path + '\\' + orc_file_name, root_path + '\\' + dest_file_name)
    except Exception as e:
        print(f"Error occurred while renaming file: {e}")
    try:
        await asyncio.wait_for(websocket.send(f'RENAME,{orc_file_name},{dest_file_name}:ok'), timeout=10)
    except asyncio.TimeoutError:
        print("Timeout while sending message to client.")


def get_server_file_name(file_name: str) -> str:
    name = file_name.replace('\\', '@0@')
    name = name.replace('/', '@0@')
    return name


def check_data(d):
    if d is None or not len(d):
        return data
    if "POSTfolder" in d or "GETfolder" in d:
        return data
    return d
