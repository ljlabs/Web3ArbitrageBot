const Migrations = artifacts.require("Migrations");
const Arbitrage = artifacts.require("Arbitrage");
const TokenA = artifacts.require("TokenA");
const TokenB = artifacts.require("TokenB");
const TokenC = artifacts.require("TokenC");

module.exports = async function(deployer) {
    await deployer.deploy(Migrations);
    const tokenA = await deployer.deploy(TokenA, "TOKEN A", "TOKA");
    await deployer.deploy(TokenB, "TOKEN B", "TOKB");
    await deployer.deploy(TokenC, "TOKEN C", "TOKC");
    await deployer.deploy(Arbitrage, tokenA.address);
};