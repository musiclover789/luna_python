import subprocess
from typing import List
import requests
import portpicker
import json
import time
from requests.exceptions import ConnectionError, Timeout

from proxy.proxy import proxy


def get_port() -> int:
    return portpicker.pick_unused_port()


def write_fingerprint_to_file(fingerprint: List[str], filename: str):
    with open(filename, 'w') as f:
        for line in fingerprint:
            # 去掉每行开头的 '--'
            line = line.lstrip('-')
            # 写入到文件中
            f.write(line + '\n')


def launch(chromium_path: str, user_data_dir: str = None, proxy_str: str = None,
           fingerprint: List[str] = None, headless=False, window_size=None) -> str:
    # 获取随机端口
    random_port = get_port()
    print("端口是:", random_port)
    # 代理ip进程idÅ
    proxy_pid = None
    # 构建命令
    command = [
        chromium_path,
        "--remote-debugging-port=" + str(random_port),
    ]

    if user_data_dir:
        command.append("--user-data-dir=" + user_data_dir)

    if proxy_str:
        proxy_result = proxy(proxy_str)
        if proxy_result:
            command.append("--proxy-server=127.0.0.1:" + proxy_result[0])
            proxy_pid = proxy_result[1]

    if fingerprint:
        write_fingerprint_to_file(fingerprint, "C:\\luna-temp\\" + str(random_port))
        for fp in fingerprint:
            if 'luna' not in fp.lower():
                command.append(fp)

    if headless:
        command.append("--headless")

    if window_size:
        command.append("--window-size={},{}".format(window_size[0], window_size[1]))

    print("all conmand :", command)

    # 执行命令，不阻塞
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 获取子进程的PID
    browser_pid = process.pid
    # 打印PID
    print(f"The PID of the subprocess is: {browser_pid}")
    # 设置超时时间
    timeout = time.time() + 30  # 等待最多 30 秒

    # 等待 Chromium 返回调试信息
    while True:
        if time.time() > timeout:
            print("等待 Chromium 准备超时")
            break
        try:
            # 请求调试信息
            response = requests.get("http://127.0.0.1:" + str(random_port) + "/json/version", timeout=1)
            response.raise_for_status()
            # 解析 JSON 数据
            data = json.loads(response.text)
            # 如果能成功解析 JSON 数据，则说明 Chromium 已经准备好
            print("Chromium 已经准备好!")
            print("版本信息:", data["Browser"])
            print("webSocketDebuggerUrl", data["webSocketDebuggerUrl"])
            return data["webSocketDebuggerUrl"], str(random_port), proxy_pid, browser_pid
        except (ConnectionError, Timeout):
            print("等待 Chromium 准备中...")
            time.sleep(1)
