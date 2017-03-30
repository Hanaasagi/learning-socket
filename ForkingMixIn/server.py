import os
import SocketServer

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8090
BUF_SIZE = 1024
ECHO_MSG = 'Hello echo server'


class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = '%s: %s' % (current_process_id, data)
        print 'Server sending response [%s]' % response
        self.request.send(response)


class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass


if __name__ == '__main__':
    server = ForkingServer((SERVER_HOST, SERVER_PORT),
                           ForkingServerRequestHandler)
    print 'Server loop running PID %s' % os.getpid()
    server.serve_forever()
