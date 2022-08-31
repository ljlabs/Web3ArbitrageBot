# Web3ArbitrageBot
This is an arbitrage bot that was built for the Velas EVM compatible chain.  
>*I want to stress the fact that this software is released as a toy example, it does execute profitable trades, however it does fail in some instances, and should therefor be treated as unsafe.*  
>*Although the tool is unsafe please fork it and make any required improvement.* **Any and all improvemtns are welcome :)**

I used some inspiration from the [uniswap-arbitrage-analysis](https://github.com/ccyanxyz/uniswap-arbitrage-analysis) report provided by uniswap to improve this bot however there is still a lot of improvements that can be made. 
The functioning of thisArbitrage bot is increbibly similar to the paper supplied above, so I would recommend reading it befor making changes to this bot. 

# A brife summary (of how the bot works)
This bot works by searching for all trading pairs on a given exchange, then using a simple breadth first search to find a trading path the begins and ends at some token (VLX in the velas network). This application will then execute a trade along that trading path iff and only if that path results in a profit. and will procket said profit in your wallet. 
> Due to stability issues we limit these trades to a single exchange, but we could expand to multiple exchanges in the future, greatly increasing the sea of profit that this bot can produce.

## How To Run Me:  
1. Please begin by making the required changes to our [config file](https://github.com/ljlabs/Web3ArbitrageBot/blob/main/const/config.py) `const/config.py` you can select a network between:
>- Velas, set `network = "vlx"`
>- Polygon, set `network = "matic"`
>- Binance, set `network = "bnb"`

2. Further you will need to set the wallet private key (of the wallet you want to execute arbitrage trades with)
3. Finaly you will need to set your wallet address (of the wallet you want to execute arbitrage trades with)
4. Set the base_token to use the token you want to trade from and to. Please make sure that you have some balance of this token in your wallet.

>I know that steps 2, and 3 are scary so please read through this applications source code to make sure that you are comfortable providing such sensitive information 


## Things to improve

There are many options to look for if you would like to make some improvements to this software. I will list a few here, but please make some feature requests in the issues  section of this project.
- Increase the number of supported chains, and decentralised exchanges.
- Improve stability to a point where we can re-enable cros exchange arbitrage trades.
- More to come :)


## Things to remember
This software makes no promise of guarenteed profits.  
If you decide to use this trading bot you will be doing it at your own risk, and the creators of this bot cannot be held liable for any loss occured because of this software.  
**THIS IS FOR EDUCATIONAL PURPOSES ONLY**
