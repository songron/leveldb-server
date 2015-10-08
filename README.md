# leveldb-server
Asynchronous server and client for LevelDB, powered by ZeroMQ.

## Dependencies


### Install LevelDB


Refer to [google/leveldb](https://github.com/google/leveldb)


### Install ZeroMQ

Refer to [ZeroMQ](http://zeromq.org/intro:get-the-software)

### Instanll pyzmq

    pip install pyzmq
    
### Install pyleveldb

    pip install leveldb
    

## Getting Startted

### Starting the server

    python leveldb_server.py -d dbpath -p 5999 -n 5 &
    
### Using the client (example)

	import random
    import sys
    sys.path.insert('path_to/leveldb-server/')
    
    from leveldb_client import Client
    client = Client('127.0.0.1', 5999)
    for key in ['a', 'b', 'c', 'd', 'e']:
        val = str(random.randint(1, 10000))
        client.call('Put', {'key': key, 'value': val})
        
    r1 = client.call('Get', {'key': 'c'})
    print r1 
    
    r2 = client.call('RangeIter', {'key_from':'a', 'key_to':'d'})
    print r2
    
    client.close()
