import platform
import subprocess


def kill_process_mac():
    # 查找特定的进程名称
    ps_command = "ps aux | grep Chromium | grep -v grep | awk '{print $2}'"
    out = subprocess.getoutput(ps_command)
    # 解析出进程ID
    pids = out.split("\n")
    for pid_str in pids:
        if pid_str:
            try:
                pid = int(pid_str)
                # 结束进程
                kill_command = f"kill {pid}"
                subprocess.run(kill_command, shell=True)
                print(f"Process {pid} killed")
            except ValueError:
                print(f"Invalid PID: {pid_str}")


def kill_process_linux():
    # 查找特定的进程名称
    cmd = "ps aux | grep chromium | grep -v grep | awk '{print $2}' | xargs kill -9"
    out = subprocess.getoutput(cmd)
    print(f"Process killed: {out}")


def kill_process_windows():
    # 执行任务列表命令获取进程信息
    out = subprocess.getoutput("tasklist /NH")
    # 解析出进程ID
    processes = out.split("\n")
    for process in processes:
        if "chromium" in process.lower() or "chrome" in process.lower():
            fields = process.split()
            if len(fields) >= 2:
                pid_str = fields[1]
                try:
                    pid = int(pid_str)
                    # 结束进程
                    subprocess.run(["taskkill", "/F", "/PID", str(pid)])
                    print(f"Process {pid} killed")
                except ValueError:
                    print(f"Invalid PID: {pid_str}")


class Process:
    @classmethod
    def kill_process_by_pid(cls, pid):
        """
        根据进程ID终止进程。
        1. 根据当前操作系统类型判断使用不同的命令来终止进程。
        2. 如果操作系统是 Windows，使用 taskkill 命令来终止进程。
        3. 如果操作系统是其他系统（如 Linux 或 Mac OS），使用 kill 命令来终止进程。
        1. Determine the command to terminate the process based on the current operating system type.
        2. If the operating system is Windows, use the taskkill command to terminate the process.
        3. If the operating system is another system (such as Linux or Mac OS), use the kill command to terminate the process.
        """
        try:
            if platform.system().lower() == "windows":
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
            else:
                subprocess.run(["kill", str(pid)], check=True)
            print(f"Successfully killed process with PID {pid}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to kill process with PID {pid}: {e}")

    @classmethod
    def kill_process(csl) -> None:
        """
        根据操作系统类型终止进程。

        1. 获取当前操作系统类型。
        2. 如果操作系统是 Windows，调用 kill_process_windows() 函数。
        3. 如果操作系统是 Linux，调用 kill_process_linux() 函数。
        4. 如果操作系统是 Mac OS，调用 kill_process_mac() 函数。
        5. 如果操作系统类型未知，打印错误信息并退出。

        1. Get the current operating system type.
        2. If the operating system is Windows, call the kill_process_windows() function.
        3. If the operating system is Linux, call the kill_process_linux() function.
        4. If the operating system is Mac OS, call the kill_process_mac() function.
        5. If the operating system type is unknown, print an error message and exit.
        """
        os_item = platform.system()
        if os_item == "Windows":
            print("您的操作系统为 Windows")
            kill_process_windows()
        elif os_item == "Linux":
            print("您的操作系统为 Linux")
            kill_process_linux()
        elif os_item == "Darwin":
            print("您的操作系统为 Mac OS")
            kill_process_mac()
        else:
            print(f"Unknown OS: {os_item}")
            exit(1)
