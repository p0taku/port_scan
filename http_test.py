import socket

def check_http(ip, port):
    try:
        # 创建一个IPv4的TCP套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间为2秒
        s.settimeout(2)
        # 尝试连接目标IP和端口
        s.connect((ip, port))
        
        # 发送HTTP GET请求
        request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip)
        s.sendall(request.encode())

        # 接收响应
        response = s.recv(4096)
        # print(response)

        # 打印响应
        if "HTTP" in str(response):
            clear_response = ''
            response_lines = response.decode().split('\n')
            for line in response_lines:
                line = line.strip()
                if line:  # 只打印非空行
                    clear_response = clear_response + line + " "
                    #print(line)
            # print(f"Response from {ip}:\n{clear_response}")
            return clear_response
        else:
            pass
    except Exception as e:
        pass
    finally:
        s.close()


# target_ip = "192.168.2.1"
# target_port = 8443
# check_http(target_ip, target_port)
