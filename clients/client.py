from web3.main import Web3

import json
import time
import requests
from clients.keys import ARBITRUM_RPC, DIAMOND, REST_API, OrderSide, StopType, \
    PositionSide, OrderType
from clients.utils import encode_bytes32
import pkg_resources


class ELFiBaseClient:
    
    def __init__(self, private_key, rpc, diamond, rest_api):
        self.rpc = rpc
        self.diamond = diamond
        self.private_key = private_key
        self.rest_api = rest_api
    
    def _init_web3(self):
        self.w3 = Web3(Web3.HTTPProvider(self.rpc))
        self.w3.is_connected(True)
        self.account = self.w3.eth.account.from_key(self.private_key).address
        self.w3.eth.defaultAccount = self.account
    
    def _erc20_contract(self, token):
        with open(pkg_resources.resource_filename('abis', 'ERC20.json'), 'r') as f:
            return self.w3.eth.contract(address=token, abi=json.loads(f.read()))
        
    def _facet_contract(self, facet):
        with open(pkg_resources.resource_filename('abis', facet + '.json'), 'r') as f:
            return self.w3.eth.contract(address=self.diamond, abi=json.loads(f.read()))

    def _sign_and_send_transaction(self, tx):
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.status

    def _token_approve(self, token, amount):
        tx = self._erc20_contract(token).functions.approve(self.diamond, amount).build_transaction({
                'from': self.account,
                'nonce': self.w3.eth.get_transaction_count(self.account)
            })
        return self._sign_and_send_transaction(tx)
    
    def _get_rest(self, uri, params=None): 
        url = f'{self.rest_api}/{uri}' 
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        } 
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return response.json()  
            else: 
                print(f"response: request failed with：{response.status_code}")
        except requests.RequestException as e: 
            print(f"request error: {e}")  
        return None 
    
    def token_decimals(self, token):
        return self._erc20_contract(token).functions.decimals().call()

    
