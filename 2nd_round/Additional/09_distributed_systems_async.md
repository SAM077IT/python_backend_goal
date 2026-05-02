# Distributed Systems, Async & Fintech Concepts
> Covers the "preferred skills" that will differentiate you: event-driven architecture, async processing, real-time data, scalable systems

---

## Table of Contents
- [Distributed Systems Fundamentals](#distributed-systems-fundamentals)
- [Event-Driven Architecture](#event-driven-architecture)
- [Asynchronous Processing Patterns](#asynchronous-processing-patterns)
- [Real-Time Data Handling](#real-time-data-handling)
- [Scalable Backend Architecture](#scalable-backend-architecture)
- [Fintech / Trading Concepts](#fintech--trading-concepts)
- [Scenario-Based Questions](#scenario-based-questions)

---

## Distributed Systems Fundamentals

<details>
<summary><strong>1. What is CAP theorem? How does it affect your database choices?</strong></summary>

**CAP Theorem** states a distributed system can guarantee at most **2 of 3**:

| Property | Meaning |
|---|---|
| **C** — Consistency | Every read gets the latest write (or an error) |
| **A** — Availability | Every request gets a response (not necessarily latest) |
| **P** — Partition tolerance | System continues despite network splits between nodes |

Network partitions **always happen** in distributed systems, so you choose **CP or AP**:

```
CP (Consistency + Partition): PostgreSQL, Redis (cluster mode), MongoDB (w:majority)
AP (Availability + Partition): Cassandra, CouchDB, DynamoDB, Redis (single node, best effort)
```

```python
# Real-world example — e-commerce order system:

# Inventory (CP — must be consistent, overselling is catastrophic)
# PostgreSQL with select_for_update() — strong consistency
@transaction.atomic
def reserve_stock(product_id: int, qty: int):
    product = Product.objects.select_for_update().get(pk=product_id)
    if product.stock < qty:
        raise InsufficientStockError()
    product.stock -= qty
    product.save()

# Product catalog (AP — OK if user sees slightly stale price for a few seconds)
# Cache in Redis, tolerate eventual consistency
def get_product_price(product_id: int) -> float:
    cached = redis.get(f"price:{product_id}")
    if cached:
        return float(cached)   # might be 1 min old — acceptable
    price = Product.objects.values_list('price', flat=True).get(pk=product_id)
    redis.setex(f"price:{product_id}", 60, price)
    return price

# Order history (AP — slight delay is fine)
# Read from replica (might lag primary by <1s)
orders = Order.objects.using('replica').filter(user=user)
```

> 💡 **Interview answer:** "For financial data like account balances and stock inventory, I use CP (PostgreSQL with transactions). For less critical data like product descriptions and analytics, I accept AP with Redis caching — faster reads with acceptable eventual consistency."

</details>

---

<details>
<summary><strong>2. What are the challenges of distributed systems and how do you handle them?</strong></summary>

```python
# Challenge 1: NETWORK FAILURES — requests may fail or time out

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
async def call_payment_service(order_id: int, amount: float) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            "http://payment-service/charge",
            json={"order_id": order_id, "amount": amount}
        )
        resp.raise_for_status()
        return resp.json()

# Challenge 2: RACE CONDITIONS — two processes updating same data

from django.db.models import F
from django.db import transaction

# WRONG — race condition (two workers read 5, both write 4)
def decrement_stock_WRONG(product_id, qty):
    product = Product.objects.get(pk=product_id)
    product.stock -= qty    # read then write — not atomic!
    product.save()

# RIGHT — atomic DB-level operation
def decrement_stock_CORRECT(product_id, qty):
    updated = Product.objects.filter(
        pk=product_id, stock__gte=qty
    ).update(stock=F('stock') - qty)
    if updated == 0:
        raise InsufficientStockError()

# Challenge 3: DUPLICATE PROCESSING — same task processed twice
# Solution: Idempotency keys

class IdempotentOrderProcessor:
    def __init__(self, redis):
        self.redis = redis

    def process(self, idempotency_key: str, order_data: dict) -> dict:
        # Check if already processed
        result_key = f"idem:{idempotency_key}"
        cached_result = self.redis.get(result_key)
        if cached_result:
            return json.loads(cached_result)   # return same result

        # Process
        result = create_order(order_data)

        # Store result with TTL (24 hours)
        self.redis.setex(result_key, 86400, json.dumps(result))
        return result

# Challenge 4: PARTIAL FAILURES — saga pattern for distributed transactions

# Saga: sequence of local transactions, each with a compensating action

class OrderSaga:
    def execute(self, order_data: dict):
        order = None
        payment = None
        try:
            # Step 1: Create order
            order = Order.objects.create(**order_data)

            # Step 2: Reserve stock
            reserve_stock(order_data['product_id'], order_data['qty'])

            # Step 3: Charge payment
            payment = charge_payment(order.total)

            # Step 4: Confirm order
            order.status = 'confirmed'
            order.save()
            return order

        except PaymentError:
            # Compensate: release reserved stock
            if order:
                release_stock(order_data['product_id'], order_data['qty'])
                order.status = 'payment_failed'
                order.save()
            raise

        except StockError:
            # Compensate: cancel order
            if order:
                order.status = 'cancelled'
                order.save()
            raise
```

</details>

---

## Event-Driven Architecture

<details>
<summary><strong>3. What is event-driven architecture? How does it compare to request-response?</strong></summary>

```
Request-Response (synchronous):
Client → Service A → Service B → Service C → Response
         (waits)    (waits)    (waits)

Event-Driven (asynchronous):
Client → Service A → [publish event to message broker] → Response (immediate)
                              ↓
                      Service B consumes event
                      Service C consumes event
                      Service D consumes event
```

**Tradeoffs:**

| | Request-Response | Event-Driven |
|---|---|---|
| Coupling | Tight (caller knows callee) | Loose (publisher doesn't know subscribers) |
| Latency | Synchronous — waits for all | Async — returns immediately |
| Reliability | Fails if any service is down | Tolerates downstream failures |
| Debugging | Easy to trace | Harder (distributed tracing needed) |
| Consistency | Easier | Eventually consistent |

```python
# Event-Driven with Celery + Redis

# Before (tightly coupled, slow):
def place_order(order_data):
    order = create_order(order_data)
    send_confirmation_email(order)      # blocks! 2s
    update_inventory(order)            # blocks! 500ms
    notify_warehouse(order)            # blocks! 1s
    update_analytics(order)            # blocks! 300ms
    return order                        # total: 3.8 seconds!

# After (event-driven, fast):
def place_order(order_data):
    order = create_order(order_data)   # only the critical path: 50ms
    order_placed.send(order_id=order.id)   # publish event, return immediately
    return order

# Handlers run independently (Celery workers):
@receiver(order_placed)
def handle_confirmation_email(sender, order_id, **kwargs):
    send_confirmation_email.delay(order_id)

@receiver(order_placed)
def handle_inventory_update(sender, order_id, **kwargs):
    update_inventory.delay(order_id)

@receiver(order_placed)
def handle_warehouse_notification(sender, order_id, **kwargs):
    notify_warehouse.delay(order_id)

# Result: API returns in 50ms, background work happens asynchronously
```

</details>

---

<details>
<summary><strong>4. What is a message queue? How does Celery implement it with Redis?</strong></summary>

```python
# Message Queue: a buffer between producers and consumers
# Producer sends messages, consumer processes at its own pace

# Flow with Celery + Redis:
# API View → task.delay() → Redis LIST (queue) → Celery Worker → Process

# redis-cli monitor shows:
# RPUSH celery {"task": "send_email", "args": [1, "hello"]}  ← producer
# BLPOP celery 0                                               ← worker polling

# Multiple queues for priority
from celery import Celery
from kombu import Queue

app = Celery()

app.conf.task_queues = [
    Queue("critical", routing_key="critical"),    # payment processing
    Queue("default", routing_key="default"),      # regular tasks
    Queue("low", routing_key="low"),              # reports, analytics
]
app.conf.task_default_queue = "default"

# Route tasks to queues
app.conf.task_routes = {
    "orders.tasks.process_payment": {"queue": "critical"},
    "orders.tasks.send_email": {"queue": "default"},
    "reports.tasks.generate_monthly": {"queue": "low"},
}

# Start workers for different queues
# celery worker -Q critical -c 8     (8 concurrent workers)
# celery worker -Q default -c 4
# celery worker -Q low -c 1

# Task chaining — pipeline of dependent tasks
from celery import chain, group, chord

# Sequential: validate → process → notify
workflow = chain(
    validate_order.s(order_id),
    process_payment.s(),
    send_confirmation.s(),
)
workflow.delay()

# Parallel: fetch stock + fetch user data simultaneously
parallel_fetch = group(
    fetch_stock_data.s(symbols),
    fetch_user_portfolio.s(user_id),
)
result = parallel_fetch.apply_async()

# chord: parallel tasks, then callback when all done
chord(
    group(resize_image.s(url) for url in image_urls)
)(save_processed_images.s(product_id))
```

</details>

---

## Asynchronous Processing Patterns

<details>
<summary><strong>5. How do you handle long-running tasks without blocking API responses?</strong></summary>

```python
# Pattern: Fire and forget + polling / webhook callback

# Step 1: Accept request, queue task, return task_id immediately
@app.post("/reports/generate", status_code=202)  # 202 Accepted
async def generate_report(
    params: ReportParams,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    # Store task status in Redis
    task_id = str(uuid.uuid4())
    await redis.setex(
        f"task:{task_id}",
        3600,
        json.dumps({"status": "queued", "progress": 0})
    )

    # Queue the heavy work
    generate_report_task.delay(task_id, params.dict(), current_user.id)

    return {
        "task_id": task_id,
        "status": "queued",
        "poll_url": f"/tasks/{task_id}",
    }

# Step 2: Client polls for status
@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    data = await redis.get(f"task:{task_id}")
    if not data:
        raise HTTPException(404, "Task not found")
    return json.loads(data)

# Step 3: Worker updates progress
@celery_app.task(bind=True)
def generate_report_task(self, task_id: str, params: dict, user_id: int):
    r = redis.Redis()

    def update_progress(progress: int, message: str):
        r.setex(f"task:{task_id}", 3600, json.dumps({
            "status": "processing",
            "progress": progress,
            "message": message,
        }))

    update_progress(10, "Fetching data...")
    data = fetch_report_data(params)

    update_progress(50, "Processing...")
    report = process_data(data)

    update_progress(80, "Generating PDF...")
    pdf_url = generate_pdf(report)

    # Final result
    r.setex(f"task:{task_id}", 3600, json.dumps({
        "status": "completed",
        "progress": 100,
        "result_url": pdf_url,
    }))

# Alternative: WebSocket for real-time progress
@app.websocket("/ws/tasks/{task_id}")
async def task_progress_ws(websocket: WebSocket, task_id: str):
    await websocket.accept()
    while True:
        data = await redis.get(f"task:{task_id}")
        if data:
            status = json.loads(data)
            await websocket.send_json(status)
            if status["status"] in ("completed", "failed"):
                break
        await asyncio.sleep(0.5)
    await websocket.close()
```

</details>

---

## Real-Time Data Handling

<details>
<summary><strong>6. How do you handle real-time data (e.g., live price feeds, order book updates)?</strong></summary>

```python
# Architecture for real-time data:
# Market Data Feed → Ingest Service → Redis (pub/sub + sorted sets) → WebSocket → Client

import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from redis.asyncio import Redis

app = FastAPI()

# Connection manager — track active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, list[WebSocket]] = {}  # symbol → [websockets]

    async def connect(self, symbol: str, ws: WebSocket):
        await ws.accept()
        self.connections.setdefault(symbol, []).append(ws)

    def disconnect(self, symbol: str, ws: WebSocket):
        self.connections.get(symbol, []).remove(ws)

    async def broadcast(self, symbol: str, message: dict):
        for ws in self.connections.get(symbol, []):
            try:
                await ws.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

# WebSocket endpoint — client subscribes to symbol price feed
@app.websocket("/ws/prices/{symbol}")
async def price_feed(websocket: WebSocket, symbol: str, redis: Redis = Depends(get_redis)):
    await manager.connect(symbol, websocket)
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"prices:{symbol}")

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])
    except WebSocketDisconnect:
        manager.disconnect(symbol, websocket)
    finally:
        await pubsub.unsubscribe(f"prices:{symbol}")

# Ingest service — receives market data, publishes to Redis
async def ingest_price_update(symbol: str, price: float, volume: int):
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    message = json.dumps({
        "symbol": symbol,
        "price": price,
        "volume": volume,
        "timestamp": time.time(),
    })

    # Publish to all subscribers
    await redis.publish(f"prices:{symbol}", message)

    # Store latest price (O(1) access)
    await redis.hset("latest_prices", symbol, price)

    # Store time-series in sorted set (score = timestamp)
    await redis.zadd(
        f"price_history:{symbol}",
        {message: time.time()}
    )
    # Keep only last 1000 price points
    await redis.zremrangebyrank(f"price_history:{symbol}", 0, -1001)

# Order book management with Redis sorted sets
class OrderBook:
    def __init__(self, redis: Redis, symbol: str):
        self.redis = redis
        self.symbol = symbol
        self.bids_key = f"orderbook:{symbol}:bids"
        self.asks_key = f"orderbook:{symbol}:asks"

    async def add_order(self, side: str, order_id: str, price: float):
        key = self.bids_key if side == "buy" else self.asks_key
        await self.redis.zadd(key, {order_id: price})

    async def remove_order(self, side: str, order_id: str):
        key = self.bids_key if side == "buy" else self.asks_key
        await self.redis.zrem(key, order_id)

    async def get_best_bid(self) -> float | None:
        result = await self.redis.zrevrange(self.bids_key, 0, 0, withscores=True)
        return result[0][1] if result else None

    async def get_best_ask(self) -> float | None:
        result = await self.redis.zrange(self.asks_key, 0, 0, withscores=True)
        return result[0][1] if result else None

    async def get_spread(self) -> float | None:
        bid = await self.get_best_bid()
        ask = await self.get_best_ask()
        if bid and ask:
            return ask - bid
        return None
```

</details>

---

## Scalable Backend Architecture

<details>
<summary><strong>7. How do you design a scalable backend for 100,000+ concurrent users?</strong></summary>

```
Architecture layers:

[CDN] → [Load Balancer]
              ↓
    [API Gateway] (rate limiting, auth, routing)
         ↓          ↓          ↓
  [FastAPI-1]  [FastAPI-2]  [FastAPI-3]   ← stateless, horizontally scalable
         ↓
  [Redis Cluster]   [PostgreSQL + Read Replicas]
         ↓
  [Celery Workers] → message queue for background jobs
         ↓
  [S3 / Object Storage]   [ElasticSearch for search]
```

```python
# Key patterns for scalability:

# 1. Stateless services — no server-side session state
# Sessions in Redis, not memory → any server can handle any request

# 2. Database read replicas — distribute read load
DATABASES = {
    "default": {"HOST": "postgres-primary"},   # writes
    "replica": {"HOST": "postgres-replica"},   # reads
}

# 3. Async all the way — don't block the event loop
@app.get("/portfolio")
async def get_portfolio(user_id: int):
    # Concurrent DB + cache + external API calls
    portfolio, prices, news = await asyncio.gather(
        get_user_portfolio_async(user_id),
        get_current_prices_from_cache(),
        get_market_news_async(),
    )
    return calculate_portfolio_value(portfolio, prices, news)

# 4. Caching at multiple levels
# L1: In-process (functools.lru_cache) — fastest, not distributed
# L2: Redis — fast, shared across all instances
# L3: CDN — for public API responses

from functools import lru_cache

@lru_cache(maxsize=100)
def get_static_config() -> dict:
    return db.query("SELECT * FROM config")   # loaded once per process

# 5. Database connection pooling — avoid connection exhaustion
# PgBouncer between FastAPI and PostgreSQL
# Configure: pool_mode = transaction, pool_size = 20

# 6. Pagination — never return unbounded results
@app.get("/orders/")
async def list_orders(
    cursor: str | None = None,   # cursor-based pagination (no page drift)
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    query = select(Order).order_by(Order.created_at.desc()).limit(limit + 1)
    if cursor:
        query = query.where(Order.created_at < decode_cursor(cursor))

    orders = (await db.execute(query)).scalars().all()
    has_next = len(orders) > limit
    orders = orders[:limit]

    return {
        "items": orders,
        "next_cursor": encode_cursor(orders[-1].created_at) if has_next else None,
    }

# 7. Background processing for non-critical work
# API: fast critical path only (~50ms)
# Celery: everything else (emails, reports, analytics, notifications)
```

</details>

---

## Fintech / Trading Concepts

<details>
<summary><strong>8. What fintech/trading concepts should you know for this interview?</strong></summary>

```python
# Key concepts — even without fintech experience, understand these

# 1. ORDER TYPES
class OrderType:
    MARKET = "market"      # buy/sell immediately at current price
    LIMIT = "limit"        # buy/sell at specific price or better
    STOP_LOSS = "stop"     # trigger market order when price hits threshold
    STOP_LIMIT = "stop_limit"  # trigger limit order when price hits threshold

# 2. ORDER BOOK — matching buyers and sellers
# Bids (buyers) sorted by price descending
# Asks (sellers) sorted by price ascending
# Best bid = highest buy order
# Best ask = lowest sell order
# Spread = best_ask - best_bid

# 3. HIGH FREQUENCY / REAL-TIME REQUIREMENTS
# - Price data changes every millisecond
# - Must handle bursts of data (market open/close, news events)
# - Latency critical — milliseconds matter

# 4. IDEMPOTENCY — critical for financial transactions
# Duplicate API calls must NOT create duplicate transactions
@app.post("/orders/")
async def create_order(
    order: OrderCreate,
    idempotency_key: str = Header(...),   # client provides unique key
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    # Check if this idempotency key was already processed
    existing = await redis.get(f"idem:{idempotency_key}")
    if existing:
        return json.loads(existing)   # return same response

    # Process once
    result = await OrderService.create(db, order)
    response = OrderResponse.from_orm(result).model_dump()

    # Store result for 24 hours
    await redis.setex(f"idem:{idempotency_key}", 86400, json.dumps(response))
    return response

# 5. AUDIT TRAIL — every financial transaction must be traceable
class OrderAuditLog(Base):
    __tablename__ = "order_audit_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(index=True)
    action: Mapped[str]           # created, filled, cancelled, modified
    old_values: Mapped[dict] = mapped_column(JSON)
    new_values: Mapped[dict] = mapped_column(JSON)
    actor_id: Mapped[int]         # who did this
    timestamp: Mapped[datetime]   # immutable, never update
    ip_address: Mapped[str]

# 6. DECIMAL PRECISION — never use float for money!
from decimal import Decimal

price = Decimal("182.50")   # exact
price_float = 182.50        # 182.4999999... — wrong for financial calc!

# PostgreSQL: NUMERIC(12, 4) — 12 digits, 4 decimal places
# SQLAlchemy: Numeric(12, 4)
# Pydantic: Decimal type

# 7. RATE AND THROUGHPUT — questions you'll be asked
# "How many trades can your system handle per second?"
# "What's your P99 latency for order creation?"
# Answer: instrument everything, use Prometheus + Grafana

import time
from prometheus_client import Histogram, Counter

order_latency = Histogram("order_creation_seconds", "Order creation latency")
order_count = Counter("orders_total", "Total orders", ["status"])

@app.post("/orders/")
async def create_order(order: OrderCreate):
    start = time.perf_counter()
    try:
        result = await OrderService.create(order)
        order_count.labels(status="success").inc()
        return result
    except Exception as e:
        order_count.labels(status="error").inc()
        raise
    finally:
        order_latency.observe(time.perf_counter() - start)
```

</details>

---

<details>
<summary><strong>9. What is eventual consistency? When is it acceptable in a trading/fintech context?</strong></summary>

```python
# Eventual consistency: all nodes will agree eventually, but may differ momentarily

# ACCEPTABLE (use caching/AP systems):
# - User profile data
# - Product catalog / stock descriptions
# - Historical reports
# - Notification history
# - Analytics dashboards (5-min delay is fine)

# NOT ACCEPTABLE (must use strong consistency / CP systems):
# - Account balance
# - Order status (placed → filled → settled)
# - Stock inventory / position limits
# - Trade execution records

# Pattern: strong consistency where it matters, eventual elsewhere

# Account balance — must be consistent (PostgreSQL + transaction)
@transaction.atomic
def execute_trade(user_id: int, symbol: str, qty: int, price: float):
    account = Account.objects.select_for_update().get(user_id=user_id)
    cost = Decimal(str(price * qty))

    if account.cash_balance < cost:
        raise InsufficientFundsError()

    account.cash_balance -= cost
    account.save(update_fields=["cash_balance"])

    Trade.objects.create(
        user_id=user_id, symbol=symbol, qty=qty, price=price,
        status="executed"
    )

# Portfolio view — eventually consistent (Redis cache, 30s TTL)
async def get_portfolio_value(user_id: int) -> Decimal:
    cache_key = f"portfolio_value:{user_id}"
    cached = await redis.get(cache_key)
    if cached:
        return Decimal(cached)   # may be 30s stale — acceptable

    value = await calculate_portfolio_from_db(user_id)
    await redis.setex(cache_key, 30, str(value))
    return value
```

</details>

---

## Scenario-Based Questions

<details>
<summary><strong>10. Design a backend for a real-time stock trading platform.</strong></summary>

```
High-level design:
┌─────────────────────────────────────────────────┐
│                  Clients (Web/Mobile)           │
└───────────────────────┬─────────────────────────┘
                        │ REST + WebSocket
┌───────────────────────▼─────────────────────────┐
│              API Gateway (FastAPI)              │
│  - JWT Auth    - Rate Limiting    - Routing     │
└──────┬────────────────┬────────────────┬────────┘
       │                │                │
  Orders API    Market Data WS    Portfolio API
       │                │                │
┌──────▼───────┐ ┌──────▼──────┐ ┌──────▼──────┐
│  Order       │ │  Price Feed │ │  Portfolio  │
│  Service     │ │  Service    │ │  Service    │
└──────┬───────┘ └──────┬──────┘ └──────┬──────┘
       │                │                │
┌──────▼────────────────▼────────────────▼──────┐
│                  Redis                        │
│  - Order queue  - Price pub/sub  - Sessions   │
│  - Rate limits  - Portfolio cache             │
└───────────────────────┬───────────────────────┘
                        │
┌───────────────────────▼───────────────────────┐
│               PostgreSQL                      │
│  - Orders (write-heavy, ACID)                 │
│  - Accounts (strong consistency)              │
│  - Audit logs (append-only)                   │
└───────────────────────────────────────────────┘
```

```python
# Key implementation decisions:

# 1. Order submission — synchronous for critical path, async for rest
@app.post("/orders/", response_model=OrderResponse, status_code=201)
async def submit_order(
    order: OrderCreateRequest,
    idempotency_key: str = Header(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    # Synchronous: validate + create order record (fast)
    async with db.begin():
        account = await db.execute(
            select(Account).where(Account.user_id == current_user.id).with_for_update()
        )
        # Validate funds, create order record
        db_order = await OrderRepo.create(db, order, current_user.id)

    # Async: send to matching engine, notify user (background)
    await redis.rpush("order_queue", json.dumps({"order_id": db_order.id}))
    await redis.publish(f"orders:{current_user.id}", json.dumps({
        "event": "order_submitted",
        "order_id": db_order.id,
        "status": "pending"
    }))
    return db_order

# 2. Matching engine (Celery worker)
@celery_app.task
def process_order(order_id: int):
    with transaction.atomic():
        order = Order.objects.select_for_update().get(pk=order_id)
        matched = find_matching_order(order)
        if matched:
            execute_trade(order, matched)
            order.status = "filled"
            matched.status = "filled"
            order.save()
            matched.save()
            publish_order_update(order.user_id, order_id, "filled")

# 3. Market data subscription via WebSocket
@app.websocket("/ws/market/{symbol}")
async def market_data(websocket: WebSocket, symbol: str):
    await websocket.accept()
    redis = Redis.from_url(settings.redis_url)
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"prices:{symbol}")

    # Send last known price immediately on connect
    last_price = await redis.hget("latest_prices", symbol)
    if last_price:
        await websocket.send_json({"symbol": symbol, "price": float(last_price)})

    async for message in pubsub.listen():
        if message["type"] == "message":
            await websocket.send_text(message["data"])
```

</details>

---

<details>
<summary><strong>11. How do you handle a spike in traffic — 10x normal load suddenly?</strong></summary>

```python
# Short-term (minutes):
# 1. Rate limiting activates — protect backend from overload
# 2. Cache absorbs most reads — Redis handles 100k+ req/sec
# 3. Queue backpressure — Celery queues tasks instead of dropping

# The rate limiting and caching layers should already be in place:

# Rate limiter cuts off abusive clients automatically
# Redis cache means most product/portfolio requests never hit PostgreSQL
# Celery queue absorbs burst of background tasks

# Medium-term (hours):
# 4. Horizontal scaling — add more FastAPI containers
# docker-compose scale web=8

# 5. DB read replicas — route reads to replicas
# 6. Increase Redis maxmemory (vertical scaling)

# Code-level resilience:
import asyncio
from fastapi import HTTPException

async def call_external_service(data: dict, timeout: float = 5.0) -> dict:
    try:
        async with asyncio.timeout(timeout):   # Python 3.11+
            return await external_api.call(data)
    except asyncio.TimeoutError:
        raise HTTPException(503, "Service temporarily unavailable")

# Circuit breaker — stop calling failing services
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failures = 0
        self.threshold = failure_threshold
        self.last_failure = None
        self.recovery_timeout = recovery_timeout

    def is_open(self) -> bool:
        if self.failures >= self.threshold:
            if time.time() - self.last_failure < self.recovery_timeout:
                return True   # circuit open — fail fast
            self.failures = 0   # reset after recovery window
        return False

    def record_failure(self):
        self.failures += 1
        self.last_failure = time.time()

cb = CircuitBreaker()

async def safe_external_call(data):
    if cb.is_open():
        return {"error": "Service unavailable", "cached": True}   # fallback
    try:
        result = await external_service.call(data)
        cb.failures = 0   # reset on success
        return result
    except Exception as e:
        cb.record_failure()
        raise
```

</details>
