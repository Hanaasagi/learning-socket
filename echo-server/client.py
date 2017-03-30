# -*-coding:utf-8-*-

import socket


host = 'localhost'


def echo_client(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    print 'Connecting to server'
    s.connect(server_address)

    try:
        message = 'hello world'
        print 'sending message'
        s.sendall(message)
        amount_received = 0
        amount_excepted = len(message)
        while amount_received < amount_excepted:
            data = s.recv(16)
            amount_received += len(data)
            print 'received %s' % data
    except socket.errno, e:
        print 'socket error %s' % e
    except Exception, e:
        print 'Other exception %s ' % e
    finally:
        print 'closing connetion'
        s.close()


if __name__ == '__main__':
    echo_client(8090)
