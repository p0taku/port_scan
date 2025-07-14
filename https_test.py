import socket
import ssl

def check_https(target_host, target_port):
    try:
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 创建SSL上下文，并禁用证书验证
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        # 使用SSL上下文包装socket
        ssl_socket = context.wrap_socket(s, server_hostname=target_host)
        # 设置连接超时时间为2秒
        ssl_socket.settimeout(2)
        # 连接到目标主机和端口
        ssl_socket.connect((target_host, target_port))
        # 发送HTTPS请求头部
        ssl_socket.send(b'GET / HTTP/1.1\r\nHost: ' + target_host.encode() + b'\r\n\r\n')
        # 接收响应数据（最多1024字节）
        response = ssl_socket.recv(1024)
        # 判断响应内容，例如根据响应的HTTP状态码或者响应头部信息来判断服务类型
        if b'HTTP' in response:
            # print(f"The service running on port {target_port} is likely an HTTPS service.")
            clear_response = ''
            response_lines = response.decode().split('\n')
            for line in response_lines:
                line = line.strip()
                if line:  # 只打印非空行
                    clear_response = clear_response + line + " "
                    #print(line)
            # print(f"Response from {target_host}:\n{clear_response}")
            return clear_response
        else:
            pass
    except Exception as e:
        pass
    finally:
        # 关闭SSL连接
        ssl_socket.close()

# # 输入目标主机和端口
# target_host = "192.168.2.1"
# target_port = 8443

# # 探测服务类型
# check_https(target_host, target_port)
