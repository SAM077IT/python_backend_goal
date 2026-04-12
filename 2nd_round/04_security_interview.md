# Security Interview Prep — JWT, RBAC, Encryption & Backend Security
> Tailored to your resume: JWT authentication, role-based access control, data encryption

---

## Table of Contents
- [JWT Authentication](#jwt-authentication)
- [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
- [Data Encryption](#data-encryption)
- [API Security](#api-security)
- [OWASP & Common Vulnerabilities](#owasp--common-vulnerabilities)
- [Scenario-Based Questions](#scenario-based-questions)

---

## JWT Authentication

<details>
<summary><strong>1. How does JWT work internally? What are its components?</strong></summary>

### Answer

A JWT (JSON Web Token) has three base64url-encoded parts separated by dots:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20iLCJleHAiOjE3MDk5MjE2MDB9.abc123signature
      HEADER                                    PAYLOAD                                                                   SIGNATURE
```

**Header:**
```json
{
  "alg": "HS256",   // signing algorithm
  "typ": "JWT"
}
```

**Payload (claims):**
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "role": "admin",
  "iat": 1709835200,   // issued at
  "exp": 1709921600,   // expiry
  "jti": "unique-id"  // JWT ID — for blacklisting
}
```

**Signature:**
```
HMACSHA256(
    base64url(header) + "." + base64url(payload),
    secret_key
)
```

**Verification process:**
```python
import jwt
import base64
import hmac
import hashlib

SECRET_KEY = "your-super-secret-key"

# How Django/simplejwt verifies a token:
def verify_jwt(token: str) -> dict:
    try:
        # 1. Split token
        header_b64, payload_b64, signature_b64 = token.split('.')

        # 2. Verify signature (tamper detection)
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(
            SECRET_KEY.encode(), signing_input, hashlib.sha256
        ).digest()
        actual_sig = base64.urlsafe_b64decode(signature_b64 + '==')

        if not hmac.compare_digest(expected_sig, actual_sig):
            raise jwt.InvalidSignatureError("Signature verification failed")

        # 3. Decode payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # 4. Check expiry (jwt.decode does this automatically)
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise AuthError(f"Invalid token: {e}")

# Generate tokens
def create_tokens(user):
    from datetime import datetime, timedelta

    access_payload = {
        'user_id': user.id,
        'email': user.email,
        'role': user.profile.role,
        'type': 'access',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=15),
    }
    refresh_payload = {
        'user_id': user.id,
        'type': 'refresh',
        'jti': str(uuid.uuid4()),   # unique ID for blacklisting
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=7),
    }
    return {
        'access': jwt.encode(access_payload, SECRET_KEY, algorithm='HS256'),
        'refresh': jwt.encode(refresh_payload, SECRET_KEY, algorithm='HS256'),
    }
```

**JWT vs Sessions:**
| | JWT | Session |
|---|---|---|
| State | Stateless (no server-side storage) | Stateful (DB/Redis lookup per request) |
| Scalability | Works across multiple servers/microservices | Sticky sessions or shared Redis needed |
| Revocation | Hard (must use blacklist or short expiry) | Easy (delete session record) |
| Size | Larger (base64-encoded payload) | Small (session ID only) |
| Use case | APIs, mobile apps, microservices | Traditional web apps |

</details>

---

<details>
<summary><strong>2. How do you handle JWT token refresh and revocation?</strong></summary>

### Answer

```python
# Token refresh flow:
# 1. Access token expires (15 min) → client sends refresh token
# 2. Server verifies refresh token → issues new access token
# 3. Old refresh token is blacklisted (rotation)

# djangorestframework-simplejwt handles this
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

# Logout — blacklist the refresh token
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()   # adds to OutstandingToken blacklist
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception:
            return Response({"error": "Invalid token"}, status=400)

# Force logout all sessions for a user (e.g., password change, security breach)
def invalidate_all_tokens(user):
    # Blacklist all outstanding refresh tokens for this user
    OutstandingToken.objects.filter(user=user).update(
        blacklistedtoken=BlacklistedToken()
    )
    # Or simpler with simplejwt:
    for token in OutstandingToken.objects.filter(user=user):
        BlacklistedToken.objects.get_or_create(token=token)

# Alternative: Redis-based token version
# Store a "token version" per user in Redis
# Include version in JWT payload
# On each request, verify token version matches

import redis
r = redis.Redis()

def get_token_version(user_id: int) -> int:
    version = r.get(f"token_version:{user_id}")
    return int(version) if version else 0

def increment_token_version(user_id: int):
    """Call this on password change, logout all, security breach."""
    r.incr(f"token_version:{user_id}")

# In token generation
def create_access_token(user):
    payload = {
        'user_id': user.id,
        'token_version': get_token_version(user.id),   # include version
        'exp': datetime.utcnow() + timedelta(minutes=15),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# In token verification middleware
def verify_token_version(payload):
    user_id = payload['user_id']
    token_version = payload.get('token_version', 0)
    current_version = get_token_version(user_id)
    if token_version != current_version:
        raise AuthError("Token invalidated — please log in again")
```

</details>

---

## Role-Based Access Control (RBAC)

<details>
<summary><strong>3. Design a complete RBAC system for a multi-tenant SaaS backend.</strong></summary>

### Answer

```python
# Three-layer RBAC: Roles → Permissions → Resources

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "order:create"
    resource = models.CharField(max_length=50)            # e.g., "order"
    action = models.CharField(max_length=50)              # e.g., "create"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission, blank=True)
    is_system_role = models.BooleanField(default=False)

    def has_permission(self, permission_name: str) -> bool:
        return self.permissions.filter(name=permission_name).exists()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    # Optional: tenant for multi-tenant
    tenant = models.ForeignKey('Tenant', null=True, on_delete=models.CASCADE)

# Default roles setup
def create_default_roles():
    # Admin: all permissions
    admin_role, _ = Role.objects.get_or_create(name='admin', is_system_role=True)
    admin_role.permissions.set(Permission.objects.all())

    # Manager: order management + product view
    manager_role, _ = Role.objects.get_or_create(name='manager')
    manager_role.permissions.set(Permission.objects.filter(
        name__in=[
            'order:view', 'order:update', 'order:list',
            'product:view', 'product:list', 'product:create', 'product:update',
            'user:view', 'user:list',
        ]
    ))

    # Customer: own resources only
    customer_role, _ = Role.objects.get_or_create(name='customer')
    customer_role.permissions.set(Permission.objects.filter(
        name__in=['order:create', 'order:view', 'product:view', 'product:list']
    ))

# DRF Permission classes
from rest_framework.permissions import BasePermission

class HasPermission(BasePermission):
    """Generic permission class — check if user's role has a specific permission."""
    def __init__(self, permission_name: str):
        self.permission_name = permission_name

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.profile.role.has_permission(self.permission_name)
        except UserProfile.DoesNotExist:
            return False

class IsOwnerOrHasPermission(BasePermission):
    """Allow access if user owns the object OR has the required permission."""
    def __init__(self, permission_name: str, owner_field: str = 'user'):
        self.permission_name = permission_name
        self.owner_field = owner_field

    def has_object_permission(self, request, view, obj):
        # Check ownership
        if getattr(obj, self.owner_field) == request.user:
            return True
        # Check role permission
        try:
            return request.user.profile.role.has_permission(self.permission_name)
        except UserProfile.DoesNotExist:
            return False

# ViewSet with granular permissions
class OrderViewSet(ModelViewSet):
    def get_permissions(self):
        permission_map = {
            'list': [HasPermission('order:list')],
            'retrieve': [IsOwnerOrHasPermission('order:view')],
            'create': [HasPermission('order:create')],
            'update': [HasPermission('order:update')],
            'partial_update': [HasPermission('order:update')],
            'destroy': [HasPermission('order:delete')],
        }
        return permission_map.get(self.action, [IsAuthenticated()])

# Cache permissions for performance
from django.core.cache import cache

def get_user_permissions(user_id: int) -> set:
    cache_key = f"user_permissions:{user_id}"
    permissions = cache.get(cache_key)
    if permissions is None:
        try:
            profile = UserProfile.objects.select_related(
                'role'
            ).prefetch_related(
                'role__permissions'
            ).get(user_id=user_id)
            permissions = set(
                profile.role.permissions.values_list('name', flat=True)
            )
            cache.set(cache_key, permissions, timeout=300)   # cache 5 min
        except UserProfile.DoesNotExist:
            permissions = set()
    return permissions

# Invalidate on role change
@receiver(post_save, sender=UserProfile)
def invalidate_permission_cache(sender, instance, **kwargs):
    cache.delete(f"user_permissions:{instance.user_id}")
```

</details>

---

## Data Encryption

<details>
<summary><strong>4. How do you handle encryption of sensitive data in a Django backend?</strong></summary>

### Answer

```python
# Principle: Encrypt at rest, decrypt only when needed, never log sensitive data

# 1. django-cryptography — field-level encryption
from django_cryptography.fields import encrypt

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_last_four = models.CharField(max_length=4)     # safe to store plain
    card_holder_name = encrypt(models.CharField(max_length=200))   # encrypted at rest
    # Never store full card number — use payment gateway tokens instead
    gateway_token = encrypt(models.CharField(max_length=255))      # Stripe customer ID

class UserProfile(models.Model):
    national_id = encrypt(models.CharField(max_length=20, blank=True))
    phone = encrypt(models.CharField(max_length=15))

# 2. Hashing passwords and PINs (one-way — can't decrypt)
from django.contrib.auth.hashers import make_password, check_password

hashed = make_password("user_pin_1234")   # bcrypt/PBKDF2
is_valid = check_password("user_pin_1234", hashed)   # True

# 3. Manual encryption for custom fields (Fernet/AES)
from cryptography.fernet import Fernet
import base64
import os
from django.conf import settings

class EncryptionService:
    def __init__(self):
        key = settings.ENCRYPTION_KEY.encode()
        self.cipher = Fernet(key)

    def encrypt(self, plaintext: str) -> str:
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        return self.cipher.decrypt(ciphertext.encode()).decode()

encryption = EncryptionService()

# 4. Data masking — for logs and APIs
def mask_card_number(card: str) -> str:
    return '*' * 12 + card[-4:]   # ************1234

def mask_email(email: str) -> str:
    local, domain = email.split('@')
    return local[:2] + '***@' + domain   # sa***@gmail.com

# 5. Encryption key management
# Never hardcode keys — use AWS KMS or environment variables

# AWS KMS integration
import boto3

class KMSEncryptionService:
    def __init__(self):
        self.client = boto3.client('kms', region_name='ap-south-1')
        self.key_id = settings.KMS_KEY_ID

    def encrypt(self, plaintext: str) -> bytes:
        response = self.client.encrypt(
            KeyId=self.key_id,
            Plaintext=plaintext.encode()
        )
        return response['CiphertextBlob']

    def decrypt(self, ciphertext: bytes) -> str:
        response = self.client.decrypt(CiphertextBlob=ciphertext)
        return response['Plaintext'].decode()

# 6. HTTPS — encryption in transit
# Handled by Nginx + SSL/TLS certificate (Let's Encrypt or AWS ACM)
# Django settings enforce HTTPS:
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
```

</details>

---

## API Security

<details>
<summary><strong>5. What API security measures do you implement in production?</strong></summary>

### Answer

```python
# 1. Input validation — never trust client data
from rest_framework import serializers
from django.core.validators import RegexValidator

class OrderCreateSerializer(serializers.ModelSerializer):
    # Strict type + format validation
    phone = serializers.CharField(
        validators=[RegexValidator(r'^\+?[1-9]\d{9,14}$', 'Invalid phone')]
    )
    quantity = serializers.IntegerField(min_value=1, max_value=100)

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value, is_active=True).exists():
            raise serializers.ValidationError("Product not found or unavailable")
        return value

# 2. Rate limiting (see middleware in Django file)

# 3. CORS — control which origins can call your API
pip install django-cors-headers

INSTALLED_APPS = ['corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]

CORS_ALLOWED_ORIGINS = [
    "https://martify.com",
    "https://www.martify.com",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']

# 4. SQL injection prevention
# Django ORM auto-parameterizes — always use ORM or parameterized queries
# NEVER: f"SELECT * FROM users WHERE email = '{email}'"  ← injection!
# ALWAYS: User.objects.filter(email=email)               ← safe

# 5. XSS prevention
# Django templates auto-escape HTML
# DRF returns JSON — not susceptible to XSS in responses
# Validate file uploads (content type, extension, size)

def validate_upload(file):
    ALLOWED_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
    MAX_SIZE_MB = 5

    if file.content_type not in ALLOWED_TYPES:
        raise ValidationError(f"File type {file.content_type} not allowed")

    if file.size > MAX_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File size exceeds {MAX_SIZE_MB}MB limit")

    # Verify file signature (magic bytes) — don't trust content_type header
    header = file.read(32)
    file.seek(0)
    if not (header[:2] == b'\xff\xd8' or    # JPEG
            header[:4] == b'\x89PNG'):        # PNG
        raise ValidationError("Invalid file content")

# 6. Sensitive data in responses — never expose internal details
class ErrorResponse:
    @staticmethod
    def create(status_code: int, message: str, user_facing=True) -> dict:
        """
        Return user-friendly errors, log detailed ones internally.
        """
        if not user_facing:
            message = "An error occurred. Please try again."
        return {"error": {"code": status_code, "message": message}}

# In DRF — custom exception handler
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Standardize error format
        response.data = {
            "error": {
                "status": response.status_code,
                "message": _get_error_message(response.data),
                "timestamp": timezone.now().isoformat(),
            }
        }
    return response

# 7. API versioning
urlpatterns = [
    path('api/v1/', include('api.v1.urls')),
    path('api/v2/', include('api.v2.urls')),
]
# Or header-based: Accept: application/vnd.myapp.v2+json

# 8. Audit logging — track all sensitive operations
class AuditLog(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=100)
    resource_id = models.IntegerField(null=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

def audit(action, resource, resource_id=None, **metadata):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            result = func(request, *args, **kwargs)
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action=action,
                resource=resource,
                resource_id=resource_id,
                ip_address=get_client_ip(request),
                metadata=metadata
            )
            return result
        return wrapper
    return decorator

@audit('delete', 'user')
def delete_user(request, user_id):
    ...
```

</details>

---

## OWASP & Common Vulnerabilities

<details>
<summary><strong>6. What are the OWASP Top 10 and how does Django protect against them?</strong></summary>

### Answer

| OWASP Risk | Django Protection | Additional Steps |
|---|---|---|
| **A01: Broken Access Control** | Permission system, `@login_required` | Implement RBAC, test all endpoints |
| **A02: Cryptographic Failures** | PBKDF2 password hashing, HTTPS | Encrypt sensitive fields, rotate keys |
| **A03: Injection** | ORM parameterizes queries | Never use raw string formatting in queries |
| **A04: Insecure Design** | N/A — architecture choice | Threat model, code reviews |
| **A05: Security Misconfiguration** | `check --deploy` command | Disable DEBUG, restrict ALLOWED_HOSTS |
| **A06: Vulnerable Components** | N/A | `pip audit`, Dependabot alerts |
| **A07: Auth Failures** | PBKDF2, session management | Implement MFA, rate limiting on login |
| **A08: Software Integrity** | N/A | Verify package checksums, use lockfiles |
| **A09: Logging Failures** | Logging framework | Structured logging, don't log secrets |
| **A10: SSRF** | N/A | Validate URLs, whitelist external hosts |

```python
# A03: Injection — always use ORM or parameterized
# Vulnerable:
def search_UNSAFE(request):
    q = request.GET.get('q')
    users = User.objects.raw(f"SELECT * FROM users WHERE name LIKE '%{q}%'")  # INJECTION!

# Safe:
def search_SAFE(request):
    q = request.GET.get('q', '')
    users = User.objects.filter(name__icontains=q)  # ORM parameterizes automatically

# A07: Authentication failures — brute force protection
from django.contrib.auth import authenticate, login
from django.core.cache import cache

def login_view(request):
    ip = get_client_ip(request)
    cache_key = f"login_attempts:{ip}"
    attempts = cache.get(cache_key, 0)

    if attempts >= 5:
        lockout_time = cache.ttl(cache_key)
        return JsonResponse(
            {"error": f"Too many attempts. Try again in {lockout_time}s"},
            status=429
        )

    user = authenticate(request, **request.data)
    if user is None:
        cache.set(cache_key, attempts + 1, timeout=300)   # 5 min lockout window
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    cache.delete(cache_key)   # reset on success
    tokens = create_tokens(user)
    return JsonResponse(tokens)

# A10: SSRF — validate URLs before fetching
import ipaddress
from urllib.parse import urlparse

def validate_url_not_internal(url: str):
    parsed = urlparse(url)
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise ValueError(f"URL {url} points to internal network — blocked")
    except ValueError:
        pass   # hostname, not IP — further DNS resolution check needed

ALLOWED_EXTERNAL_HOSTS = {'api.supplier.com', 'cdn.images.com'}

def fetch_external(url: str):
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_EXTERNAL_HOSTS:
        raise PermissionError(f"Host {parsed.hostname} not in whitelist")
    return requests.get(url, timeout=10)
```

</details>

---

## Scenario-Based Questions

<details>
<summary><strong>7. A user reports their account was compromised. What do you do?</strong></summary>

### Answer

```python
# Immediate response — incident handling

# Step 1: Invalidate ALL sessions and tokens for this user
def emergency_lockdown_user(user_id: int, reason: str):
    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=user_id)

        # 1. Force password reset
        user.set_unusable_password()   # prevents any login
        user.save(update_fields=['password'])

        # 2. Blacklist all JWT refresh tokens
        from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
        for token in OutstandingToken.objects.filter(user=user):
            token.blacklist()

        # 3. Delete all sessions
        from django.contrib.sessions.models import Session
        Session.objects.filter(
            session_data__contains=user.pk
        ).delete()

        # 4. Increment token version (invalidates all access tokens)
        r.incr(f"token_version:{user_id}")

        # 5. Log the security event
        AuditLog.objects.create(
            user=user,
            action='emergency_lockdown',
            resource='user',
            resource_id=user_id,
            metadata={'reason': reason, 'timestamp': timezone.now().isoformat()}
        )

    # 6. Send notification to user
    send_security_alert_email.delay(user_id, reason)

    # 7. Alert security team
    send_slack_alert(f"🚨 User {user_id} account locked: {reason}")

# Step 2: Investigate
def investigate_user_activity(user_id: int, hours_back: int = 24):
    since = timezone.now() - timedelta(hours=hours_back)
    return {
        'login_history': LoginLog.objects.filter(user_id=user_id, timestamp__gte=since),
        'api_requests': AuditLog.objects.filter(user_id=user_id, timestamp__gte=since),
        'data_accessed': AuditLog.objects.filter(
            user_id=user_id, timestamp__gte=since, action__in=['view', 'download', 'export']
        ),
    }
```

</details>

---

<details>
<summary><strong>8. How do you prevent your API from being scraped or abused?</strong></summary>

### Answer

```python
# Multi-layer defense strategy

# 1. Authentication — require valid token for all endpoints
# (JWT-based auth from your resume)

# 2. Rate limiting (sliding window per user/IP)
class AdvancedRateLimiter:
    """Per-user rate limiting with different tiers."""
    LIMITS = {
        'anonymous': (20, 60),      # 20 req/min
        'customer': (100, 60),      # 100 req/min
        'premium': (500, 60),       # 500 req/min
        'api_key': (1000, 60),      # 1000 req/min
    }

    def get_user_tier(self, request):
        if not request.user.is_authenticated:
            return 'anonymous'
        return getattr(request.user.profile, 'tier', 'customer')

# 3. Pagination — limit response size
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 100,   # never return more than 100
}

# 4. Response throttling — add delays for suspicious patterns
# 5. Bot detection — check User-Agent, request patterns

# 6. API key rotation + monitoring
class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=64, unique=True, default=generate_api_key)
    name = models.CharField(max_length=100)   # "Mobile App", "Integration"
    last_used = models.DateTimeField(null=True)
    request_count = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True)
    allowed_ips = ArrayField(models.CharField(max_length=45), default=list)   # IP whitelist

# 7. Honeypot endpoints — detect scrapers
urlpatterns += [
    path('api/admin-secret-data/', honeypot_view),   # flag any request to this
]

def honeypot_view(request):
    ip = get_client_ip(request)
    logger.warning(f"Honeypot triggered", extra={"ip": ip, "path": request.path})
    block_ip_temporarily(ip, duration=3600)
    return Response({"data": []})   # return empty — don't reveal it's a trap
```

</details>

