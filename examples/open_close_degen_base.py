from clients.client import ELFiClient
from clients.utils import to_address, multi_pow10
from clients.keys import OrderSide, Network
from time import sleep

PRIVATE_KEY = ''
elfiClient = ELFiClient(PRIVATE_KEY, network=Network.BASE)

# ------ open & close long crossed position ------
print("open & close long degen position")

# DEGEN_BTCUSD long margin token is WETH and short margin token is USDC
# check with elfiClient.get_symbol('DEGEN_BTCUSD')

# place long degen order with 10 USD
longOrderMargin = multi_pow10(10, 18)

# 1000x leverage
leverage = multi_pow10(1000, 5)

longMarginToken = to_address(elfiClient.get_symbol('DEGEN_BTCUSD')[4])

takeProfitRate = multi_pow10(1, 5)

# open long degen position
elfiClient.create_increase_degen_order('DEGEN_BTCUSD', longMarginToken, OrderSide.LONG, longOrderMargin, leverage, takeProfitRate)

sleep(5)

# get long degen position
longPosition = elfiClient.get_single_position('DEGEN_BTCUSD', longMarginToken, True)

print(longPosition)

# close long degen position
elfiClient.create_decrease_market_order('DEGEN_BTCUSD', longMarginToken, OrderSide.SHORT, longPosition[7], True)


