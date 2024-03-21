import socket

def get_local_ip():
    try:
        # 创建套接字并连接到外部主机（比如 Google 的 DNS 服务器）
        # 这将返回本机的 IP 地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return str(e)


local_ip = get_local_ip()
