import socket

def check_ftp(ip, port):
    try:
        # 创建一个TCP socket对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间为3秒
        sock.settimeout(3)
        # 尝试连接指定的IP地址和端口号
        sock.connect((ip, port))
        # 发送一个简单的命令来检查FTP服务
        sock.send(b"SYST\r\n")
        # 接收服务器返回的数据
        response = sock.recv(1024)
        # 关闭socket连接
        sock.close()
        # 检查是否包含FTP协议的回应
        if b"220" in response:
            # print(f"Port {port} on {ip} is open for FTP protocol.")
            # print(f"Banner:\n{response.decode()}")
            return response.decode()
        else:
            pass
    except socket.error:
        pass

# # 指定要探测的IP地址和端口号
# target_ip = "125.229.107.11"
# target_port = 21

# # 调用函数进行探测
# check_ftp(target_ip, target_port)
