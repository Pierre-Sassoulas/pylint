from web3 import Web3
from web3._utils.abi import get_abi_output_types

WEB3 = Web3()

address = '0x0'
abi = {'foo': 'boo'}
method_name = 'foo'
arguments = None
contract = WEB3.eth.contract(address=address, abi=abi)
fn_abi = contract._find_matching_fn_abi(
    fn_identifier=method_name,
    args=arguments if arguments else [],
)
output_types = get_abi_output_types(fn_abi)
result = b'dasdad'
decoded_method = WEB3.codec.decode_abi(output_types, result)

if len(decoded_method) == 1:
    a = decoded_method[0]
else:
    a = decoded_method

print(a)
