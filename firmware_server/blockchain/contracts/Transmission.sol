pragma solidity ^0.4.23;

contract Transmission { 
    string[] dataStorage;

    function _save(string _message) public {
        dataStorage.push(_message);
    }
}
