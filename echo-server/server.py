#-*-coding:utf_8-*-
import socket
import sys
import argparse

host = '127.0.0.1'
data_payload = 2048
backlog = 5

def echo_server(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# s.setblocking(0)
	server_address = (host, port)
	print 'starting'
	s.bind(server_address)
	s.listen(backlog)
	while True:
		print 'waiting to receive'
		try:
			# no blocking will raise a error 
			client, address = s.accept()
			data = client.recv(data_payload)
			if data:
				print data
				client.send(data)
			client.close()
		except:
			pass

if __name__ == '__main__':
	echo_server(8090)