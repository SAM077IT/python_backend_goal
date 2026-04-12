# Python Interview Prep — Backend Developer (3+ Years)
> Tailored to your resume: Django, FastAPI, REST APIs, Microservices, PostgreSQL, AWS, Docker

---

## Table of Contents
- [OOP & Design Principles](#oop--design-principles)
- [Functions, Decorators & Closures](#functions-decorators--closures)
- [Concurrency & Async](#concurrency--async)
- [Memory & Performance](#memory--performance)
- [Data Structures & Algorithms](#data-structures--algorithms)
- [Error Handling & Logging](#error-handling--logging)
- [Testing](#testing)
- [Python in Production](#python-in-production)

---

## OOP & Design Principles

<details>
<summary><strong>1. You mentioned OOP principles in your resume. Walk me through how you applied them in your Django/FastAPI projects.</strong></summary>

### Answer

In backend projects, OOP principles map directly to maintainable, scalable code:

**Encapsulation** — wrapping data + behavior together, hiding internals:
```python
class OrderService:
    def __init__(self, db_session, email_client):
        self._db = db_session           # private — callers don't touch DB directly
        self._email = email_client

    def place_order(self, user_id: int, items: list) -> 'Order':
        order = self._create_order(user_id, items)
        self._db.add(order)
        self._db.commit()
        self._email.send_confirmation(order)
        return order

    def _create_order(self, user_id, items):   # private helper
        total = sum(item.price for item in items)
        return Order(user_id=user_id, items=items, total=total)
```

**Inheritance** — reusing shared behavior:
```python
class BaseAPIView(View):
    def dispatch(self, request, *args, **kwargs):
        # Common auth check for all child views
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return super().dispatch(request, *args, **kwargs)

class OrderView(BaseAPIView):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        return JsonResponse(order.to_dict())
```

**Polymorphism** — different classes, same interface:
```python
class EmailNotifier:
    def send(self, user, message): ...

class SMSNotifier:
    def send(self, user, message): ...

class PushNotifier:
    def send(self, user, message): ...

def notify_user(notifier, user, message):
    notifier.send(user, message)   # works with any notifier
```

**Abstraction** — hiding complexity behind clean interfaces:
```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, token: str) -> dict: ...

    @abstractmethod
    def refund(self, transaction_id: str) -> bool: ...

class StripeGateway(PaymentGateway):
    def charge(self, amount, token):
        return stripe.PaymentIntent.create(amount=amount, payment_method=token)

    def refund(self, transaction_id):
        return stripe.Refund.create(payment_intent=transaction_id)
```

> 💡 **Interview tip:** Be ready to walk through a real project example. In Martify, you likely used OOP for model design, service layers, and cart logic. Tie your answer to actual code you wrote.

</details>

---

<details>
<summary><strong>2. What are SOLID principles? Give a Python backend example for each.</strong></summary>

### Answer

```python
# S — Single Responsibility Principle
# One class = one reason to change

# BAD
class UserManager:
    def create_user(self, data): ...
    def send_welcome_email(self, user): ...   # email is not user management!
    def generate_pdf_report(self): ...        # reporting is not user management!

# GOOD
class UserService:
    def create_user(self, data): ...

class EmailService:
    def send_welcome_email(self, user): ...

# O — Open/Closed Principle
# Open for extension, closed for modification

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float: ...

class NoDiscount(DiscountStrategy):
    def apply(self, price): return price

class PercentDiscount(DiscountStrategy):
    def __init__(self, percent): self.percent = percent
    def apply(self, price): return price * (1 - self.percent / 100)

class Order:
    def __init__(self, price, discount: DiscountStrategy):
        self.total = discount.apply(price)
# Add new discounts without touching Order class

# L — Liskov Substitution
# Subclass must be usable wherever parent is expected

class Storage(ABC):
    @abstractmethod
    def save(self, key, data): ...
    @abstractmethod
    def load(self, key): ...

class S3Storage(Storage):
    def save(self, key, data): s3.put_object(Key=key, Body=data)
    def load(self, key): return s3.get_object(Key=key)['Body'].read()

class RedisStorage(Storage):
    def save(self, key, data): redis.set(key, data)
    def load(self, key): return redis.get(key)

# Both are interchangeable — LSP satisfied

# I — Interface Segregation
# Don't force clients to implement unused methods

# BAD
class ReportInterface(ABC):
    @abstractmethod
    def generate_pdf(self): ...
    @abstractmethod
    def generate_csv(self): ...
    @abstractmethod
    def send_email(self): ...   # not every report needs email!

# GOOD — smaller interfaces
class PDFReport(ABC):
    @abstractmethod
    def generate_pdf(self): ...

class EmailableReport(ABC):
    @abstractmethod
    def send_email(self): ...

# D — Dependency Inversion
# Depend on abstractions, not concretions

# BAD
class OrderService:
    def __init__(self):
        self.db = PostgreSQLDB()   # tightly coupled to PostgreSQL

# GOOD — inject dependency
class OrderService:
    def __init__(self, db: DatabaseInterface):
        self.db = db   # works with any DB that implements the interface
```

</details>

---

<details>
<summary><strong>3. What is the difference between @classmethod, @staticmethod, and instance methods? Where did you use them?</strong></summary>

### Answer

```python
class Order:
    TAX_RATE = 0.18    # class variable

    def __init__(self, amount, user_id):
        self.amount = amount
        self.user_id = user_id

    # Instance method — has access to self (instance state)
    def total_with_tax(self):
        return self.amount * (1 + self.TAX_RATE)

    def to_dict(self):
        return {"amount": self.amount, "user_id": self.user_id}

    # Class method — has access to cls (class itself), not instance
    # Use for: alternative constructors, factory methods
    @classmethod
    def from_dict(cls, data: dict) -> 'Order':
        return cls(amount=data['amount'], user_id=data['user_id'])

    @classmethod
    def from_request(cls, request) -> 'Order':
        return cls(
            amount=request.POST.get('amount'),
            user_id=request.user.id
        )

    # Static method — no access to self or cls
    # Use for: utility functions logically related to the class
    @staticmethod
    def validate_amount(amount: float) -> bool:
        return isinstance(amount, (int, float)) and amount > 0

    @staticmethod
    def calculate_tax(amount: float) -> float:
        return amount * 0.18


# Usage
order = Order.from_dict({"amount": 500, "user_id": 1})   # classmethod
Order.validate_amount(500)                                  # staticmethod — no instance needed
order.total_with_tax()                                      # instance method
```

> 💡 **Real use case from resume:** In Martify's cart/order system, `from_request()` is a clean classmethod for creating orders from POST data. `validate_amount()` is a staticmethod for reusable validation logic.

</details>

---

<details>
<summary><strong>4. Explain MRO (Method Resolution Order) and how Python resolves multiple inheritance.</strong></summary>

### Answer

Python uses the **C3 linearization algorithm** to determine MRO. The order is: current class → left parent → right parent → their parents.

```python
class Timestamped:
    def save(self):
        self.updated_at = datetime.now()
        print("Timestamped.save()")

class SoftDelete:
    def save(self):
        self.is_deleted = False
        print("SoftDelete.save()")

class AuditLog:
    def save(self):
        log_action("save")
        print("AuditLog.save()")

class UserProfile(Timestamped, SoftDelete, AuditLog):
    def save(self):
        super().save()   # follows MRO
        print("UserProfile.save()")

print(UserProfile.__mro__)
# (UserProfile, Timestamped, SoftDelete, AuditLog, object)

up = UserProfile()
up.save()
# UserProfile.save()
# Timestamped.save()  ← super() picks next in MRO
# SoftDelete.save()
# AuditLog.save()

# Practical backend use with Django
class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    class Meta:
        abstract = True

class Order(TimestampMixin, SoftDeleteMixin):
    # inherits both mixins — MRO handles method resolution
    pass
```

</details>

---

## Functions, Decorators & Closures

<details>
<summary><strong>5. You use JWT auth in your projects. How would you implement a custom authentication decorator in Python?</strong></summary>

### Answer

```python
import functools
import jwt
from django.http import JsonResponse

SECRET_KEY = "your-secret-key"

def require_jwt(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Missing or invalid token"}, status=401)

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = payload["user_id"]
            request.role = payload.get("role", "user")
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        return func(request, *args, **kwargs)
    return wrapper

# RBAC decorator
def require_role(*roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if not hasattr(request, 'role') or request.role not in roles:
                return JsonResponse({"error": "Insufficient permissions"}, status=403)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

# Usage — stacking decorators
@require_jwt
@require_role("admin", "manager")
def delete_user(request, user_id):
    User.objects.filter(pk=user_id).delete()
    return JsonResponse({"status": "deleted"})
```

</details>

---

<details>
<summary><strong>6. Explain closures and how Python's decorator pattern uses them. Write a retry decorator with exponential backoff.</strong></summary>

### Answer

```python
import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts=3, base_delay=1.0, backoff=2.0,
          exceptions=(Exception,), on_retry=None):
    """
    Decorator with exponential backoff + jitter.
    Used for AWS calls, external API calls, DB connections.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    if attempt == max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {exc}"
                        )
                        raise

                    if on_retry:
                        on_retry(attempt, exc)

                    jitter = delay * 0.1 * (2 * __import__('random').random() - 1)
                    sleep_time = delay + jitter
                    logger.warning(
                        f"{func.__name__} attempt {attempt} failed. "
                        f"Retrying in {sleep_time:.2f}s. Error: {exc}"
                    )
                    time.sleep(sleep_time)
                    delay *= backoff   # exponential: 1s, 2s, 4s, 8s...

        return wrapper
    return decorator

# Usage — AWS S3, external APIs
@retry(max_attempts=3, base_delay=1.0, exceptions=(ConnectionError, TimeoutError))
def upload_to_s3(file_path, bucket, key):
    s3_client.upload_file(file_path, bucket, key)

@retry(max_attempts=5, base_delay=0.5, backoff=2.0)
def send_email_notification(to, subject, body):
    ses_client.send_email(...)
```

> 💡 **Closure explanation:** The `decorator` function "closes over" `max_attempts`, `base_delay`, and `backoff` from its enclosing `retry` scope — even after `retry()` has returned. This is why each decorated function has its own retry configuration.

</details>

---

<details>
<summary><strong>7. What is a generator and how would you use it in a backend context (e.g., processing large DB results)?</strong></summary>

### Answer

```python
# Problem: fetching 100,000 orders from DB — don't load all into memory
# Bad:
orders = Order.objects.all()   # loads everything into RAM!
for order in orders:
    process(order)

# Good: Generator approach
def iter_orders_in_batches(batch_size=1000):
    offset = 0
    while True:
        batch = Order.objects.filter(
            status='pending'
        ).order_by('id')[offset:offset + batch_size]

        if not batch:
            break

        for order in batch:
            yield order

        offset += batch_size

# Memory-efficient processing
for order in iter_orders_in_batches(batch_size=500):
    send_reminder_email(order)

# Generator pipeline for ETL tasks
def read_csv_lines(filepath):
    with open(filepath, encoding='utf-8') as f:
        next(f)   # skip header
        for line in f:
            yield line.strip()

def parse_row(lines):
    for line in lines:
        parts = line.split(',')
        yield {
            'name': parts[0].strip(),
            'email': parts[1].strip(),
            'amount': float(parts[2])
        }

def filter_valid(rows):
    for row in rows:
        if '@' in row['email'] and row['amount'] > 0:
            yield row

# Compose pipeline — no intermediate lists
lines = read_csv_lines('orders.csv')
rows = parse_row(lines)
valid = filter_valid(rows)

for record in valid:
    Order.objects.create(**record)

# Django's iterator() — same idea, built-in
for order in Order.objects.filter(status='pending').iterator(chunk_size=500):
    process(order)
```

</details>

---

## Concurrency & Async

<details>
<summary><strong>8. When would you use asyncio vs threading vs multiprocessing in a backend application?</strong></summary>

### Answer

| Scenario | Use | Why |
|---|---|---|
| 1000+ concurrent HTTP calls to external APIs | `asyncio` | I/O-bound, event loop handles all concurrently |
| Reading/writing to S3, sending emails | `asyncio` or `threading` | I/O-bound, GIL released during I/O |
| Image resizing, PDF generation | `multiprocessing` | CPU-bound, needs true parallelism |
| Running Django with sync ORM | `threading` (Celery workers) | Can't use asyncio with sync ORM easily |
| Background jobs (reports, emails) | Celery + Redis | Production-grade task queue |

```python
# asyncio — 1000 concurrent API calls
import asyncio
import aiohttp

async def fetch_product_data(session, product_id):
    url = f"https://supplier-api.com/products/{product_id}"
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
        return await resp.json()

async def sync_all_products(product_ids):
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(50)  # limit to 50 concurrent

        async def bounded_fetch(pid):
            async with semaphore:
                return await fetch_product_data(session, pid)

        return await asyncio.gather(
            *[bounded_fetch(pid) for pid in product_ids],
            return_exceptions=True
        )

# multiprocessing — CPU-bound (image processing)
from concurrent.futures import ProcessPoolExecutor
from PIL import Image

def resize_image(args):
    path, size = args
    img = Image.open(path)
    img.thumbnail(size)
    img.save(path.replace('.jpg', '_thumb.jpg'))

with ProcessPoolExecutor(max_workers=4) as executor:
    executor.map(resize_image, [(p, (200, 200)) for p in image_paths])
```

> 💡 **From your resume:** You use CI/CD and Docker — mention that Celery workers handle background tasks, and async views (FastAPI/Django ASGI) handle high-concurrency endpoints.

</details>

---

<details>
<summary><strong>9. Explain the GIL. How does it affect your backend applications and how do you work around it?</strong></summary>

### Answer

The **Global Interpreter Lock (GIL)** is a mutex in CPython that allows only one thread to execute Python bytecode at a time — even on multi-core machines.

**Impact on backends:**

```python
# GIL does NOT hurt I/O-bound threading
# When a thread waits for network/disk, it releases the GIL
# So threads work well for: DB queries, HTTP calls, file I/O

import threading
import requests

results = []
lock = threading.Lock()

def fetch(url):
    r = requests.get(url)    # GIL released during network wait
    with lock:
        results.append(r.json())

threads = [threading.Thread(target=fetch, args=(url,)) for url in urls]
for t in threads: t.start()
for t in threads: t.join()

# GIL DOES hurt CPU-bound threading
# Image processing, data crunching — threads compete for GIL, no speedup

# Workarounds:
# 1. multiprocessing — separate processes, each has its own GIL
from multiprocessing import Pool
with Pool(4) as p:
    results = p.map(cpu_heavy_task, data)

# 2. Celery — distribute CPU tasks across worker processes
@celery_app.task
def generate_report(data):
    # runs in separate worker process
    return process_data(data)

# 3. NumPy/Pandas — C extensions release GIL for their operations
# 4. PyPy — no GIL restrictions for certain workloads

# In production (from your resume):
# Gunicorn with multiple workers = multiple processes = no GIL conflict
# gunicorn --workers 4 myapp.wsgi:application
```

</details>

---

## Memory & Performance

<details>
<summary><strong>10. You mentioned optimizing PostgreSQL queries and improving performance by 35%. How do you profile and optimize Python code?</strong></summary>

### Answer

```python
# Step 1: Identify the bottleneck — profile first, optimize second

# cProfile — function-level profiling
import cProfile
import pstats
import io

def profile_view():
    pr = cProfile.Profile()
    pr.enable()

    # ... run the slow code ...
    result = slow_api_function()

    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(20)
    print(s.getvalue())

# Django Debug Toolbar — visual query profiler in browser
# Shows: SQL queries, query time, duplicate queries, cache hits

# django-silk — production profiling middleware
MIDDLEWARE = ['silk.middleware.SilkyMiddleware']

# Step 2: Common Python optimizations

# Use built-ins (C-implemented, faster than pure Python)
# Slow:
total = 0
for x in numbers:
    total += x
# Fast:
total = sum(numbers)

# Use list comprehension over manual append
# Slow:
result = []
for x in data:
    if x > 0:
        result.append(x * 2)
# Fast:
result = [x * 2 for x in data if x > 0]

# Avoid repeated attribute lookup in loops
# Slow:
for i in range(len(items)):
    items[i].process()
    items[i].save()

# Fast:
for item in items:
    process = item.process   # cache attribute lookup
    process()
    item.save()

# Use sets for membership testing (O(1) vs O(n))
valid_statuses = {'pending', 'active', 'completed'}   # set
if order.status in valid_statuses:   # O(1) lookup
    pass

# Step 3: DB-level optimizations (see databases .md for full coverage)
# - select_related / prefetch_related
# - .only() / .defer()
# - Add indexes
# - Use .values() for read-only queries
```

</details>

---

## Data Structures & Algorithms

<details>
<summary><strong>11. What data structures from Python's standard library do you use in backend development?</strong></summary>

### Answer

```python
from collections import defaultdict, Counter, deque, OrderedDict
import heapq

# defaultdict — grouping query results
def group_orders_by_status(orders):
    grouped = defaultdict(list)
    for order in orders:
        grouped[order.status].append(order.id)
    return dict(grouped)

# Counter — analytics dashboard (your Micro-data analyst project)
def get_top_products(orders, n=10):
    product_counts = Counter()
    for order in orders:
        for item in order.items:
            product_counts[item.product_id] += item.quantity
    return product_counts.most_common(n)

# deque — rate limiting (fixed-size sliding window)
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls, period_seconds):
        self.max_calls = max_calls
        self.period = timedelta(seconds=period_seconds)
        self.calls = deque()

    def is_allowed(self) -> bool:
        now = datetime.utcnow()
        # Remove old calls outside the window
        while self.calls and now - self.calls[0] > self.period:
            self.calls.popleft()
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

# heapq — priority queue for task scheduling
import heapq
from dataclasses import dataclass, field

@dataclass(order=True)
class Task:
    priority: int
    name: str = field(compare=False)

task_queue = []
heapq.heappush(task_queue, Task(1, "send_invoice"))
heapq.heappush(task_queue, Task(3, "generate_report"))
heapq.heappush(task_queue, Task(2, "send_notification"))

while task_queue:
    task = heapq.heappop(task_queue)
    print(f"Processing: {task.name}")
# send_invoice → send_notification → generate_report
```

</details>

---

## Error Handling & Logging

<details>
<summary><strong>12. How do you implement structured logging in a Python backend application?</strong></summary>

### Answer

```python
# settings.py — structured logging config
import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        },
        'verbose': {
            'format': '{asctime} {levelname} {module} {process:d} {thread:d} {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10 * 1024 * 1024,   # 10MB
            'backupCount': 5,
            'formatter': 'json',
        },
    },
    'root': {'handlers': ['console', 'file'], 'level': 'INFO'},
    'loggers': {
        'django.db.backends': {'level': 'WARNING'},  # suppress SQL logs in prod
        'myapp': {'level': 'DEBUG', 'propagate': True},
    }
}

# Usage in views/services
import logging
logger = logging.getLogger(__name__)

def process_payment(order_id, amount):
    logger.info(
        "Payment initiated",
        extra={"order_id": order_id, "amount": amount, "currency": "INR"}
    )
    try:
        result = payment_gateway.charge(amount)
        logger.info("Payment successful", extra={"transaction_id": result['id']})
        return result
    except PaymentError as e:
        logger.error(
            "Payment failed",
            exc_info=True,
            extra={"order_id": order_id, "error_code": e.code}
        )
        raise

# Middleware for request logging
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('requests')

    def __call__(self, request):
        import time
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start) * 1000

        self.logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "user_id": getattr(request.user, 'id', None),
            }
        )
        return response
```

</details>

---

## Testing

<details>
<summary><strong>13. How do you write unit tests for a Python backend service? Mock external dependencies.</strong></summary>

### Answer

```python
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from decimal import Decimal

# Service under test
class PaymentService:
    def __init__(self, payment_gateway, order_repo, email_service):
        self.gateway = payment_gateway
        self.orders = order_repo
        self.email = email_service

    def process_payment(self, order_id: int, card_token: str):
        order = self.orders.get(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")

        result = self.gateway.charge(order.total, card_token)
        order.status = 'paid'
        order.transaction_id = result['id']
        self.orders.save(order)
        self.email.send_receipt(order)
        return result

# Tests
class TestPaymentService:
    def setup_method(self):
        self.mock_gateway = MagicMock()
        self.mock_orders = MagicMock()
        self.mock_email = MagicMock()

        self.service = PaymentService(
            self.mock_gateway,
            self.mock_orders,
            self.mock_email
        )

    def test_successful_payment(self):
        # Arrange
        mock_order = MagicMock()
        mock_order.total = Decimal('999.00')
        self.mock_orders.get.return_value = mock_order
        self.mock_gateway.charge.return_value = {'id': 'txn_123', 'status': 'success'}

        # Act
        result = self.service.process_payment(1, 'tok_valid')

        # Assert
        self.mock_gateway.charge.assert_called_once_with(Decimal('999.00'), 'tok_valid')
        assert mock_order.status == 'paid'
        assert mock_order.transaction_id == 'txn_123'
        self.mock_orders.save.assert_called_once_with(mock_order)
        self.mock_email.send_receipt.assert_called_once_with(mock_order)
        assert result['id'] == 'txn_123'

    def test_order_not_found_raises_error(self):
        self.mock_orders.get.return_value = None

        with pytest.raises(ValueError, match="Order 999 not found"):
            self.service.process_payment(999, 'tok_valid')

        self.mock_gateway.charge.assert_not_called()

    @patch('myapp.services.payment.send_alert')
    def test_gateway_failure_sends_alert(self, mock_alert):
        self.mock_gateway.charge.side_effect = ConnectionError("Gateway down")

        with pytest.raises(ConnectionError):
            self.service.process_payment(1, 'tok_valid')

        mock_alert.assert_called_once()
```

</details>

---

## Python in Production

<details>
<summary><strong>14. How do you manage configuration and secrets in a Python backend application?</strong></summary>

### Answer

```python
# Never hardcode secrets — use environment variables
# Never commit .env files — add to .gitignore

# pydantic-settings — typed, validated, documented config
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn, SecretStr

class Settings(BaseSettings):
    # Database
    database_url: PostgresDsn
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Cache
    redis_url: RedisDsn = "redis://localhost:6379/0"

    # Auth
    secret_key: SecretStr          # never logged, masked in repr
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60

    # AWS
    aws_access_key_id: str
    aws_secret_access_key: SecretStr
    aws_region: str = "ap-south-1"
    s3_bucket: str

    # App
    debug: bool = False
    allowed_hosts: list[str] = ["*"]
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Singleton — import once, use everywhere
settings = Settings()

# In production, use AWS Secrets Manager
import boto3
import json

def get_secret(secret_name: str, region: str = "ap-south-1") -> dict:
    client = boto3.client('secretsmanager', region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

db_creds = get_secret("prod/myapp/database")
```

</details>

---

<details>
<summary><strong>15. What is WSGI vs ASGI? How does it relate to your Django/FastAPI experience?</strong></summary>

### Answer

| | WSGI | ASGI |
|---|---|---|
| **Stands for** | Web Server Gateway Interface | Asynchronous Server Gateway Interface |
| **Type** | Synchronous | Asynchronous |
| **Introduced** | PEP 333 (2003) | PEP 3333 extension (2019) |
| **Supports** | HTTP only | HTTP + WebSockets + Server-Sent Events |
| **Django support** | Since beginning | Django 3.1+ |
| **Servers** | Gunicorn, uWSGI | Uvicorn, Hypercorn, Daphne |

```python
# WSGI — traditional Django
# myapp/wsgi.py (auto-generated by Django)
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
application = get_wsgi_application()

# Run: gunicorn myapp.wsgi:application --workers 4

# ASGI — Django with async support
# myapp/asgi.py
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
application = get_asgi_application()

# Run: uvicorn myapp.asgi:application --workers 4

# Async Django views (Django 3.1+)
from django.http import JsonResponse
import asyncio

async def async_dashboard(request):
    # Run multiple DB queries concurrently
    orders_task = asyncio.create_task(fetch_orders_async(request.user))
    stats_task = asyncio.create_task(fetch_stats_async(request.user))

    orders, stats = await asyncio.gather(orders_task, stats_task)
    return JsonResponse({"orders": orders, "stats": stats})

# FastAPI (ASGI by default)
from fastapi import FastAPI
app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await db.fetch_one(query, {"id": user_id})
    return user

# Run: uvicorn main:app --host 0.0.0.0 --port 8000
```

> 💡 **Interview tip:** Mention you used Django (WSGI with Gunicorn) for the e-commerce project and FastAPI (ASGI with Uvicorn) for the microservices APIs. ASGI is needed for WebSockets and high-concurrency async endpoints.

</details>

---

*Good luck! Tie every answer back to Martify, the microservices work, or your Codeclouds experience.*
