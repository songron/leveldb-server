#!/usr/bin/env python
#coding=utf8


import os
from leveldb_client import Client


host = '127.0.0.1'
port = 5678
dbpath = 'temp/db'


cmd = 'python leveldb_server.py -p %d -d %s &' % (port dbpath)
os.system(cmd)


client = Client(host, port)

for i in xrange(1000):
    key = str(i)
    val = str(i*1000)
    client.call('Put', {'key': key, 'value': val})

v = client.call('Get', {'key': 34})
print v


r = client.call('RangeIter', {'key_from': '100', 'key_to': '200'})
print len(r)
print r


client.close()
