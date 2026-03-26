from __future__ import annotations

from django.conf import settings
from web3 import Web3

from counter.services.constants import INCREMENT_TX_GAS_LIMIT
from counter.services.exceptions import RPCNotConnectedException


class ChainHandler:
    def __init__(self) -> None:
        self.w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))

        if not self.w3.is_connected():
            raise RPCNotConnectedException('Cannot connect to RPC')

        self.counter_contract_address = self.w3.to_checksum_address(settings.COUNTER_ADDRESS)
        self.counter_contract = self.w3.eth.contract(address=self.counter_contract_address, abi=settings.COUNTER_ABI)
        self.counter_contract.functions.getValue().build_transaction

    def get_base_fee(self) -> int:
        latest_block = self.w3.eth.get_block('latest')
        return latest_block['baseFeePerGas']

    def get_max_fee_per_gas(self, max_priority_fee: int) -> int:
        return self.get_base_fee() * 2 + max_priority_fee

    def get_value(self) -> int:
        return self.counter_contract.functions.getValue().call()

    def send_increment_transaction(self, public_key: str, private_key: str, tx_params: dict[str, str]) -> str:
        public_key_checksum = self.w3.to_checksum_address(public_key)
        max_priority_fee = self.w3.eth.max_priority_fee

        tx = {
            'from': public_key_checksum,
            'to': tx_params['to'],
            'data': tx_params['data'],
            'nonce': self.w3.eth.get_transaction_count(public_key_checksum),
            'chainId': settings.CHAIN_ID,
            'gas': INCREMENT_TX_GAS_LIMIT,
            'maxPriorityFeePerGas': max_priority_fee,
            'maxFeePerGas': self.get_max_fee_per_gas(max_priority_fee),
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=private_key)

        return self.w3.eth.send_raw_transaction(signed_tx.raw_transaction).hex()
