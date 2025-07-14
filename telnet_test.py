import telnetlib

def check_telnet(ip, port):
    try:
        # 连接Telnet服务器
        tn = telnetlib.Telnet(ip, port, timeout=3)
        
        # 读取欢迎消息或banner
        banner = tn.read_until(b"\r\n", timeout=3).decode("utf-8")

        # 发送命令并等待响应
        tn.write(b"echo\r\n")  # 发送一个命令，比如这里是echo命令
        response = tn.read_until(b"\r\n", timeout=3).decode("utf-8")  # 读取响应并解码

        # 检查是否收到了预期的响应
        # print(response)
        if "echo" in response.lower() or "account:" in response.lower():
            # print(f"Telnet service is available on {ip}:{port}")
            if not banner.isspace():
                return banner
            else:
                pass
        else:
            pass

        # 关闭Telnet连接
        tn.close()
    except Exception as e:
        pass


# ip = "192.168.2.1"
# port = 23  # Telnet默认端口是23
# check_telnet(ip, port)
