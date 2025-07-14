#!/usr/bin/python3
#coding:utf-8
#Author:se55i0n
#目标tcp端口开放扫描及应用端口banner识别

import sys
import socket
import logging
import json
import requests
import dns.resolver
from time import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib3.exceptions import InsecureRequestWarning
#线程池
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Lock
from ftp_test import check_ftp
from http_test import check_http
from https_test import check_https
from rtsp_test import check_rtsp
from ssh_test import check_ssh
from telnet_test import check_telnet
from upnp_test import check_upnp

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 配置日志记录，将结果输出到 'scan_results.log'
logging.basicConfig(filename='scan_results.log', level=logging.INFO, format='%(message)s')

class Scanner:
    def __init__(self, target, start, end):
        self.target = target
        self.start = int(start)
        self.end = int(end)
        self.W = '\033[0m'
        self.G = '\033[1;32m'
        self.O = '\033[1;33m'
        self.R = '\033[1;31m'
        self.time = time()
        self.ports = []
        self.result = []
        self.scan_result = []
        self.mutex = Lock()
        self.get_ports()

    def get_ports(self):
        self.ports = list(range(self.start, self.end + 1))

    def check_cdn(self):
        #目标域名cdn检测
        myResolver = dns.resolver.Resolver()
        myResolver.lifetime = myResolver.timeout = 2.0
        dnsserver = [['114.114.114.114'],['8.8.8.8'],['223.6.6.6']]
        try:
            for i in dnsserver:
                myResolver.nameservers = i
                record = myResolver.resolve(self.target)
                self.result.append(record[0].address)
        except Exception as e:
            pass
        finally:
            return True if len(set(list(self.result))) > 1 else False

    def tcp_scan_port(self, port):# TCP全连接扫描，更准确，SYN误报高
        #端口扫描
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
                s.settimeout(0.2)
                return True if s.connect_ex((self.target, port)) == 0 else False
        except Exception as e:
            pass

    def important_port_scan(self, port): #直接先对几个重点端口进行扫描
        if port == 21:
            return check_ftp(self.target, port)
        elif port == 22:
            return check_ssh(self.target, port)
        elif port == 23:
            return check_telnet(self.target, port)
        elif port == 554:
            return check_rtsp(self.target, port)
        elif port == 1900:
            return check_upnp(self.target, port)
        else:
            pass

    def get_socket_info(self, port):
        #socket获取banner
        try: 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.2)
                s.connect((self.target, port))
                s.send(b'HELLO\r\n')
                return s.recv(1024).split(b'\r\n')[0].decode().strip('\r\n')
        except Exception as e:
            pass

    def log_scan_result(self, port, status, banner=''):
        # 日志记录，输出JSON格式到 'scan_results.log'
        result = {
            'target': self.target,
            'port': port,
            'status': status,
            'banner': banner,
            'timestamp': time()
        }
        logging.info(json.dumps(result))

    def gen_result_list(self, port, banner=''):
        new_scan_result = {'port':port, 'banner':banner}
        self.scan_result.append(new_scan_result)
        self.log_scan_result(port, 'open', banner)

    def get_result(self):
        # print(self.scan_result)
        print(f'{self.R}    {"port".rjust(6)}      status {"banner".rjust(18)}{self.W}')
        result = sorted(self.scan_result, key=lambda x: x['port'])
        for item in result:
            s_port = item['port']
            s_banner = item['banner']
            print(f'{self.G}[+] {str(s_port).rjust(6)} ----- open  {s_banner[:18]}{self.W}')

    def run(self, port):
        try:
            if port in [21, 22, 23, 554, 1900]:
                self.gen_result_list(port, self.important_port_scan(port)[:18])
            elif self.tcp_scan_port(port):
                banner = check_http(self.target, port)
                self.mutex.acquire()
                if banner:
                    self.gen_result_list(port, banner[:18])
                else:
                    banner = check_https(self.target, port)
                    if banner:
                        self.gen_result_list(port, banner[:18])
                    else:
                        banner = self.get_socket_info(port)
                        if banner:
                            self.gen_result_list(port, banner[:18])
                        else:
                            self.gen_result_list(port)
                self.mutex.release()
            else:
                pass
        except Exception as e:
            pass

    def _start(self):
        try:
            print('-'*60)
            print(f'{self.O}[-] 正在扫描地址: {socket.gethostbyname(self.target)}{self.W}')
            print('-'*60)
            #线程数
            pool = ThreadPool(processes=100)
            #get传递超时时间，用于捕捉ctrl+c
            pool.map_async(self.run, self.ports).get(0xffff)
            pool.close()
            pool.join()
            self.get_result()
            print('-'*60)
            print(f'{self.O}[-] 扫描完成耗时: {time()-self.time} 秒.{self.W}')
        except KeyboardInterrupt:
            print(f'{self.R}\n[-] 用户终止扫描...')
            sys.exit(1)

    def check_target(self):
        #判断目标是域名还是还是ip地址
        flag = self.target.split('.')[-1]
        try:
            #ip地址
            if int(flag) >= 0:
                self._start()
        except:
            #域名地址
            if not self.check_cdn():
                self._start()
            else:
                print('-'*60)
                print(f'{self.R}[-] 目标使用了CDN技术,停止扫描.{self.W}')
                print('-'*60)

if __name__ == '__main__':
    myscan = Scanner("192.168.2.242", 1, 10000)
    myscan.check_target()
    # result = myscan.get_result()

    # myscan._start()
