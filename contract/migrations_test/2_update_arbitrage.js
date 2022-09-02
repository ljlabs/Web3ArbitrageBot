const Migrations = artifacts.require("Migrations");
const Arbitrage = artifacts.require("Arbitrage");
const TokenA = artifacts.require("TokenA");
const TokenB = artifacts.require("TokenB");
const TokenC = artifacts.require("TokenC");

module.exports = async function(deployer) {
    await deployer.deploy(Migrations);
    const tokenA = await TokenA.deployed()
    await deployer.deploy(Arbitrage, tokenA.address);
};