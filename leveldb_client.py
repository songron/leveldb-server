#!/usr/bin/env python
#coding=utf8


import json
import zmq


class Client(object):

    def __init__(self, host, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect('tcp://%s:%d' % (host, port))

    def close(self):
        self.socket.close()
        self.context.term()

    def call(self, method, params):
        self.socket.send_multipart([method, json.dumps(params)])
        msg = self.socket.recv_multipart()
        data = json.loads(msg[0])
        return data


def test():
    import optparse
    optparser = optparse.OptionParser()
    optparser.add_option('-i', '--host', dest='host', default='localhost')
    optparser.add_option('-p', '--port', type='int', dest='port')
    options, args = optparser.parse_args()
    if not options.port:
        optparser.print_help()
        return

    client = Client(options.host, options.port)
    r = client.call('Get', {'key':'name'})
    print r
    client.close()


if __name__ == '__main__':
    test()
