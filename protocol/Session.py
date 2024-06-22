import sys
import json
import asyncio
import websockets


class Session:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.receive_task = None
        self.callbacks = {}  # 存储回调函数的字典，以消息 ID 作为键

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri, ping_interval=sys.float_info.max)
            self.start_receiving()
            #print("WebSocket 连接成功")
        except websockets.exceptions.InvalidStatusCode as e:
            print(f"WebSocket 连接失败: {e}")

    def is_connected(self):
        if self.websocket and self.websocket.open:
            return True
        else:
            return False

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            #print("WebSocket 主动关闭链接")

    async def send_message(self, message):
        if self.websocket:
            await self.websocket.send(json.dumps(message))
            # print("socket 消息发送成功:", message)

    async def receive_messages(self):
        if self.websocket:
            try:
                async for message in self.websocket:
                    # print("socket 接收到到信息是:", message)
                    await self.handle_message(message)
                # await self.wait_until_closed()  # 等待连接关闭
            except websockets.exceptions.ConnectionClosed as e:
                print(f"WebSocket 连接关闭: {e}")

    async def handle_message(self, message):
        parsed_message = json.loads(message)
        message_id = parsed_message.get("id")
        if message_id in self.callbacks:
            callback = self.callbacks[message_id]
            # await callback(parsed_message)
            asyncio.create_task(callback(parsed_message))

        method = parsed_message.get("method")
        if method and method in self.callbacks:
            callback = self.callbacks[method]
            # await callback(parsed_message)
            asyncio.create_task(callback(parsed_message))

    def start_receiving(self):
        # 开始接收消息的线程
        self.receive_task = asyncio.create_task(self.receive_messages())

    def stop_receiving(self):
        # 停止接收消息的线程
        if self.receive_task:
            self.receive_task.cancel()

    def register_callback(self, message_id, callback):
        # 注册回调函数
        self.callbacks[message_id] = callback
       # print(f"注册回调函数 ID 为 {message_id} 的回调函数成功,callbacks size:", len(self.callbacks), " function is",{callback.__name__})

    def remove_callback(self, message_id):
        if message_id in self.callbacks:
            del self.callbacks[message_id]
            #print(f"移除消息 ID 为 {message_id} 的回调函数成功")
       # else:
           # print(f"消息 ID 为 {message_id} 的回调函数不存在")
