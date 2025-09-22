from __future__ import annotations

from fast_django import create_app
from .settings import Settings

app = create_app(Settings())
