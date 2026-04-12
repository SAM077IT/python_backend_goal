# Django Interview Prep — Backend Developer (3+ Years)
> Heavily tailored to your resume: REST APIs, JWT Auth, RBAC, PostgreSQL, ORM optimization, CI/CD

---

## Table of Contents
- [Architecture & Request Lifecycle](#architecture--request-lifecycle)
- [Models & ORM](#models--orm)
- [Views, URLs & Serializers](#views-urls--serializers)
- [Authentication & Authorization](#authentication--authorization)
- [Django REST Framework (DRF)](#django-rest-framework-drf)
- [Middleware & Signals](#middleware--signals)
- [Caching](#caching)
- [Performance & Query Optimization](#performance--query-optimization)
- [Security](#security)
- [Migrations & Database](#migrations--database)
- [Testing in Django](#testing-in-django)
- [Django in Production](#django-in-production)
- [Scenario-Based Questions](#scenario-based-questions)

---

## Architecture & Request Lifecycle

<details>
<summary><strong>1. Explain Django's request-response lifecycle step by step.</strong></summary>

### Answer

```
Browser / Client
     ↓
Web Server (Nginx)
     ↓
WSGI/ASGI Server (Gunicorn/Uvicorn)
     ↓
Django Application
     ↓
MIDDLEWARE STACK (top-down: SecurityMiddleware, SessionMiddleware, etc.)
     ↓
URL Resolver (urls.py → finds matching pattern)
     ↓
View (function-based or class-based)
     ↓  ↑
  ORM / DB  Cache  External APIs
     ↓
Template / Serializer
     ↓
MIDDLEWARE STACK (bottom-up: response processing)
     ↓
HTTP Response
```

**In detail:**

1. **Nginx** receives the request, serves static files directly, forwards dynamic requests to Gunicorn
2. **Gunicorn** passes it to the Django WSGI application
3. **Request middleware** runs top-to-bottom (`process_request`)
4. **URL resolver** matches `urls.py`, extracts path parameters
5. **View middleware** runs (`process_view`)
6. **View** executes — queries DB, applies business logic
7. **Response middleware** runs bottom-to-top (`process_response`)
8. **Response** is returned to the client

```python
# You can see all middleware in settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',           # HTTPS, HSTS
    'django.contrib.sessions.middleware.SessionMiddleware',    # session cookies
    'django.middleware.common.CommonMiddleware',               # URL normalization
    'django.middleware.csrf.CsrfViewMiddleware',              # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # request.user
    'django.contrib.messages.middleware.MessageMiddleware',    # flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # X-Frame-Options
]
```

</details>

---

<details>
<summary><strong>2. What is Django's MVT pattern? How is it different from MVC?</strong></summary>

### Answer

| Layer | Django | MVC equivalent | Responsibility |
|---|---|---|---|
| **Model** | `models.py` | Model | Data + business logic + ORM |
| **View** | `views.py` | Controller | Request handling + response |
| **Template** | `templates/` | View | HTML presentation |

Django's "View" is the MVC "Controller." The framework itself is the "Controller" for routing (URLs). This causes the naming confusion.

```python
# Model — data layer
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')

    def mark_paid(self):   # business logic in model
        self.status = 'paid'
        self.save()

# View — controller logic
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})

# Template — presentation
# orders/detail.html
# <h1>Order #{{ order.id }}</h1>
# <p>Total: ₹{{ order.total }}</p>
```

</details>

---

## Models & ORM

<details>
<summary><strong>3. How do you design Django models for an e-commerce application like Martify?</strong></summary>

### Answer

```python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)

    class Meta:
        indexes = [models.Index(fields=['email'])]

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='children'
    )

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['slug']),
        ]

    def is_in_stock(self):
        return self.stock > 0

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def subtotal(self):
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot!
```

> 💡 **Key design decisions to explain:**
> - `price_at_purchase` — snapshot of price at time of order (product price may change later)
> - `on_delete=PROTECT` for order-product — never delete a product that has orders
> - `unique_together` on CartItem — prevents duplicate product entries in cart
> - Custom `AbstractUser` — extend before first migration, much harder after

</details>

---

<details>
<summary><strong>4. Explain select_related vs prefetch_related with real examples from an e-commerce context.</strong></summary>

### Answer

```python
# The N+1 problem — most common performance issue in Django

# BAD: N+1 queries
orders = Order.objects.filter(status='pending')   # 1 query
for order in orders:
    print(order.user.email)      # +1 query per order!
    for item in order.items.all():  # +1 query per order!
        print(item.product.name)    # +1 query per item!

# With 100 orders and 5 items each: 1 + 100 + 500 + 500 = 1101 queries!

# GOOD: select_related — for ForeignKey/OneToOne (SQL JOIN, single query)
orders = Order.objects.select_related('user').filter(status='pending')
for order in orders:
    print(order.user.email)   # no extra query!

# Chain select_related for multiple levels
orders = Order.objects.select_related(
    'user',
    'user__profile',    # user's profile
).filter(status='pending')

# GOOD: prefetch_related — for ManyToMany / reverse FK (separate query + Python join)
orders = Order.objects.prefetch_related(
    'items',              # reverse FK to OrderItem
    'items__product',     # then product for each item
    'items__product__category',  # then category for each product
).select_related('user').filter(status='pending')

for order in orders:
    for item in order.items.all():    # no extra queries!
        print(item.product.name)

# Advanced: Prefetch with custom queryset
from django.db.models import Prefetch

orders = Order.objects.prefetch_related(
    Prefetch(
        'items',
        queryset=OrderItem.objects.select_related('product').only(
            'quantity', 'price_at_purchase', 'product__name', 'product__price'
        ),
        to_attr='order_items'    # access as order.order_items (list, not queryset)
    )
)

# Verify: check query count in tests
from django.test.utils import CaptureQueriesContext
from django.db import connection

with CaptureQueriesContext(connection) as ctx:
    list(Order.objects.select_related('user').prefetch_related('items__product'))
print(f"Query count: {len(ctx)}")   # should be 3: orders + items + products
```

</details>

---

<details>
<summary><strong>5. What is the difference between annotate() and aggregate()? Give a real reporting example.</strong></summary>

### Answer

```python
from django.db.models import (
    Count, Sum, Avg, Max, Min, F, Q, Value,
    DecimalField, ExpressionWrapper
)
from django.db.models.functions import TruncMonth, TruncDate, Coalesce

# aggregate() — single value for entire queryset
total_revenue = Order.objects.filter(
    status='paid'
).aggregate(
    total=Sum('total'),
    avg_order_value=Avg('total'),
    order_count=Count('id'),
    max_order=Max('total')
)
# → {'total': Decimal('152400.00'), 'avg_order_value': ..., ...}

# annotate() — per-object computed field (like SQL GROUP BY)
# "How many orders does each user have?"
users = User.objects.annotate(
    order_count=Count('orders'),
    total_spent=Sum('orders__total'),
    last_order_date=Max('orders__created_at')
).filter(order_count__gt=0).order_by('-total_spent')

for user in users:
    print(f"{user.email}: {user.order_count} orders, ₹{user.total_spent}")

# Monthly revenue report (analytics dashboard)
from django.db.models.functions import TruncMonth

monthly_revenue = Order.objects.filter(
    status='paid',
    created_at__year=2024
).annotate(
    month=TruncMonth('created_at')
).values('month').annotate(
    revenue=Sum('total'),
    order_count=Count('id'),
    avg_value=Avg('total')
).order_by('month')

# Annotate with F expressions (DB-level calculation)
products = Product.objects.annotate(
    revenue=ExpressionWrapper(
        F('orderitem__price_at_purchase') * F('orderitem__quantity'),
        output_field=DecimalField()
    )
).values('name').annotate(total_revenue=Sum('revenue'))

# Conditional annotation
from django.db.models import Case, When, IntegerField

orders = Order.objects.annotate(
    is_high_value=Case(
        When(total__gte=5000, then=Value(1)),
        default=Value(0),
        output_field=IntegerField()
    )
)
high_value_count = orders.aggregate(count=Sum('is_high_value'))
```

</details>

---

<details>
<summary><strong>6. How do custom Managers and QuerySets work? Write one for an e-commerce app.</strong></summary>

### Answer

```python
from django.db import models
from django.utils import timezone

class OrderQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(status='pending')

    def paid(self):
        return self.filter(status='paid')

    def by_user(self, user):
        return self.filter(user=user)

    def recent(self, days=30):
        cutoff = timezone.now() - timezone.timedelta(days=days)
        return self.filter(created_at__gte=cutoff)

    def high_value(self, threshold=5000):
        return self.filter(total__gte=threshold)

    def with_details(self):
        """Optimized queryset for list views."""
        return self.select_related('user').prefetch_related(
            'items__product__category'
        )

    def revenue_total(self):
        from django.db.models import Sum
        return self.filter(status='paid').aggregate(
            total=Sum('total')
        )['total'] or 0

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def pending(self):
        return self.get_queryset().pending()

    def for_dashboard(self, user):
        return self.get_queryset().by_user(user).with_details().recent(90)

class Order(models.Model):
    # ... fields ...
    objects = OrderManager()   # replace default manager

# Usage — chainable!
Order.objects.pending().high_value(10000).recent(7)
Order.objects.by_user(user).paid().with_details()[:10]
Order.objects.for_dashboard(request.user)

# ProductManager — active products only
class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, stock__gt=0)

class Product(models.Model):
    objects = models.Manager()       # default — all products
    active = ActiveProductManager()  # only active in-stock products

Product.active.all()   # only active products
Product.objects.all()  # all products including inactive
```

</details>

---

## Views, URLs & Serializers

<details>
<summary><strong>7. Function-Based Views vs Class-Based Views — when to use each?</strong></summary>

### Answer

```python
# FBV — simple, explicit, readable for custom logic
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def products(request):
    if request.method == 'GET':
        qs = Product.active.all().values('id', 'name', 'price')
        return JsonResponse(list(qs), safe=False)
    elif request.method == 'POST':
        # create product
        ...

# CBV — reusable, DRY, good for standard CRUD
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 20
    queryset = Product.active.all()

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs

# Mixin CBV — combining behaviors
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ['items']
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# When to use what:
# FBV: complex business logic, non-CRUD, custom HTTP methods
# CBV: standard CRUD, reusable patterns, mixins
# DRF ViewSet: APIs with consistent CRUD + router
```

</details>

---

## Authentication & Authorization

<details>
<summary><strong>8. How does JWT authentication work in Django? Walk me through the full flow you implemented.</strong></summary>

### Answer

```python
# JWT Flow:
# 1. User logs in → server creates JWT (signed with secret key)
# 2. Client stores token (localStorage or httpOnly cookie)
# 3. Client sends token in Authorization header with each request
# 4. Server verifies signature, extracts claims, identifies user
# 5. Token expires → client uses refresh token to get new access token

# Using djangorestframework-simplejwt (industry standard)
pip install djangorestframework-simplejwt

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,      # new refresh token on each refresh
    'BLACKLIST_AFTER_ROTATION': True,   # old refresh token blacklisted
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

urlpatterns = [
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/auth/verify/', TokenVerifyView.as_view()),
    path('api/auth/logout/', TokenBlacklistView.as_view()),  # blacklists refresh token
]

# Custom token with extra claims
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.profile.role
        token['full_name'] = user.get_full_name()
        return token

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

# Protected view usage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).with_details()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
```

> 💡 **JWT vs Session-based auth:**
> - JWT: stateless, works for microservices, mobile apps, no DB lookup per request
> - Session: server-side state (DB/Redis lookup per request), easier to invalidate, more secure for web apps

</details>

---

<details>
<summary><strong>9. How did you implement Role-Based Access Control (RBAC) in Django?</strong></summary>

### Answer

```python
# Approach 1: Django's built-in permission system (model-level)
from django.contrib.auth.models import Group, Permission

# Create groups with permissions programmatically
def setup_roles():
    # Admin group
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    admin_group.permissions.set(Permission.objects.all())

    # Manager group
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    manager_group.permissions.set(Permission.objects.filter(
        codename__in=['view_order', 'change_order', 'view_product', 'change_product']
    ))

    # Customer group
    customer_group, _ = Group.objects.get_or_create(name='Customer')
    customer_group.permissions.set(Permission.objects.filter(
        codename__in=['view_order', 'view_product']
    ))

# Assign user to role
user.groups.add(Group.objects.get(name='Manager'))

# Check in view
user.has_perm('orders.change_order')      # True if in a group with this permission
user.has_perm('products.delete_product')   # False for manager

# Approach 2: Custom role field (simpler, flexible)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

# DRF custom permission classes
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.profile.role == 'admin')

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.profile.role in ('manager', 'admin'))

class IsOwnerOrAdmin(BasePermission):
    """Object-level: user can only access their own data."""
    def has_object_permission(self, request, view, obj):
        if request.user.profile.role == 'admin':
            return True
        return obj.user == request.user

# Apply to ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            return [IsManagerOrAdmin()]
        elif self.action in ['retrieve', 'update']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.profile.role in ('admin', 'manager'):
            return Order.objects.all().with_details()
        return Order.objects.filter(user=user).with_details()
```

</details>

---

## Django REST Framework (DRF)

<details>
<summary><strong>10. Explain DRF serializers in depth. How do you handle validation and nested data?</strong></summary>

### Answer

```python
from rest_framework import serializers
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    is_available = serializers.SerializerMethodField()
    price_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'price_display',
            'stock', 'is_available', 'category', 'category_id'
        ]
        read_only_fields = ['slug', 'created_at']

    def get_is_available(self, obj):
        return obj.stock > 0

    def get_price_display(self, obj):
        return f"₹{obj.price:,.2f}"

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value

    def validate(self, data):
        """Object-level validation (cross-field)."""
        if data.get('stock', 0) == 0 and data.get('is_active', True):
            raise serializers.ValidationError(
                "Cannot activate a product with zero stock"
            )
        return data

# Nested writable serializer — Order with OrderItems
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_purchase', 'subtotal']
        read_only_fields = ['price_at_purchase', 'subtotal']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'total', 'status', 'created_at']
        read_only_fields = ['total', 'status', 'created_at']

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must contain at least one item")
        for item in items:
            product = item['product']
            if product.stock < item['quantity']:
                raise serializers.ValidationError(
                    f"Insufficient stock for '{product.name}'. "
                    f"Available: {product.stock}, Requested: {item['quantity']}"
                )
        return items

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total = sum(
            item['product'].price * item['quantity']
            for item in items_data
        )
        order = Order.objects.create(
            user=self.context['request'].user,
            total=total,
            **validated_data
        )
        for item_data in items_data:
            product = item_data['product']
            OrderItem.objects.create(
                order=order,
                price_at_purchase=product.price,   # snapshot current price
                **item_data
            )
            # Reduce stock
            product.stock -= item_data['quantity']
            product.save(update_fields=['stock'])
        return order
```

</details>

---

<details>
<summary><strong>11. What is the difference between APIView, GenericAPIView, and ViewSet? When do you use each?</strong></summary>

### Answer

```python
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework import status

# 1. APIView — maximum flexibility, explicit HTTP methods
class OrderStatsView(APIView):
    """Custom endpoint — doesn't fit standard CRUD."""
    permission_classes = [IsManagerOrAdmin]

    def get(self, request):
        stats = {
            'total_orders': Order.objects.count(),
            'pending': Order.objects.pending().count(),
            'revenue_today': Order.objects.filter(
                created_at__date=timezone.now().date(), status='paid'
            ).aggregate(total=Sum('total'))['total'] or 0
        }
        return Response(stats)

# 2. GenericAPIView + mixins — less code, standard patterns
class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.active.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsManagerOrAdmin()]
        return [IsAuthenticated()]

# 3. ViewSet — most DRY, auto-generates URLs with Router
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.role in ('admin', 'manager'):
            return Order.objects.all().with_details()
        return Order.objects.filter(user=user).with_details()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['list']:
            return OrderListSerializer    # lighter serializer for list
        return OrderDetailSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Custom actions beyond CRUD
    from rest_framework.decorators import action

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response(
                {'error': 'Only pending orders can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = 'cancelled'
        order.save()
        return Response({'status': 'cancelled'})

    @action(detail=False, methods=['get'], url_path='my-orders')
    def my_orders(self, request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

# Router auto-generates URLs
router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')
router.register('products', ProductViewSet, basename='product')

# Generated URLs:
# GET    /api/orders/          → list
# POST   /api/orders/          → create
# GET    /api/orders/{pk}/     → retrieve
# PUT    /api/orders/{pk}/     → update
# PATCH  /api/orders/{pk}/     → partial_update
# DELETE /api/orders/{pk}/     → destroy
# POST   /api/orders/{pk}/cancel/ → cancel_order (custom)
# GET    /api/orders/my-orders/   → my_orders (custom)
```

</details>

---

<details>
<summary><strong>12. How do you implement pagination, filtering, and searching in DRF?</strong></summary>

### Answer

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'myapp.pagination.StandardPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# Custom pagination
from rest_framework.pagination import PageNumberPagination, CursorPagination

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

class CursorBasedPagination(CursorPagination):
    """Better for real-time feeds — no page drift."""
    page_size = 20
    ordering = '-created_at'

# Custom FilterSet
import django_filters

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(
        method='filter_in_stock', label='In Stock'
    )
    category_slug = django_filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Product
        fields = ['category', 'is_active']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)

class ProductViewSet(ModelViewSet):
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name']  # ?search=shirt
    ordering_fields = ['price', 'name', 'created_at', 'stock']
    ordering = ['-created_at']  # default

# Usage:
# GET /api/products/?min_price=500&max_price=2000&in_stock=true&search=shirt&ordering=-price&page=2&page_size=10
```

</details>

---

## Middleware & Signals

<details>
<summary><strong>13. Write a custom middleware for request logging and rate limiting.</strong></summary>

### Answer

```python
import time
import json
import logging
from django.http import JsonResponse
from django.core.cache import cache

logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware:
    """Log every request with timing."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "API Request",
            extra={
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "user_id": getattr(request.user, 'id', None),
                "ip": self._get_client_ip(request),
            }
        )
        response['X-Response-Time'] = f"{duration_ms}ms"
        return response

    def _get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

class RateLimitMiddleware:
    """Sliding window rate limiter using Redis cache."""
    LIMITS = {
        '/api/auth/login/': (5, 300),      # 5 requests per 5 minutes
        '/api/auth/register/': (3, 3600),  # 3 requests per hour
        'default': (100, 60),              # 100 requests per minute
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        limit, window = self.LIMITS.get(
            request.path,
            self.LIMITS['default']
        )
        key = f"rate_limit:{self._get_client_ip(request)}:{request.path}"

        current = cache.get(key, 0)
        if current >= limit:
            return JsonResponse(
                {
                    "error": "Rate limit exceeded",
                    "retry_after": window
                },
                status=429,
                headers={'Retry-After': str(window)}
            )

        # Increment counter
        if current == 0:
            cache.set(key, 1, timeout=window)
        else:
            cache.incr(key)

        response = self.get_response(request)
        response['X-RateLimit-Limit'] = limit
        response['X-RateLimit-Remaining'] = limit - (current + 1)
        return response

    def _get_client_ip(self, request):
        return request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() \
               or request.META.get('REMOTE_ADDR')
```

</details>

---

<details>
<summary><strong>14. How do Django signals work? Give a practical example from an e-commerce backend.</strong></summary>

### Answer

```python
# signals.py
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver, Signal
from django.contrib.auth.models import User

# Built-in signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile whenever a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)
        # Send welcome email via Celery (non-blocking)
        send_welcome_email.delay(instance.id)

@receiver(post_save, sender=Order)
def on_order_status_change(sender, instance, created, **kwargs):
    """Send notifications when order status changes."""
    if not created:
        # Compare with previous value using instance tracker
        if instance.tracker.has_changed('status'):
            prev_status = instance.tracker.previous('status')
            send_order_status_email.delay(
                order_id=instance.id,
                new_status=instance.status,
                prev_status=prev_status
            )

            # Trigger specific logic
            if instance.status == 'paid':
                generate_invoice.delay(instance.id)
            elif instance.status == 'shipped':
                update_tracking.delay(instance.id)

# Custom signal
order_paid = Signal()   # custom signal for payment

# Emit the signal
def process_payment(order, payment_data):
    # ... process payment logic ...
    order_paid.send(
        sender=Order,
        order=order,
        payment_data=payment_data
    )

# Receive the custom signal
@receiver(order_paid)
def on_order_paid(sender, order, payment_data, **kwargs):
    """Runs when an order is paid."""
    order.status = 'paid'
    order.save(update_fields=['status'])
    generate_invoice.delay(order.id)

# apps.py — CRITICAL: connect signals here, not in models.py
class OrdersConfig(AppConfig):
    name = 'orders'

    def ready(self):
        import orders.signals   # noqa: F401

# When NOT to use signals:
# - Core business logic (hard to trace)
# - When a direct method call is simpler
# - In tight loops (signals are synchronous and add overhead)
```

</details>

---

## Caching

<details>
<summary><strong>15. How do you implement caching in Django? Describe a real scenario from your projects.</strong></summary>

### Answer

```python
# settings.py — Redis cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'IGNORE_EXCEPTIONS': True,   # app still works if Redis is down
        },
        'TIMEOUT': 300,    # 5 minutes default
    }
}

# 1. Per-view cache (simple pages)
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

@cache_page(60 * 15)   # 15 minutes
@vary_on_headers('Accept-Language')   # different cache per language
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

# 2. Low-level API — most flexible (used in DRF views)
from django.core.cache import cache

class ProductViewSet(ModelViewSet):
    def list(self, request):
        cache_key = f"products:list:{request.query_params.urlencode()}"
        cached = cache.get(cache_key)

        if cached is not None:
            return Response(cached)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = serializer.data

        cache.set(cache_key, data, timeout=300)
        return self.get_paginated_response(data)

    def retrieve(self, request, pk=None):
        cache_key = f"product:{pk}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)
        response = super().retrieve(request, pk)
        cache.set(cache_key, response.data, timeout=600)
        return response

# 3. Cache invalidation — critical part
@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """Invalidate cache when a product is saved."""
    cache.delete(f"product:{instance.pk}")
    # Delete all list caches (pattern delete — requires Redis)
    from django_redis import get_redis_connection
    redis = get_redis_connection("default")
    keys = redis.keys("*products:list*")
    if keys:
        redis.delete(*keys)

# 4. @cache_page equivalent for DRF
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 5), name='list')
@method_decorator(cache_page(60 * 15), name='retrieve')
class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# 5. Database query caching with select_for_update for race conditions
from django.db import transaction

@transaction.atomic
def reduce_stock(product_id, quantity):
    product = Product.objects.select_for_update().get(pk=product_id)
    if product.stock < quantity:
        raise ValueError("Insufficient stock")
    product.stock -= quantity
    product.save(update_fields=['stock'])
    return product
```

</details>

---

## Performance & Query Optimization

<details>
<summary><strong>16. How do you debug and resolve slow Django ORM queries?</strong></summary>

### Answer

```python
# Step 1: Enable SQL logging in development
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

# Step 2: Django Debug Toolbar — install and use in browser
# Shows: queries, query time, duplicate queries, cache hits
pip install django-debug-toolbar

# Step 3: Programmatically inspect queries
from django.db import connection, reset_queries
from django.conf import settings

settings.DEBUG = True
reset_queries()

# Run the suspect view or function
result = list(Order.objects.filter(status='paid').select_related('user'))

for query in connection.queries:
    print(f"[{query['time']}s] {query['sql'][:200]}")
print(f"Total queries: {len(connection.queries)}")

# Step 4: Use explain() to analyze query plans
queryset = Order.objects.filter(
    status='paid',
    created_at__year=2024
).select_related('user')

print(queryset.explain(verbose=True, analyze=True))
# Shows: Seq Scan vs Index Scan, cost, actual rows

# Step 5: Fix common issues

# Issue 1: N+1 — solved with select_related / prefetch_related (see Q4)

# Issue 2: Full table scan — add index
class Order(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at'], name='order_status_created_idx'),
            models.Index(fields=['user', 'status'], name='order_user_status_idx'),
        ]

# Issue 3: Fetching too many columns
# Bad:
orders = Order.objects.filter(status='pending')   # all columns
# Good:
orders = Order.objects.filter(status='pending').only('id', 'user_id', 'total', 'created_at')
# or:
orders = Order.objects.filter(status='pending').values('id', 'total', 'user__email')

# Issue 4: Count on a big table
# Bad:
total = len(Order.objects.all())   # loads all objects!
# Good:
total = Order.objects.count()      # SELECT COUNT(*) — no data transfer

# Issue 5: exists() vs filter + count
# Bad:
if Order.objects.filter(user=user, status='pending').count() > 0:
# Good:
if Order.objects.filter(user=user, status='pending').exists():  # SELECT 1 LIMIT 1
```

</details>

---

<details>
<summary><strong>17. How does Django's database connection pooling work? How did you configure it for production?</strong></summary>

### Answer

```python
# Django's default: new connection per request, closed after response
# This is fine for low traffic but expensive for high-traffic apps

# Option 1: CONN_MAX_AGE — keep connections alive
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'martify_db',
        'USER': 'db_user',
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
        'CONN_MAX_AGE': 60,   # keep connection alive 60 seconds
        'OPTIONS': {
            'connect_timeout': 10,
            'sslmode': 'require',         # always use SSL
            'application_name': 'martify_api',
        },
    }
}

# Option 2: pgBouncer — external connection pooler (production standard)
# Sits between Django and PostgreSQL, maintains a pool of real connections
# Django connects to pgBouncer, pgBouncer manages PostgreSQL connections

# With pgBouncer, set CONN_MAX_AGE=0 (let pgBouncer handle pooling)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'pgbouncer-host',   # point to pgBouncer, not PostgreSQL directly
        'PORT': '6432',             # pgBouncer default port
        'CONN_MAX_AGE': 0,          # disable Django's own pooling
    }
}

# Option 3: django-db-connection-pool with SQLAlchemy pool
pip install django-db-connection-pool[postgresql]

DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.postgresql',
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 20,
            'RECYCLE': 300,      # recycle connections every 5 min
        }
    }
}
```

</details>

---

## Security

<details>
<summary><strong>18. What security measures did you implement? Walk through each one.</strong></summary>

### Answer

```python
# 1. Django security settings (settings/production.py)
SECRET_KEY = env('SECRET_KEY')   # never hardcode!
DEBUG = False
ALLOWED_HOSTS = ['api.martify.com', 'www.martify.com']

# HTTPS enforcement
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000    # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600   # 1 hour session

# Headers
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# 2. JWT security
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),   # short-lived
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': env('JWT_SECRET_KEY'),   # separate from Django secret
}

# 3. Data encryption — sensitive fields
from django_cryptography.fields import encrypt

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_last_four = models.CharField(max_length=4)
    card_holder_name = encrypt(models.CharField(max_length=100))   # encrypted at rest
    # Never store full card number — use payment gateway tokens (Stripe, Razorpay)

# 4. Input validation — prevent SQL injection
# Django ORM automatically parameterizes queries
# Never do this:
User.objects.raw(f"SELECT * FROM users WHERE email = '{email}'")   # SQL injection!
# Always do this:
User.objects.filter(email=email)   # parameterized, safe
# Or with raw (if needed):
User.objects.raw("SELECT * FROM users WHERE email = %s", [email])

# 5. CSRF protection
# Django auto-protects all POST/PUT/DELETE views with CsrfViewMiddleware
# For APIs using JWT (stateless), exempt from CSRF:
from rest_framework.decorators import api_view
# DRF by default uses SessionAuthentication (needs CSRF) or JWTAuthentication (no CSRF needed)

# 6. Rate limiting — prevent brute force
# See middleware section (Q13)

# 7. Sensitive data masking in logs
import logging

class SensitiveDataFilter(logging.Filter):
    SENSITIVE_FIELDS = {'password', 'token', 'secret', 'card_number'}

    def filter(self, record):
        if hasattr(record, 'extra'):
            for field in self.SENSITIVE_FIELDS:
                if field in record.extra:
                    record.extra[field] = '***REDACTED***'
        return True

# 8. Password policy
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

</details>

---

## Migrations & Database

<details>
<summary><strong>19. How do you handle Django migrations in a team/production environment?</strong></summary>

### Answer

```python
# Team workflow best practices

# 1. Always review generated migrations before committing
python manage.py makemigrations
python manage.py sqlmigrate myapp 0005   # review the SQL

# 2. Data migrations — use RunPython
from django.db import migrations

def populate_order_number(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    for i, order in enumerate(Order.objects.all().order_by('created_at'), 1):
        order.order_number = f"ORD-{str(i).zfill(6)}"
        order.save(update_fields=['order_number'])

def reverse_order_number(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Order.objects.all().update(order_number='')

class Migration(migrations.Migration):
    dependencies = [('orders', '0010_order_order_number')]

    operations = [
        migrations.RunPython(populate_order_number, reverse_order_number)
    ]

# 3. Zero-downtime migration strategy for large tables
# Step 1: Add nullable column (no lock)
migrations.AddField(
    model_name='product',
    name='sku',
    field=models.CharField(max_length=50, null=True, blank=True)   # nullable first
)
# Deploy → backfill data (Q19 RunPython above) → make it required in next migration

# 4. Production: always backup before migrating
pg_dump mydb > backup_before_migration.sql
python manage.py migrate

# 5. Check for unapplied migrations in CI/CD
python manage.py migrate --check   # exits with non-zero if unapplied migrations exist

# 6. Squash migrations when they pile up
python manage.py squashmigrations orders 0001 0020

# 7. Avoid circular dependencies between apps
# Structure dependencies explicitly:
class Migration(migrations.Migration):
    dependencies = [
        ('products', '0005_product_sku'),
        ('users', '0003_userprofile'),
    ]
```

</details>

---

## Testing in Django

<details>
<summary><strong>20. How do you test Django REST API endpoints? Walk through a complete test suite.</strong></summary>

### Answer

```python
import pytest
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
import factory

# factory_boy — clean test fixtures
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@test.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    stock = 50
    is_active = True

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    total = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    status = 'pending'

# Full test suite
@pytest.mark.django_db
class TestOrderAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.manager = UserFactory()
        UserProfile.objects.create(user=self.manager, role='manager')
        self.product = ProductFactory(stock=20, price=999)
        self.client.force_authenticate(user=self.user)

    def test_create_order_success(self):
        url = reverse('order-list')
        payload = {
            'items': [
                {'product': self.product.id, 'quantity': 2}
            ]
        }
        response = self.client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Order.objects.count() == 1
        assert response.data['total'] == '1998.00'
        # Verify stock reduced
        self.product.refresh_from_db()
        assert self.product.stock == 18

    def test_create_order_insufficient_stock(self):
        payload = {'items': [{'product': self.product.id, 'quantity': 100}]}
        response = self.client.post(reverse('order-list'), payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Insufficient stock' in str(response.data)
        assert Order.objects.count() == 0   # no order created

    def test_unauthenticated_request_returns_401(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('order-list'))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_only_sees_own_orders(self):
        other_user = UserFactory()
        OrderFactory(user=other_user)
        OrderFactory(user=self.user)

        response = self.client.get(reverse('order-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['user'] == self.user.id

    def test_cancel_pending_order(self):
        order = OrderFactory(user=self.user, status='pending')
        url = reverse('order-cancel', kwargs={'pk': order.pk})
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK
        order.refresh_from_db()
        assert order.status == 'cancelled'

    def test_cannot_cancel_paid_order(self):
        order = OrderFactory(user=self.user, status='paid')
        url = reverse('order-cancel', kwargs={'pk': order.pk})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch('orders.tasks.send_order_confirmation.delay')
    def test_order_creation_triggers_email_task(self, mock_task):
        payload = {'items': [{'product': self.product.id, 'quantity': 1}]}
        self.client.post(reverse('order-list'), payload, format='json')
        mock_task.assert_called_once()

    def test_query_count_on_order_list(self):
        OrderFactory.create_batch(10, user=self.user)
        from django.db import connection, reset_queries
        from django.conf import settings
        settings.DEBUG = True
        reset_queries()

        self.client.get(reverse('order-list'))

        query_count = len(connection.queries)
        assert query_count <= 5, f"Too many queries: {query_count}"
```

</details>

---

## Django in Production

<details>
<summary><strong>21. How do you deploy a Django application with Docker and CI/CD?</strong></summary>

### Answer

```dockerfile
# Dockerfile — multi-stage build
FROM python:3.11-slim as builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=myapp.settings.production

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "myapp.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--timeout", "120", \
     "--access-logfile", "-"]
```

```yaml
# docker-compose.yml
version: '3.9'

services:
  web:
    build: .
    command: gunicorn myapp.wsgi:application --bind 0.0.0.0:8000 --workers 4
    env_file: .env
    depends_on:
      - db
      - redis
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  celery:
    build: .
    command: celery -A myapp worker --loglevel=info --concurrency=4
    env_file: .env
    depends_on:
      - db
      - redis

  celery-beat:
    build: .
    command: celery -A myapp beat --loglevel=info
    env_file: .env

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/staticfiles
    depends_on:
      - web
```

```yaml
# .github/workflows/ci.yml — CI/CD pipeline (Jenkins equivalent)
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready --health-interval 10s

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run linting
        run: |
          flake8 .
          black --check .

      - name: Run type checks
        run: mypy .

      - name: Check migrations
        run: python manage.py migrate --check

      - name: Run tests with coverage
        run: pytest --cov=. --cov-report=xml --cov-fail-under=80

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Build and push Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker push myapp:${{ github.sha }}

      - name: Deploy to server
        run: |
          ssh deploy@server "
            docker pull myapp:${{ github.sha }}
            docker-compose up -d --no-deps web celery
            docker-compose exec web python manage.py migrate --noinput
          "
```

</details>

---

## Scenario-Based Questions

<details>
<summary><strong>22. Your API endpoint is slow under high load. Walk me through how you'd diagnose and fix it.</strong></summary>

### Answer

**Step 1: Reproduce and measure**
```python
# Add timing to identify where time is spent
import time
import logging
logger = logging.getLogger(__name__)

def slow_view(request):
    t0 = time.perf_counter()
    orders = Order.objects.filter(user=request.user)
    t1 = time.perf_counter()
    logger.info(f"DB query: {(t1-t0)*1000:.2f}ms")

    serialized = OrderSerializer(orders, many=True).data
    t2 = time.perf_counter()
    logger.info(f"Serialization: {(t2-t1)*1000:.2f}ms")

    return Response(serialized)
```

**Step 2: Check query count (usually the culprit)**
```python
from django.test.utils import CaptureQueriesContext
from django.db import connection

with CaptureQueriesContext(connection) as ctx:
    response = client.get('/api/orders/')
print(f"Queries: {len(ctx)}")   # if > 5-10, you have N+1
```

**Step 3: Fix based on root cause**
```python
# If N+1: add select_related/prefetch_related
# If full table scan: add indexes
# If data volume: add pagination + caching
# If serialization is slow: use .values() instead of model instances

class OrderViewSet(ModelViewSet):
    def list(self, request):
        # Cache the list
        cache_key = f"orders:user:{request.user.id}:list"
        data = cache.get(cache_key)
        if data:
            return Response(data)

        # Optimized queryset
        orders = Order.objects.filter(
            user=request.user
        ).select_related(
            'user'
        ).prefetch_related(
            'items__product'
        ).only(
            'id', 'status', 'total', 'created_at', 'user_id'
        )

        serializer = OrderListSerializer(orders, many=True)
        data = serializer.data
        cache.set(cache_key, data, timeout=60)
        return Response(data)
```

</details>

---

<details>
<summary><strong>23. How would you design a real-time order tracking system in Django?</strong></summary>

### Answer

```python
# Option 1: Polling (simplest)
# Client polls /api/orders/{id}/status/ every 5 seconds
# Simple but inefficient for scale

# Option 2: Django Channels (WebSockets) — real-time
# pip install channels channels-redis

# settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('redis', 6379)]},
    }
}

# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.room_name = f"order_{self.order_id}"

        # Verify ownership
        user = self.scope['user']
        order = await self.get_order(self.order_id)
        if not order or order.user_id != user.id:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    # Receive message from channel layer (sent by server)
    async def order_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'order_update',
            'status': event['status'],
            'message': event['message'],
        }))

# Send update from anywhere in Django (e.g., in a signal)
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify_order_update(order_id, status, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"order_{order_id}",
        {
            'type': 'order_update',
            'status': status,
            'message': message,
        }
    )

# In signal
@receiver(post_save, sender=Order)
def broadcast_order_status(sender, instance, **kwargs):
    if instance.tracker.has_changed('status'):
        notify_order_update(
            instance.id,
            instance.status,
            f"Your order is now {instance.status}"
        )

# Option 3: Server-Sent Events (simpler than WebSockets for one-way updates)
from django.http import StreamingHttpResponse

def order_status_stream(request, order_id):
    def event_stream():
        last_status = None
        while True:
            order = Order.objects.get(pk=order_id)
            if order.status != last_status:
                last_status = order.status
                yield f"data: {json.dumps({'status': order.status})}\n\n"
            time.sleep(2)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
```

</details>

---

<details>
<summary><strong>24. How do you handle background tasks (like email notifications) in Django?</strong></summary>

### Answer

```python
# Celery + Redis — production-grade task queue

# celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
app = Celery('myapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# settings.py
CELERY_BROKER_URL = env('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_TASK_ALWAYS_EAGER = False   # True in tests
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,    # retry after 60 seconds
    autoretry_for=(Exception,),
    retry_backoff=True,         # exponential backoff
)
def send_order_confirmation_email(self, order_id):
    try:
        order = Order.objects.select_related('user').get(pk=order_id)
        from django.core.mail import EmailMultiAlternatives
        from django.template.loader import render_to_string

        html_content = render_to_string('emails/order_confirmation.html', {'order': order})
        msg = EmailMultiAlternatives(
            subject=f"Order Confirmed — #{order.id}",
            body=f"Your order #{order.id} has been confirmed.",
            from_email='orders@martify.com',
            to=[order.user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info(f"Confirmation email sent for order {order_id}")
    except Order.DoesNotExist:
        logger.error(f"Order {order_id} not found — aborting")
        return    # don't retry if order doesn't exist
    except Exception as exc:
        logger.warning(f"Email failed for order {order_id}: {exc}. Retrying...")
        raise self.retry(exc=exc)

# Periodic tasks — Celery Beat
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-daily-sales-report': {
        'task': 'orders.tasks.generate_daily_report',
        'schedule': crontab(hour=8, minute=0),
    },
    'cleanup-expired-carts': {
        'task': 'cart.tasks.cleanup_expired_carts',
        'schedule': crontab(hour=2, minute=0),  # 2am daily
    },
    'update-product-stock': {
        'task': 'products.tasks.sync_stock',
        'schedule': crontab(minute='*/15'),  # every 15 minutes
    },
}

# Trigger from view (non-blocking)
def checkout(request):
    order = create_order(request)
    send_order_confirmation_email.delay(order.id)   # fire and forget
    return Response({'order_id': order.id}, status=201)
```

</details>

---

*Remember: For every answer, connect it to your actual experience at Codeclouds and your Martify/Micro-data analyst projects.*
