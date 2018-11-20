const info = require('./../info.json');
const wallet = info['device']['wallet'];

const args = process.argv;
const command = args[2];

var Caver = require('caver-js');
var caver = new Caver('http://ubuntu.hanukoon.com:8551/');
caver.klay.unlockAccount(wallet, '_labc', 30000);
var Biss = require('./blockchain/build/contracts/Biss.json');
var Biss = new caver.klay.Contract(Biss.abi, '0x17231a90f559f87ff1490c2eb8cec0c884d79a5d');

if (command == 'data'){
    // node send.js data {data}
    try {
        const data = args[3];
        Biss.methods.saveData(data).send({from: wallet})
        .on('receipt', function(receipt) {
            console.log(JSON.stringify({'result': receipt.transactionHash}));
        });
    }
    catch (e) {
        console.log(JSON.stringify({'result': e.toString()}));
    } 
}
else if (command == 'hash') {
    // node send.js hash {file_id} {hash}
    try {
        const file_id = Number(args[3]);
        const hash = args[4];
        Biss.methods.verifyHash(file_id, hash).call().then(function(same){
            if (same == true) {
                console.log(JSON.stringify({'result': true}));
            }
            else {
                console.log(JSON.stringify({'result': false}));
            }
        });
    } 
    catch (e) {
        console.log(JSON.stringify({'result': e.toString()}));
    } 
}
else if (command == 'sendKey') {
    // node send.js sendKey {file_id} {key}
    try {
        const file_id = Number(args[3]);
        const key = args[4];
        Biss.methods.saveKey(file_id, key).send({from: wallet})
        .on('receipt', function(receipt) {
            console.log(JSON.stringify({'result': receipt.transactionHash}));
        });
    }
    catch (e) {
        console.log(JSON.stringify({'result': e.toString()}));
    }
}
else if (command == 'sendHash') { // tmp
    // node send.js sendKey {file_id} {hash}
    try {
        const file_id = Number(args[3]);
        const hash = args[4];
        Biss.methods.saveHash(file_id, hash).send({from: wallet})
        .on('receipt', function(receipt) {
            console.log(JSON.stringify({'result': receipt.transactionHash}));
        });
    }
    catch (e) {
        console.log(JSON.stringify({'result': e.toString()}));
    } 
}
else {
    console.log(JSON.stringify({'result': 'Error: not a valid command'}));
}
