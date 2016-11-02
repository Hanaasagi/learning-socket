#-*-coding:utf-8-*-
import select
import socket
import sys
import signal
import cPickle
import struct
import argparse

SERVER_HOST = '0.0.0.0'
CHAT_SERVER_NAME = 'server'

def send(channel, *args):
	buffer = cPickle.dumps(args)
	value = socket.htonl(len(buffer))
	size = struct.pack('L', value)
	channel.send(size)
	channel.send(buffer)

def receive(channel):
	size = struct.calcsize('L')
	size = channel.recv(size)
	try:
		size = socket.ntohl(struct.unpack('L', size)[0])
	except struct.error, e:
		return ''
	buf = ''
	while len(buf)<size:
		buf = channel.recv(size-len(buf))
	return cPickle.loads(buf)[0]

class ChatServer(object):
	def __init__(self, port, backlog=5):
		self.clients = 0
		self.clientmap = {}
		# 存储要写入的socket
		self.outputs = []
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET,	 socket.SO_REUSEADDR,1)
		self.server.bind((SERVER_HOST,port))
		print 'Server listening to port:%s' % port
		self.server.listen(backlog)
		signal.signal(signal.SIGINT, self.sighandler)

	def sighandler(self, signum, frame):
		print 'Shutting down server'
		for output in self.outputs:
			output.close()
		self.server.close()

	def get_client_name(self, client):
		info = self.clientmap[client]
		host , name = info[0][0], info[1]
		return '@'.join((name, host))

	def run(self):
		# 存储 select要监视的socket
		inputs = [self.server]
		self.outputs = []
		running = True
		while running:
			try:
				# select.select（rlist, wlist, xlist[, timeout]） 传递三个参数，一个为输入而观察的文件对象列表，一个为输出而观察的文件对象列表和一个观察错误异常的文件列表。第四个是一个可选参数，表示超时秒数。其返回3个tuple，每个tuple都是一个准备好的对象列表，它和前边的参数是一样的顺序
				readable, writeable, exceptional = select.select(inputs, self.outputs, [])
			except select.error ,e:
				break
			for sock in readable:
				if sock == self.server:
					client, address = self.server.accept()
					print 'Chat server:got connection %d from %s' % (client.fileno(), address)
					cname = receive(client).split('NAME: ')[1]
					self.clients += 1
					send(client, 'CLIENT: '+ str(address[0]))
					inputs.append(client)
					self.clientmap[client] = (address, cname)
					msg = '\n(Connected: New client (%d) from %s)' % (self.clients, self.get_client_name(client))
					# 在连上的客户端中发送 新客户端上线通知
					for output in self.outputs:
						send(output, msg)
					# 添加新的客户端
					self.outputs.append(client)
				# 处理serve人中的输入
				#elif sock == sys.stdin:
				#	junk = sys.stdin.readline()
				#	running = False
				else:
					try:
						data = receive(sock)
						if data:
							msg = '\n#[' + self.get_client_name(sock) + ']>>' + data
							for output in self.outputs:
								if output != sock:
									send(output, msg)
						else:
							# 处理客户端关闭
							print 'Connection : %d hung up ' % sock.fileno()
							self.clients -= 1
							sock.close()
							inputs.remove(sock)
							self.outputs.remove(sock)
							msg = '\n(Now hung up : Client from %s)' % self.get_client_name(sock)
							for output in self.outputs:
								send(output, msg)
					except socket.error, e:
						inputs.remove(sock)
						self.outputs.remove(sock)
			#self.server.close()

if __name__ == '__main__':
	server = ChatServer(8090)
	server.run()
