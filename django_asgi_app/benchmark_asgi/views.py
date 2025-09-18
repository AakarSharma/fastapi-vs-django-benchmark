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
from asgiref.sync import sync_to_async
from .models import User, Product, Order, OrderItem
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from django.http import JsonResponse

class BenchmarkViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def health(self, request):
        return Response({"status": "healthy", "timestamp": time.time()})
    
    @action(detail=False, methods=['post'])
    def io_intensive(self, request):
        """I/O intensive endpoint combining file and database operations"""
        start_time = time.time()
        
        file_results = []
        db_results = []
        
        # Run operations sequentially like FastAPI but using asyncio.run
        for _ in range(2):
            file_result = asyncio.run(self._simulate_file_io())
            file_results.append(file_result)
        
        for _ in range(8):
            db_result = asyncio.run(self._simulate_database_io())
            db_results.append(db_result)
        
        end_time = time.time()
        
        return Response({
            "file_operations": len(file_results),
            "db_operations": len(db_results),
            "execution_time": end_time - start_time,
            "timestamp": time.time()
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
        """Simulate database I/O operations wrapped in a single atomic transaction"""
        base_timestamp = int(time.time() * 1000000)
        unique_id = str(uuid.uuid4())[:8]
        
        # Use sync operations in a thread pool
        def atomic_operation():
            with transaction.atomic():
                users_list = []
                for i in range(10):
                    user = User.objects.create(
                        name=f"User {base_timestamp}_{unique_id}_{i}",
                        email=f"user{base_timestamp}_{unique_id}_{i}@example.com",
                        age=20 + (i % 50)
                    )
                    users_list.append(user)

                user_count_before = User.objects.count()

                for user in users_list[:5]:
                    user.name = f"Updated {user.name}"
                    user.save()

                # Ensure net-zero change to keep steady-state
                for user in users_list:
                    user.delete()

                return len(users_list), user_count_before, User.objects.count()
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        created_count, user_count_before, user_count_after = await loop.run_in_executor(None, atomic_operation)
        return {"created": created_count, "total_before": user_count_before, "total_after": user_count_after}

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

async def benchmark_io_intensive(request):
    start_time = time.time()
    file_results = []
    db_results = []
    # Sequential like FastAPI
    # Reuse helpers defined above on the class by instantiating a temporary object
    temp = BenchmarkViewSet()
    for _ in range(2):
        file_result = await temp._simulate_file_io()
        file_results.append(file_result)
    for _ in range(8):
        db_result = await temp._simulate_database_io()
        db_results.append(db_result)
    end_time = time.time()
    return JsonResponse({
        "file_operations": len(file_results),
        "db_operations": len(db_results),
        "execution_time": end_time - start_time,
        "timestamp": time.time()
    })

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
