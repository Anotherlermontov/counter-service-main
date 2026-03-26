from __future__ import annotations

import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.request import Request

from counter.forms import IncrementForm
from counter.models import Wallet
from counter.services.chain_handler import ChainHandler
from counter.services.exceptions import RPCNotConnectedException
from counter.services.tx_builder_client import get_increment_tx_params


@require_GET
def get_value(request: Request) -> JsonResponse:
    try:
        chain_handler = ChainHandler()
    except RPCNotConnectedException as exc:
        return JsonResponse({'error': str(exc)}, status=500)

    try:
        value = chain_handler.get_value()
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)
    return JsonResponse({'value': value})


@require_POST
@csrf_exempt
def increment(request: Request) -> JsonResponse:
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    form = IncrementForm(payload)

    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)

    amount = form.cleaned_data['amount']

    wallet = Wallet.objects.first()
    if wallet is None:
        return JsonResponse({'error': 'No wallet configured in database'}, status=500)

    try:
        tx_params = get_increment_tx_params(
            counter_contract_address=settings.COUNTER_ADDRESS, from_address=wallet.address, amount=int(amount)
        )
        chain_handler = ChainHandler()
        tx_hash = chain_handler.send_increment_transaction(private_key=wallet.private_key, tx_params=tx_params)
        response = JsonResponse({'tx_hash': tx_hash})
    except Exception as exc:
        response = JsonResponse({'error': str(exc)}, status=500)

    return response
