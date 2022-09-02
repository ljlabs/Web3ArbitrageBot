// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "./Uniswap/IUniswapV2Router02.sol";

interface IArbitrage {
    /**
     * @dev Emitted when a trade is executed
     */
    event trade_copmleted(TradeInstruction[] instructions, uint input, uint output);
    /**
     * @dev Emitted when a deposit occures
     */
    event deposit_copmleted(uint deposited, uint total_deposited);
    /**
     * @dev Emitted when a withdrawl occures
     */
    event withdrawl_copmleted(uint withdrawl, uint total_deposited);
}

struct TradeInstruction {
  address exchange;
  address[] path;
  uint input;
  uint output;
}

contract Arbitrage is Ownable, IArbitrage {
  IERC20 base_token;

  constructor(
    address base_token_address
  ) {
    base_token = IERC20(base_token_address);
  }

  function updateBaseToken(
    address base_token_address
  ) public onlyOwner {
    base_token = IERC20(base_token_address);
  }

  function getBaseToken() public view returns (address){
    return address(base_token);
  }


  function deposit(uint256 amount) public {
    address addr = _msgSender();
    require(amount > 0, "Error insufficeint deposit amount");
    require(
      base_token.transferFrom(addr, address(this), amount),
      "Error insufficient funds to pay fee"
    );
    emit deposit_copmleted(amount, getTradeBalance());
  }

  function getTradeBalance() public view returns (uint256) {
    address addr = address(this);
    return base_token.balanceOf(addr);
  }

  function withdraw(uint256 amount) public onlyOwner {
    address addr = _msgSender();
    require(amount > 0, "Error insufficeint withdrawl amount");
    require(amount <= getTradeBalance(), "Error withdrawl is too large");
    require(base_token.transfer(addr, amount), "Error occured withdrawing tokens");
    emit withdrawl_copmleted(amount, getTradeBalance());
  }

  function withdraw_other_token(address token_address, uint256 amount) public onlyOwner {
    address addr = _msgSender();
    IERC20 token = IERC20(token_address);
    require(amount > 0, "Error insufficeint withdrawl amount");
    require(amount <= token.balanceOf(address(this)), "Error withdrawl is too large");
    token.transfer(addr, amount);
  }

  function get_expected_output(TradeInstruction[] calldata instructions) public onlyOwner view returns (uint[][] memory) {
    uint instruction_count = instructions.length;
    uint[][] memory output = new uint256[][](instruction_count);
    uint out = instructions[0].input;
    for (uint i = 0; i < instructions.length; i++) {
      IUniswapV2Router02 router = IUniswapV2Router02(instructions[i].exchange);
      uint[] memory amountsOut = router.getAmountsOut(out, instructions[i].path);
      out = amountsOut[amountsOut.length - 1];
      output[i] = amountsOut;
    }
    return output;
  }

  function execute_trade(TradeInstruction[] calldata instructions) public onlyOwner {
    uint instruction_count = instructions.length;
    uint[][] memory output = new uint256[][](instruction_count);
    for (uint i = 0; i < instructions.length; i++) {
      TradeInstruction memory instruction = instructions[i];
      IUniswapV2Router02 router = IUniswapV2Router02(instruction.exchange);
      IERC20 token = IERC20(instruction.path[0]);
      require(instruction.input > 0, "Error insufficeint trade amount");
      require(instruction.input <= token.balanceOf(address(this)), "Error trade size is too large");
      require(
        token.approve(instruction.exchange, instruction.input),
        "Error token: approval failed"
      );
      output[i] = router.swapExactTokensForTokens(
        instruction.input,
        instruction.output,
        instruction.path, 
        address(this),
        block.timestamp + 20);
    }
    emit trade_copmleted(
      instructions,
      output[0][0],
      output[output.length - 1][output[output.length - 1].length - 1]
    );
  }
}