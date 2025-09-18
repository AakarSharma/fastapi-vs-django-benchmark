import asyncio
import time
import json
import os
import uuid
import tempfile
from fastapi import FastAPI, HTTPException
from tortoise import Tortoise
from models import User, Product, Order, OrderItem
import aiofiles
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = FastAPI(title="FastAPI Benchmark", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    await Tortoise.init(
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.mysql",
                    "credentials": {
                        "host": "mysql",
                        "port": "3306",
                        "user": "benchmark_user",
                        "password": "benchmark_pass",
                        "database": "benchmark_fastapi",
                        "minsize": 100,
                        "maxsize": 10000,
                        "charset": "utf8mb4",
                    }
                }
            },
            "apps": {
                "models": {
                    "models": ["models"],
                    "default_connection": "default",
                }
            }
        }
    )

@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()

async def simulate_file_io():
    """Simulate file I/O operations with per-call unique temp file"""
    fd, temp_path = tempfile.mkstemp(prefix="benchmark_fastapi_", suffix=".json")
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

async def simulate_database_io():
    """Simulate database I/O operations wrapped in a single transaction"""
    from tortoise.transactions import in_transaction
    base_timestamp = int(time.time() * 1000000)
    unique_id = str(uuid.uuid4())[:8]
    users = []

    async with in_transaction():
        for i in range(10):
            user = await User.create(
                name=f"User {base_timestamp}_{unique_id}_{i}",
                email=f"user{base_timestamp}_{unique_id}_{i}@example.com",
                age=20 + (i % 50)
            )
            users.append(user)

        user_count_before = await User.all().count()

        for user in users[:5]:
            user.name = f"Updated {user.name}"
            await user.save()

        # Ensure net-zero change to keep steady-state
        for user in users:
            await user.delete()

    user_count_after = await User.all().count()
    return {"created": len(users), "total_before": user_count_before, "total_after": user_count_after}

@app.get("/")
async def root():
    return {"message": "FastAPI Benchmark API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/io-intensive")
async def io_intensive_operation():
    """I/O intensive endpoint combining file and database operations"""
    start_time = time.time()
    
    file_results = []
    db_results = []
    
    for _ in range(2):
        file_result = await simulate_file_io()
        file_results.append(file_result)
    
    for _ in range(8):
        db_result = await simulate_database_io()
        db_results.append(db_result)
    
    end_time = time.time()
    
    return {
        "file_operations": len(file_results),
        "db_operations": len(db_results),
        "execution_time": end_time - start_time,
        "timestamp": time.time()
    }

@app.get("/users")
async def get_users():
    """Get all users with I/O operations"""
    users = await User.all()
    return [{"id": user.id, "name": user.name, "email": user.email, "age": user.age} for user in users]

@app.post("/users")
async def create_user(user_data: dict):
    """Create a new user"""
    try:
        user = await User.create(
            name=user_data.get("name", "Test User"),
            email=user_data.get("email", f"test{int(time.time())}@example.com"),
            age=user_data.get("age", 25)
        )
        return {"id": user.id, "name": user.name, "email": user.email, "age": user.age}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reset")
async def reset_database():
    """Delete all data to restore baseline state."""
    try:
        # Delete in FK-safe order
        await OrderItem.all().delete()
        await Order.all().delete()
        await Product.all().delete()
        await User.all().delete()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products")
async def get_products():
    """Get all products with I/O operations"""
    products = await Product.all()
    return [{"id": product.id, "name": product.name, "price": product.price, "description": product.description} for product in products]

@app.post("/products")
async def create_product(product_data: dict):
    """Create a new product"""
    try:
        product = await Product.create(
            name=product_data.get("name", "Test Product"),
            price=product_data.get("price", 10.0),
            description=product_data.get("description", "Test Description")
        )
        return {"id": product.id, "name": product.name, "price": product.price, "description": product.description}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders")
async def get_orders():
    """Get all orders with I/O operations"""
    orders = await Order.all()
    return [{"id": order.id, "user_id": order.user_id, "total_amount": order.total_amount, "created_at": order.created_at} for order in orders]

@app.post("/orders")
async def create_order(order_data: dict):
    """Create a new order"""
    try:
        order = await Order.create(
            user_id=order_data.get("user_id", 1),
            total_amount=order_data.get("total_amount", 0.0)
        )
        return {"id": order.id, "user_id": order.user_id, "total_amount": order.total_amount, "created_at": order.created_at}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))