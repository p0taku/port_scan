import socket

def check_ssh(ip, port):
    try:
        # 创建socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间
        s.settimeout(2)
        # 尝试连接到指定的IP和端口
        s.connect((ip, port))
        # 发送SSH协议版本信息，获取banner
        s.send(b'SSH-2.0-Test\r\n')
        # 接收banner信息
        banner = s.recv(1024)
        #print(f"Port {port} is open. \nSSH banner: {banner.decode()}")
        return banner.decode(encoding='UTF-8', errors='ignore')
    except Exception as e:
        #print(f"Port {port} is closed or an error occurred: {e}")
        pass
    finally:
        s.close()

# # 要检测的IP地址和端口号
# ip = '192.168.2.1'
# port = 22  # SSH默认端口号为22

# # 调用函数进行检测
# check_ssh(ip, port)
