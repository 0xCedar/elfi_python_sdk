from clients.client import ELFiClient
from examples.example_config import PRIVATE_KEY
from clients.utils import to_address, multi_pow10
from clients.keys import OrderSide
from time import sleep

elfiClient = ELFiClient(PRIVATE_KEY)

# ------ deposit ------

# deposit 10USDC
USDC = to_address("0xaf88d065e77c8cC2239327C5EDb3A432268e5831")
depositAmount = multi_pow10(10, elfiClient.token_decimals(USDC))

elfiClient.deposit(USDC, depositAmount)

# withdraw
# elfiClient.withdraw(USDC, depositAmount)

# ------ open & close long crossed position ------

print("open & close long crossed position")

# place long crossed order with 6 USD
longOrderMargin = multi_pow10(6, 18)

# 20x leverage
leverage = multi_pow10(20, 5)

WBTC = to_address(elfiClient.get_symbol('BTCUSD')[4])

# open long crossed position
elfiClient.create_increase_market_order('BTCUSD', WBTC, OrderSide.LONG, longOrderMargin, leverage, True)

sleep(3)

# get long crossed position
longPosition = elfiClient.get_single_position('BTCUSD', WBTC, True)

print(longPosition)

# close long crossed position
elfiClient.create_decrease_market_order('BTCUSD', WBTC, OrderSide.SHORT, longPosition[7], True)

# ------ open & close short crossed position ------

print("open & close short crossed position")

# place short crossed order with 7 USD
shortOrderMargin = multi_pow10(7, 18)

# 10x leverage
leverage = multi_pow10(10, 5)

# open short crossed position
elfiClient.create_increase_market_order('BTCUSD', USDC, OrderSide.SHORT, shortOrderMargin, leverage, True)

sleep(3)

# get short crossed position
shortPosition = elfiClient.get_single_position('BTCUSD', USDC, True)

print(shortPosition)

# close short crossed position
elfiClient.create_decrease_market_order('BTCUSD', USDC, OrderSide.LONG, shortPosition[7], True)

