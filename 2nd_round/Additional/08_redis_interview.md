# Redis Interview Prep
> Focused on what this role needs: caching, Celery broker, rate limiting, real-time data, async Redis

---

## Table of Contents
- [Redis Fundamentals](#redis-fundamentals)
- [Data Structures & Use Cases](#data-structures--use-cases)
- [Caching Patterns](#caching-patterns)
- [Redis with Django](#redis-with-django)
- [Redis with FastAPI (Async)](#redis-with-fastapi-async)
- [Redis as Celery Broker](#redis-as-celery-broker)
- [Rate Limiting](#rate-limiting)
- [Real-Time & Pub/Sub](#real-time--pubsub)
- [Production & Reliability](#production--reliability)
- [Scenario-Based Questions](#scenario-based-questions)

---

## Redis Fundamentals

<details>
<summary><strong>1. What is Redis and why is it used alongside PostgreSQL in a backend?</strong></summary>

Redis is an **in-memory data store** — data lives in RAM, making reads/writes ~100,000x faster than PostgreSQL disk operations.

| | Redis | PostgreSQL |
|---|---|---|
| **Speed** | Sub-millisecond (in-memory) | 1–100ms (disk-based) |
| **Persistence** | Optional (RDB snapshots, AOF logs) | Always |
| **Data model** | Key-value + rich structures | Relational |
| **Queries** | Key-based, O(1) most ops | Full SQL |
| **Best for** | Caching, sessions, queues, pub/sub | Durable, complex data |

**Roles Redis plays in your stack:**

```
Client Request
      ↓
Django/FastAPI
      ↓
   Redis ←→ (Cache hit? Return immediately. No DB hit.)
      ↓
 PostgreSQL (Only hit when cache misses)
```

**Typical uses in your projects:**
- **Session storage** — faster than DB session lookups
- **API response caching** — product list, user dashboard
- **Celery message broker** — task queue for background jobs
- **Rate limiting** — sliding window counters
- **Real-time features** — pub/sub for live order status
- **Leaderboards / sorted sets** — e.g., top trading volumes

</details>

---

<details>
<summary><strong>2. What Redis data types do you know? When do you use each?</strong></summary>

```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# STRING — most common: cache, counters, flags, simple key-value
r.set("user:1:name", "Samirul", ex=3600)    # ex = TTL in seconds
r.get("user:1:name")                         # "Samirul"
r.incr("page_views:home")                   # atomic counter (no race condition)
r.incrby("order_count", 5)
r.setnx("lock:payment:order_1", "1")        # set if not exists — distributed lock

# HASH — object fields, avoids JSON serialize/deserialize for partial updates
r.hset("user:1", mapping={"name": "Samirul", "role": "admin", "plan": "pro"})
r.hget("user:1", "role")                    # "admin"
r.hmget("user:1", ["name", "plan"])         # ["Samirul", "pro"]
r.hset("user:1", "last_login", "2024-01-15")  # update one field
r.hgetall("user:1")                          # {"name": "Samirul", ...}
r.hincrby("user:1", "login_count", 1)        # atomic field increment

# LIST — task queues, recent activity log
r.lpush("notifications:user:1", "Order shipped")   # push to front
r.rpush("job_queue", "task_1", "task_2")            # push to back
r.lpop("job_queue")                                 # pop from front (FIFO queue)
r.lrange("notifications:user:1", 0, 9)             # latest 10 items
r.ltrim("notifications:user:1", 0, 99)             # keep only last 100

# SET — unique membership, tags, online users
r.sadd("online_users", "user_1", "user_2", "user_3")
r.srem("online_users", "user_1")
r.sismember("online_users", "user_2")       # True/False
r.smembers("online_users")                  # all members
r.scard("online_users")                     # count
# Set operations:
r.sinter("users:premium", "users:active")  # premium AND active
r.sunion("users:admin", "users:manager")   # admin OR manager
r.sdiff("users:all", "users:banned")       # all except banned

# SORTED SET — ranking, leaderboards, time-series with score=timestamp
r.zadd("leaderboard", {"alice": 9500, "bob": 8200, "carol": 9800})
r.zrank("leaderboard", "alice")             # rank (0-indexed, ascending)
r.zrevrank("leaderboard", "alice")          # rank (descending — position 1 = top)
r.zscore("leaderboard", "alice")            # 9500.0
r.zrevrange("leaderboard", 0, 9, withscores=True)  # top 10

# Trading use case: order book by price
r.zadd("orderbook:AAPL:bids", {"order_1": 182.50, "order_2": 182.45})
best_bid = r.zrevrange("orderbook:AAPL:bids", 0, 0, withscores=True)  # highest price

# STREAM — time-series events, append-only log
r.xadd("orders", {"symbol": "AAPL", "qty": 100, "price": 182.50})
r.xread(count=10, streams={"orders": "0-0"})  # read from beginning

# Expire any key type
r.expire("session:abc123", 1800)   # expire in 30 min
r.ttl("session:abc123")            # time remaining in seconds
r.persist("session:abc123")        # remove expiry
```

</details>

---

## Caching Patterns

<details>
<summary><strong>3. What are the main caching patterns? Which do you use and when?</strong></summary>

```python
import redis
import json
from functools import wraps

r = redis.Redis(decode_responses=True)

# PATTERN 1: Cache-Aside (Lazy Loading) — most common
# Read: check cache → miss → read DB → populate cache
# Write: update DB → invalidate/update cache

def get_product(product_id: int) -> dict:
    cache_key = f"product:{product_id}"

    # 1. Check cache
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)    # cache HIT

    # 2. Cache miss — query DB
    product = Product.objects.select_related("category").get(pk=product_id)
    data = ProductSerializer(product).data

    # 3. Store in cache
    r.setex(cache_key, 300, json.dumps(data))   # 5 minute TTL
    return data

# Cache invalidation — call on product update
def invalidate_product_cache(product_id: int):
    r.delete(f"product:{product_id}")

# PATTERN 2: Write-Through — update cache on every write
# Pros: cache always fresh. Cons: write overhead.

def update_product(product_id: int, data: dict) -> dict:
    # Update DB
    Product.objects.filter(pk=product_id).update(**data)
    product = Product.objects.get(pk=product_id)
    serialized = ProductSerializer(product).data

    # Immediately update cache too
    r.setex(f"product:{product_id}", 600, json.dumps(serialized))
    return serialized

# PATTERN 3: Cache decorator — DRY caching

def cache(ttl: int = 300, key_prefix: str = ""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key from function args
            key = f"{key_prefix or func.__name__}:{args}:{sorted(kwargs.items())}"
            cached = r.get(key)
            if cached:
                return json.loads(cached)
            result = func(*args, **kwargs)
            r.setex(key, ttl, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

@cache(ttl=600, key_prefix="product_list")
def get_product_list(category_id: int, page: int) -> list:
    return list(Product.objects.filter(category_id=category_id).values())

# PATTERN 4: Cache stampede prevention (mutex lock)
# Problem: 1000 requests hit cache at same time after expiry → all hit DB!

import time

def get_with_lock(key: str, factory, ttl: int = 300):
    cached = r.get(key)
    if cached:
        return json.loads(cached)

    # Acquire lock — only one worker rebuilds the cache
    lock_key = f"lock:{key}"
    acquired = r.set(lock_key, "1", nx=True, ex=10)   # nx=only if not exists

    if acquired:
        try:
            data = factory()
            r.setex(key, ttl, json.dumps(data, default=str))
            return data
        finally:
            r.delete(lock_key)
    else:
        # Wait for lock holder to populate cache
        for _ in range(10):
            time.sleep(0.1)
            cached = r.get(key)
            if cached:
                return json.loads(cached)
        return factory()   # fallback — query DB directly
```

</details>

---

## Redis with Django

<details>
<summary><strong>4. How do you configure Redis in Django for cache, sessions, and Celery?</strong></summary>

```python
# pip install django-redis redis

# settings.py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "RETRY_ON_TIMEOUT": True,
            "IGNORE_EXCEPTIONS": True,   # app still works if Redis down
            "MAX_CONNECTIONS": 1000,
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
        },
        "KEY_PREFIX": "martify",
        "TIMEOUT": 300,
    }
}

# Session storage in Redis (not DB — faster)
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Django cache API usage
from django.core.cache import cache

# Basic
cache.set("key", {"data": 123}, timeout=300)
value = cache.get("key")                          # None if expired
value = cache.get("key", default="fallback")

# Atomic operations
cache.incr("api_calls_today")                     # atomic counter
cache.decr("stock:product_1")                     # atomic decrement

# Batch operations
cache.set_many({"k1": "v1", "k2": "v2"}, timeout=300)
cache.get_many(["k1", "k2"])                      # {"k1": "v1", "k2": "v2"}
cache.delete_many(["k1", "k2"])

# Pattern delete (Redis-specific)
from django_redis import get_redis_connection
redis_conn = get_redis_connection("default")
keys = redis_conn.keys("martify:product:*")       # find all product keys
if keys:
    redis_conn.delete(*keys)

# Cache lock for preventing duplicate processing
from django.core.cache import cache

def process_order(order_id: int):
    lock_key = f"processing_lock:order:{order_id}"
    acquired = cache.add(lock_key, "locked", timeout=60)   # add = set if not exists
    if not acquired:
        return   # already being processed
    try:
        do_heavy_work(order_id)
    finally:
        cache.delete(lock_key)
```

</details>

---

## Redis with FastAPI (Async)

<details>
<summary><strong>5. How do you use Redis asynchronously in FastAPI?</strong></summary>

```python
# pip install redis[asyncio]
from redis.asyncio import Redis, ConnectionPool
from fastapi import FastAPI, Depends
import json

# Connection pool — shared across all requests
pool = ConnectionPool.from_url(
    "redis://localhost:6379/0",
    max_connections=100,
    decode_responses=True,
)

async def get_redis() -> Redis:
    """Dependency — provides Redis client per request."""
    return Redis(connection_pool=pool)

# Lifespan — create pool on startup, close on shutdown
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(connection_pool=pool)
    yield
    await app.state.redis.aclose()

app = FastAPI(lifespan=lifespan)

# Usage in endpoints
@app.get("/products/{product_id}")
async def get_product(
    product_id: int,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    cache_key = f"product:{product_id}"
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Not found")

    data = ProductSchema.from_orm(product).model_dump()
    await redis.setex(cache_key, 300, json.dumps(data))
    return data

# Async pipeline — batch Redis operations
@app.get("/dashboard")
async def dashboard(
    user_id: int,
    redis: Redis = Depends(get_redis),
):
    async with redis.pipeline(transaction=True) as pipe:
        pipe.get(f"stats:orders:{user_id}")
        pipe.get(f"stats:revenue:{user_id}")
        pipe.zrevrange("leaderboard", 0, 9, withscores=True)
        orders_cached, revenue_cached, leaderboard = await pipe.execute()

    return {
        "orders": json.loads(orders_cached) if orders_cached else None,
        "revenue": float(revenue_cached) if revenue_cached else None,
        "leaderboard": leaderboard,
    }

# Distributed lock in async context
from redis.asyncio.lock import Lock

async def process_with_lock(redis: Redis, resource_id: int):
    lock = Lock(redis, f"lock:resource:{resource_id}", timeout=30)
    async with lock:
        await do_exclusive_work(resource_id)
```

</details>

---

## Redis as Celery Broker

<details>
<summary><strong>6. How does Redis work as a Celery broker? What are the key configurations?</strong></summary>

```python
# celery.py
from celery import Celery

app = Celery("martify")

app.conf.update(
    # Broker — where tasks are sent (Redis list)
    broker_url="redis://localhost:6379/0",

    # Backend — where results are stored (Redis key)
    result_backend="redis://localhost:6379/0",

    # Serialization
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],

    # Task routing — different queues for priority
    task_routes={
        "orders.tasks.send_email": {"queue": "emails"},
        "orders.tasks.generate_report": {"queue": "reports"},
        "orders.tasks.process_payment": {"queue": "critical"},
    },

    # Result expiry — don't keep results forever
    result_expires=3600,

    # Retry failed tasks
    task_acks_late=True,          # ack after task completes (not on receipt)
    task_reject_on_worker_lost=True,  # re-queue if worker crashes

    # Rate limiting
    task_default_rate_limit="100/m",  # max 100 tasks/minute globally
)

# Start workers for specific queues
# celery -A martify worker -Q critical,default -c 4
# celery -A martify worker -Q emails -c 2
# celery -A martify worker -Q reports -c 1

# How Redis stores tasks:
# - Producer calls task.delay() → serialized task pushed to Redis LIST
# - Celery worker BLPOP from that list (blocking pop — efficient)
# - Result stored as Redis key with TTL

# Monitor Redis queue depth
import redis
r = redis.Redis()
queue_length = r.llen("celery")   # number of pending tasks
print(f"Pending tasks: {queue_length}")

# Flower — web-based Celery monitoring
# celery -A martify flower --port=5555
```

</details>

---

## Rate Limiting

<details>
<summary><strong>7. Implement a Redis-based rate limiter (sliding window algorithm).</strong></summary>

```python
import redis
import time
from fastapi import HTTPException, Request, Depends

r = redis.Redis(decode_responses=True)

# Fixed Window — simple but has burst problem at window boundaries
def fixed_window_limit(key: str, limit: int, window_seconds: int) -> bool:
    current = r.incr(key)
    if current == 1:
        r.expire(key, window_seconds)
    return current <= limit

# Sliding Window — more accurate, prevents boundary bursts
def sliding_window_limit(
    identifier: str,
    limit: int,
    window_seconds: int,
) -> tuple[bool, int]:
    """
    Uses a Sorted Set where score = timestamp.
    Each request adds an entry, old entries are removed.
    """
    now = time.time()
    window_start = now - window_seconds
    key = f"rate_limit:{identifier}"

    with r.pipeline() as pipe:
        # Remove expired entries (outside window)
        pipe.zremrangebyscore(key, 0, window_start)
        # Count remaining requests in window
        pipe.zcard(key)
        # Add current request with timestamp as score
        pipe.zadd(key, {f"{now}:{id(object())}": now})
        # Set expiry on the key
        pipe.expire(key, window_seconds)
        _, count, _, _ = pipe.execute()

    allowed = count < limit
    remaining = max(0, limit - count - 1)
    return allowed, remaining

# Token Bucket — allows short bursts, smooth long-term
def token_bucket_limit(key: str, capacity: int, refill_rate: float) -> bool:
    """
    capacity: max tokens (burst size)
    refill_rate: tokens added per second
    """
    now = time.time()
    bucket_key = f"bucket:{key}"

    with r.pipeline() as pipe:
        pipe.hmget(bucket_key, ["tokens", "last_refill"])
        tokens_data, = [pipe.execute()]

    tokens = float(tokens_data[0] or capacity)
    last_refill = float(tokens_data[1] or now)

    # Add tokens based on elapsed time
    elapsed = now - last_refill
    tokens = min(capacity, tokens + elapsed * refill_rate)

    if tokens >= 1:
        r.hset(bucket_key, mapping={"tokens": tokens - 1, "last_refill": now})
        r.expire(bucket_key, 3600)
        return True
    return False

# FastAPI middleware using sliding window
class RateLimitMiddleware:
    def __init__(self, app, limit: int = 60, window: int = 60):
        self.app = app
        self.limit = limit
        self.window = window

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            ip = request.client.host
            identifier = f"{ip}:{request.url.path}"

            allowed, remaining = sliding_window_limit(identifier, self.limit, self.window)

            if not allowed:
                from fastapi.responses import JSONResponse
                response = JSONResponse(
                    {"error": "Rate limit exceeded", "retry_after": self.window},
                    status_code=429,
                    headers={"Retry-After": str(self.window), "X-RateLimit-Remaining": "0"},
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)

app.add_middleware(RateLimitMiddleware, limit=100, window=60)
```

</details>

---

## Real-Time & Pub/Sub

<details>
<summary><strong>8. How do you use Redis Pub/Sub for real-time features?</strong></summary>

```python
# Redis Pub/Sub — publisher sends messages, subscribers receive instantly
# Use case: broadcast order updates, price changes, notifications

# Publisher — send order status update
import redis
import json

r = redis.Redis(decode_responses=True)

def publish_order_update(order_id: int, status: str, user_id: int):
    message = json.dumps({
        "order_id": order_id,
        "status": status,
        "user_id": user_id,
        "timestamp": time.time(),
    })
    r.publish(f"orders:{user_id}", message)   # channel per user

# Subscriber — listen and process
def order_status_listener():
    pubsub = r.pubsub()
    pubsub.psubscribe("orders:*")   # subscribe to all order channels

    for message in pubsub.listen():
        if message["type"] == "pmessage":
            data = json.loads(message["data"])
            print(f"Order {data['order_id']} → {data['status']}")
            notify_user(data["user_id"], data)

# Run listener in thread
import threading
listener_thread = threading.Thread(target=order_status_listener, daemon=True)
listener_thread.start()

# FastAPI WebSocket + Redis Pub/Sub — real-time price feed
from fastapi import WebSocket
from redis.asyncio import Redis

@app.websocket("/ws/orders/{user_id}")
async def order_updates_ws(websocket: WebSocket, user_id: int):
    await websocket.accept()

    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"orders:{user_id}")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])
    except Exception:
        pass
    finally:
        await pubsub.unsubscribe(f"orders:{user_id}")
        await redis.aclose()
        await websocket.close()

# From a background task, trigger the update:
async def on_order_status_change(order_id: int, status: str, user_id: int):
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    await redis.publish(
        f"orders:{user_id}",
        json.dumps({"order_id": order_id, "status": status}),
    )
    await redis.aclose()
```

</details>

---

## Production & Reliability

<details>
<summary><strong>9. How do you make Redis reliable in production?</strong></summary>

```python
# 1. Persistence — don't lose data on restart

# RDB snapshots — periodic full dump
# redis.conf:
# save 900 1        # save if 1 key changed in 900 seconds
# save 300 10       # save if 10 keys changed in 300 seconds

# AOF (Append-Only File) — log every write (more durable, larger file)
# appendonly yes
# appendfsync everysec   # flush to disk every second (good balance)

# 2. Django Redis with circuit breaker
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "OPTIONS": {
            "IGNORE_EXCEPTIONS": True,  # if Redis fails, app continues (cache miss)
        }
    }
}

# 3. Connection pool — prevent connection exhaustion
pool = redis.ConnectionPool(
    host="localhost",
    port=6379,
    max_connections=50,     # limit total connections
    socket_connect_timeout=2,
    socket_timeout=2,
    retry_on_timeout=True,
)
r = redis.Redis(connection_pool=pool)

# 4. Key naming conventions — prevent collisions
# Format: app:entity:id:field
# Examples:
# martify:product:123:detail
# martify:user:456:session
# martify:rate_limit:192.168.1.1:/api/orders

# 5. Always set TTL — prevent memory bloat
r.setex("key", 3600, "value")   # always use setex, not set alone

# 6. Memory management
# redis.conf:
# maxmemory 256mb
# maxmemory-policy allkeys-lru   # evict least-recently-used keys when full

# 7. Sentinel (HA without Cluster)
from redis.sentinel import Sentinel
sentinel = Sentinel([
    ("sentinel-1", 26379),
    ("sentinel-2", 26379),
], socket_timeout=0.1)
master = sentinel.master_for("mymaster", socket_timeout=0.1)
slave = sentinel.slave_for("mymaster", socket_timeout=0.1)

# 8. Health check in FastAPI startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis.from_url(settings.redis_url)
    try:
        await redis.ping()
    except Exception as e:
        raise RuntimeError(f"Redis unavailable: {e}")
    app.state.redis = redis
    yield
    await redis.aclose()
```

</details>

---

## Scenario-Based Questions

<details>
<summary><strong>10. Your Redis cache is consuming too much memory. How do you fix it?</strong></summary>

```bash
# Step 1: Diagnose
redis-cli info memory          # used_memory, maxmemory, mem_fragmentation_ratio
redis-cli info keyspace        # key count per database
redis-cli --bigkeys            # find largest keys
redis-cli --memkeys            # memory usage per key

# Step 2: Analyse key patterns
redis-cli keys "*"            # list all keys (use SCAN in prod — non-blocking)
redis-cli object encoding key  # see how a key is stored
redis-cli debug object key     # serializedlength

# Step 3: Fixes
```

```python
# Fix 1: Add TTL to keys that don't have one
# Find keys with no expiry:
# redis-cli --no-auth-warning keys "*" | while read key; do ttl=$(redis-cli ttl $key); [ $ttl -eq -1 ] && echo $key; done

# Fix 2: Use more memory-efficient data types
# Instead of storing JSON strings, use Hashes for structured data
# Hash uses ~70% less memory than equivalent JSON strings for many small fields

# Fix 3: Enable key compression
# For string values, use msgpack instead of JSON (smaller)
import msgpack

def cache_set(key, data, ttl=300):
    r.setex(key, ttl, msgpack.packb(data))

def cache_get(key):
    raw = r.get(key)
    return msgpack.unpackb(raw) if raw else None

# Fix 4: Reduce TTL on less critical caches
# Fix 5: Enable maxmemory-policy in redis.conf
# Fix 6: Use Redis Cluster for horizontal scaling

# Fix 7: Eviction policy tuning
# allkeys-lru: evict any key (good for pure cache)
# volatile-lru: only evict keys with TTL (if you mix cache + persistent data)
```

</details>

---

<details>
<summary><strong>11. How do you implement a distributed lock with Redis?</strong></summary>

```python
import redis
import time
import uuid

r = redis.Redis(decode_responses=True)

# Simple distributed lock — prevent parallel processing of same resource
class RedisLock:
    def __init__(self, key: str, timeout: int = 30):
        self.key = f"lock:{key}"
        self.timeout = timeout
        self.lock_id = str(uuid.uuid4())   # unique per lock instance

    def acquire(self) -> bool:
        # SET key value NX PX milliseconds — atomic!
        return r.set(self.key, self.lock_id, nx=True, ex=self.timeout)

    def release(self):
        # Only release if WE own the lock (prevent releasing other's lock)
        # Use Lua script for atomic check-and-delete
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        r.eval(lua_script, 1, self.key, self.lock_id)

    def __enter__(self):
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            if self.acquire():
                return self
            time.sleep(0.1)
        raise TimeoutError(f"Could not acquire lock: {self.key}")

    def __exit__(self, *args):
        self.release()

# Usage — prevent double-processing an order
def process_payment(order_id: int):
    with RedisLock(f"payment:{order_id}", timeout=60):
        # Only one instance processes this order at a time
        order = Order.objects.select_for_update().get(pk=order_id)
        if order.status != "pending":
            return   # already processed
        charge(order)
        order.status = "paid"
        order.save()

# Python redis-py has built-in lock:
lock = r.lock("payment:123", timeout=60, blocking_timeout=10)
with lock:
    process_payment(123)

# For async FastAPI:
from redis.asyncio.lock import Lock as AsyncLock

async def process_async(order_id: int, redis: Redis):
    async with AsyncLock(redis, f"lock:payment:{order_id}", timeout=60):
        await do_work(order_id)
```

</details>
