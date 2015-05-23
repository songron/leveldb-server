#!/usr/bin/env python
#coding=utf8


import os
from leveldb_client import Client


host = '127.0.0.1'
port = 5999
dbpath = 'temp.db'


cmd = 'python leveldb_server.py -p %d -d %s &' % (port, dbpath)
os.system(cmd)
print 'Start Server OK!'


client = Client(host, port)

start = ord('a')
for i in xrange(26):
    key = chr(start+i)
    val = str(i)
    client.call('Put', {'key': key, 'value': val})

print 'Insert OK!'

v = client.call('Get', {'key': 'b'})
print v


r = client.call('RangeIter', {'key_from': 'a', 'key_to': 'f'})
print len(r)
print r


client.close()
print 'Finished!'
