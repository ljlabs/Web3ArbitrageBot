const Arbitrage = artifacts.require("Arbitrage");
const TokenA = artifacts.require("TokenA");
const TokenB = artifacts.require("TokenB");
const TokenC = artifacts.require("TokenC");


/* test on remix
THIS CAN WORK ACROSS MULTIPLE EXCHANGES SIMULTANEOUSLY
> get_expected_output(): THIS CAN WORK ACROSS MULTIPLE EXCHANGES SIMULTANEOUSLY
[["0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3",["0x11024FeA6039fd29E5251c99261B73A00447E580","0x7306F86932f0232A163e5Db8A8531E371a0864DE","0xa8616Df032435768a2C43f4F36f07c37901Ff704","0x11024FeA6039fd29E5251c99261B73A00447E580"],99939822916501678447,0],
["0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3",["0x11024FeA6039fd29E5251c99261B73A00447E580","0x7306F86932f0232A163e5Db8A8531E371a0864DE","0xa8616Df032435768a2C43f4F36f07c37901Ff704","0x11024FeA6039fd29E5251c99261B73A00447E580"],99939822916501678447,0]]
{ EXAMPLE RESPONSE
	"0": "uint256[][]: 99939822916501678447,99728003730496991146,99516658519648931181,99305786118276609871,99305786118276609871,99095373450101377651,98885431345620136465,98675958648656536387"
}

> execute_trade(): THIS CAN WORK ACROSS MULTIPLE EXCHANGES SIMULTANEOUSLY
[["0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3",["0x11024FeA6039fd29E5251c99261B73A00447E580","0x7306F86932f0232A163e5Db8A8531E371a0864DE","0xa8616Df032435768a2C43f4F36f07c37901Ff704","0x11024FeA6039fd29E5251c99261B73A00447E580"],99939822916501678447,99305786118276609871],
["0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3",["0x11024FeA6039fd29E5251c99261B73A00447E580","0x7306F86932f0232A163e5Db8A8531E371a0864DE","0xa8616Df032435768a2C43f4F36f07c37901Ff704","0x11024FeA6039fd29E5251c99261B73A00447E580"],99305786118276609871,9830009737613530843]]
*/


const e18 = "".padStart(18, '0');

contract("config tests", accounts => {
    it("test updateBaseToken", async() => {
        const arbitrage = await Arbitrage.deployed()
        const tokenA = await TokenA.deployed()
        const tokenB = await TokenB.deployed()
        assert.equal(
            await arbitrage.getBaseToken(),
            tokenA.address,
            "Incorrect Base Token step 1"
        );
        await arbitrage.updateBaseToken(tokenB.address, { from: accounts[0] })
        assert.equal(
            await arbitrage.getBaseToken(),
            tokenB.address,
            "Incorrect Base Token step 2"
        );
        await arbitrage.updateBaseToken(tokenA.address, { from: accounts[0] })
        assert.equal(
            await arbitrage.getBaseToken(),
            tokenA.address,
            "Incorrect Base Token step 3"
        );
    });

    it("test deposit and withdraw", async() => {
        const arbitrage = await Arbitrage.deployed()
        const tokenA = await TokenA.deployed()
        let balance = await tokenA.balanceOf(arbitrage.address)
        assert.equal(
            balance.valueOf(),
            "0",
            "More tokens than 0 on arbitrage contract"
        );
        await tokenA.approve(arbitrage.address, ("100" + e18), { from: accounts[0] })
        await arbitrage.deposit(("100" + e18), { from: accounts[0] })
        balance = await tokenA.balanceOf(arbitrage.address)
        assert.equal(
            balance.valueOf(),
            ("100" + e18),
            "Wrong amount of tokens on arbitrage contract"
        );
        await arbitrage.withdraw(("100" + e18), { from: accounts[0] })
        balance = await tokenA.balanceOf(arbitrage.address)
        assert.equal(
            balance.valueOf(),
            "0",
            "More tokens than 0 on arbitrage contract after withdrawl"
        );
    });

    it("test withdraw_other_token", async() => {
        const arbitrage = await Arbitrage.deployed()
        const tokenB = await TokenB.deployed()
        let balance = await tokenB.balanceOf(arbitrage.address)
        assert.equal(
            balance.valueOf(),
            "0",
            "More tokens than 0 on arbitrage contract"
        );
        await tokenB.transfer(arbitrage.address, ("100" + e18), { from: accounts[0] })
        balance = await tokenB.balanceOf(arbitrage.address)
        assert.equal(
            balance.valueOf(),
            ("100" + e18),
            "Wrong amount of tokens on arbitrage contract"
        );
        await arbitrage.withdraw_other_token(tokenB.address, ("100" + e18), { from: accounts[0] })
        balance = await tokenB.balanceOf(arbitrage.address)
        assert.equal(
            balance.valueOf(),
            "0",
            "More tokens than 0 on arbitrage contract after withdrawl"
        );
    });
});