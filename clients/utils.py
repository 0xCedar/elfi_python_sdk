from web3.main import Web3


def multi_pow10(value, exponent):
    return value * pow(10, exponent)


def to_address(addr):
    if Web3.is_address(addr):
        return Web3.to_checksum_address(addr)

    
def encode_bytes32(text):
    return Web3.to_bytes(text = text).ljust(32, b'\0')  

