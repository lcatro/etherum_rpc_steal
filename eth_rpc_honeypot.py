
import json

import requests
import tornado.ioloop
import tornado.web

import eth_rpc_output
#import sql_module

TARGET_HOST = 'http://47.88.236.91:8545/'


def redirect_eth_request(request_data) :
    responed = requests.post(TARGET_HOST,headers = {
        'Content-Type' : 'application/json' ,
    },data = request_data)
    
    if 200 == responed.status_code :
        return json.loads(responed.text)
    
    return False

class root_handler(tornado.web.RequestHandler) :
    
    def get(self) :
        self.write('ETH RPC ..')
        
    def post(self) :
        try :
            data = json.loads(self.request.body)
        except :
            self.write('Post Body is not JSON')
            
            return
        
        try :
            method = data['method']
            params = data['params']
            json_id = data['id']
        except :
            self.write('JSON Error')
            
            return
        
        remote_ip = self.request.remote_ip
        
        eth_rpc_output.output_function('Remote IP : %s' % (remote_ip))
        
        result = redirect_eth_request(self.request.body)
        
        if not result :    
            result = {
                'jsonrpc' : '2.0' ,
                'id' : json_id ,
                'result' : '' ,
            }
        
        if 'eth_sendTransaction' == method :
            for params_index in params :
                local_address = params_index['from']
                target_address = params_index['to']
                transfer_value = params_index['value'] / 10 ** 18
                
                eth_rpc_output.output_function('Try Transation %s -> %s   Balance : %f ETH' % (local_address,target_address,transfer_value),'red')
        elif 'personal_unlockAccount' == method :
            unlock_account = params[0]
            password = params[1]
            
            eth_rpc_output.output_function('Try UnLock Account : %s   Password : %s' % (unlock_account,password),'red')
        elif 'personal_importRawKey' == method :
            import_account = params[0]
            password = params[1]
            
            eth_rpc_output.output_function('Try Import Account : %s   Password : %s' % (unlock_account,password),'red')
        elif 'eth_getBalance' == method :
            account = params[0]
            
            eth_rpc_output.output_function('Try To GetBalance Account : %s  Modify Account Balance to 500.0 ETH' % (account),'red')
            
            result['result'] = 500 * 10 ** 18
        else :
            eth_rpc_output.output_function('Call RPC Method : %s   Params : %s' % (method,params),'green')
        
        self.write(json.dumps(result))

if __name__ == '__main__' :
    app = tornado.web.Application([
        (r'/' , root_handler),
    ])
    
    print 'eth_rpc_honeypot.py Start'
    
    app.listen(8545)
    tornado.ioloop.IOLoop.current().start()


