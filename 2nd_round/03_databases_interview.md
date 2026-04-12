# Database Interview Prep — PostgreSQL, MySQL & MongoDB
> Tailored to your resume: query optimization, indexing, connection pooling, ORM vs raw SQL

---

## Table of Contents
- [PostgreSQL Fundamentals](#postgresql-fundamentals)
- [Indexing & Query Optimization](#indexing--query-optimization)
- [Transactions & Concurrency](#transactions--concurrency)
- [Django ORM vs Raw SQL](#django-orm-vs-raw-sql)
- [MongoDB](#mongodb)
- [Database Design](#database-design)
- [Scenario-Based Questions](#scenario-based-questions)

---

## PostgreSQL Fundamentals

<details>
<summary><strong>1. What are the key differences between PostgreSQL and MySQL? Why did you choose PostgreSQL?</strong></summary>

### Answer

| Feature | PostgreSQL | MySQL |
|---|---|---|
| ACID compliance | Full, always | Depends on engine (InnoDB: yes) |
| JSON support | Native JSONB (indexable) | JSON (less powerful) |
| Full-text search | Built-in, powerful | Basic |
| Extensibility | Custom types, operators, functions | Limited |
| Concurrency | MVCC — no read locks | MVCC (InnoDB) |
| Geospatial | PostGIS extension | Limited |
| Array types | Native | No |
| Window functions | Full support | Limited (8.0+) |
| Standards compliance | High | Medium |

**Why PostgreSQL for your projects:**
- Django's ORM has the best support for PostgreSQL-specific features
- JSONB fields for flexible data (product attributes, order metadata)
- Better analytics queries with window functions
- Superior full-text search for product catalog
- Stronger data integrity constraints

```python
# PostgreSQL-specific Django features
from django.contrib.postgres.fields import ArrayField, JSONBField
from django.contrib.postgres.indexes import GinIndex, GistIndex
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

class Product(models.Model):
    tags = ArrayField(models.CharField(max_length=50), default=list)
    attributes = models.JSONField(default=dict)   # JSONB internally
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=['tags']),           # fast array containment queries
            GinIndex(fields=['attributes']),      # fast JSONB queries
            GinIndex(fields=['search_vector']),   # full-text search
        ]

# Array queries
Product.objects.filter(tags__contains=['electronics', 'sale'])
Product.objects.filter(tags__overlap=['new', 'featured'])

# JSONB queries
Product.objects.filter(attributes__color='red')
Product.objects.filter(attributes__size__in=['S', 'M', 'L'])

# Full-text search
from django.contrib.postgres.search import SearchVector, SearchQuery

query = SearchQuery('wireless headphones')
vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
products = Product.objects.annotate(
    rank=SearchRank(vector, query)
).filter(rank__gte=0.1).order_by('-rank')
```

</details>

---

<details>
<summary><strong>2. Explain ACID properties with examples relevant to an e-commerce backend.</strong></summary>

### Answer

**ACID = Atomicity, Consistency, Isolation, Durability**

```python
from django.db import transaction

# A — Atomicity: all operations succeed or all fail (no partial state)
@transaction.atomic
def process_checkout(user, cart_items, payment_token):
    """
    Either ALL of this succeeds or NONE of it persists.
    If payment succeeds but order creation fails → payment is rolled back.
    """
    # 1. Create order
    order = Order.objects.create(user=user, total=calculate_total(cart_items))

    # 2. Create order items + reduce stock
    for item in cart_items:
        product = Product.objects.select_for_update().get(pk=item.product_id)
        if product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for {product.name}")
        OrderItem.objects.create(order=order, product=product, quantity=item.quantity)
        product.stock -= item.quantity
        product.save()

    # 3. Charge payment
    result = payment_gateway.charge(order.total, payment_token)
    if not result['success']:
        raise PaymentError(result['message'])   # entire transaction rolls back!

    order.status = 'paid'
    order.transaction_id = result['id']
    order.save()
    return order

# C — Consistency: DB constraints always maintained
class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()   # DB constraint: no negative quantities
    # ForeignKey constraints: order/product must exist

# I — Isolation: concurrent transactions don't interfere
# Django uses READ COMMITTED by default
# Use SERIALIZABLE for critical financial operations

@transaction.atomic
def transfer_wallet(from_user, to_user, amount):
    # Lock both rows to prevent race conditions
    from_wallet = Wallet.objects.select_for_update().get(user=from_user)
    to_wallet = Wallet.objects.select_for_update().get(user=to_user)

    if from_wallet.balance < amount:
        raise ValueError("Insufficient balance")

    from_wallet.balance -= amount
    to_wallet.balance += amount
    from_wallet.save()
    to_wallet.save()

# D — Durability: committed data survives crashes
# PostgreSQL uses WAL (Write-Ahead Log) — changes logged before applied
# Data is safe even if server crashes mid-write
```

</details>

---

## Indexing & Query Optimization

<details>
<summary><strong>3. How did you optimize PostgreSQL queries to improve system performance? Walk through your process.</strong></summary>

### Answer

```sql
-- Step 1: Find slow queries using pg_stat_statements
SELECT query, mean_exec_time, calls, total_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 100   -- slower than 100ms
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Step 2: EXPLAIN ANALYZE — see the actual execution plan
EXPLAIN ANALYZE
SELECT o.*, u.email
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending'
  AND o.created_at > '2024-01-01'
ORDER BY o.created_at DESC;

-- Look for:
-- Seq Scan (bad on large tables) vs Index Scan (good)
-- Nested Loop with large row estimates (N+1 in SQL)
-- Sort operations without index
-- Hash Join vs Nested Loop

-- Step 3: Add targeted indexes
CREATE INDEX idx_orders_status_created
ON orders(status, created_at DESC)
WHERE status = 'pending';   -- Partial index — smaller, faster

CREATE INDEX idx_orders_user_status
ON orders(user_id, status);
```

```python
# Django equivalent
class Order(models.Model):
    class Meta:
        indexes = [
            # Composite index for common query pattern
            models.Index(
                fields=['status', '-created_at'],
                name='order_status_created_idx'
            ),
            # Partial index — only pending orders
            models.Index(
                fields=['user', 'status'],
                condition=Q(status='pending'),
                name='pending_orders_user_idx'
            ),
        ]

# Real optimization I did: (from your Codeclouds experience)
# Before: Product listing with category + filters was taking 800ms
# Found: 3 queries (products, categories, stock counts) + no index on status+category

# After:
class ProductAdmin(admin.ModelAdmin):
    list_select_related = True   # auto select_related in admin

# View optimization
def product_list(request):
    # Before — N+1 issue, 150+ queries for 50 products
    products = Product.objects.filter(is_active=True)

    # After — 2 queries total
    products = Product.objects.filter(
        is_active=True
    ).select_related(
        'category'
    ).prefetch_related(
        'images'
    ).only(
        'id', 'name', 'slug', 'price', 'stock',
        'category__name', 'category__slug'
    ).annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    )
    # Result: 800ms → 45ms
```

</details>

---

<details>
<summary><strong>4. What types of indexes are available in PostgreSQL? When do you use each?</strong></summary>

### Answer

| Index Type | Use Case | Django Support |
|---|---|---|
| B-tree (default) | Range queries, equality, ORDER BY | `models.Index` |
| Hash | Equality only, faster than B-tree for exact match | `HashIndex` |
| GIN | Array containment, JSONB, full-text search | `GinIndex` |
| GiST | Geometric data, full-text search, range types | `GistIndex` |
| BRIN | Very large tables with sequential correlation (timestamps) | `BrinIndex` |
| Partial | Index only subset of rows (WHERE clause) | `condition=Q(...)` |
| Covering | Include extra columns to avoid table lookup | `include=[...]` |
| Functional | Index on expression result | `OpClass` |

```python
from django.contrib.postgres.indexes import GinIndex, GistIndex, HashIndex, BrinIndex
from django.db.models import Index, Q

class Product(models.Model):
    class Meta:
        indexes = [
            # B-tree — default, good for most cases
            Index(fields=['category', 'price'], name='product_cat_price_idx'),

            # Partial — only active products (smaller, faster)
            Index(
                fields=['category'],
                condition=Q(is_active=True, stock__gt=0),
                name='active_products_category_idx'
            ),

            # Covering index — avoid table lookup for common query
            Index(
                fields=['slug'],
                include=['name', 'price', 'stock'],  # extra columns
                name='product_slug_covering_idx'
            ),

            # GIN — for JSONB and ArrayField
            GinIndex(fields=['attributes'], name='product_attrs_gin_idx'),
            GinIndex(fields=['tags'], name='product_tags_gin_idx'),

            # BRIN — for large tables with time-ordered data
            BrinIndex(fields=['created_at'], name='product_created_brin_idx'),
        ]

class OrderItem(models.Model):
    class Meta:
        indexes = [
            # Hash — for exact equality lookups on high-cardinality field
            HashIndex(fields=['transaction_id'], name='orderitem_txn_hash_idx'),
        ]
```

</details>

---

## Transactions & Concurrency

<details>
<summary><strong>5. How do you handle race conditions in Django? Explain select_for_update.</strong></summary>

### Answer

```python
from django.db import transaction

# Problem: Two users simultaneously buying the last item in stock
# Without locking:
def buy_product_UNSAFE(user, product_id, quantity):
    product = Product.objects.get(pk=product_id)
    if product.stock >= quantity:   # Thread A and B both pass this check!
        product.stock -= quantity   # Both reduce from 1 → -1 (oversold!)
        product.save()

# Solution 1: select_for_update() — database-level row lock
@transaction.atomic
def buy_product_SAFE(user, product_id, quantity):
    # SELECT ... FOR UPDATE — locks the row until transaction ends
    # Other transactions block here until lock is released
    product = Product.objects.select_for_update().get(pk=product_id)

    if product.stock < quantity:
        raise ValueError(f"Only {product.stock} units available")

    product.stock -= quantity
    product.save(update_fields=['stock'])
    order = Order.objects.create(user=user, product=product, quantity=quantity)
    return order

# select_for_update options
Product.objects.select_for_update(nowait=True)      # raise DatabaseError instead of waiting
Product.objects.select_for_update(skip_locked=True) # skip locked rows — good for task queues
Product.objects.select_for_update(of=('self',))     # lock only this table in a JOIN

# Solution 2: Optimistic locking — no DB lock, retry on conflict
# Using a version field
class Product(models.Model):
    stock = models.PositiveIntegerField()
    version = models.PositiveIntegerField(default=0)

def update_stock_optimistic(product_id, quantity, max_retries=3):
    for attempt in range(max_retries):
        product = Product.objects.get(pk=product_id)
        if product.stock < quantity:
            raise ValueError("Insufficient stock")

        updated = Product.objects.filter(
            pk=product_id,
            version=product.version   # only update if version hasn't changed
        ).update(
            stock=F('stock') - quantity,
            version=F('version') + 1
        )

        if updated == 1:   # successfully updated
            return
        # Another transaction updated it first — retry

    raise RuntimeError("Could not update stock after retries")

# Solution 3: F() expressions — atomic DB-level update
from django.db.models import F

# Atomic increment/decrement without locking
Product.objects.filter(pk=product_id).update(
    stock=F('stock') - quantity
)
# This translates to: UPDATE products SET stock = stock - 2 WHERE id = 1
# The subtraction happens in the DB atomically
```

</details>

---

<details>
<summary><strong>6. Explain database transaction isolation levels.</strong></summary>

### Answer

| Level | Dirty Read | Non-Repeatable Read | Phantom Read | Performance |
|---|---|---|---|---|
| **READ UNCOMMITTED** | Possible | Possible | Possible | Highest |
| **READ COMMITTED** ← Django default | No | Possible | Possible | High |
| **REPEATABLE READ** | No | No | Possible | Medium |
| **SERIALIZABLE** | No | No | No | Lowest |

```python
# Django default: READ COMMITTED
# Good for most web apps — fast, prevents dirty reads

# Set per-transaction
from django.db import connection

with transaction.atomic():
    connection.cursor().execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
    # Now all reads are fully isolated
    account = BankAccount.objects.get(pk=user_id)
    account.balance -= 500
    account.save()

# Globally (settings.py)
DATABASES = {
    'default': {
        'OPTIONS': {
            'isolation_level': 'read committed',   # explicit setting
        }
    }
}

# Practical example:
# READ COMMITTED problem: non-repeatable read
# Transaction 1: reads product stock = 5
# Transaction 2: updates stock to 3, commits
# Transaction 1: reads stock again = 3 (different! non-repeatable)

# REPEATABLE READ solution: Transaction 1 always sees stock = 5
# throughout its transaction, even after Transaction 2 commits
```

</details>

---

## Django ORM vs Raw SQL

<details>
<summary><strong>7. When would you use raw SQL instead of Django ORM? Show examples.</strong></summary>

### Answer

```python
# Use raw SQL when:
# 1. Complex queries with CTEs, window functions
# 2. Database-specific features not exposed by ORM
# 3. Bulk operations for performance
# 4. Query optimization that ORM can't achieve

# Method 1: Manager.raw() — returns model instances
orders = Order.objects.raw("""
    SELECT o.*,
           u.email as user_email,
           COUNT(oi.id) as item_count
    FROM orders o
    JOIN users u ON o.user_id = u.id
    LEFT JOIN order_items oi ON oi.order_id = o.id
    WHERE o.created_at > %s
    GROUP BY o.id, u.email
    ORDER BY o.created_at DESC
""", [thirty_days_ago])

# Method 2: connection.cursor() — fully raw
from django.db import connection

def get_revenue_by_category():
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH category_revenue AS (
                SELECT
                    c.name as category,
                    SUM(oi.price_at_purchase * oi.quantity) as revenue,
                    COUNT(DISTINCT o.id) as order_count,
                    RANK() OVER (ORDER BY SUM(oi.price_at_purchase * oi.quantity) DESC) as revenue_rank
                FROM categories c
                JOIN products p ON p.category_id = c.id
                JOIN order_items oi ON oi.product_id = p.id
                JOIN orders o ON o.id = oi.order_id
                WHERE o.status = 'paid'
                  AND o.created_at >= NOW() - INTERVAL '30 days'
                GROUP BY c.id, c.name
            )
            SELECT * FROM category_revenue
            WHERE revenue_rank <= 10
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for cursor.fetchall()]

# Method 3: Bulk operations — much faster than ORM for large datasets
# ORM: 1000 separate INSERT statements
for item in data:
    Product.objects.create(**item)

# Raw bulk: 1 INSERT statement
from django.db import connection
with connection.cursor() as cursor:
    cursor.executemany(
        "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
        [(p['name'], p['price'], p['stock']) for p in data]
    )

# Django's bulk_create — usually the best option
Product.objects.bulk_create([
    Product(name=p['name'], price=p['price'], stock=p['stock'])
    for p in data
], batch_size=1000)

# bulk_update
products = list(Product.objects.filter(category=cat))
for p in products:
    p.price *= 1.1   # 10% price increase
Product.objects.bulk_update(products, ['price'], batch_size=500)
```

</details>

---

## MongoDB

<details>
<summary><strong>8. How does MongoDB differ from PostgreSQL? When would you choose MongoDB?</strong></summary>

### Answer

| | PostgreSQL | MongoDB |
|---|---|---|
| **Model** | Relational (tables + rows) | Document (collections + BSON documents) |
| **Schema** | Fixed, enforced | Flexible, optional validation |
| **Joins** | Native SQL JOINs | `$lookup` (limited) |
| **ACID** | Full ACID | Multi-document ACID (4.0+) |
| **Scalability** | Vertical + read replicas | Horizontal sharding (native) |
| **Query language** | SQL | MongoDB Query Language (MQL) |
| **Indexing** | B-tree, GIN, etc. | B-tree, text, geo, compound |
| **Best for** | Complex relations, transactions | Flexible/hierarchical data, high write throughput |

```python
# When to use MongoDB (in your context — Micro-data analyst project)
# - Analytics data with varying schema (different events have different fields)
# - Log storage
# - Real-time dashboards with high write throughput
# - Storing user activity/behavior data

# pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["analytics"]

# Insert analytics events (flexible schema)
db.events.insert_one({
    "user_id": 1,
    "event": "page_view",
    "page": "/products/laptop",
    "timestamp": datetime.utcnow(),
    "metadata": {
        "browser": "Chrome",
        "device": "mobile",
        "duration_seconds": 45
    }
})

# Aggregation pipeline — powerful for analytics
pipeline = [
    {"$match": {"timestamp": {"$gte": thirty_days_ago}}},
    {"$group": {
        "_id": {"page": "$page", "event": "$event"},
        "count": {"$sum": 1},
        "unique_users": {"$addToSet": "$user_id"}
    }},
    {"$addFields": {"unique_user_count": {"$size": "$unique_users"}}},
    {"$sort": {"count": -1}},
    {"$limit": 20}
]
results = list(db.events.aggregate(pipeline))

# mongoengine — ODM for Django integration
from mongoengine import Document, StringField, IntField, DateTimeField

class AnalyticsEvent(Document):
    user_id = IntField(required=True)
    event_type = StringField(required=True)
    page = StringField()
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'events',
        'indexes': ['user_id', 'event_type', 'timestamp']
    }

# When NOT to use MongoDB:
# Financial transactions (need strong ACID)
# Complex relational data with many joins
# When data integrity constraints are important
```

</details>

---

## Database Design

<details>
<summary><strong>9. What is database normalization? When would you denormalize and why?</strong></summary>

### Answer

```
Normalization reduces redundancy and improves data integrity:

1NF: Atomic values — no arrays or nested structures in columns
2NF: Non-key columns depend on ENTIRE primary key (no partial dependencies)
3NF: Non-key columns depend ONLY on primary key (no transitive dependencies)
BCNF: Every determinant is a candidate key
```

```python
# 3NF — normalized (your e-commerce schema)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    # price_at_purchase is a SNAPSHOT — not product.price (which may change)

# Denormalization — deliberately add redundancy for performance

# Example 1: Storing computed total on Order instead of recalculating
class Order(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)  # cached total
    # Instead of: SELECT SUM(quantity * price) FROM order_items WHERE order_id=X

# Example 2: Analytics — denormalized table for fast reporting
class OrderDailySummary(models.Model):
    """Pre-aggregated daily stats — no need to query orders table for dashboard."""
    date = models.DateField(unique=True)
    order_count = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    avg_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    new_customers = models.IntegerField()

# Populate via Celery beat task
@shared_task
def aggregate_daily_stats(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    stats = Order.objects.filter(
        created_at__date=date, status='paid'
    ).aggregate(
        order_count=Count('id'),
        total_revenue=Sum('total'),
        avg_order_value=Avg('total'),
        new_customers=Count('user', filter=Q(user__date_joined__date=date))
    )
    OrderDailySummary.objects.update_or_create(date=date, defaults=stats)

# Example 3: Materialized views (PostgreSQL)
# Great for complex reports that don't need real-time data
from django.db import connection

def create_product_stats_view():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE MATERIALIZED VIEW product_stats AS
            SELECT
                p.id, p.name, p.price,
                COUNT(oi.id) as total_sold,
                SUM(oi.quantity) as units_sold,
                SUM(oi.price_at_purchase * oi.quantity) as revenue
            FROM products p
            LEFT JOIN order_items oi ON oi.product_id = p.id
            LEFT JOIN orders o ON o.id = oi.order_id AND o.status = 'paid'
            GROUP BY p.id, p.name, p.price
        """)
        cursor.execute("CREATE UNIQUE INDEX ON product_stats (id)")

# Refresh periodically
cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY product_stats")
```

</details>

---

## Scenario-Based Questions

<details>
<summary><strong>10. Your database is running out of connections under high load. How do you diagnose and fix it?</strong></summary>

### Answer

```sql
-- Step 1: Check current connections
SELECT count(*), state, wait_event_type, wait_event
FROM pg_stat_activity
GROUP BY state, wait_event_type, wait_event
ORDER BY count DESC;

-- Check max connections
SHOW max_connections;   -- default 100

-- Step 2: Identify connection hogs
SELECT pid, usename, application_name, state,
       now() - pg_stat_activity.query_start AS duration,
       query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;
```

**Fixes:**

```python
# Fix 1: CONN_MAX_AGE — reuse connections per Django worker
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 60,   # keep alive 60s instead of closing after each request
    }
}

# Fix 2: Reduce worker count if each holds many connections
# Gunicorn: --workers = (2 * CPU cores) + 1
# Each worker can hold 1 connection (per CONN_MAX_AGE)
# 4 workers × 60s CONN_MAX_AGE = max 4 persistent connections per dyno

# Fix 3: pgBouncer — connection pooler
# Install pgBouncer between Django and PostgreSQL
# pgBouncer maintains e.g. 10 connections to PostgreSQL
# But Django thinks it has 100+ connections

# pgbouncer.ini
[databases]
mydb = host=postgres-server port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction    # transaction pooling — most efficient
max_client_conn = 1000    # client connections
default_pool_size = 20    # actual PostgreSQL connections

# Fix 4: Async DB driver (asyncpg) for high-throughput async apps
pip install asyncpg
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # With async Django/FastAPI, use asyncpg for non-blocking DB queries
    }
}
```

</details>

---

<details>
<summary><strong>11. How would you design a database schema for an order tracking system with status history?</strong></summary>

### Answer

```python
# Pattern: Event sourcing + status log
# Never overwrite status — keep full history

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('payment_initiated', 'Payment Initiated'),
        ('paid', 'Paid'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['user', 'status', 'created_at'])]

    def transition_to(self, new_status, note='', changed_by=None):
        """Validated status transition with history logging."""
        valid_transitions = {
            'pending': ['payment_initiated', 'cancelled'],
            'payment_initiated': ['paid', 'cancelled'],
            'paid': ['confirmed', 'refunded'],
            'confirmed': ['shipped'],
            'shipped': ['out_for_delivery'],
            'out_for_delivery': ['delivered'],
            'delivered': ['refunded'],
        }
        allowed = valid_transitions.get(self.status, [])
        if new_status not in allowed:
            raise ValueError(
                f"Cannot transition from '{self.status}' to '{new_status}'. "
                f"Allowed: {allowed}"
            )
        old_status = self.status
        self.status = new_status
        self.save(update_fields=['status'])

        # Log the transition
        OrderStatusLog.objects.create(
            order=self,
            from_status=old_status,
            to_status=new_status,
            note=note,
            changed_by=changed_by
        )

class OrderStatusLog(models.Model):
    """Immutable audit log of all status changes."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    from_status = models.CharField(max_length=30)
    to_status = models.CharField(max_length=30)
    note = models.TextField(blank=True)
    changed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['changed_at']
        indexes = [models.Index(fields=['order', 'changed_at'])]

# Usage
order = Order.objects.get(pk=1)
order.transition_to('paid', note='Stripe payment txn_123', changed_by=None)
order.transition_to('confirmed', note='Auto-confirmed', changed_by=admin_user)

# Query history
history = OrderStatusLog.objects.filter(order=order).select_related('changed_by')
```

</details>

