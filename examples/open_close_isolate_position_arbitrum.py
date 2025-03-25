from clients.client import ELFiClient
from clients.utils import to_address, multi_pow10
from clients.keys import OrderSide
from time import sleep

PRIVATE_KEY = ''

elfiClient = ELFiClient(PRIVATE_KEY)

# ------ open & close long isolated position ------

print("open & close long isolated position")

# token address: https://docs.elfi.xyz/doc-api/tokens
longMarginToken = to_address(elfiClient.get_symbol('SOLUSD')[4])

# place long isolated order with 1 longMarginToken(WETH)
longOrderMargin = multi_pow10(1, elfiClient.token_decimals(longMarginToken))

# 5x leverage
leverage = multi_pow10(5, 5)


# open long isolated position
elfiClient.create_increase_market_order('SOLUSD', longMarginToken, OrderSide.LONG, longOrderMargin, leverage, False)

sleep(5)

# get long isolated position
longPosition = elfiClient.get_single_position('SOLUSD', longMarginToken, True)

print(longPosition)

# close long isolated position
elfiClient.create_decrease_market_order('SOLUSD', longMarginToken, OrderSide.SHORT, longPosition[7], False)


# ------ open & close short isolated position ------

print("open & close short isolated position")

USDC = to_address("0xaf88d065e77c8cC2239327C5EDb3A432268e5831")

# place short isolated order with 100 USDC
shortOrderMargin = multi_pow10(100, elfiClient.token_decimals(USDC))

# 8x leverage
leverage = multi_pow10(8, 5)

# open short isolated position
elfiClient.create_increase_market_order('SOLUSD', USDC, OrderSide.SHORT, shortOrderMargin, leverage, False)

sleep(5)

# get short isolated position
shortPosition = elfiClient.get_single_position('SOLUSD', USDC, False)

print(shortPosition)

# close short isolated position
elfiClient.create_decrease_market_order('SOLUSD', USDC, OrderSide.LONG, shortPosition[7], False)
    
