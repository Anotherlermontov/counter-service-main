from __future__ import annotations

from typing import Any

from django.conf import settings
from web3 import Web3

from counter.services.exceptions import RPCNotConnectedException


class ChainHandler:
    def __init__(self) -> None:
        self.w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))

        if not self.w3.is_connected():
            raise RPCNotConnectedException('Cannot connect to RPC')

        self.counter_contract_address = self.w3.to_checksum_address(settings.COUNTER_ADDRESS)
        self.counter_contract = self.w3.eth.contract(
            address=self.counter_contract_address, abi=settings.COUNTER_ABI
        )

    def get_value(self) -> int:
        return self.counter_contract.functions.value().call()

    def send_increment_transaction(self, private_key: str, tx_params: dict[str, Any]) -> str:
        signed_tx = self.w3.eth.account.sign_transaction(tx_params, private_key=private_key)

        return self.w3.eth.send_raw_transaction(signed_tx.raw_transaction).hex()
