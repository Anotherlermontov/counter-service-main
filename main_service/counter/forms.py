from __future__ import annotations

from django import forms


class IncrementForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
