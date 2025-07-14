import socket

def check_rtsp(ip, port):
    try:
        # 创建一个TCP socket对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间为3秒
        sock.settimeout(3)
        # 尝试连接指定的IP地址和端口号
        sock.connect((ip, port))
        # 发送RTSP协议的OPTIONS请求
        sock.send(b"OPTIONS * RTSP/1.0\r\n\r\n")
        # 接收服务器返回的数据
        response = sock.recv(1024)
        # 检查是否包含RTSP协议的回应
        if b"RTSP" in response:
            clear_response = ''
            response_lines = response.decode().split('\n')
            for line in response_lines:
                line = line.strip()
                if line:  # 只打印非空行
                    clear_response = clear_response + line + " "
            # print(f"Port {port} on {ip} is open for RTSP protocol.")
            # print(f"Banner:\n{clear_response}")
            return clear_response
        else:
            pass
    except Exception as e:
        pass
    finally:
        # 关闭socket连接
        sock.close()

# # 指定要探测的IP地址和端口号
# target_ip = "118.232.126.31"
# target_port = 554

# # 调用函数进行探测
# check_rtsp(target_ip, target_port)
