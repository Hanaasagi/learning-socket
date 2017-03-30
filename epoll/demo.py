# -*-coding:utf-8-*-

'''
当 一个程序使用阻塞socket时，常常使用一个线程（甚至是一个专门的程序）来进行各个socket之间的通信。主程序线程会包含接收客户端连接的服务端 监听socket。这个socket一次接收一个客户端连接，把连接传给另外一个线程新建的socket去处理。因为这些线程每个只和一个客户端通信，所 以处理时即便在某几个点阻塞也没有关系。这种阻塞并不会对其他线程的处理造成任何影响。
'''

'''
epoll 水平触发模式 
'''
import socket
import select
import argparse

SERVER_HOST = '127.0.0.1'

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
SERVER_RESPONSE = b'''HTTP/1.1 200 OK\r\nContent-Tyep: text/plain\r\nContent-Length: 25\r\n\r\nHello from Epoll Server'''


class EpollServer(object):
    def __init__(self, host=SERVER_HOST, port=0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(5)
        self.sock.setblocking(0)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print 'Start Epoll server'
        self.epoll = select.epoll()
        # sock.fileno()返回监听的文件描述符
        # 在服务端socket上面注册对读event的关注。一个读event随时会触发服务端socket去接收一个socket连接
        self.epoll.register(self.sock.fileno(), select.EPOLLIN)

    def run(self):
        try:
            # 映射文件描述符（整数）到其相应的网络连接对象
            connections = {}
            requests = {}
            responses = {}
            while True:
                # 查询epoll对象，看是否有任何关注的event被触发。参数“1”表示，我们会等待1秒来看是否有event发生。如果有任何我们感兴趣的event发生在这次查询之前，这个查询就会带着这些event的列表立即返回
                events = self.epoll.poll(1)
                # event作为一个序列（fileno，event code）的元组返回。fileno是文件描述符的代名词，始终是一个整数
                for fileno, event in events:
                    if fileno == self.sock.fileno():
                        connection, address = self.sock.accept()
                        connection.setblocking(0)
                        self.epoll.register(
                            connection.fileno(), select.EPOLLIN)
                        connections[connection.fileno()] = connection
                        requests[connection.fileno()] = b''
                        responses[connection.fileno()] = SERVER_RESPONSE
                    # 读事件
                    elif event & select.EPOLLIN:
                        # 将请求数据保存在 requests[fileno]中
                        requests[fileno] += connections[fileno].recv(1024)
                        # 判断请求是否完成
                        if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                            # 一旦完成请求已收到，就注销对读event的关注，注册对写（EPOLLOUT）event的关注。写event发生的时候，会回复数据给客户端
                            self.epoll.modify(fileno, select.EPOLLOUT)
                        # 打印请求头 requests[fileno].decode()[:-2]
                            print('-' * 40 + '\n' +
                                  requests[fileno].decode()[:-2])
                    # 写事件
                    elif event & select.EPOLLOUT:
                        byteswritten = connections[
                            fileno].send(responses[fileno])
                        responses[fileno] = responses[fileno][byteswritten:]
                        if len(responses[fileno]) == 0:
                            # 不关注任何事件
                            self.epoll.modify(fileno, 0)
                            # 关闭连接
                            connections[fileno].shutdown(socket.SHUT_RDWR)
                    # HUP（挂起）event表明客户端socket已经断开（即关闭），所以服务端也需要关闭。没有必要注册对HUP
                    # event的关注。在socket上面，它们总是会被epoll对象注册。
                    elif event & select.EPOLLHUP:
                        self.epoll.unregister(fileno)
                        connections[fileno].close()
                        del connections[fileno]
        except KeyboardInterrupt:
            print 'server stopping...'
        except socket.error, e:
            print e
        finally:
            self.epoll.unregister(self.sock.fileno())
            self.epoll.close()
            self.sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scoket Server Example with Epoll')
    parser.add_argument('--port', action='store',
                        dest='port', type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    server = EpollServer(host=SERVER_HOST, port=port)
    server.run()