class ELFiClient(ELFiBaseClient):
    
    def __init__(self, private_key, rpc=ARBITRUM_RPC, diamond=DIAMOND, rest_api=REST_API):
        super().__init__(private_key, rpc, diamond, rest_api)
        self._init_web3()
    
    def create_increase_market_order(self, symbol, marginToken, orderSide: OrderSide, orderMargin, leverage, isCrossMargin=True):
        params = self._get_order_params()
        params.update({
            "symbol": encode_bytes32(symbol),
            "marginToken": marginToken,
            "isCrossMargin": isCrossMargin,
            "orderSide": orderSide.value,
            "orderMargin": orderMargin,
            "leverage": leverage
            })
        if (isCrossMargin is False):
            self._token_approve(marginToken, orderMargin)
        return self.create_order_request(params)
    
    def create_increase_limit_order(self, symbol, marginToken, orderSide: OrderSide, orderMargin, leverage, triggerPrice, isCrossMargin=True):
        params = self._get_order_params()
        params.update({
            "symbol": encode_bytes32(symbol),
            "marginToken": marginToken,
            "isCrossMargin": isCrossMargin,
            "orderSide": orderSide.value,
            "orderMargin": orderMargin,
            "leverage": leverage,
            "orderType": OrderType.LIMIT.value,
            "trigger_price": triggerPrice
            })
        if (isCrossMargin is False):
            self._token_approve(marginToken, orderMargin)
        return self.create_order_request(params)
    
    def create_decrease_market_order(self, symbol, marginToken, orderSide: OrderSide, qty, isCrossMargin=True):
        params = self._get_order_params()
        params.update({
            "symbol": encode_bytes32(symbol),
            "marginToken": marginToken,
            "isCrossMargin": isCrossMargin,
            "posSide": PositionSide.DECRASE.value,
            "orderSide": orderSide.value,
            "qty": qty
            })
        
        return self.create_order_request(params)
    
    def create_stop_order(self, symbol, marginToken, orderSide: OrderSide, qty, triggerPrice, stopType: StopType, isCrossMargin=True):
        params = self._get_order_params()
        params.update({
            "symbol": encode_bytes32(symbol),
            "marginToken": marginToken,
            "isCrossMargin": isCrossMargin,
            "qty": qty,
            "posSide": PositionSide.DECRASE.value,
            "orderSide": orderSide.value,
            "orderType": OrderType.STOP.value,
            "stopType": stopType.value,
            "trigger_price": triggerPrice            
            })
        return self.create_order_request(params)
    
    def create_order_request(self, params):
        params = tuple(params.values())
        tx = self._facet_contract("OrderFacet").functions.createOrderRequest(params).build_transaction({
                'from': self.account,
                'nonce': self.w3.eth.get_transaction_count(self.account)
            })
        return self._sign_and_send_transaction(tx)
    
    def cancel_order(self, orderId):
        tx = self._facet_contract("OrderFacet").functions.cancelOrder(orderId).build_transaction({
                'from': self.account,
                'nonce': self.w3.eth.get_transaction_count(self.account)
            })
        return self._sign_and_send_transaction(tx)
    
    def deposit(self, token, amount):
        self._token_approve(token, amount)
        tx = self._facet_contract("AccountFacet").functions.deposit(token, amount).build_transaction({
                'from': self.account,
                'nonce': self.w3.eth.get_transaction_count(self.account)
            })
        return self._sign_and_send_transaction(tx)
    
    def withdraw(self, token, amount, isWithdrawMax=False):
        tx = self._facet_contract("AccountFacet").functions.createWithdrawRequest(token, amount, 0, isWithdrawMax).build_transaction({
                'from': self.account,
                'nonce': self.w3.eth.get_transaction_count(self.account)
            })
        return self._sign_and_send_transaction(tx)
    
    def get_account_info(self):
        return self._facet_contract("AccountFacet").functions.getAccountInfo(self.account).call()
    
    def get_all_orders(self):
        return self._facet_contract("OrderFacet").functions.getAccountOrders(self.account).call()
    
    def get_all_positions(self):
        return self._facet_contract("PositionFacet").functions.getAllPositions(self.account).call()
    
    def get_single_position(self, symbol, marginToken, isCrossMargin):
        '''
            :returns: position information
            .. code-block:: solidiy
             struct Position.Props {
                bytes32 key;
                bytes32 symbol;
                bool isLong;
                bool isCrossMargin;
                address account;
                address marginToken;
                address indexToken;
                uint256 qty;
                uint256 entryPrice;
                uint256 entryMarginTokenPrice;
                uint256 leverage;
                uint256 initialMargin;
                uint256 initialMarginInUsd;
                uint256 initialMarginInUsdFromBalance;
                uint256 holdPoolAmount;
                PositionFee positionFee;
                int256 realizedPnl;
                uint256 lastUpdateTime;
            }
        '''
        return self._facet_contract("PositionFacet").functions.getSinglePosition(self.account, encode_bytes32(symbol), marginToken, isCrossMargin).call()

    def get_all_symbols(self):
        return self._facet_contract("MarketFacet").functions.getAllSymbols().call()
    
    def get_symbol(self, symbol):
        '''
            :returns: symbol information
            .. code-block:: solidiy
            struct SymbolInfo {
                bytes32 code;
                Symbol.Status status;
                address stakeToken;
                address indexToken;
                address baseToken;
                SymbolConfig config;
            }
        '''
        return self._facet_contract("MarketFacet").functions.getSymbol(encode_bytes32(symbol)).call()

    def get_tickers(self):
        return self._get_rest("prices/tickers")
    
    def get_candles(self, symbol, period, limit=500):
        return self.getKlines(symbol, period, limit)
    
    def get_klines(self, symbol, period, limit=500):
        return self._get_rest("prices/candles", {"symbol": encode_bytes32(symbol), "period": period, "limit":limit})
    
    def _get_order_params(self):
        params = {}
        params['symbol'] = encode_bytes32('BTCUSD')
        params['isCrossMargin'] = True
        params['isNativeToken'] = False
        params['orderSide'] = OrderSide.LONG.value
        params['posSide'] = PositionSide.INCRASE.value
        params['orderType'] = OrderType.MARKET.value
        params['stopType'] = StopType.NOT_STOP_ORDER.value
        params['marginToken'] = ''
        params['qty'] = 0
        params['orderMargin'] = 0
        params['leverage'] = 0
        params['triggerPrice'] = 0
        params['acceptablePrice'] = 0
        params['executionFee'] = 0
        params['placeTime'] = int(round(time.time() * 1000))
        return params
