from __future__ import annotations

import requests
from django.conf import settings


def get_increment_tx_params(counter_contract_address: str, from_address: str, amount: int) -> dict:
    response = requests.get(
        settings.TX_BUILDER_URL,
        params={'counter_contract_address': counter_contract_address, 'from_address': from_address, 'amount': amount},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
