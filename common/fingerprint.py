import os
import time

def write_command_line_args_to_file(args):
    # 构建文件夹路径
    folder_path = "C:\\luna-temp"
    # 检查文件夹是否存在，如果不存在则创建
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 获取当前毫秒数字作为文件名
    millis = int(round(time.time() * 1000))
    file_path = os.path.join(folder_path, f"{millis}")

    try:
        # 打开文件并写入命令行参数
        with open(file_path, 'w') as file:
            for arg in args:
                # 去掉每个命令前面的两个短横线，并写入文件
                file.write(arg[2:] + '\n')
        print(f"命令行参数已成功写入到文件: {file_path}")
    except Exception as e:
        print(f"写入文件时出现错误: {e}")

