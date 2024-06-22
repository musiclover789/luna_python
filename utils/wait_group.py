import asyncio

class WaitGroup:
    def __init__(self):
        self.counter = 0
        self.event = asyncio.Event()

    async def add(self, count=1):
        self.counter += count

    async def done(self):
        self.counter -= 1
        if self.counter <= 0:
            self.event.set()  # 设置事件，唤醒等待的协程

    async def wait(self):
        await self.event.wait()  # 等待事件被设置
