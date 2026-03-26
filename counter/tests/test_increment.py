from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

from django.test import Client


@patch('counter.views.get_increment_tx_params')
@patch('counter.views.ChainHandler')
@patch('counter.views.Wallet.objects.first')
def test__increment_success(mock_wallet_first, mock_chain_handler_cls, mock_get_increment_tx_params):
    mock_wallet_first.return_value = SimpleNamespace(
        address='0x6619142c47E4cC98d54851A3835f32405bC48443', private_key='0x123'
    )
    mock_get_increment_tx_params.return_value = {'to': '0x9b9c4929b86e63611439651e4bc0361e4e5d3602', 'data': '0xabcdef'}
    mock_chain_handler = mock_chain_handler_cls.return_value
    mock_chain_handler.send_increment_transaction.return_value = '0x' + '12' * 32

    client = Client()
    response = client.post('/increment', data='{"amount": 200}', content_type='application/json')

    assert response.status_code == 200
    assert response.json() == {'tx_hash': '0x1212121212121212121212121212121212121212121212121212121212121212'}
    mock_get_increment_tx_params.assert_called_once_with(
        counter_contract_address='0x9b9c4929b86e63611439651e4bc0361e4e5d3602',
        from_address='0x6619142c47E4cC98d54851A3835f32405bC48443',
        amount=200,
    )
    mock_chain_handler.send_increment_transaction.assert_called_once_with(
        private_key='0x123', tx_params={'to': '0x9b9c4929b86e63611439651e4bc0361e4e5d3602', 'data': '0xabcdef'}
    )


def test__increment_returns_400_when_amount_is_missing():
    client = Client()
    response = client.post('/increment', data='{}', content_type='application/json')

    assert response.status_code == 400
    assert response.json() == {'errors': {'amount': ['This field is required.']}}
