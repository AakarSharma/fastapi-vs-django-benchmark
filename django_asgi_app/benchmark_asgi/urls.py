from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'benchmark', views.BenchmarkViewSet, basename='benchmark')
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('benchmark/health/', views.benchmark_health, name='benchmark_health_async'),
    path('benchmark/io_intensive/', views.benchmark_io_intensive, name='benchmark_io_intensive_async'),
]
