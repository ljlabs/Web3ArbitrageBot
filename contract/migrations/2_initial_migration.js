const Migrations = artifacts.require("Migrations");
const Arbitrage = artifacts.require("Arbitrage");
const TokenA = artifacts.require("TokenA");
const TokenB = artifacts.require("TokenB");
const TokenC = artifacts.require("TokenC");

module.exports = async function(deployer) {
    await deployer.deploy(Arbitrage, "0xc579D1f3CF86749E05CD06f7ADe17856c2CE3126");
};