# -*-coding:utf-8-*-
'''
线程服务器
'''

import socket
import threading
import SocketServer

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 0
BUF_SIZE = 1024


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(BUF_SIZE)
        print 'Client received: %s' % response
    finally:
        sock.close()


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        current_thread = threading.current_thread()
        response = '%s : %s' % (current_thread.name, data)
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == '__main__':
    server = ThreadedTCPServer(
        (SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print 'Server loop running on thread: %s' % server_thread.name

    client(ip, port, 'hello from client1')
    client(ip, port, 'hello from client2')

    server.shutdown()
