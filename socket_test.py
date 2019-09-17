#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socketserver
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('logging.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(file_handler)


# 地址和端口 连接对象
class MyConn(object):  # 存放连接
    listconn = {}  # 地址端口:连接对象


class MyServer(socketserver.BaseRequestHandler):

    def setup(self):
        MyConn.listconn[self.client_address] = self.request
        logger.info('{0} is connectioned.'.format(self.client_address))
        pass

    def handle(self):
        while True:
            conn = self.request
            data = conn.recv(1024)
            if not data:
                break

            # 如果目标客户端在发送数据给目标客服端
            # 这里可以根据对方的ip和端口号来查找 我这里直接发给每一个用户了
            # print(MyConn.listconn)
            if len(MyConn.listconn) > 1:
                for i in MyConn.listconn.keys():
                    if self.client_address != i:
                        # print(data.decode("utf-8"))
                        MyConn.listconn[i].sendall(data)
                        logger.debug('{0}-->{1}:{2}'.format(self.client_address, i, data))
                pass
            else:  # 只有一个客户端则发送数据给客户端
                conn.sendall(data)
                logger.debug('{0}:{1}'.format(self.client_address, data))
                pass
            # conn.sendall(data)

    def finish(self):
        del MyConn.listconn[self.client_address]
        logger.info('{} is disconnectioned.'.format(self.client_address))
        pass

    pass


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 8023), MyServer)
    logger.info('waiting for connection....:8023')
    server.serve_forever()
