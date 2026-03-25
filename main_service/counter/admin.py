from __future__ import annotations

from django.contrib import admin

from main_service.counter.models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')
