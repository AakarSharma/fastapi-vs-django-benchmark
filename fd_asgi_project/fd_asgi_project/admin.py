from __future__ import annotations

from importlib import import_module

from fastapi import FastAPI

from fast_django.settings import Settings


def init_admin(app: FastAPI, settings: Settings) -> None:
    pass
