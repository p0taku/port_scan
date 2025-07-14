import socket

def check_upnp(ip, port):
    # 创建UDP套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(2)  # 设置超时时间为2秒

    try:
        # 向指定IP地址和端口发送一个UPnP的发现消息
        udp_socket.sendto(b'M-SEARCH * HTTP/1.1\r\nHost:239.255.255.250:1900\r\nST:upnp:rootdevice\r\nMan:"ssdp:discover"\r\nMX:3\r\n\r\n', (ip, port))
        
        # 接收响应数据
        data, addr = udp_socket.recvfrom(1024)
        
        # 解码并打印响应数据
        clear_response = ''
        response_lines = data.decode().split('\n')
        for line in response_lines:
            line = line.strip()
            if line:  # 只打印非空行
                clear_response = clear_response + line + " "
        # print(f"Response from {addr}: {clear_response}")
        return clear_response

    except socket.timeout:
        pass

    finally:
        udp_socket.close()

# # 要检测的IP地址和端口号
# ip_address = "111.255.97.180"
# udp_port = 1900

# # 调用函数检测UPnP端口是否开放
# check_upnp(ip_address, udp_port)
