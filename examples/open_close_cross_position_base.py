from clients.client import ELFiClient
from clients.utils import to_address, multi_pow10
from clients.keys import OrderSide, Network
from time import sleep

PRIVATE_KEY = ''
# ------ set network to Network.BASE, default is Network.ARBITRUM ------
elfiClient = ELFiClient(PRIVATE_KEY, network=Network.BASE)

# ------ deposit ------

# deposit 100USDC
# token address: https://docs.elfi.xyz/doc-api/tokens
USDC = to_address("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")
# depositAmount = multi_pow10(100, elfiClient.token_decimals(USDC))
# elfiClient.deposit(USDC, depositAmount)

# withdraw
# elfiClient.withdraw(USDC, depositAmount)

# ------ open & close long crossed position ------
print("open & close long crossed position")

# BTCUSD long margin token is WETH and short margin token is USDC
# check with elfiClient.get_symbol('BTCUSD')

# place long crossed order with 50 USD
longOrderMargin = multi_pow10(50, 18)

# 10x leverage
leverage = multi_pow10(10, 5)

longMarginToken = to_address(elfiClient.get_symbol('BTCUSD')[4])

# open long crossed position
elfiClient.create_increase_market_order('BTCUSD', longMarginToken, OrderSide.LONG, longOrderMargin, leverage, True)

sleep(10)

# get long crossed position
longPosition = elfiClient.get_single_position('BTCUSD', longMarginToken, True)

print(longPosition)

# close long crossed position
elfiClient.create_decrease_market_order('BTCUSD', longMarginToken, OrderSide.SHORT, longPosition[7], True)

# ------ open & close short crossed position ------

print("open & close short crossed position")

# place short crossed order with 50 USD
shortOrderMargin = multi_pow10(50, 18)

# 10x leverage
leverage = multi_pow10(10, 5)

# open short crossed position
elfiClient.create_increase_market_order('BTCUSD', USDC, OrderSide.SHORT, shortOrderMargin, leverage, True)

sleep(10)

# get short crossed position
shortPosition = elfiClient.get_single_position('BTCUSD', USDC, True)

print(shortPosition)

# change to 20x leverage
leverage = multi_pow10(20, 5)

elfiClient.change_cross_leverage('BTCUSD', USDC, False, leverage)

sleep(10)

# get short crossed position
shortPosition = elfiClient.get_single_position('BTCUSD', USDC, True)

print(shortPosition)

# close short crossed position
elfiClient.create_decrease_market_order('BTCUSD', USDC, OrderSide.LONG, shortPosition[7], True)

