import os
import random
import string
import time
import threading
import shutil
import os

mutex = threading.Lock()


def create_cache_dir_in_sub_dir(base_path):
    random.seed(time.time_ns())

    # 生成随机字母
    letters = [random.choice(string.ascii_lowercase) for _ in range(3)]

    # 获取当前时间戳的中间 9 到 16 位数字
    timestamp = int(time.time() * 1e9)
    middle_digits = (timestamp // 1e6) % 1e8

    rand_folder_name = f"user_{middle_digits:08.0f}{''.join(letters)}"

    # 加锁
    mutex.acquire()
    try:
        cache_dir_full_path = os.path.join(base_path, rand_folder_name)

        # 检查文件夹是否已存在
        if os.path.exists(cache_dir_full_path):
            return cache_dir_full_path

        os.makedirs(cache_dir_full_path, exist_ok=True)
        time.sleep(0.01)
        print("当前缓存目录为:", cache_dir_full_path)
        return cache_dir_full_path
    finally:
        mutex.release()

