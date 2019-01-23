
import json
import socket
import sys
import threading
import time

import requests
from web3 import Web3

import eth_rpc_output
import eth_rpc_cli


ACCESS_TIMEOUT = 5
DEFAULT_PORT = 8545
DEFAULT_THREAD_NUMBER = 550

def try_connect_by_socket(ip,port) :
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    result = True
    
    try :
        sock.settimeout(ACCESS_TIMEOUT)
        sock.connect((ip,port))
    except :
        result = False 
    
    sock.close()
    
    return result

def try_connect_by_http(ip,port) :
    #try :
    #    responed = requests.get('https://%s:%d/' % (ip,port),timeout = 5)
    #    
    #    return 2
    #except :
    #    pass
    
    try :
        responed = requests.get('http://%s:%d/' % (ip,port),timeout = ACCESS_TIMEOUT)
        
        return 1
    except :
        pass
    
    return 0

def split_network_session(string) :
    offset = string.find('/')
    
    if -1 == offset :
        return False
    
    return string.split('/')

def ip_to_list(ip_segment) :
    ip_segment = ip_segment.split('.')
    ip_segment[0] = int(ip_segment[0])
    ip_segment[1] = int(ip_segment[1])
    ip_segment[2] = int(ip_segment[2])
    ip_segment[3] = int(ip_segment[3])

    return ip_segment
    
def make_network_range(ip_segment,mask_number) :
    ip_segment = ip_to_list(ip_segment)
    make_range = pow(2,32 - mask_number)
    ip_list = []

    for index in range(make_range) :
        if 0 < ip_segment[3] and ip_segment[3] < 255 :
            ip = '%d.%d.%d.%d' % (ip_segment[0],ip_segment[1],ip_segment[2],ip_segment[3])

            ip_list.append(ip)

        ip_segment[3] += 1

        if ip_segment[3] > 255 :
            ip_segment[2] += 1
            ip_segment[3] = 1

        if ip_segment[2] > 255 :
            ip_segment[1] += 1
            ip_segment[2] = 1

    return ip_list
    
thread_save_lock = threading.Lock()
global_scan_data = []
    
def add_new_record(data) :
    thread_save_lock.acquire()
    
    global_scan_data.append(data)
    
    thread_save_lock.release()
    
def save_data(file_name,data) :
    file = open(file_name,'w')
    
    file.write(json.dumps(data,indent = 2))
    file.close()
    
def background_thread(ip_list) :
    eth_rpc_output.output_function('Thread Running ..','blue')
    
    for ip_index in ip_list :
        state = try_connect_by_http(ip_index,DEFAULT_PORT)
        
        if not state :
            continue
            
        eth_rpc_output.output_function('Port Open : http://%s:%d/' % (ip_index,DEFAULT_PORT))

        eth_connector = Web3(Web3.HTTPProvider('http://%s:%d/' % (ip_index,DEFAULT_PORT)))

        try :
            block_information = eth_connector.eth.getBlock('latest')
            block_height = block_information['number']
            timestamp = block_information['timestamp']

            if not len(block_information) :
                continue

            eth_rpc_output.output_function('Is ETH Node : http://%s:%d/    Block Height : %d TimeStamp : %d' % (ip_index,DEFAULT_PORT,block_height,timestamp),'green')

            if 6120000 > block_height :
                eth_rpc_output.output_function('%s:%d Is Not ETH Node ..' % (ip,port))

                continue
        
            account_list = eth_connector.personal.listAccounts
            result = {}

            eth_rpc_output.output_function('ETH Account Count : %d' % (len(account_list)),'green')

            for account_index in account_list :
                balance = eth_connector.eth.getBalance(account_index) / 10 ** 18
                result[account_index] = balance

                eth_rpc_output.output_function('IP : %s  Address : %s  Balance : %d ETH' % (ip_index,account_index,balance),'red')

            if not account_list :
                continue

            eth_rpc_cli.create_monitor_task(ip_index,DEFAULT_PORT)

            add_new_record({
                'ip' : ip_index ,
                'height' : block_information['number'] ,
                'timestamp' : block_information['timestamp'] ,
                'port' : DEFAULT_PORT ,
                'data' : result ,
            })
        except :
            pass
    
    #eth_rpc_output.output_function('Thread Shutdown ..')

def get_help() :
    eth_rpc_output.output_function('Using : python3 eth_rpc_scan.py network_session')
    eth_rpc_output.output_function('Example : python3 eth_rpc_scan.py 192.168.1.0/24')

    exit()
    
'''

aliyun : 47.74.0.0/11
tencent hk : 119.28.0.0/17
usa : 144.202.0.0/16
canada : 144.217.0.0/16
germany : 144.76.0.0/16
idc : 45.0.0.0/9

'''

if __name__ == '__main__' :
    if 1 == len(sys.argv) or 3 < len(sys.argv) :
        get_help()
        
    network_session = split_network_session(sys.argv[1])

    if not network_session :
        eth_rpc_output.output_function('Network Session Error , Format like : 192.168.1.0/24')

        exit()

    ip_list = make_network_range(network_session[0],int(network_session[1]))
    
    if 3 == len(sys.argv) :
        DEFAULT_PORT = int(sys.argv[2])
        
    ip_list_length = len(ip_list)
    block_length = int(ip_list_length / DEFAULT_THREAD_NUMBER)
    thread_list = []

    eth_rpc_output.output_function('Create IP List Success ..')

    for thread_create_index in range(DEFAULT_THREAD_NUMBER) :
        current_index = block_length * thread_create_index
        create_thread = threading.Thread(target = background_thread,args = (ip_list[ current_index : current_index + block_length ],))

        thread_list.append(create_thread)
        create_thread.start()

    input()
    
    save_data('scan_data_%d.txt' % int(time.time() * 1000),global_scan_data)
