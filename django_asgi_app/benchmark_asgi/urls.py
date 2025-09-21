from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Do not register 'benchmark' ViewSet to avoid shadowing async endpoints
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    # Async function-based endpoints take precedence
    path('benchmark/health/', views.benchmark_health, name='benchmark_health_async'),
    path('benchmark/io_intensive/', views.benchmark_io_intensive, name='benchmark_io_intensive_async'),
    path('benchmark/reset/', views.benchmark_reset, name='benchmark_reset_async'),
    path('users/', views.users_list, name='users_list_async'),
    path('products/', views.products_list, name='products_list_async'),
    path('orders/', views.orders_list, name='orders_list_async'),
    # DRF router for other operations (detail endpoints, POST/PUT not used in benchmark)
    path('', include(router.urls)),
]
