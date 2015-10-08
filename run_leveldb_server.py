#!/usr/bin/env python
#coding=utf8


from leveldb_server import Server


dbpath = '/home/rxs/data/weibo_user_profiles/profile.db/'
host = '162.105.146.246'
port = 8889
front_url = 'tcp://*:%d' % port
front_url = 'ipc://ipcipc'
back_url = 'inproc://backend'
num_workers = 1

server = Server(dbpath, front_url, back_url, 5)
server.start()
