#-*-coding:utf-8-*-
import select
import socket
import sys
import signal
import cPickle
import struct
import argparse

SERVER_HOST = '127.0.0.1'

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


class ChatClient(object):
	def __init__(self, name, port, host=SERVER_HOST):
		self.name = name
		self.connected = False
		self.host = host
		self.port = port
		self.prompt = '[' + '@'.join((name, socket.gethostname().split('.')[0])) + ']>'
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((host,self.port))
			self.connected = True
			send(self.sock, 'NAME: '+self.name)
			data = receive(self.sock)
			addr = data.split('CLIENT: ')[1]
			self.prompt = '['+'@'.join((self.name, addr)) +']>'
		except socket.error, e:
			print 'Failed to connect to chat server @ port %d' % self.port
			sys.exit(1)

	def run(self):
		while self.connected:
			try:
				sys.stdout.write(self.prompt)
				sys.stdout.flush()
				readable, writeable, exceptional = select.select([0, self.sock],[],[])
				for sock in readable:
					if sock == 0:
						data = sys.stdin.readline().strip()
						if data:
							send(self.sock, data)
					elif sock == self.sock:
						data = receive(self.sock)
						if not data:
							print 'Client shutting down.'
							self.connected = False
							break
						else:
							sys.stdout.write(data+'\n')
							sys.stdout.flush()
			except KeyboardInterrupt:
				print 'Client interrupted'
				self.sock.close()
				break

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Socket Server Exampl with Select')
	parser.add_argument('--name',action='store', dest='name',required = True)
	parser.add_argument('--port',action='store',dest='port',type=int,required=True)
	args = parser.parse_args()
	client = ChatClient(name=args.name, port=args.port)
	client.run()
