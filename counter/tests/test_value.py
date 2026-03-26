from __future__ import annotations

from unittest.mock import patch

from django.test import Client


@patch('counter.views.ChainHandler')
def test__get_value_returns_counter_value(mock_chain_handler):
    mock_chain_handler.return_value.get_value.return_value = 42

    client = Client()
    response = client.get('/value')

    assert response.status_code == 200
    assert response.json() == {'value': 42}
    mock_chain_handler.assert_called_once()
    mock_chain_handler.return_value.get_value.assert_called_once()
