# -*-coding:utf-8-*-

import socket
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from OpenSSL import SSL

'''
需要ssl证书
'''


class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        fpem = 'Server.pem'
        ctx.use_privatekey_file(fpem)
        ctx.use_certificate_file(fpem)
        self.socket = SSL.Connection(ctx, socket.socket(
            self.address_family, self.socket_type))
        self.server_bind()


class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, 'rb', self.rbufsize)
        self.wfile = socket._fileobject(self.request, 'wb', self.wbufsize)


def run_server(HandlerClass=SecureHTTPRequestHandler,
               ServerClass=SecureHTTPServer):
    server_address = ('', 4443)
    server = ServerClass(server_address, HandlerClass)
    running_address = server.socket.getsockname()
    print 'Serving HTTPS Server on %s:%s ...' % (running_address[0],
                                                 running_address[1])
    server.serve_forever()


if __name__ == '__main__':
    run_server()
