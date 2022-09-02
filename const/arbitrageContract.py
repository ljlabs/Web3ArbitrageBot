arbitrage_contract_abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "deposit",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "base_token_address",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "deposited",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "total_deposited",
				"type": "uint256"
			}
		],
		"name": "deposit_copmleted",
		"type": "event"
	},
	{
		"inputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "exchange",
						"type": "address"
					},
					{
						"internalType": "address[]",
						"name": "path",
						"type": "address[]"
					},
					{
						"internalType": "uint256",
						"name": "input",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "output",
						"type": "uint256"
					}
				],
				"internalType": "struct TradeInstruction[]",
				"name": "instructions",
				"type": "tuple[]"
			}
		],
		"name": "execute_trade",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "renounceOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "exchange",
						"type": "address"
					},
					{
						"internalType": "address[]",
						"name": "path",
						"type": "address[]"
					},
					{
						"internalType": "uint256",
						"name": "input",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "output",
						"type": "uint256"
					}
				],
				"indexed": False,
				"internalType": "struct TradeInstruction[]",
				"name": "instructions",
				"type": "tuple[]"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "input",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "output",
				"type": "uint256"
			}
		],
		"name": "trade_copmleted",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "base_token_address",
				"type": "address"
			}
		],
		"name": "updateBaseToken",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "token_address",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "withdraw_other_token",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "withdrawl",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "total_deposited",
				"type": "uint256"
			}
		],
		"name": "withdrawl_copmleted",
		"type": "event"
	},
	{
		"inputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "exchange",
						"type": "address"
					},
					{
						"internalType": "address[]",
						"name": "path",
						"type": "address[]"
					},
					{
						"internalType": "uint256",
						"name": "input",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "output",
						"type": "uint256"
					}
				],
				"internalType": "struct TradeInstruction[]",
				"name": "instructions",
				"type": "tuple[]"
			}
		],
		"name": "get_expected_output",
		"outputs": [
			{
				"internalType": "uint256[][]",
				"name": "",
				"type": "uint256[][]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getBaseToken",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTradeBalance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]