# Django Interview Preparation — 3+ Years Experience

> A comprehensive guide covering intermediate to advanced Django concepts. Each question includes a detailed answer, code examples, and interview tips.

---

## Table of Contents

- [Architecture](#architecture)
- [ORM](#orm)
- [Performance](#performance)
- [Security](#security)
- [Django REST Framework](#django-rest-framework)
- [Advanced Topics](#advanced-topics)
- [Testing](#testing)

---

## Architecture

<details>
<summary><strong>1. Explain Django's MVT architecture and how it differs from MVC.</strong></summary>

### Answer

Django follows the **MVT (Model-View-Template)** pattern:

| Layer | Responsibility |
|---|---|
| **Model** | Data layer — defines schema, handles DB interactions via ORM |
| **View** | Business logic — processes requests, returns responses |
| **Template** | Presentation layer — HTML rendering with Django template language |

The key difference from classic MVC is that Django's **View** combines the MVC Controller + View roles. The framework itself acts as the controller for URL routing (`urls.py` → `views.py`).

```
HTTP Request → urls.py → View → Model (ORM) → DB
                              ↓
HTTP Response ← Template ←───┘
```

```python
# urls.py → routes requests to views
path('products/', views.product_list, name='product-list'),

# views.py → business logic + selects template
def product_list(request):
    products = Product.objects.filter(active=True)
    return render(request, 'products/list.html', {'products': products})

# models.py → data layer
class Product(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

# templates/products/list.html → HTML presentation
```

> 💡 **Interview tip:** Interviewers may ask you to draw the request/response cycle. Be ready to walk through: browser → Django WSGI server → middleware stack → URL resolver → view → ORM → DB → template → response.

</details>

---

<details>
<summary><strong>2. What is Django middleware and how does it work? Give an example of custom middleware.</strong></summary>

### Answer

Middleware is a framework of hooks into Django's **request/response processing**. It's a thin layer that sits between the server and the view — processing requests before they reach the view and responses before they return to the client.

Each middleware class implements the `__call__` pattern (modern style). Middleware is stacked in `settings.MIDDLEWARE` and executes **top-down for requests**, **bottom-up for responses**.

```python
# Custom middleware — request timing
class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import time
        start = time.time()

        response = self.get_response(request)  # Call next middleware/view

        duration = time.time() - start
        response['X-Page-Duration-ms'] = str(round(duration * 1000, 2))
        return response


# Custom middleware — block IPs
class IPBlocklistMiddleware:
    BLOCKED = {'192.168.1.100', '10.0.0.5'}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip in self.BLOCKED:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden('Access denied.')
        return self.get_response(request)
```

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'myapp.middleware.TimingMiddleware',   # custom
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

> 💡 **Interview tip:** Middleware order matters. `SecurityMiddleware` should be first for HTTPS redirects. `SessionMiddleware` must come before `AuthenticationMiddleware`. CSRF middleware must be before any view that uses `request.POST`.

</details>

---

<details>
<summary><strong>3. What are Django signals and when should (and shouldn't) you use them?</strong></summary>

### Answer

Signals allow **decoupled applications** to get notified when certain actions occur elsewhere in the framework.

**Common built-in signals:**
- `post_save` / `pre_save`
- `post_delete` / `pre_delete`
- `m2m_changed`
- `request_started` / `request_finished`

**When to use signals:**
- Sending notifications (emails, push) on model creation
- Audit logging across multiple apps
- Invalidating cache entries on model save
- Cross-app side effects where direct coupling is undesirable

**When NOT to use signals:**
- For core business logic (makes code hard to trace and test)
- When a direct method call would be clearer
- In performance-critical paths (signals add overhead and are synchronous)

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def on_user_created(sender, instance, created, **kwargs):
    if created:
        # Create user profile
        UserProfile.objects.create(user=instance)
        # Send welcome email via Celery
        send_welcome_email.delay(instance.id)


# Custom signals
from django.dispatch import Signal

order_completed = Signal()  # define

# Send the signal
order_completed.send(sender=Order, order=order_instance)

# Receive the signal
@receiver(order_completed)
def on_order_complete(sender, order, **kwargs):
    generate_invoice.delay(order.id)
```

```python
# apps.py — always connect signals here
class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        import myapp.signals  # noqa: F401
```

> 💡 **Interview tip:** A common mistake is connecting signals in `models.py`, causing duplicate signal receivers. Always connect in `AppConfig.ready()`. Also mention that signals can cause N+1 issues if you're doing DB queries inside `post_save` loops.

</details>

---

## ORM

<details>
<summary><strong>4. How do you solve the N+1 query problem in Django ORM?</strong></summary>

### Answer

The N+1 problem occurs when you query a list of objects and then make a **separate DB query for each object** while accessing a related field in a loop.

**Solutions:**

| Method | Use Case | SQL Strategy |
|---|---|---|
| `select_related()` | ForeignKey, OneToOne | SQL JOIN — single query |
| `prefetch_related()` | ManyToMany, reverse FK | Separate query + Python join |
| `Prefetch()` object | Filtered/annotated prefetch | Custom queryset per relation |

```python
# Bad — N+1 queries (1 for orders + 1 per order for customer)
orders = Order.objects.all()
for order in orders:
    print(order.customer.name)  # DB query per iteration!

# Good — select_related (SQL JOIN, single query)
orders = Order.objects.select_related('customer').all()

# Good — prefetch_related (for ManyToMany / reverse FK)
orders = Order.objects.prefetch_related('items').all()

# Advanced — filtered prefetch
from django.db.models import Prefetch

orders = Order.objects.prefetch_related(
    Prefetch(
        'items',
        queryset=Item.objects.filter(active=True).select_related('product'),
        to_attr='active_items'  # access as order.active_items
    )
).select_related('customer')

# Detecting N+1 in development
# Use django-debug-toolbar or log queries:
import logging
logging.getLogger('django.db.backends').setLevel(logging.DEBUG)
```

> 💡 **Interview tip:** Mention `django-debug-toolbar` as your go-to tool to detect N+1 issues in development. Also worth noting: `select_related()` follows FK chains — `select_related('order__customer__address')` works.

</details>

---

<details>
<summary><strong>5. Explain QuerySet lazy evaluation and when database hits actually occur.</strong></summary>

### Answer

QuerySets are **lazy** — they don't hit the database until the data is actually needed. The query is built up as you chain methods, but executed only when evaluated.

**Database hits occur when:**
- Iterating over a queryset (`for obj in qs`)
- Slicing with a step (`qs[::2]`)
- Calling `len()`, `bool()`, `list()`, `repr()`
- Template rendering iterates the queryset
- Calling `.exists()`, `.count()`, `[0]`

**QuerySet caching:** Once evaluated, a queryset caches its results. But calling `.filter()` on a cached queryset creates a *new* queryset and re-hits the DB.

```python
qs = User.objects.filter(active=True)   # No DB hit — just builds query
qs = qs.order_by('name')               # No DB hit — appends ORDER BY
qs = qs.exclude(role='guest')          # No DB hit — appends WHERE

users = list(qs)                        # DB hit here — evaluates queryset

# Re-using the cached queryset
print(len(users))    # No DB hit — uses cached list

# Efficient evaluation methods
qs.exists()          # SELECT 1 LIMIT 1 — cheapest existence check
qs.count()           # SELECT COUNT(*) — no data transfer
qs.first()           # SELECT ... ORDER BY pk LIMIT 1
qs[0]                # SELECT ... LIMIT 1

# Forcing evaluation without iterating
list(qs)             # evaluates and caches
bool(qs)             # evaluates (use .exists() instead for performance)
```

> 💡 **Interview tip:** Always use `.exists()` over `bool(qs)` or `if qs.count() > 0` — it generates `SELECT 1 LIMIT 1` which is far cheaper than fetching full rows.

</details>

---

<details>
<summary><strong>6. How do custom Managers and QuerySets work? When do you use each?</strong></summary>

### Answer

- A **custom Manager** replaces or extends the default `objects` manager on a model.
- A **custom QuerySet** lets you define reusable, chainable filter logic.

**Best practice:** Define a custom QuerySet and expose it via a Manager. This way both `Article.objects.published()` and `Article.objects.filter(...).published()` work.

```python
class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')

    def recent(self):
        return self.order_by('-created_at')

    def by_author(self, author):
        return self.filter(author=author)

    def with_stats(self):
        from django.db.models import Count
        return self.annotate(comment_count=Count('comments'))


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    # Expose QuerySet methods at the manager level
    def published(self):
        return self.get_queryset().published()

    def featured(self):
        return self.get_queryset().published().filter(featured=True)


class Article(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = ArticleManager()

    class Meta:
        ordering = ['-created_at']


# Usage — chaining works because QuerySet methods return QuerySets
Article.objects.published().recent()[:10]
Article.objects.by_author(user).with_stats()
Article.objects.published().by_author(user).recent()
```

> 💡 **Interview tip:** Ask yourself — "Would I write this filter in more than one view?" If yes, it belongs in a QuerySet method.

</details>

---

<details>
<summary><strong>7. Explain the difference between annotate() and aggregate() in Django ORM.</strong></summary>

### Answer

| Method | Returns | Adds |
|---|---|---|
| `aggregate()` | A single Python dictionary | One computed value for the entire queryset |
| `annotate()` | A QuerySet | A computed attribute per object |

Think of it this way: `aggregate()` is like `SELECT SUM(amount) FROM orders`. `annotate()` is like `SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id`.

```python
from django.db.models import Count, Avg, Sum, Max, Min, F, Q

# aggregate() — single summary for entire queryset
stats = Order.objects.filter(status='completed').aggregate(
    total_revenue=Sum('amount'),
    avg_order=Avg('amount'),
    max_order=Max('amount'),
    order_count=Count('id')
)
# → {'total_revenue': 50000, 'avg_order': 250.0, ...}

# annotate() — per-object computed field
customers = Customer.objects.annotate(
    order_count=Count('orders'),
    total_spent=Sum('orders__amount'),
    last_order=Max('orders__created_at')
).order_by('-total_spent')

for customer in customers:
    print(customer.name, customer.order_count, customer.total_spent)

# Combining annotate + aggregate
avg_orders_per_customer = Customer.objects.annotate(
    order_count=Count('orders')
).aggregate(avg=Avg('order_count'))

# Conditional annotation with Case/When
from django.db.models import Case, When, IntegerField

products = Product.objects.annotate(
    stock_status=Case(
        When(stock=0, then=0),
        When(stock__lt=10, then=1),
        default=2,
        output_field=IntegerField()
    )
)
```

</details>

---

## Performance

<details>
<summary><strong>8. What caching strategies does Django support? How do you implement per-view and low-level caching?</strong></summary>

### Answer

**Cache backends supported:** Memcached, Redis (`django-redis`), database, file-based, in-memory (dev only).

**Cache granularity levels:**

| Level | Tool | Use Case |
|---|---|---|
| Site-wide | `UpdateCacheMiddleware` + `FetchFromCacheMiddleware` | Fully static sites |
| Per-view | `@cache_page` decorator | Public pages with no user context |
| Template fragment | `{% cache %}` tag | Expensive template sections |
| Low-level | `cache.get/set/delete` | Fine-grained control |

```python
# settings.py — Redis cache backend
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
        'TIMEOUT': 300,
    }
}

# Per-view cache
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def product_list(request):
    products = Product.objects.filter(active=True)
    return render(request, 'products/list.html', {'products': products})

# Low-level API with versioning
from django.core.cache import cache

def get_dashboard_data(user_id):
    cache_key = f'dashboard:user:{user_id}'
    data = cache.get(cache_key)

    if data is None:
        data = {
            'orders': list(Order.objects.filter(user_id=user_id).values()),
            'stats': compute_stats(user_id),
        }
        cache.set(cache_key, data, timeout=300)

    return data

# Cache invalidation in signal
from django.db.models.signals import post_save

@receiver(post_save, sender=Order)
def invalidate_dashboard_cache(sender, instance, **kwargs):
    cache.delete(f'dashboard:user:{instance.user_id}')

# Cache many keys at once
cache.set_many({'key1': val1, 'key2': val2}, timeout=300)
results = cache.get_many(['key1', 'key2'])
```

```html
<!-- Template fragment cache -->
{% load cache %}
{% cache 500 product_sidebar product.id %}
    <!-- expensive sidebar content -->
{% endcache %}
```

> 💡 **Interview tip:** Cache invalidation is the hard part. Mention strategies: explicit deletion in signals, key versioning (`cache.incr('product_version')` and including the version in keys), or time-based expiry as a fallback.

</details>

---

<details>
<summary><strong>9. How do you use database indexing in Django models and when should you add indexes?</strong></summary>

### Answer

Indexes speed up reads but **slow down writes** and consume storage. Add them on fields used frequently in `WHERE`, `ORDER BY`, or `JOIN` conditions.

**Rule of thumb:** Add an index if a query on that field/combination runs frequently and the table has more than ~10,000 rows.

```python
class Order(models.Model):
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            # Composite index — filters by status + sorts by date
            models.Index(fields=['status', 'created_at'], name='order_status_date_idx'),

            # Partial index — only index pending orders (smaller, faster)
            models.Index(
                fields=['customer'],
                condition=Q(status='pending'),
                name='pending_orders_customer_idx'
            ),

            # Functional index (Django 3.2+) — case-insensitive search
            models.Index(
                Upper('email'),
                name='upper_email_idx'
            ),
        ]


# Field-level index (single column)
class Product(models.Model):
    sku = models.CharField(max_length=50, db_index=True, unique=True)
    slug = models.SlugField(unique=True)  # unique=True creates an index automatically


# Analyzing slow queries
# Run in Django shell:
from django.db import connection
qs = Order.objects.filter(status='pending').order_by('created_at')
print(qs.query)  # see raw SQL

# Or explain the query plan:
with connection.cursor() as cursor:
    cursor.execute('EXPLAIN ANALYZE ' + str(qs.query))
    print(cursor.fetchall())
```

> 💡 **Interview tip:** ForeignKey fields automatically get an index in Django. Mention that composite indexes are column-order sensitive — `Index(fields=['status', 'created_at'])` helps `WHERE status=X ORDER BY created_at` but not `WHERE created_at=X` alone.

</details>

---

<details>
<summary><strong>10. How do you use only() and defer() for query optimization?</strong></summary>

### Answer

These methods control which fields are loaded from the database. Use them when models have large `TextField` or `BinaryField` columns you don't always need.

- `only(*fields)` — loads only the specified fields (plus PK)
- `defer(*fields)` — loads everything except the specified fields
- Accessing a deferred field triggers **an additional DB query per object** (lazy loading)

```python
# only() — ideal for list views where you show minimal fields
users = User.objects.only('id', 'first_name', 'email')

# defer() — defer heavy fields you rarely need
articles = Article.objects.defer('body', 'raw_html', 'metadata')

# values() — returns dicts, not model instances (no ORM overhead)
users = User.objects.values('id', 'first_name', 'email')
# → [{'id': 1, 'first_name': 'Alice', 'email': 'alice@example.com'}, ...]

# values_list() — returns tuples
emails = User.objects.values_list('email', flat=True)
# → ['alice@example.com', 'bob@example.com', ...]

# Named tuples
coords = Location.objects.values_list('lat', 'lng', named=True)
for point in coords:
    print(point.lat, point.lng)
```

**Comparison:**

| Method | Returns | Can call model methods? | Overhead |
|---|---|---|---|
| `only()` / `defer()` | Model instances | Yes | Low |
| `values()` | Dicts | No | Very low |
| `values_list()` | Tuples | No | Lowest |

> 💡 **Interview tip:** Accessing a deferred field inside a loop is still an N+1 problem. If you know you'll need a deferred field for some objects, use `only()` with that field included instead.

</details>

---

## Security

<details>
<summary><strong>11. What are Django's built-in security protections and how do they work?</strong></summary>

### Answer

| Protection | Mechanism | Django Component |
|---|---|---|
| CSRF | Token per session, verified on POST | `CsrfViewMiddleware` |
| SQL Injection | Parameterized queries | ORM (always) |
| XSS | Auto-escape HTML in templates | Template engine |
| Clickjacking | `X-Frame-Options` header | `XFrameOptionsMiddleware` |
| HTTPS enforcement | Redirect HTTP → HTTPS | `SecurityMiddleware` |
| Secure cookies | `Secure` + `HttpOnly` flags | Settings |
| Password hashing | PBKDF2 (pluggable hashers) | `AbstractBaseUser` |

```python
# settings.py — production security checklist
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# HTTPS & headers
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000      # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

```python
# Manually mark content as safe (use with caution — only for trusted content)
from django.utils.safestring import mark_safe
# Never: mark_safe(user_input)  — XSS vulnerability!

# CSRF exemption for specific views (e.g., webhook endpoints)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def stripe_webhook(request):
    # Verify Stripe signature manually instead
    ...
```

> 💡 **Interview tip:** Run `python manage.py check --deploy` — Django will flag any security misconfigurations before production deployment.

</details>

---

<details>
<summary><strong>12. How does Django's permission system work? How do you implement object-level permissions?</strong></summary>

### Answer

Django's built-in system provides **model-level permissions**: `add_<model>`, `change_<model>`, `delete_<model>`, `view_<model>` — auto-created for each model.

Users can be assigned permissions directly or via **Groups** (recommended for maintainability).

For **object-level permissions** (e.g., "can user X edit *this specific* post?"), Django's default backend doesn't support it. You implement it via custom authentication backends or libraries like `django-guardian`.

```python
# Model-level permission check
request.user.has_perm('blog.change_post')       # returns True/False
request.user.has_perm('blog.delete_post')

# Assign permissions programmatically
from django.contrib.auth.models import Permission
perm = Permission.objects.get(codename='change_post')
user.user_permissions.add(perm)

# Group-based permissions
from django.contrib.auth.models import Group
editors = Group.objects.get(name='Editors')
user.groups.add(editors)

# Custom permission backend for object-level
class PostOwnerBackend:
    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        if obj is None:
            return False  # fall through to default backend
        if perm == 'blog.change_post':
            return obj.author == user_obj or user_obj.is_staff
        return False

# In views — check object-level permission
from django.core.exceptions import PermissionDenied

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.user.has_perm('blog.change_post', post):
        raise PermissionDenied
    ...

# In DRF — custom permission class
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.author == request.user
```

```python
# settings.py — register custom backend
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'myapp.backends.PostOwnerBackend',
]
```

> 💡 **Interview tip:** Mention `django-guardian` for a full object-level permission system with DB persistence. For simpler cases, a custom backend is sufficient and adds no dependencies.

</details>

---

## Django REST Framework

<details>
<summary><strong>13. What is the difference between APIView, GenericAPIView, and ViewSets in DRF?</strong></summary>

### Answer

| Class | Code Volume | Flexibility | Best For |
|---|---|---|---|
| `APIView` | Most | Highest | Custom, non-CRUD endpoints |
| `GenericAPIView` + mixins | Medium | High | Partial CRUD, custom logic |
| `ModelViewSet` | Least | Lower | Full CRUD on a model |

```python
# APIView — explicit control over every method
from rest_framework.views import APIView
from rest_framework.response import Response

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.filter(active=True)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


# GenericAPIView with mixins — reuse common patterns
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

class UserListCreateView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Or use shorthand generic views:
from rest_framework.generics import ListCreateAPIView
class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ModelViewSet — full CRUD with minimal code
from rest_framework.viewsets import ModelViewSet

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Customize per-request
        return User.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        # Hook into creation without overriding create()
        serializer.save(created_by=self.request.user)

# Router auto-generates all URLs
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('users', UserViewSet)
# Generates: GET/POST /users/, GET/PUT/PATCH/DELETE /users/{pk}/
```

> 💡 **Interview tip:** Know when NOT to use ModelViewSet — when your endpoint logic diverges significantly from CRUD (e.g., a `POST /send-invoice/` endpoint), use `APIView` or `@api_view` for clarity.

</details>

---

<details>
<summary><strong>14. How do you handle serializer validation and nested serializers in DRF?</strong></summary>

### Answer

DRF serializers support three levels of validation:
1. **Field-level:** `validate_<field_name>(self, value)`
2. **Object-level:** `validate(self, data)` — for cross-field validation
3. **Built-in validators:** `UniqueValidator`, `UniqueTogetherValidator`

For nested objects, define nested serializers as fields and **override `create()` / `update()`** to handle the nested data (DRF does not do this automatically for writable nested serializers).

```python
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'zip_code']


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'confirm_password', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    # Field-level validation
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value.lower()

    # Object-level (cross-field) validation
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    # Handle nested creation
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        validated_data.pop('confirm_password')

        user = User.objects.create_user(**validated_data)
        Address.objects.create(user=user, **address_data)
        return user

    # Handle nested update
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if address_data:
            Address.objects.update_or_create(
                user=instance, defaults=address_data
            )
        return instance
```

> 💡 **Interview tip:** Interviewers often ask about writable nested serializers specifically. The key point: DRF's default `create()` and `update()` do not know how to handle nested data — you must override them. For read-only nested data, no override is needed.

</details>

---

<details>
<summary><strong>15. How do you implement filtering, searching, and pagination in DRF?</strong></summary>

### Answer

DRF provides built-in support via `django-filter`, `SearchFilter`, and pagination classes.

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# Custom pagination
class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# filters.py
import django_filters

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category', 'in_stock']

# views.py
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku']      # ?search=...
    ordering_fields = ['price', 'created_at', 'name']   # ?ordering=-price
    ordering = ['-created_at']                          # default ordering

# Usage:
# GET /products/?min_price=10&max_price=100&search=shirt&ordering=-price&page=2
```

</details>

---

## Advanced Topics

<details>
<summary><strong>16. How do Django database migrations work internally? How do you handle data migrations?</strong></summary>

### Answer

Migrations are Python files in `migrations/` that describe schema changes as a series of **Operations**. Django tracks which migrations have been applied in the `django_migrations` table.

**Workflow:** `makemigrations` → inspects model changes → generates migration file. `migrate` → applies unapplied migrations in dependency order.

**Data migrations** use `RunPython` to execute arbitrary Python (with ORM access) to transform existing data during a schema change.

```python
# Auto-generated schema migration (simplified)
class Migration(migrations.Migration):
    dependencies = [('myapp', '0004_previous')]

    operations = [
        migrations.AddField(
            model_name='article',
            name='full_name',
            field=models.CharField(max_length=200, default=''),
        ),
    ]


# Data migration — always use apps.get_model(), NOT direct model import
from django.db import migrations

def populate_full_name(apps, schema_editor):
    """Forward: populate full_name from first_name + last_name."""
    User = apps.get_model('auth', 'User')  # historical model version
    for user in User.objects.all().iterator(chunk_size=500):
        user.full_name = f"{user.first_name} {user.last_name}".strip()
        user.save(update_fields=['full_name'])

def reverse_full_name(apps, schema_editor):
    """Reverse: clear the field."""
    User = apps.get_model('auth', 'User')
    User.objects.all().update(full_name='')

class Migration(migrations.Migration):
    dependencies = [('myapp', '0005_add_full_name')]

    operations = [
        migrations.RunPython(populate_full_name, reverse_full_name),
    ]


# Useful migration commands
# python manage.py showmigrations
# python manage.py migrate myapp 0003   ← roll back to specific migration
# python manage.py sqlmigrate myapp 0004 ← see the SQL
# python manage.py migrate --fake myapp 0005  ← mark as applied without running
```

> 💡 **Interview tip:** Always use `apps.get_model()` inside data migrations. Importing the model directly uses the *current* model definition, which may differ from what existed when the migration runs — causing errors in future re-runs or on fresh environments.

</details>

---

<details>
<summary><strong>17. Explain Django's ContentTypes framework and GenericForeignKey.</strong></summary>

### Answer

The ContentTypes framework (`django.contrib.contenttypes`) creates a **registry of all installed models**. `GenericForeignKey` allows a model to point to *any* model instance — enabling polymorphic relationships.

**Common use cases:** comments that can belong to any content type, activity feeds, tagging systems, notifications.

**Downsides:** no DB-level referential integrity, harder to query across types, no ORM JOIN support directly.

```python
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')  # virtual field

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

# Add reverse relation to target models
class Post(models.Model):
    title = models.CharField(max_length=200)
    comments = GenericRelation(Comment)  # enables post.comments.all()

# Creating a comment on any object
post = Post.objects.first()
Comment.objects.create(content_object=post, author=user, text="Great post!")

# Fetching efficiently
ct = ContentType.objects.get_for_model(Post)
post_comments = Comment.objects.filter(content_type=ct, object_id=post.id)

# Prefetch for performance
from django.contrib.contenttypes.prefetch import GenericRelatedObjectManager
comments = Comment.objects.prefetch_related('content_object')
```

> 💡 **Interview tip:** Mention that `ContentType.objects.get_for_model()` uses an internal cache, so it doesn't hit the DB on every call. Also, always add a composite index on `(content_type, object_id)` for query performance.

</details>

---

<details>
<summary><strong>18. How do you implement asynchronous tasks in Django using Celery?</strong></summary>

### Answer

For tasks too slow for the request/response cycle (emails, PDF generation, API calls, report generation), offload them to a **task queue**. Celery is the standard choice — it runs as a separate worker process with a message broker (Redis or RabbitMQ) between Django and the workers.

```python
# celery.py (project root)
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_ALWAYS_EAGER = False  # set True in tests


# tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation(self, order_id):
    try:
        order = Order.objects.select_related('customer').get(pk=order_id)
        send_mail(
            subject=f'Order #{order.id} confirmed',
            message=render_email_template(order),
            from_email='orders@shop.com',
            recipient_list=[order.customer.email],
        )
        logger.info(f'Confirmation sent for order {order_id}')
    except Order.DoesNotExist:
        logger.error(f'Order {order_id} not found')
    except Exception as exc:
        raise self.retry(exc=exc)

# Periodic tasks with Celery Beat
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-daily-report': {
        'task': 'myapp.tasks.generate_daily_report',
        'schedule': crontab(hour=8, minute=0),
    },
}


# In views — fire and forget
def checkout(request):
    order = create_order(request)
    send_order_confirmation.delay(order.id)          # async, non-blocking
    send_order_confirmation.apply_async(              # more control
        args=[order.id],
        countdown=30,           # delay 30 seconds
        expires=3600,           # expire if not started in 1 hour
        queue='high_priority',
    )
    return redirect('order_success')
```

```bash
# Start worker
celery -A myproject worker --loglevel=info --concurrency=4

# Start scheduler (for periodic tasks)
celery -A myproject beat --loglevel=info

# Monitor
celery -A myproject flower  # web UI at localhost:5555
```

> 💡 **Interview tip:** `.delay()` is shorthand for `.apply_async()` with no options. Use `.apply_async()` when you need `countdown`, `eta`, `queue` routing, `expires`, or task chaining with `.chain()` / `.chord()`.

</details>

---

<details>
<summary><strong>19. What is select_for_update() and when do you use it?</strong></summary>

### Answer

`select_for_update()` issues a `SELECT ... FOR UPDATE` SQL statement, which **locks the selected rows** until the end of the current transaction. Use it to prevent race conditions when multiple processes might try to update the same row simultaneously.

```python
from django.db import transaction

# Preventing race condition on inventory
@transaction.atomic
def purchase_item(user_id, product_id, quantity):
    # Lock the product row for the duration of this transaction
    product = Product.objects.select_for_update().get(pk=product_id)

    if product.stock < quantity:
        raise InsufficientStockError()

    product.stock -= quantity
    product.save()

    Order.objects.create(user_id=user_id, product=product, quantity=quantity)
    return product

# select_for_update options
Product.objects.select_for_update(nowait=True)    # raise DatabaseError instead of waiting
Product.objects.select_for_update(skip_locked=True)  # skip already-locked rows (good for task queues)
Product.objects.select_for_update(of=('self',))   # only lock this table in a JOIN
```

> 💡 **Interview tip:** `select_for_update()` must be used inside a `transaction.atomic()` block — otherwise the lock is immediately released. Also, it's not supported by SQLite (no-op) — only PostgreSQL, MySQL, and Oracle.

</details>

---

## Testing

<details>
<summary><strong>20. How do you write effective tests in Django? Explain the different TestCase classes.</strong></summary>

### Answer

| Class | DB Access | Transactions | Speed | Use When |
|---|---|---|---|---|
| `SimpleTestCase` | No | No | Fastest | URL routing, pure logic, template rendering |
| `TestCase` | Yes | Wrapped (rolled back) | Fast | Most tests — the default |
| `TransactionTestCase` | Yes | Real commits | Slow | Testing transaction behavior, signals with `on_commit` |
| `LiveServerTestCase` | Yes | Real commits | Slowest | Selenium / browser tests |

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch, MagicMock


class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name='Widget', price=10.00, stock=100)

    def test_create_order_success(self):
        url = reverse('order-list')
        data = {'product': self.product.id, 'quantity': 2}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(response.data['total'], '20.00')

    def test_create_order_insufficient_stock(self):
        data = {'product': self.product.id, 'quantity': 999}
        response = self.client.post(reverse('order-list'), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('stock', response.data)

    def test_unauthenticated_returns_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 401)

    @patch('myapp.tasks.send_order_confirmation.delay')
    def test_order_triggers_email_task(self, mock_task):
        data = {'product': self.product.id, 'quantity': 1}
        self.client.post(reverse('order-list'), data, format='json')
        mock_task.assert_called_once()
        call_args = mock_task.call_args[0]
        self.assertEqual(call_args[0], Order.objects.first().id)


# Testing with factory_boy (cleaner fixtures)
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')

# Usage in tests
user = UserFactory()
user = UserFactory(username='alice', email='alice@custom.com')
users = UserFactory.create_batch(10)
```

> 💡 **Interview tip:** Use `factory_boy` for fixtures instead of manually creating objects — it handles complex model hierarchies cleanly. For Celery tasks, always `@patch` the `.delay()` call so tests don't require a running broker.

</details>

---

<details>
<summary><strong>21. How do you test views that require authentication and specific permissions?</strong></summary>

### Answer

```python
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission


class PostViewPermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='pw')
        self.editor = User.objects.create_user('bob', password='pw')
        perm = Permission.objects.get(codename='change_post')
        self.editor.user_permissions.add(perm)

        self.post = Post.objects.create(title='Test', author=self.user)

    def test_unauthenticated_redirects_to_login(self):
        url = reverse('post-edit', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f'/login/?next={url}')

    def test_non_owner_gets_403(self):
        other = User.objects.create_user('charlie', password='pw')
        self.client.force_login(other)
        response = self.client.get(reverse('post-edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)

    def test_owner_can_edit(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('post-edit', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_editor_with_permission_can_edit(self):
        self.client.force_login(self.editor)
        response = self.client.post(
            reverse('post-edit', kwargs={'pk': self.post.pk}),
            {'title': 'Updated Title', 'body': 'Content'},
        )
        self.assertRedirects(response, reverse('post-detail', kwargs={'pk': self.post.pk}))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
```

</details>

---

## Additional Tips for the Interview

### Topics to prepare beyond this list

- `select_for_update()` for preventing race conditions
- Database connection pooling with `CONN_MAX_AGE`
- Multi-database routing (`DATABASE_ROUTERS`)
- Django Channels for WebSockets
- Django admin customization (`ModelAdmin`, `InlineModelAdmin`)
- Deploying with Gunicorn + Nginx + Supervisor
- Environment-based settings management (`django-environ`)
- API versioning strategies in DRF

### What interviewers expect at 3+ years

At this level, interviewers don't just want to hear *what* you used — they want to hear **why** you chose it and what tradeoffs you made. For example:

- Not just "I used `select_related()`" but "I noticed 47 queries on the page using Debug Toolbar, traced it to the order loop, and fixed it with `select_related('customer__address')`"
- Not just "I used Celery" but "I moved the invoice generation off the request thread because it was adding 3+ seconds to checkout and causing timeouts under load"

### Useful commands to know

```bash
python manage.py check --deploy       # security audit
python manage.py showmigrations       # migration status
python manage.py dbshell              # direct DB access
python manage.py shell_plus           # enhanced shell (django-extensions)
python manage.py test --keepdb        # preserve test DB between runs (faster)
python manage.py collectstatic --noinput
```

---

*Good luck with your interview!*
