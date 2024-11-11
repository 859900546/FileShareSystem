import asyncio
import websockets
from datetime import datetime
import server_fun
from server_fun import handle_postfile, handle_postfolder, handle_getfolder

connected_clients = set()

name = ''
size = 0


# 处理客户端消息
async def handle_client(websocket, path):
    global name, size
    # 添加连接到集合
    connected_clients.add(websocket)

    address = websocket.remote_address[0]
    print(f'{address}连接成功\n当前连接数{len(connected_clients)}')
    try:
        async for message in websocket:
            # 处理接收到的消息
            message = message.split(',')
            # print(f'{address}/{message[1]}:{message[0]}')
            if 'POSTfolder' in message[0]:
                await handle_postfolder(websocket)

            elif 'POSTfile' in message[0]:  # 接收文件
                await asyncio.wait_for(websocket.send('Post:startfile'), timeout=10)
                name = message[2]
                size = int(message[1])
            # await handle_postfile(websocket, message[1], message[2])

            elif 'GETfolder' in message[0]:
                await handle_getfolder(websocket)

            elif 'GETfile' in message[0]:  # 发送文件
                pass
            elif 'DELfile' in message[0]:  # 删除文件
                await server_fun.handle_deletefile(websocket, message[1])

            elif 'CREfile' in message[0]:  # 创建文件
                await server_fun.handle_createfile(websocket, message[1])

            elif 'COPYfile' in message[0]:  # 复制文件
                await server_fun.handle_copyfile(websocket, message[1], message[2])

            elif 'RENfile' in message[0]:  # 重命名文件
                await server_fun.handle_renamefile(websocket, message[1], message[2])

            elif 'hello_server' in message[0]:
                with open('message.txt', "r") as f:
                    await asyncio.wait_for(websocket.send(f.readlines(), timeout=10))
            else:
                pass
    except asyncio.TimeoutError:
        await asyncio.wait_for(websocket.send('Post:timeout'), timeout=10)
        server_fun.mutex = 1
    except websockets.exceptions.ConnectionClosedError:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        server_fun.mutex = 1
    finally:
        print(f'{address}断开连接\n当前连接数{len(connected_clients)}')
        # 客户端断开连接时，从集合中移除
        if websocket in connected_clients:
            connected_clients.remove(websocket)
            del websocket
        else:
            del websocket
        server_fun.mutex = 1


# 文件服务器处理客户端消息
async def handle_file_client(websocket, path):
    # 添加连接到集合
    # connected_clients.add(websocket)

    address = websocket.remote_address[0]
    print(f'file {address}连接成功\n当前连接数{len(connected_clients)}')
    await handle_postfile(websocket, name, size)


# 广播消息给所有客户端
async def broadcast(message):
    for websocket in connected_clients:
        await websocket.send(message)


async def control_server():
    print(f'文件服务器启动时间：{datetime.now()}')
    # 启动文件服务器
    server = await websockets.serve(handle_client, "0.0.0.0", 8608)
    await server.wait_closed()


async def file_server():
    print(f'文件服务器启动时间：{datetime.now()}')
    # 启动文件服务器
    server_1 = await websockets.serve(handle_file_client, "0.0.0.0", 8609)
    await server_1.wait_closed()


async def main():
    task_1 = asyncio.create_task(control_server())
    task_2 = asyncio.create_task(file_server())

    # 等待两个服务器的关闭
    await asyncio.gather(task_1, task_2)


if __name__ == '__main__':
    asyncio.run(main())
# 主线程用于管理用户
