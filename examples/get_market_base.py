from clients.client import ELFiClient
from clients.keys import Network

PRIVATE_KEY = ''
# ------ set network to Network.BASE, default is Network.ARBITRUM ------
elfiClient = ELFiClient(PRIVATE_KEY, network=Network.BASE)
print(elfiClient.get_all_symbols())   
print(elfiClient.get_tickers())
print(elfiClient.get_symbol('BTCUSD'))  