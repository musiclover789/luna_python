import subprocess

# 设置代理参数  
upstream_url = 'http://example.com:80'
local_port = 8899

# 构建命令行参数列表  
command = ['proxy.py', '--upstream', upstream_url, '--port', str(local_port)]

# 使用subprocess运行proxy.py  
try:
    process = subprocess.Popen(command)
    print("proxy.py started successfully.")
except Exception as e:
    print(f"An error occurred while trying to start proxy.py: {e}")