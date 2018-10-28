var Migrations = artifacts.require("./Migrations.sol");
var Transmission = artifacts.require("./Transmission.sol");

module.exports = function(deployer) {
  deployer.deploy(Migrations);
  deployer.deploy(Transmission);
};
