from clients.client import ELFiClient
from examples.example_config import PRIVATE_KEY

elfiClient = ELFiClient(PRIVATE_KEY)
print(elfiClient.get_all_symbols())   
print(elfiClient.get_tickers())
print(elfiClient.get_symbol('BTCUSD'))  