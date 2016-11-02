#-*-coding:utf-8-*-

"""
进程服务器
setDaemon(True) 主线程停止会将子线程也停止，就算里面有死循环
setDaemon(False) 主线程会在子线程停止后停止 相当于join()
"""



import os
import socket
import threading
import SocketServer

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 0
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server'

class ForkingClient():
	def __init__(self, ip, port):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((ip,port))

	def run(self):
		current_process_id = os.getpid()
		print 'PID %s Sending echo message to the server :%s' % (current_process_id, ECHO_MSG)
		sent_data_length = self.s.send(ECHO_MSG)
		response = self.s.recv(BUF_SIZE)
		print 'PID %s received %s' % (current_process_id, response[5:])

	def shutdown(self):
		self.s.close()


class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		data = self.request.recv(BUF_SIZE)
		current_process_id = os.getpid()
		response = '%s: %s' % (current_process_id, data)
		print 'Server sending response [%s]' % response
		self.request.send(response)

class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
	pass


def main():
	server = ForkingServer((SERVER_HOST,SERVER_PORT),ForkingServerRequestHandler)
	ip, port = server.server_address
	print server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.setDaemon(False)
	server_thread.start()
	print 'Server loop running PID %s' % os.getpid()
	client1 = ForkingClient(ip, port)
	client1.run()

	client2 = ForkingClient(ip, port)
	client2.run()

	server.shutdown()
	client1.shutdown()
	client2.shutdown()
	server.socket.close()


if __name__ == '__main__':
	main()
