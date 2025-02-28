from enum import Enum

REST_API = "https://api.elfi.xyz"
NONE_RPC = "NONE"

class Network(Enum):
    ARBITRUM = 42161
    BASE = 8453


class OrderType(Enum):
    MARKET = 1
    LIMIT = 2
    STOP = 3

    
class OrderSide(Enum):
    LONG = 1
    SHORT = 2


class PositionSide(Enum):
    INCRASE = 1
    DECRASE = 2 

    
class StopType(Enum):
    NOT_STOP_ORDER = 0
    STOP_LOSS = 1   
    TAKE_PROFIT = 2
    POSITION_STOP_LOSS = 3
    POSITION_TAKE_PROFIT = 4
