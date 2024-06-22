import threading

# 全局变量
counter = 1
counter_lock = threading.Lock()


def next_id():
    global counter
    with counter_lock:
        counter += 1
        return counter