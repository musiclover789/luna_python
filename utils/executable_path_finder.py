import platform

from utils.file_locator import find_path


def get_os_type(find_path):
    system = platform.system()
    machine = platform.machine()
    if system == "Windows":
        print("您当前的系统是: Windows")
        return find_path("windows_auth.exe")
    elif system == "Linux":
        if "aarch64" in machine:
            print("您当前的系统是: Linux ARM")
            return find_path("Linux ARM")
        else:
            print("您当前的系统是: Linux x86/x64")
            return find_path("linux_auth")
    elif system == "Darwin":
        if "arm" in machine:
            print("您当前的系统是: macOS ARM")
            return find_path("mac_arm_auth")
        else:
            print("您当前的系统是: macOS Intel")
            return find_path("mac_intel_auth")
    else:
        print("Unknown")
        return None

# 测试函数
# print(get_os_path())
