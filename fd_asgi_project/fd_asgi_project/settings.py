from __future__ import annotations

from pydantic import Field

from fast_django.settings import Settings as BaseSettings
from pydantic import BaseModel
from typing import Any


class OrmConfig(BaseModel):
    models: list[str] = Field(default_factory=lambda: ["aerich.models"])
    connections: dict[str, Any] = Field(default_factory=lambda: {"default": "sqlite://db.sqlite3"})
    apps: dict[str, dict[str, Any]] = Field(default_factory=dict)


BaseSettings.orm = OrmConfig


class Settings(BaseSettings):
    app_name: str = "fd_asgi_project"
    debug: bool = True
    orm: OrmConfig = OrmConfig(
        models=["aerich.models"],
        connections={
            "default": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": "mysql",
                    "port": "3306",
                    "user": "benchmark_user",
                    "password": "benchmark_pass",
                    "database": "benchmark_fast_django_asgi",
                    "minsize": 100,
                    "maxsize": 10000,
                    "charset": "utf8mb4",
                }
            }
        },
        apps={
            "models": {
                "models": ["fd_asgi_project.models"],
                "default_connection": "default",
            }
        }
    )
    installed_apps: list[str] = Field(default_factory=lambda: ["fd_asgi_project", "benchmark"])
    admin_enabled: bool = True
