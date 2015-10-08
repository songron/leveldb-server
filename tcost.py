#!/usr/bin/env python
#coding=utf8


import time
from leveldb_client import Client

host = '162.105.146.246'
host = '127.0.0.1'
port = 8889

server_url = 'ipc://ipcipc'
client = Client(server_url)
print 'Connected OK!'


t_start = time.time()
for i in xrange(1000):
    key = str(1990786715 + i)
    r = client.call('Get', {'key': key})


print 'Cost: %s' % (time.time() - t_start)

client.close()
