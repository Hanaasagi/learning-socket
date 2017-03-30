# -*-coding:utf-8-*-
import socket
import os

BUFSIZE = 1024
'''
子进程会复制父进程的上下文
父子进程并不能确定执行顺序
'''


def test_socketpair():
    parent, child = socket.socketpair()
    pid = os.fork()
    try:
        if pid:
            print '************'
            print '@Parent, sending message...'
            child.close()
            parent.sendall('Hello from parent!')
            response = parent.recv(BUFSIZE)
            print 'Response from child:', response
            parent.close()
        else:
            print '-------------'
            print '@Child, waiting for message from parent'
            parent.close()
            message = child.recv(BUFSIZE)
            print 'Message from parent:', message
            child.sendall('Hello from child')
            child.close()
    except Exception, err:
        print 'Error :%s' % err


if __name__ == '__main__':
    test_socketpair()
