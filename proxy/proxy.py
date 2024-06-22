import subprocess
import time
import platform
from utils.file_locator import find_path


def proxy(proxy_str):
    file_name = None
    system = platform.system()
    machine = platform.machine()
    if system == "Windows":
        print("您当前的系统是: Windows")
        file_name = "rp.exe"
    elif system == "Linux":
        if "aarch64" in machine:
            print("您当前的系统是: Linux ARM")
        else:
            print("您当前的系统是: Linux x86/x64")
    elif system == "Darwin":
        if "arm" in machine:
            print("您当前的系统是: macOS ARM")
            file_name = "rp"
        else:
            print("您当前的系统是: macOS Intel")
            file_name = "rp"
    else:
        print("Unknown")
        return None, None

    file_path = find_path(file_name)
    print(f"Executing file at: {file_path}")

    # 使用 Popen 启动 Golang 程序
    process = subprocess.Popen(
        [file_path, "start", proxy_str],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # 读取标准输出的第一行
    stdout, stderr = process.stdout.readline(), process.stderr.readline()

    if stdout:
        print(f"Output from Golang program: {stdout.strip()}")
    if stderr:
        print(f"Error from Golang program: {stderr.strip()}")

    # 检查进程是否仍在运行
    if process.poll() is None:
        print(f"Process is still running with PID: {process.pid}")
    else:
        print(f"Process exited with return code: {process.returncode}")

    return stdout.strip(), process.pid
