const args = process.argv;
const wallet = args[2];
const data = args[3];

var Caver = require('caver-js');
var caver = new Caver('http://klaytn.ngrok.io');
var Transmission = require('./blockchain/build/contracts/Transmission.json');
var Transmission = new caver.klay.Contract(Transmission.abi, '0x20c0b6bc23bfcbe9dad09221f90365f740f779c9');
Transmission.methods._save(data).send({from: wallet})
.on('receipt', function(receipt) {
    console.log(receipt.transactionHash);
});

// usage:   node send.js {sender-wallet} {data}
// example: node send.js 0x4543553d76289473c6d38fadfd4f13541bf43c19 test-data
// output: 0xbf33d06c77df85caae8d52676bc54c8e01b8de5f203fa490d8091c4c0a32cedf -> txHash

// example-2: node send.js 0x4543553d76289473c6d38fadfd4f13541bf43c19 'sfghgsfag gfhjs'
// output-2: 0xe1c47ed7dcdc757bb73cee22d118ef0a3f4c126deae8b88b811a71d76f0704ba
