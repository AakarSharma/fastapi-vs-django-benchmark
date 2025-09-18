import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'benchmark_project_asgi.settings')

application = get_asgi_application()
