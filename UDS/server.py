#-*-coding:utf-8-*-
import socket
import os
import time
'''
UDS unix域套接字 处理进程间通信 (IPC)
'''
SERVER_PATH = '/tmp/python_unix_socket_server'

def run_unix_domain_socket_server():
	if os.path.exists(SERVER_PATH):
		os.remove(SERVER_PATH)
	print 'starting unix domain socket server'
	server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	server.bind(SERVER_PATH)
	server.listen(2)
	print 'Listening on path: %s' % SERVER_PATH

	while True:
		try:
			connection, client_address = server.accept()
			while True:
				data = connection.recv(1024)
				if data == 'DONE':
					print data
					connection.close()
					break
				else:
					print '-' * 20
					print data
					connection.sendall(data)
		except KeyboardInterrupt,e:
			print '-' * 20
			print 'Server is shutting down notw...'
			server.close()
			os.remove(SERVER_PATH)
			print 'Server shutdown and path removed'
			return 

if __name__ == '__main__':
	run_unix_domain_socket_server()
