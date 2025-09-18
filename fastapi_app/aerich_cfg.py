from os import getenv

# Aerich expects a module attribute TORTOISE_ORM

db_url = getenv("AERICH_DB", "mysql://benchmark_user:benchmark_pass@mysql:3306/benchmark_fastapi")

TORTOISE_ORM = {
    "connections": {
        "default": db_url,
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    },
}


