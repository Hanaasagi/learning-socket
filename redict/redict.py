#-*-coding:utf-8-*-

'''
asyncore库是python的一个标准库，它是一个异步socket的包装

[client]	 from_remote_buffer	[redict server] 	to_remote_buffer 	[server]

handle_read
handle_write

'''
import argparse
import asyncore
import socket

BUFSIZE = 4096

class PortForwarder(asyncore.dispatcher):
	def __init__(self, ip, port, remoteip, remoteport, backlog=5):
		asyncore.dispatcher.__init__(self)
		self.remoteip = remoteip
		self.remoteport = remoteport
		self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((ip,port))
		self.listen(backlog)

	def handle_accept(self):
		conn, addr = self.accept()
		print 'Connected to:',addr
		Sender(Receiver(conn),self.remoteip,self.remoteport)

class Receiver(asyncore.dispatcher):
	def __init__(self,conn):
		asyncore.dispatcher.__init__(self, conn)
		# save client request
		self.from_remote_buffer = ''
		# save remote server response
		self.to_remote_buffer = ''
		self.sender = None
	
	def handle_connect(self):
		pass

	# 接收客户端请求
	def handle_read(self):
		read = self.recv(BUFSIZE)
		# print read
		self.from_remote_buffer += read

	def writeable(self):
		return (len(self.to_remote_buffer)>0)

	# 向客户端返回
	def handle_write(self):
		sent = self.send(self.to_remote_buffer)
		self.to_remote_buffer = self.to_remote_buffer[sent:]

	def handle_close(self):
		self.close()
		if self.sender:
			self.sender.close()

class Sender(asyncore.dispatcher):
	def __init__(self, receiver, remoteaddr, remoteport):
		asyncore.dispatcher.__init__(self)
		self.receiver = receiver
		receiver.sender = self
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((remoteaddr,remoteport))

	def handle_connect(self):
		pass

		# 获取响应头
	def handle_read(self):
		read = self.recv(BUFSIZE)
		self.receiver.to_remote_buffer += read

	def writable(self):
		return (len(self.receiver.from_remote_buffer)>0)

	def handle_write(self):
		# 客户端请求转发
		request = self.receiver.from_remote_buffer.replace('Host: 127.0.0.1:8090\r\n','Host: www.baidu.com\r\n')
		# print request
		sent = self.send(request)
		self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]

	def handle_close(self):
		self.close()
		self.receiver.close()

PortForwarder('0.0.0.0',8090,'163.44.167.40',80)
asyncore.loop()