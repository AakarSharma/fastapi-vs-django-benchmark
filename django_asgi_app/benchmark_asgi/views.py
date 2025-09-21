import asyncio
import time
import json
import os
import uuid
import tempfile
import aiofiles
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Value
from django.db.models.functions import Concat
from .models import User, Product, Order, OrderItem
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from django.http import JsonResponse

class BenchmarkViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def health(self, request):
        return Response({"status": "healthy", "timestamp": time.time()})
    
    @action(detail=False, methods=['post'])
    def io_intensive(self, request):
        """Deprecated in ASGI: function-based async view is used instead."""
        start_time = time.time()
        return Response({
            "file_operations": 0,
            "db_operations": 0,
            "execution_time": time.time() - start_time,
            "timestamp": time.time(),
            "note": "Use /api/benchmark/io_intensive/ async endpoint"
        })
    
    async def _simulate_file_io(self):
        """Simulate file I/O operations with per-call unique temp file"""
        fd, temp_path = tempfile.mkstemp(prefix="benchmark_django_asgi_", suffix=".json")
        os.close(fd)
        data = {"timestamp": time.time(), "data": "x" * 1000}
        try:
            async with aiofiles.open(temp_path, 'w') as f:
                await f.write(json.dumps(data))
            async with aiofiles.open(temp_path, 'r') as f:
                content = await f.read()
                data = json.loads(content)
            return data
        except Exception as e:
            return {"timestamp": time.time(), "data": "fallback_data", "error": str(e)}
        finally:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass
    
    async def _simulate_database_io(self):
        """Deprecated: async function-based helper is used instead."""
        return {"created": 0, "total_before": 0, "total_after": 0}

    @action(detail=False, methods=['post'])
    def reset(self, request):
        """Delete all data to restore baseline state."""
        try:
            # Delete in FK-safe order using sync operations
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Product.objects.all().delete()
            User.objects.all().delete()
            return Response({"status": "ok"})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

async def benchmark_health(request):
    return JsonResponse({"status": "healthy", "timestamp": time.time()})

async def _simulate_file_io_async():
    fd, temp_path = tempfile.mkstemp(prefix="benchmark_django_asgi_", suffix=".json")
    os.close(fd)
    data = {"timestamp": time.time(), "data": "x" * 1000}
    try:
        async with aiofiles.open(temp_path, 'w') as f:
            await f.write(json.dumps(data))
        async with aiofiles.open(temp_path, 'r') as f:
            content = await f.read()
            data = json.loads(content)
        return data
    except Exception as e:
        return {"timestamp": time.time(), "data": "fallback_data", "error": str(e)}
    finally:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass

async def _simulate_database_io_async():
    base_timestamp = int(time.time() * 1000000)
    unique_id = str(uuid.uuid4())[:8]
    created_ids = []
    for i in range(10):
        user = await User.objects.acreate(
            name=f"User {base_timestamp}_{unique_id}_{i}",
            email=f"user{base_timestamp}_{unique_id}_{i}@example.com",
            age=20 + (i % 50)
        )
        created_ids.append(user.id)
    user_count_before = await User.objects.acount()
    # Bulk update first 5 users' names using async queryset aupdate
    if created_ids:
        await User.objects.filter(id__in=created_ids[:5]).aupdate(
            name=Concat(Value("Updated "), F("name"))
        )
        # Bulk delete all created users using async queryset adelete
        await User.objects.filter(id__in=created_ids).adelete()
    user_count_after = await User.objects.acount()
    return {"created": len(created_ids), "total_before": user_count_before, "total_after": user_count_after}

@csrf_exempt
async def benchmark_io_intensive(request):
    start_time = time.time()
    file_results = []
    db_results = []
    for _ in range(2):
        file_result = await _simulate_file_io_async()
        file_results.append(file_result)
    for _ in range(8):
        db_result = await _simulate_database_io_async()
        db_results.append(db_result)
    end_time = time.time()
    return JsonResponse({
        "file_operations": len(file_results),
        "db_operations": len(db_results),
        "execution_time": end_time - start_time,
        "timestamp": time.time()
    })

@csrf_exempt
async def benchmark_reset(request):
    try:
        # Delete in FK-safe order using async queryset methods
        await OrderItem.objects.all().adelete()
        await Order.objects.all().adelete()
        await Product.objects.all().adelete()
        await User.objects.all().adelete()
        return JsonResponse({"status": "ok"})
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def list(self, request, *args, **kwargs):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Async function-based list endpoints used by the benchmark
async def users_list(request):
    results = []
    async for u in User.objects.all().aiterator(chunk_size=1000):
        results.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "age": u.age,
        })
    return JsonResponse(results, safe=False)

async def products_list(request):
    results = []
    async for p in Product.objects.all().aiterator(chunk_size=1000):
        results.append({
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "description": p.description,
        })
    return JsonResponse(results, safe=False)

async def orders_list(request):
    results = []
    async for o in Order.objects.all().aiterator(chunk_size=1000):
        results.append({
            "id": o.id,
            "user_id": o.user_id,
            "total_amount": float(o.total_amount),
            "created_at": o.created_at.isoformat() if o.created_at else None,
        })
    return JsonResponse(results, safe=False)
