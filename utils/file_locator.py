import os
import sys


def find_file(script_dir, file_name):
    while True:
        file_path = os.path.join(script_dir, file_name)  # 构造文件路径
        if os.path.isfile(file_path):  # 判断文件是否存在
            return file_path
        else:
            parent_dir = os.path.dirname(script_dir)  # 获取上一级目录
            # 如果已经到达根目录，仍未找到文件
            if parent_dir == script_dir:
                break
            script_dir = parent_dir  # 更新当前目录为上一级目录

    print("未找到文件：", file_name)
    return None


def find_path(file_name):
    try:
        # 尝试使用 os.path.dirname(os.path.abspath(sys.argv[0])) 获取路径
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        path = find_file(script_dir, file_name)
        if path:
            return path
        script_dir = os.getcwd()
        path = find_file(script_dir, file_name)
        if path:
            return path
    except:
        print("未找到可执行文件：", file_name)
    return None


# 示例调用
# 测试函数
# file_name = "img_win_x86_64.exe"
# file_path = find_path(file_name)
# print(file_path)
