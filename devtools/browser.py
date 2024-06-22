import asyncio
import os
import signal
import subprocess
from sys import platform
from typing import List, Optional, Callable
from common import chromium
from common.id_generator import next_id
from devtools.page import Page
from protocol.Session import Session


class Browser:
    def __init__(self):
        self._session = None  # Browser session object
        self.chromium_path: Optional[str] = None  # Path to Chromium executable
        self.user_data_dir: Optional[str] = None  # Path to user data directory
        self.proxy_str: Optional[str] = None  # Proxy string
        self.fingerprint: Optional[List[str]] = None  # Browser fingerprint information
        self.headless: bool = False  # Whether to run in headless mode
        self.window_size: Optional[str] = None  # Window size
        self.port: Optional[int] = None  # Port number
        self.proxy_pid: Optional[int] = None  # Proxy process ID
        self.browser_pid: Optional[int] = None  # Browser process ID

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    async def launch(self, chromium_path: str, user_data_dir: str = None, proxy_str: str = None,
                     fingerprint: List[str] = None, headless=False, window_size=None
                     ) -> 'Browser':
        """
              Launches a Chromium browser instance with specified settings.

              :param chromium_path: Path to the Chromium executable.
              :param user_data_dir: Path to the user data directory. If None, a temporary directory will be used.
              :param proxy_str: Proxy server address in the format "protocol://ip:port". If None, no proxy will be used.
              :param fingerprint: A list of strings representing the desired browser fingerprint settings.
              :param headless: Boolean indicating whether to run the browser in headless mode.
              :param window_size: Tuple representing the window size (width, height). If None, default size will be used.
              :return: An instance of the 'Browser' class.
              启动一个具有指定设置的Chromium浏览器实例。

              :param chromium_path: Chromium可执行文件的路径。
              :param user_data_dir: 用户数据目录的路径。如果为None，将使用临时目录。
              :param proxy_str: 代理服务器地址，格式为"protocol://ip:port"。如果为None，则不使用代理。
              :param fingerprint: 表示所需浏览器指纹设置的字符串列表。
              :param headless: 布尔值，指示是否以无头模式运行浏览器。
              :param window_size: 表示窗口大小的元组（宽度，高度）。如果为None，将使用默认大小。
              :return: 'Browser'类的实例。
          """

        self.chromium_path = chromium_path
        self.user_data_dir = user_data_dir
        self.proxy_str = proxy_str
        self.fingerprint = fingerprint
        self.headless = headless
        self.window_size = window_size
        uri_port = chromium.launch(self.chromium_path, self.user_data_dir, self.proxy_str, self.fingerprint,
                                   self.headless, self.window_size)
        self.session = Session(uri_port[0])
        self.port = uri_port[1]
        self.proxy_pid = uri_port[2]
        self.browser_pid = uri_port[3]
        if not self.session.is_connected():
            await self.session.connect()
            return self

    async def open_page(self, url: str) -> Page:
        """
                Opens a new page with the specified URL.

                :param url: The URL of the page to be opened.
                :return: An instance of the 'Page' class representing the opened page.
               打开指定URL的新页面。

               :param url: 要打开的页面的URL。
               :return: 代表已打开页面的 'Page' 类的实例。
       """

        id = next_id()
        message = {
            "id": id,
            "method": "Target.createTarget",
            "params": {
                "url": url,
            }
        }
        if not self.session.is_connected():
            await self.session.connect()

        page = Page()
        page.url = url

        async def callback_function(message):
            page.target_id = message["result"]["targetId"]

        self.session.register_callback(id, callback_function)
        await self.session.send_message(message)

        while True:
            if page.target_id:
                uri = f"ws://127.0.0.1:{self.port}/devtools/page/{page.target_id}"
                page.session = Session(uri)
                self.session.remove_callback(id)
                page.port = self.port
                return page
            await asyncio.sleep(0.001)
        self.session.remove_callback(id)
        return page

    async def open_page_and_listen(self, url: str, callback: Optional[Callable[[Page], None]] = None) -> Page:
        """
                Opens a new page and navigates to the specified URL, optionally executing a callback function before navigation.

                :param url: The URL to navigate to after opening the page.
                :param callback: An optional asynchronous callback function to be executed before navigating to the URL.
                                 The callback function should accept a single parameter, which is the 'Page' instance of the opened page.
                :return: An instance of the 'Page' class representing the opened and navigated page.
                打开一个新页面并导航到指定的URL，可选地在导航之前执行回调函数。

                :param url: 在打开页面后导航到的URL。
                :param callback: 一个可选的异步回调函数，在导航到URL之前执行。
                                 回调函数应接受一个参数，即已打开页面的 'Page' 类实例。
                :return: 代表已打开并导航页面的 'Page' 类的实例。
        """
        page = await self.open_page("")
        if callback:
            await callback(page)
        await page.navigate(url)
        return page

    async def get_pages(self) -> List[Page]:
        """
                Retrieves information about all open pages and returns a list of 'Page' instances representing each page.

                :return: A list of 'Page' instances representing all open pages.
                获取所有打开页面的信息，并返回表示每个页面的 'Page' 实例列表。

                :return: 包含所有打开页面的 'Page' 实例列表。
        """
        current_id = next_id()
        message = {
            "id": current_id,
            "method": "Target.getTargets",
        }
        if not self.session.is_connected():
            await self.session.connect()

        async def callback_function(message):
            for item in message["result"]["targetInfos"]:
                page = Page()
                page.url = item["url"]
                page.title = item["title"]
                page.type = item["type"]
                if page.type:
                    if page.type == "iframe":
                        continue
                page.target_id = item["targetId"]
                page.browser_context_id = item["browserContextId"]
                uri = f"ws://127.0.0.1:{self.port}/devtools/page/{page.target_id}"
                page.session = Session(uri)
                page.port = self.port
                pages.append(page)
            excute.append("")

        self.session.register_callback(current_id, callback_function)

        await self.session.send_message(message)
        pages = []
        excute = []
        while True:
            if len(excute) > 0:
                self.session.remove_callback(current_id)
                return pages
            await asyncio.sleep(0.001)
        self.session.remove_callback(current_id)
        return pages

    async def close(self) -> None:
        """
                Closes the browser and stops the associated services.

                This method sends a message to the browser to close, waits for 1 second, and then closes the session. If a proxy process ID is available, it also terminates the proxy process.

                :return: None
               关闭浏览器并停止相关服务。

               该方法向浏览器发送关闭消息，等待1秒，然后关闭会话。如果存在代理进程ID，则也会终止代理进程。

               :return: 无
        """
        id = next_id()
        message = {
            "id": id,
            "method": "Browser.close"
        }
        if not self.session.is_connected():
            await self.session.connect()
        await self.session.send_message(message)
        await asyncio.sleep(1)
        await self.session.close()
        if self.proxy_pid:
            if platform.system().lower() == "windows":
                subprocess.run(["taskkill", "/F", "/PID", str(self.proxy_pid)], check=True)
            else:
                os.kill(self.proxy_pid, signal.SIGTERM)
