# -*-coding:utf-8-*-

import json
from multiprocessing.connection import Client


class RPCProxy(object):

    def __init__(self, connection):
        self._connection = connection

    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(json.dumps((name, args, kwargs)))
            result = json.loads(self._connection.recv())
            return result
        return do_rpc


if __name__ == '__main__':
    c = Client(('localhost', 17000), authkey=b'hello')
    proxy = RPCProxy(c)
    print proxy.add(2, 3)
