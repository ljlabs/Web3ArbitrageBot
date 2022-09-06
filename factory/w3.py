from web3 import Web3
from const.controlls import network
from const.config import private_key, wallet_address


class W3:
    _instance = None
    velas_private_key = private_key
    velas_network_url = "https://evmexplorer.velas.com/rpc"
    velas_network_id = 106
    matic_private_key = private_key
    matic_network_url = "https://polygon-rpc.com"
    matic_network_id = 137
    bnb_private_key = private_key
    bnb_network_url = "https://bsc-dataseed.binance.org/"
    bnb_network_id = 56

    executor_wallet = wallet_address # this is just to test that the wallet will be used
    velasW3 = None
    maticW3 = None
    bnbW3 = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(W3, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def velas(self):
        if self.velasW3 is None:
            self.velasW3 = Web3(Web3.HTTPProvider(self.velas_network_url))
            self.velasW3.eth.account.from_key(self.velas_private_key)
        return self.velasW3

    def matic(self):
        if self.maticW3 is None:
            self.maticW3 = Web3(Web3.HTTPProvider(self.matic_network_url))
            self.maticW3.eth.account.from_key(self.matic_private_key)
        return self.maticW3

    def bnb(self):
        if self.bnbW3 is None:
            self.bnbW3 = Web3(Web3.HTTPProvider(self.bnb_network_url))
        return self.bnbW3

    def get_private_key(self):
        if network == "vlx":
            return self.velas_private_key
        if network == "matic":
            return self.velas_private_key
        if network == "bnb":
            return ""

    def getWeb3(self):
        if network == "vlx":
            return self.velas()
        if network == "matic":
            return self.matic()
        if network == "bnb":
            return self.bnb()

    def get_chain_id(self):
        if network == "vlx":
            return self.velas_network_id
        if network == "matic":
            return self.matic_network_id
        if network == "bnb":
            return self.bnb_network_id

    def get_tx_args(self) -> dict[str, int | str]:
        nonce = self.getWeb3().eth.get_transaction_count(self.executor_wallet)
        return {
            'chainId': self.get_chain_id(),
            'gas': 3000000,
            'gasPrice': self.getWeb3().toWei('35', 'gwei'),
            'nonce': nonce
        }

