const Migrations = artifacts.require("Migrations");
const Arbitrage = artifacts.require("Arbitrage");
const ERC20 = artifacts.require("TokenA");

module.exports = async function(deployer) {
    await deployer.deploy(Migrations);
    const weth = await ERC20.at("0x7ceb23fd6bc0add59e62ac25578270cff1b9f619")

    // Deploy trading script
    const arbitrage = await deployer.deploy(Arbitrage, weth.address);

    // Configure the trading script
    await weth.approve(arbitrage.address, ("69859498588681775"), { from: "0x3eD58d30250b06dEe2Ff676158b3E2Ae0798959a" })
    await arbitrage.deposit(("69859498588681775"), { from: "0x3eD58d30250b06dEe2Ff676158b3E2Ae0798959a" })
};