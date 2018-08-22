
import json
import socket
import sys

import eth_rpc_monitor


DEFAULT_PORT = 8545


def create_monitor_task(ip,port) :
    data = {
        'ip' : ip ,
        'port' : port
    }
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    sock.connect(('127.0.0.1',eth_rpc_monitor.DEFAULT_PORT))
    sock.send(json.dumps(data).encode('utf-8'))
    sock.close()


if __name__ == '__main__' :
    argv_length = len(sys.argv)
    
    if argv_length < 2 :
        print('Using : eth_rpc_cli.py  ip  [ port ]')
        
    if argv_length == 2 :
        ip = sys.argv[1]
        port = DEFAULT_PORT
    elif argv_length == 3 :
        ip = sys.argv[1]
        port = sys.argv[2]
    
    create_monitor_task(ip,port)
