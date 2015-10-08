#!/usr/bin/env python
#coding=utf8


import json
import optparse
import threading
import leveldb
import zmq


class Worker(threading.Thread):

    def __init__(self, context, db, back_url):
        threading.Thread.__init__(self)
        self.context = context
        self.db = db
        self.back_url = back_url

    def run(self):
        socket = self.context.socket(zmq.DEALER)
        socket.connect(self.back_url)
        while True:
            try:
                msg = socket.recv_multipart()
            except zmq.ContextTerminated:
                break

            data = None
            if len(msg) == 3:
                ident, method, params = msg
                params = json.loads(params)
                if hasattr(self.db, method):
                    func = getattr(self.db, method)
                    try:
                        data = func(**params)
                    except KeyError:
                        data = None
                    if method == 'RangeIter':
                        data = list(data)
            else:
                ident = msg[0]

            result = [ident, json.dumps(data)]
            socket.send_multipart(result)

        socket.close()


class Server(object):

    def __init__(self, dbpath, front_url, back_url, num_workers):
        self.db = leveldb.LevelDB(dbpath)
        self.front_url = front_url
        self.back_url = back_url
        self.num_workers = num_workers

    def start(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind(self.front_url)
        backend = context.socket(zmq.DEALER)
        backend.bind(self.back_url)

        workers = []
        for i in xrange(self.num_workers):
            worker = Worker(context, self.db, self.back_url)
            worker.start()
            workers.append(worker)

        poller = zmq.Poller()
        poller.register(frontend, zmq.POLLIN)
        poller.register(backend, zmq.POLLIN)

        try:
            while True:
                sockets = dict(poller.poll())
                if frontend in sockets:
                    msg = frontend.recv_multipart()
                    backend.send_multipart(msg)
                if backend in sockets:
                    msg = backend.recv_multipart()
                    frontend.send_multipart(msg)
        except KeyboardInterrupt:
            frontend.close()
            backend.close()
            context.term()
            print 'Bye-Bye!'


def main():
    optparser = optparse.OptionParser()
    optparser.add_option('-p', '--port', type='int', dest='port', default=5599)
    optparser.add_option('-d', '--dbpath', dest='dbpath')
    optparser.add_option('-n', '--num_workers', type='int', dest='num_workers',
                         default=5)
    options, args = optparser.parse_args()
    if not options.dbpath:
        optparser.print_help()
        return

    front_url = 'tcp://*:%d' % options.port
    back_url = 'inproc://backend'
    server = Server(options.dbpath, front_url, back_url, options.num_workers)
    server.start()


if __name__ == '__main__':
    main()
