#!/usr/bin/env python
#coding=utf8


import json
import zmq


class Client(object):

    def __init__(self, server_url):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.connect(server_url)

    def close(self):
        self.socket.close()
        self.context.term()

    def call(self, method, params):
        self.socket.send_multipart([method, json.dumps(params)])
        msg = self.socket.recv_multipart()
        data = json.loads(msg[0])
        return data
