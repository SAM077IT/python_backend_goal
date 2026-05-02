# FastAPI Interview Prep
> Focused on what this role needs: REST APIs, async, PostgreSQL integration, production patterns

---

## Table of Contents
- [FastAPI vs Django](#fastapi-vs-django)
- [Core FastAPI Concepts](#core-fastapi-concepts)
- [Pydantic & Validation](#pydantic--validation)
- [Dependency Injection](#dependency-injection)
- [Database with SQLAlchemy (Async)](#database-with-sqlalchemy-async)
- [Authentication & Security](#authentication--security)
- [Background Tasks & Async](#background-tasks--async)
- [Production Patterns](#production-patterns)
- [Scenario-Based Questions](#scenario-based-questions)

---

## FastAPI vs Django

<details>
<summary><strong>1. When do you choose FastAPI over Django? What are the tradeoffs?</strong></summary>

| | FastAPI | Django |
|---|---|---|
| **Speed** | Very fast (Starlette + Pydantic, async-native) | Slower (sync by default, WSGI) |
| **Async** | Native `async/await` throughout | Added in 3.1, not full-stack async |
| **Auto docs** | Built-in Swagger + ReDoc | Third-party (drf-spectacular) |
| **ORM** | Bring your own (SQLAlchemy, Tortoise) | Built-in (powerful) |
| **Admin** | None | Full-featured admin |
| **Validation** | Pydantic (fast, typed) | Serializers (verbose) |
| **Learning curve** | Low | Medium |
| **Best for** | High-throughput APIs, microservices, ML APIs | Full-stack apps, CMS, monoliths |

```python
# Same endpoint in both:

# Django DRF
class UserView(APIView):
    def get(self, request, user_id: int):
        user = get_object_or_404(User, pk=user_id)
        return Response(UserSerializer(user).data)

# FastAPI — less code, auto-validated, auto-documented
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

> 💡 **Your answer:** "I use FastAPI for microservices and high-throughput APIs — it's async-native and self-documenting. I use Django for full-stack apps where I need the admin, ORM, and built-in auth."

</details>

---

## Core FastAPI Concepts

<details>
<summary><strong>2. Explain FastAPI's request lifecycle and how routing works.</strong></summary>

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(
    title="Trading API",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc
)

# Middleware — runs around every request
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Response-Time"] = f"{duration:.4f}s"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path parameters — automatically validated and typed
@app.get("/users/{user_id}")
async def get_user(user_id: int):   # FastAPI auto-validates: int only
    return {"user_id": user_id}

# Query parameters — optional with defaults
@app.get("/products/")
async def list_products(
    page: int = 1,
    page_size: int = 20,
    category: str | None = None,
    min_price: float | None = None,
):
    return {"page": page, "filters": {"category": category, "min_price": min_price}}

# Multiple HTTP methods on same path
@app.get("/orders/{order_id}")
async def get_order(order_id: int): ...

@app.put("/orders/{order_id}")
async def update_order(order_id: int, data: OrderUpdate): ...

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int): ...

# Router — organise routes into modules
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

@router.get("/")
async def list_orders(): ...

@router.post("/")
async def create_order(): ...

app.include_router(router)
```

</details>

---

<details>
<summary><strong>3. What are response models and status codes in FastAPI?</strong></summary>

```python
from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderResponse(BaseModel):
    id: int
    user_id: int
    status: str
    total: float
    items: List[OrderItem]

    class Config:
        from_attributes = True   # read from ORM objects (SQLAlchemy)

class OrderCreate(BaseModel):
    items: List[OrderItem]

# response_model filters and validates the output
# Only fields in OrderResponse are returned — internal fields excluded
@app.post(
    "/orders/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
    description="Creates an order and returns full order details.",
)
async def create_order(payload: OrderCreate, db: AsyncSession = Depends(get_db)):
    order = await OrderService.create(db, payload)
    return order   # FastAPI serializes using OrderResponse

# Different response models per status
from fastapi.responses import JSONResponse

@app.post("/orders/", responses={
    201: {"model": OrderResponse},
    400: {"model": ErrorResponse},
    409: {"description": "Duplicate order"},
})
async def create_order(payload: OrderCreate): ...

# Exclude fields from response
class UserResponse(BaseModel):
    id: int
    email: str
    # password is NOT here — never exposed

class UserInDB(UserResponse):
    hashed_password: str   # internal only

@app.get("/users/me", response_model=UserResponse)  # hashed_password filtered out
async def get_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user
```

</details>

---

## Pydantic & Validation

<details>
<summary><strong>4. How do you use Pydantic for data validation in FastAPI?</strong></summary>

```python
from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr
from decimal import Decimal
from datetime import datetime
from typing import Literal

class OrderCreateRequest(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=10, example="AAPL")
    side: Literal["buy", "sell"]
    quantity: int = Field(..., gt=0, le=10000, description="Number of shares")
    price: Decimal = Field(..., gt=0, decimal_places=2)
    order_type: Literal["market", "limit", "stop_limit"] = "limit"
    notes: str | None = Field(None, max_length=500)

    # Field-level validator
    @field_validator("symbol")
    @classmethod
    def symbol_must_be_uppercase(cls, v: str) -> str:
        return v.upper().strip()

    @field_validator("price")
    @classmethod
    def price_precision(cls, v: Decimal) -> Decimal:
        if v.as_tuple().exponent < -2:
            raise ValueError("Price cannot have more than 2 decimal places")
        return v

    # Cross-field validator
    @model_validator(mode="after")
    def validate_limit_price(self) -> "OrderCreateRequest":
        if self.order_type == "limit" and self.price is None:
            raise ValueError("Limit orders require a price")
        if self.order_type == "market" and self.price is not None:
            raise ValueError("Market orders should not have a price")
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "side": "buy",
                "quantity": 100,
                "price": "182.50",
                "order_type": "limit"
            }
        }

# Usage — FastAPI auto-validates and returns 422 on error
@app.post("/orders/")
async def create_order(order: OrderCreateRequest):
    # If we get here, data is guaranteed valid
    return await place_order(order)

# Nested models
class Address(BaseModel):
    street: str
    city: str
    pincode: str = Field(..., pattern=r"^\d{6}$")

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    address: Address   # nested — auto-validated recursively
    password: str = Field(..., min_length=8)

# Settings with pydantic-settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    debug: bool = False
    allowed_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()   # reads from env, validates types
```

</details>

---

## Dependency Injection

<details>
<summary><strong>5. How does FastAPI's dependency injection work? Show real examples.</strong></summary>

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

# 1. Database session dependency — injected per request
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# 2. Auth dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id: int = payload.get("user_id")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 3. Role-based dependency
def require_role(*roles: str):
    async def check_role(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return check_role

# 4. Pagination dependency — reusable across endpoints
class PaginationParams:
    def __init__(self, page: int = 1, page_size: int = 20):
        if page < 1:
            raise HTTPException(400, "page must be >= 1")
        if page_size > 100:
            raise HTTPException(400, "page_size cannot exceed 100")
        self.page = page
        self.page_size = page_size
        self.offset = (page - 1) * page_size

# Compose dependencies
@app.get("/orders/")
async def list_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: PaginationParams = Depends(),
):
    orders = await OrderRepo.get_by_user(
        db, current_user.id,
        offset=pagination.offset,
        limit=pagination.page_size
    )
    return orders

@app.delete("/orders/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_role("admin", "manager")),  # only admin/manager
):
    await OrderRepo.delete(db, order_id)
    return {"deleted": order_id}

# 5. Rate limiter dependency
from fastapi import Request
from redis.asyncio import Redis

async def get_redis() -> Redis:
    yield app.state.redis   # stored on app startup

async def rate_limit(
    request: Request,
    redis: Redis = Depends(get_redis),
    limit: int = 60,
    window: int = 60,
):
    key = f"rate:{request.client.host}:{request.url.path}"
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, window)
    if current > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
```

</details>

---

## Database with SQLAlchemy (Async)

<details>
<summary><strong>6. How do you use async SQLAlchemy with FastAPI and PostgreSQL?</strong></summary>

```python
# pip install sqlalchemy[asyncio] asyncpg alembic

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, ForeignKey, Enum as SAEnum
from sqlalchemy import select, update, delete
from datetime import datetime
import enum

# Engine
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"
engine = create_async_engine(
    DATABASE_URL,
    echo=False,                 # set True to log SQL
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,         # verify connection health
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Base model
class Base(DeclarativeBase):
    pass

# Models with typed mapped_column (SQLAlchemy 2.0 style)
class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    symbol: Mapped[str] = mapped_column(String(10))
    quantity: Mapped[int]
    price: Mapped[float] = mapped_column(Numeric(12, 4))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="orders", lazy="selectin")

# Repository pattern — clean, testable
class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, order_id: int) -> Order | None:
        return await self.session.get(Order, order_id)

    async def list_by_user(
        self, user_id: int, offset: int = 0, limit: int = 20
    ) -> list[Order]:
        result = await self.session.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, data: dict) -> Order:
        order = Order(**data)
        self.session.add(order)
        await self.session.flush()   # get ID without committing
        return order

    async def update_status(self, order_id: int, status: OrderStatus) -> int:
        result = await self.session.execute(
            update(Order)
            .where(Order.id == order_id)
            .values(status=status)
            .returning(Order.id)
        )
        return result.scalar_one_or_none()

    async def bulk_insert(self, orders: list[dict]) -> None:
        self.session.add_all([Order(**o) for o in orders])

# In endpoint
@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    repo = OrderRepository(db)
    order = await repo.get(order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    return order

# Alembic migrations — same as Django but manual
# alembic init alembic
# alembic revision --autogenerate -m "add orders table"
# alembic upgrade head
```

</details>

---

## Authentication & Security

<details>
<summary><strong>7. Implement JWT auth in FastAPI from scratch.</strong></summary>

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

def create_access_token(user_id: int, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "type": "access",
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Login endpoint
@app.post("/auth/token", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await UserRepo.get_by_email(db, form.username)
    if not user or not pwd_context.verify(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return TokenResponse(
        access_token=create_access_token(user.id, user.role),
        refresh_token=create_refresh_token(user.id),
    )

# Token refresh
@app.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise ValueError()
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(401, "Invalid refresh token")

    user = await db.get(User, payload["user_id"])
    return TokenResponse(
        access_token=create_access_token(user.id, user.role),
        refresh_token=create_refresh_token(user.id),
    )

# Protected route
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise jwt.InvalidTokenError()
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    user = await db.get(User, payload["user_id"])
    if not user:
        raise HTTPException(401, "User not found")
    return user

@app.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

</details>

---

## Background Tasks & Async

<details>
<summary><strong>8. How do you run background tasks in FastAPI?</strong></summary>

```python
from fastapi import BackgroundTasks
from celery import Celery
import asyncio

# Method 1: FastAPI BackgroundTasks — simple, in-process, no queue
@app.post("/orders/", response_model=OrderResponse)
async def create_order(
    payload: OrderCreateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = await OrderRepo.create(db, payload, current_user.id)

    # Runs after response is sent — non-blocking for client
    background_tasks.add_task(send_order_confirmation, order.id, current_user.email)
    background_tasks.add_task(update_portfolio_stats, current_user.id)

    return order

async def send_order_confirmation(order_id: int, email: str):
    # Runs async in background
    await email_client.send(to=email, subject=f"Order #{order_id} confirmed")

# Method 2: Celery — production grade, distributed, retryable
celery = Celery("app", broker=settings.redis_url, backend=settings.redis_url)

@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def process_order_async(self, order_id: int):
    try:
        # Long-running work in separate process
        order = Order.objects.get(pk=order_id)
        result = exchange_api.execute(order)
        order.status = "filled"
        order.save()
    except Exception as exc:
        raise self.retry(exc=exc)

# Trigger from FastAPI
@app.post("/orders/")
async def create_order(payload: OrderCreateRequest):
    order = await OrderRepo.create(db, payload)
    process_order_async.delay(order.id)   # fire and forget
    return order

# Method 3: asyncio tasks — for async I/O concurrent operations
@app.post("/portfolio/refresh")
async def refresh_portfolio(current_user: User = Depends(get_current_user)):
    # Fetch from multiple sources concurrently
    stocks, crypto, bonds = await asyncio.gather(
        fetch_stock_prices(current_user.holdings),
        fetch_crypto_prices(current_user.crypto),
        fetch_bond_prices(current_user.bonds),
    )
    portfolio = calculate_portfolio(stocks, crypto, bonds)
    return portfolio

# WebSocket for real-time updates
from fastapi import WebSocket

@app.websocket("/ws/prices/{symbol}")
async def price_feed(websocket: WebSocket, symbol: str):
    await websocket.accept()
    try:
        while True:
            price = await get_latest_price(symbol)   # from Redis or market feed
            await websocket.send_json({"symbol": symbol, "price": price})
            await asyncio.sleep(1)   # push every second
    except Exception:
        await websocket.close()
```

</details>

---

## Production Patterns

<details>
<summary><strong>9. How do you structure a production FastAPI application?</strong></summary>

```
app/
├── main.py              # app factory, middleware, routers
├── config.py            # pydantic settings
├── dependencies.py      # shared dependencies (db, auth, redis)
├── models/
│   ├── user.py
│   └── order.py         # SQLAlchemy models
├── schemas/
│   ├── user.py
│   └── order.py         # Pydantic request/response schemas
├── repositories/
│   ├── user.py
│   └── order.py         # DB access layer
├── services/
│   └── order_service.py # business logic
├── routers/
│   ├── auth.py
│   ├── orders.py
│   └── users.py
└── core/
    ├── security.py
    └── exceptions.py
```

```python
# main.py — app factory
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.redis = await create_redis_pool(settings.redis_url)
    await create_db_tables()
    yield
    # Shutdown
    await app.state.redis.close()
    await engine.dispose()

app = FastAPI(
    title="Trading API",
    version="1.0.0",
    lifespan=lifespan,
)

# Global exception handler — clean error responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import logging
    logging.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc) if settings.debug else None},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status": exc.status_code},
    )

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(order_router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])

# Health check endpoint — required for Docker/K8s
@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
```

```dockerfile
# Dockerfile for FastAPI
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app",
     "--host", "0.0.0.0",
     "--port", "8000",
     "--workers", "4",
     "--loop", "uvloop",
     "--http", "httptools"]
```

```bash
# requirements.txt — key packages
fastapi==0.111.0
uvicorn[standard]==0.29.0      # includes uvloop + httptools
sqlalchemy[asyncio]==2.0.30
asyncpg==0.29.0               # async PostgreSQL driver
pydantic[email]==2.7.0
pydantic-settings==2.2.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
redis[asyncio]==5.0.4
celery==5.4.0
alembic==1.13.1
```

</details>

---

## Scenario-Based Questions

<details>
<summary><strong>10. How do you handle high-throughput in a FastAPI service — e.g., 10,000 requests/second?</strong></summary>

```python
# 1. Async everything — no blocking calls in async context
# WRONG — blocks the event loop!
@app.get("/slow")
async def slow_endpoint():
    time.sleep(2)   # blocks entire event loop
    return {}

# RIGHT — use asyncio.sleep or run blocking code in thread pool
import asyncio
from fastapi.concurrency import run_in_threadpool

@app.get("/right")
async def right_endpoint():
    await asyncio.sleep(2)   # non-blocking
    result = await run_in_threadpool(blocking_cpu_work, data)
    return result

# 2. Connection pooling — reuse DB and Redis connections
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,        # connections always ready
    max_overflow=40,     # burst capacity
    pool_timeout=30,
    pool_pre_ping=True,
)

# 3. Redis for caching hot data
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

    product = await ProductRepo.get(db, product_id)
    await redis.setex(cache_key, 300, json.dumps(product.dict()))
    return product

# 4. Multiple Uvicorn workers (process-level parallelism)
# uvicorn app.main:app --workers 4 --loop uvloop

# 5. Batch DB operations instead of row-by-row
@app.post("/orders/bulk")
async def bulk_create_orders(
    orders: list[OrderCreateRequest],
    db: AsyncSession = Depends(get_db),
):
    db_orders = [Order(**o.model_dump()) for o in orders]
    db.add_all(db_orders)
    await db.commit()
    return {"created": len(db_orders)}

# 6. Concurrency with asyncio.gather
@app.get("/dashboard")
async def dashboard(current_user: User = Depends(get_current_user)):
    orders, portfolio, notifications = await asyncio.gather(
        OrderRepo.get_recent(current_user.id, limit=5),
        PortfolioService.get_summary(current_user.id),
        NotificationRepo.get_unread(current_user.id),
    )
    return {"orders": orders, "portfolio": portfolio, "notifications": notifications}
```

</details>

---

<details>
<summary><strong>11. How do you test a FastAPI application?</strong></summary>

```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.dependencies import get_db

# Use an in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncTestSession = async_sessionmaker(engine)
    async with AsyncTestSession() as session:
        yield session
    await engine.dispose()

@pytest.fixture
async def client(db_session: AsyncSession):
    # Override DB dependency with test DB
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_order(client: AsyncClient):
    # Login first
    login_resp = await client.post("/auth/token", data={
        "username": "test@example.com",
        "password": "testpass",
    })
    token = login_resp.json()["access_token"]

    # Create order
    response = await client.post(
        "/api/v1/orders/",
        json={"symbol": "AAPL", "side": "buy", "quantity": 10, "price": "182.50"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_invalid_quantity_returns_422(client: AsyncClient):
    response = await client.post(
        "/api/v1/orders/",
        json={"symbol": "AAPL", "side": "buy", "quantity": -1},   # invalid!
    )
    assert response.status_code == 422
    assert "quantity" in response.text
```

</details>
