from __future__ import annotations

from django.contrib import admin

from counter.models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')
