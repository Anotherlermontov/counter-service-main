from __future__ import annotations

from django.db import models


class Wallet(models.Model):
    address = models.CharField(max_length=42, unique=True)
    private_key = models.TextField()

    def __str__(self) -> str:
        return self.address
