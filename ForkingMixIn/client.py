import os
import socket
import threading
import SocketServer

ECHO_MSG = 'hello world by client'
BUF_SIZE = 1024
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

if __name__ == '__main__':
	ip = '127.0.0.1'
	port = 8090
	client = ForkingClient(ip, port)
	client.run()