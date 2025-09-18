import time
import json
import os
import uuid
import tempfile
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Product, Order, OrderItem
from .serializers import UserSerializer, ProductSerializer, OrderSerializer

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
        
        for _ in range(2):
            file_result = self._simulate_file_io()
            file_results.append(file_result)
        
        for _ in range(8):
            db_result = self._simulate_database_io()
            db_results.append(db_result)
        
        end_time = time.time()
        
        return Response({
            "file_operations": len(file_results),
            "db_operations": len(db_results),
            "execution_time": end_time - start_time,
            "timestamp": time.time()
        })
    
    def _simulate_file_io(self):
        """Simulate file I/O operations with per-call unique temp file"""
        fd, temp_path = tempfile.mkstemp(prefix="benchmark_django_", suffix=".json")
        os.close(fd)
        data = {"timestamp": time.time(), "data": "x" * 1000}
        try:
            with open(temp_path, 'w') as f:
                json.dump(data, f)
            with open(temp_path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            return {"timestamp": time.time(), "data": "fallback_data", "error": str(e)}
        finally:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass
    
    def _simulate_database_io(self):
        """Simulate database I/O operations wrapped in a single atomic transaction"""
        from django.db import transaction
        base_timestamp = int(time.time() * 1000000)
        unique_id = str(uuid.uuid4())[:8]
        users = []
        with transaction.atomic():
            for i in range(10):
                user = User.objects.create(
                    name=f"User {base_timestamp}_{unique_id}_{i}",
                    email=f"user{base_timestamp}_{unique_id}_{i}@example.com",
                    age=20 + (i % 50)
                )
                users.append(user)

            user_count_before = User.objects.count()

            for user in users[:5]:
                user.name = f"Updated {user.name}"
                user.save()

            # Ensure net-zero change to keep steady-state
            for user in users:
                user.delete()

        user_count_after = User.objects.count()
        return {"created": len(users), "total_before": user_count_before, "total_after": user_count_after}

    @action(detail=False, methods=['post'])
    def reset(self, request):
        """Delete all data to restore baseline state."""
        try:
            # Delete in FK-safe order
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Product.objects.all().delete()
            User.objects.all().delete()
            return Response({"status": "ok"})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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