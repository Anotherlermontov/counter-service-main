from __future__ import annotations

from django.urls import path

from main_service.counter.views import get_value, increment

urlpatterns = [path('value', get_value), path('increment', increment)]
