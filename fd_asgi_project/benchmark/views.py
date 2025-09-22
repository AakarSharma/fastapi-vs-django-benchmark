from __future__ import annotations

import asyncio
import json
import os
import tempfile
import time
import uuid
import aiofiles
from fast_django.routers import APIRouter
from fd_asgi_project.models import User, Product, Order, OrderItem

router = APIRouter()


@router.get("/api/benchmark/health/")
async def health() -> dict[str, float | str]:
    return {"status": "healthy", "timestamp": time.time()}


async def _simulate_file_io() -> dict:
    fd, temp_path = tempfile.mkstemp(prefix="benchmark_fd_", suffix=".json")
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


async def _simulate_database_io() -> dict:
    base_timestamp = int(time.time() * 1000000)
    unique_id = str(uuid.uuid4())[:8]
    created = []
    for i in range(10):
        u = await User.create(
            name=f"User {base_timestamp}_{unique_id}_{i}",
            email=f"user{base_timestamp}_{unique_id}_{i}@example.com",
            age=20 + (i % 50),
        )
        created.append(u.id)
    user_count_before = await User.all().count()
    if created:
        # Delete all created users to keep steady state
        await User.filter(id__in=created).delete()
    user_count_after = await User.all().count()
    return {"created": len(created), "total_before": user_count_before, "total_after": user_count_after}


@router.post("/api/benchmark/io_intensive/")
async def io_intensive() -> dict:
    start = time.time()
    file_results = []
    db_results = []
    for _ in range(2):
        file_results.append(await _simulate_file_io())
    for _ in range(8):
        db_results.append(await _simulate_database_io())
    end = time.time()
    return {
        "file_operations": len(file_results),
        "db_operations": len(db_results),
        "execution_time": end - start,
        "timestamp": time.time(),
    }


@router.get("/api/users/")
async def users_list() -> list[dict]:
    users = await User.all()
    return [{"id": u.id, "name": u.name, "email": u.email, "age": u.age} for u in users]


@router.get("/api/products/")
async def products_list() -> list[dict]:
    products = await Product.all()
    return [
        {"id": p.id, "name": p.name, "price": float(p.price), "description": p.description}
        for p in products
    ]


@router.get("/api/orders/")
async def orders_list() -> list[dict]:
    orders = await Order.all()
    return [
        {
            "id": o.id,
            "user_id": o.user_id,
            "total_amount": float(o.total_amount),
            "created_at": o.created_at.isoformat() if o.created_at else None,
        }
        for o in orders
    ]
