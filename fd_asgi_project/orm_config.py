ORM = {
    'connections': {
        'default': 'mysql://benchmark_user:benchmark_pass@mysql:3306/benchmark_fast_django_asgi?charset=utf8mb4'
    },
    'apps': {
        'models': {
            'models': ['fd_asgi_project.models', 'aerich.models'],
            'default_connection': 'default'
        }
    }
}