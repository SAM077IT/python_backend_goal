# 🧪 Python Testing Mastery — Calsoft Interview Prep
> **Stack:** Python · Django · DRF · pytest · GitHub Actions  
> **Project anchor:** Martify (Django e-commerce + Stripe + Blog)  
> **Coverage:** High Priority → Medium Priority → CI/CD Integration

---

## 📋 Table of Contents

1. [pytest vs unittest](#1-pytest-vs-unittest)
2. [pytest Fixtures](#2-pytest-fixtures)
3. [Mocking & Patching](#3-mocking--patching)
4. [Asserting Exceptions](#4-asserting-exceptions)
5. [DRF API Client Testing](#5-drf-api-client-testing)
6. [Database Isolation in Django](#6-database-isolation-in-django)
7. [CI/CD Pipeline Integration](#7-cicd-pipeline-integration)
8. [Code Coverage & Quality Gates](#8-code-coverage--quality-gates)

---

## 1. pytest vs unittest

### 📖 Definition

| Feature | `unittest` | `pytest` |
|---|---|---|
| Origin | Built into Python stdlib | Third-party (`pip install pytest`) |
| Style | Class-based (`class TestFoo(unittest.TestCase)`) | Function-based (plain `def test_foo():`) |
| Assertions | Custom methods: `assertEqual`, `assertTrue`, `assertRaises` | Native Python `assert` — pytest rewrites it for rich output |
| Fixtures | `setUp` / `tearDown` on the class | `@pytest.fixture` — composable, reusable, scoped |
| Discovery | Finds `test*.py` files and `Test*` classes | Finds any `test_*.py` or `*_test.py`, any `test_*` function |
| Plugins | Limited | Enormous ecosystem: `pytest-django`, `pytest-cov`, `pytest-mock` |

**When to use which?**
- `unittest` — maintaining legacy codebases or when no extra dependency is allowed.
- `pytest` — all modern projects. Less boilerplate, better output, fixture DI.

---

### 🎯 Why Python Developers Need This

If you are interviewing for any backend Python role in 2024+, **not knowing pytest is a red flag**. Here is exactly why this matters day-to-day:

| Real-world situation | Why pytest matters |
|---|---|
| You write a discount function and push to `main` | CI runs `pytest` automatically — broken logic is caught before it ships |
| A colleague changes `calculate_discount()` | Your tests break immediately, alerting them that they broke something |
| You onboard to a new codebase | `pytest -v` gives you a living document of every feature the system has |
| A bug is reported in production | You write a test that reproduces it, fix the code, and the test proves it's fixed |
| Code review | Reviewer asks "where are the tests?" — having them ends that conversation |

**The professional reality:** Every Django, FastAPI, and Flask project you will encounter uses pytest. `unittest` still exists in legacy codebases (pre-2015 projects), and knowing the difference shows maturity. But the job you are interviewing for will run `pytest` in its CI pipeline — that is the tool to master.

---

### 🛠️ Best Way to Use It

**1. Configure pytest globally in `pytest.ini` or `pyproject.toml`** — so you never need to type flags every time:

```ini
# pytest.ini (place at project root)
[pytest]
DJANGO_SETTINGS_MODULE = martify.settings.test
python_files = test_*.py *_test.py
python_functions = test_*
addopts = -v --tb=short            # verbose + short traceback by default
testpaths = tests                  # only look here, not the whole project
```

**2. Use `@pytest.mark.parametrize` to test multiple inputs with one function** — never copy-paste test bodies:

```python
import pytest
from martify.orders.utils import calculate_discount

@pytest.mark.parametrize("total, expected", [
    (600,   60.0),   # above threshold
    (1000, 100.0),   # high value
    (400,    0.0),   # below threshold
    (500,    0.0),   # exact threshold (no discount)
    (500.01, 50.0),  # just above threshold
])
def test_discount_parametrized(total, expected):
    assert calculate_discount(total) == expected
```

This replaces **5 separate functions** with 1. pytest runs each row as its own test and reports failures individually.

**3. Keep test files mirrored to source files:**

```
martify/
  orders/
    utils.py          ← source
    services.py       ← source
tests/
  orders/
    test_utils.py     ← mirrors utils.py
    test_services.py  ← mirrors services.py
```

**4. Run only the tests you care about** while developing:

```bash
pytest tests/orders/test_utils.py          # just one file
pytest -k "discount"                       # tests whose name contains "discount"
pytest -x                                  # stop at the first failure
pytest --lf                               # re-run only last-failed tests
```

---

### 💡 Educative Example

**Scenario:** Testing a `calculate_discount()` function in Martify that applies a 10% discount to orders above ₹500.

```python
# martify/orders/utils.py

def calculate_discount(order_total: float) -> float:
    """Apply 10% discount if order total exceeds 500."""
    if order_total <= 0:
        raise ValueError("Order total must be positive.")
    if order_total > 500:
        return round(order_total * 0.10, 2)
    return 0.0
```

**unittest style:**

```python
# tests/test_utils_unittest.py
import unittest
from martify.orders.utils import calculate_discount

class TestCalculateDiscount(unittest.TestCase):

    def test_discount_applied_above_threshold(self):
        self.assertEqual(calculate_discount(600), 60.0)

    def test_no_discount_below_threshold(self):
        self.assertEqual(calculate_discount(400), 0.0)

    def test_raises_on_zero_total(self):
        with self.assertRaises(ValueError):
            calculate_discount(0)

if __name__ == "__main__":
    unittest.main()
```

**pytest style (same logic, far less noise):**

```python
# tests/test_utils_pytest.py
import pytest
from martify.orders.utils import calculate_discount

def test_discount_applied_above_threshold():
    assert calculate_discount(600) == 60.0

def test_no_discount_below_threshold():
    assert calculate_discount(400) == 0.0

def test_discount_exact_boundary():
    # Boundary: exactly 500 gets no discount (strictly greater than)
    assert calculate_discount(500) == 0.0

def test_discount_just_above_boundary():
    assert calculate_discount(500.01) == 50.0
```

---

### ✅ Test Cases

```python
# tests/test_utils_pytest.py  — FULL TEST FILE

import pytest
from martify.orders.utils import calculate_discount

# --- Happy path ---
def test_discount_high_value_order():
    assert calculate_discount(1000) == 100.0

def test_discount_returns_float():
    result = calculate_discount(600)
    assert isinstance(result, float)

# --- Edge cases ---
def test_discount_exact_500_gets_nothing():
    assert calculate_discount(500) == 0.0

def test_discount_500_01_gets_discount():
    assert calculate_discount(500.01) == 50.0

def test_no_discount_below_threshold():
    assert calculate_discount(250) == 0.0

# --- Error cases ---
def test_raises_on_zero():
    with pytest.raises(ValueError):
        calculate_discount(0)

def test_raises_on_negative():
    with pytest.raises(ValueError):
        calculate_discount(-100)
```

> **Interview tip:** When asked "why pytest?", lead with: *"Pytest uses plain assert statements and rewrites them at collection time, so when a test fails you get a detailed diff — no need to choose between assertEqual, assertIn, assertGreater, etc."*

---

### 📚 More Examples

**Example A — Parametrize with IDs (readable test names in output):**

```python
# tests/orders/test_utils_parametrize.py

import pytest
from martify.orders.utils import calculate_discount

@pytest.mark.parametrize("total, expected", [
    pytest.param(600,    60.0,  id="above-threshold"),
    pytest.param(400,     0.0,  id="below-threshold"),
    pytest.param(500,     0.0,  id="exact-boundary"),
    pytest.param(1000,  100.0,  id="high-value"),
    pytest.param(500.01, 50.0,  id="one-paisa-above"),
], )
def test_discount_parametrized(total, expected):
    # pytest output: test_discount_parametrized[above-threshold] PASSED ✓
    assert calculate_discount(total) == expected
```

**Example B — Testing a slug generator (string utility, common in Django):**

```python
# martify/products/utils.py

import re

def slugify_product_name(name: str) -> str:
    """Convert 'Men\'s Kurta & Pyjama' → 'mens-kurta-pyjama'"""
    name = name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)   # remove special chars
    name = re.sub(r"[\s_]+", "-", name)    # spaces/underscores → dash
    return name
```

```python
# tests/products/test_utils.py

import pytest
from martify.products.utils import slugify_product_name

# unittest version — notice the repetition:
# class TestSlugify(unittest.TestCase):
#     def test_basic(self): self.assertEqual(slugify_product_name("Kurta"), "kurta")
#     def test_space(self): self.assertEqual(slugify_product_name("Men Kurta"), "men-kurta")
#     ... 5 more methods ...

# pytest + parametrize — clean and DRY:
@pytest.mark.parametrize("input_name, expected_slug", [
    ("Kurta",                  "kurta"),
    ("Men Kurta",              "men-kurta"),
    ("Men's Kurta & Pyjama",   "mens-kurta-pyjama"),
    ("  Summer   Collection ", "summer-collection"),
    ("Shirt_v2",               "shirt-v2"),
])
def test_slugify_product_name(input_name, expected_slug):
    assert slugify_product_name(input_name) == expected_slug

def test_slugify_returns_string():
    assert isinstance(slugify_product_name("Kurta"), str)

def test_slugify_empty_string():
    assert slugify_product_name("") == ""
```

**Example C — unittest vs pytest failure output comparison:**

```
# unittest failure output (unhelpful):
FAIL: test_discount_applied_above_threshold
AssertionError: 50.0 != 60.0

# pytest failure output (immediately tells you the problem):
FAILED tests/test_utils.py::test_discount_applied_above_threshold
>       assert calculate_discount(600) == 60.0
E       assert 50.0 == 60.0
E        +  where 50.0 = calculate_discount(600)
```

This is WHY you use pytest — the diff output is diagnostic, not just an error count.

---

---

## 2. pytest Fixtures

### 📖 Definition

A **fixture** is a reusable piece of setup/teardown logic decorated with `@pytest.fixture`. It is **injected as a function argument** into any test that declares it — no inheritance needed.

Key concepts:

| Concept | Explanation |
|---|---|
| `@pytest.fixture` | Marks a function as a fixture |
| `yield` | Code before `yield` = **setup**; code after `yield` = **teardown** |
| `scope` | How long the fixture lives: `"function"` (default) · `"class"` · `"module"` · `"session"` |
| `conftest.py` | Special file where shared fixtures live — auto-discovered by pytest |

---

### 🎯 Why Python Developers Need This

Imagine you have 30 tests that all need a logged-in user and a product. Without fixtures, each test writes the same 5 lines of setup — 150 lines of duplicate code. When the `User` model adds a required field, you update **150 places** instead of **1**.

| Pain without fixtures | How fixtures solve it |
|---|---|
| Copy-pasted `setUp` blocks in every test | Define once in `conftest.py`, inject everywhere |
| Tests pollute each other's state | `yield` + scope guarantee clean state |
| Expensive setup (DB, API client) repeated every test | `scope="session"` runs it once for the whole suite |
| 50-line test files for simple tests | Tests are 5 lines; setup is the fixture's job |

**Real cost:** At Calsoft, if a new developer joins and your test file has 200 lines of copy-pasted `setUp` code, they waste a day understanding it. If you have composable fixtures in `conftest.py`, they understand the structure in 10 minutes.

---

### 🛠️ Best Way to Use It

**Rule 1: One fixture = one responsibility.** Don't build a "god fixture" that creates everything. Compose small fixtures:

```python
# Good — composable
@pytest.fixture
def user(db): ...

@pytest.fixture
def product(db): ...

@pytest.fixture
def order(user, product): ...   # depends on the two above

# Bad — monolithic
@pytest.fixture
def everything(db):
    user = User.objects.create(...)
    product = Product.objects.create(...)
    order = Order.objects.create(...)
    return user, product, order   # tests have to unpack this tuple
```

**Rule 2: Use the narrowest scope.** Default to `"function"`. Only go wider when setup is provably expensive:

```
function  → fresh per test           (99% of the time)
module    → shared across a file     (test_reports.py all need the same big dataset)
session   → shared across whole run  (Stripe client, read-only seed data)
```

**Rule 3: Name fixtures for what they ARE, not how they're built:**

```python
# Good
@pytest.fixture
def admin_user(db): ...    # "I get an admin user"

# Bad
@pytest.fixture
def create_admin(db): ...  # Sounds like a helper function, not a noun
```

**Rule 4: Use `yield` for any cleanup:**

```python
@pytest.fixture
def temp_upload_dir(tmp_path):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    yield upload_dir          # test runs here
    # Cleanup is automatic because tmp_path is managed by pytest
    # But for things like open files, DB connections: close them here
```

---

### 💡 Educative Example

**Scenario:** Martify needs tests for a `CartService` that requires a pre-built user and an empty cart.

```python
# martify/cart/services.py

class CartService:
    def __init__(self, user):
        self.user = user
        self.items = []

    def add_item(self, product_id: int, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        self.items.append({"product_id": product_id, "quantity": quantity})

    def total_items(self) -> int:
        return sum(item["quantity"] for item in self.items)

    def clear(self):
        self.items = []
```

```python
# tests/conftest.py  — shared fixtures for the whole test suite

import pytest
from martify.cart.services import CartService

class FakeUser:
    """Lightweight stand-in for Django's User model in unit tests."""
    def __init__(self, id=1, email="sami@martify.com"):
        self.id = id
        self.email = email

@pytest.fixture
def fake_user():
    """Provide a minimal user object. No DB needed."""
    return FakeUser()

@pytest.fixture
def cart_service(fake_user):
    """
    Provide a fresh CartService per test.
    Because scope defaults to 'function', each test gets its own instance.
    """
    service = CartService(user=fake_user)
    yield service                  # <-- SETUP complete, hand control to test
    service.clear()                # <-- TEARDOWN: runs after the test finishes
```

```python
# tests/test_cart_service.py

def test_add_item_increases_count(cart_service):
    cart_service.add_item(product_id=42, quantity=3)
    assert cart_service.total_items() == 3

def test_multiple_items_sum_correctly(cart_service):
    cart_service.add_item(product_id=1, quantity=2)
    cart_service.add_item(product_id=2, quantity=5)
    assert cart_service.total_items() == 7

def test_cart_starts_empty(cart_service):
    # Because scope='function', each test gets a fresh cart
    assert cart_service.total_items() == 0
```

**Session-scoped fixture** (expensive setup done once):

```python
# tests/conftest.py — for a real Django DB connection or a Stripe test client

@pytest.fixture(scope="session")
def stripe_test_client():
    """
    Create a Stripe client once for the entire test session.
    Expensive objects (API clients, DB connections) belong in session scope.
    """
    import stripe
    stripe.api_key = "sk_test_..."
    yield stripe
    # No teardown needed — Stripe client is stateless
```

---

### ✅ Test Cases

```python
# tests/test_cart_fixtures.py

import pytest
from martify.cart.services import CartService

def test_fixture_injection_works(cart_service):
    """Fixture is injected by name — no self, no setUp needed."""
    assert cart_service is not None

def test_teardown_resets_cart(cart_service):
    """Proves scope='function' isolation: adding here doesn't bleed into next test."""
    cart_service.add_item(product_id=99, quantity=10)
    assert cart_service.total_items() == 10
    # After this test, cart_service.clear() is called by fixture teardown

def test_next_test_sees_empty_cart(cart_service):
    """This test should start with 0 items — proves teardown ran."""
    assert cart_service.total_items() == 0

def test_fake_user_email(cart_service):
    assert cart_service.user.email == "sami@martify.com"

def test_raises_on_zero_quantity(cart_service):
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart_service.add_item(product_id=1, quantity=0)
```

> **Interview tip:** *"I put all shared fixtures in `conftest.py` so they're auto-discovered. For heavyweight fixtures like DB connections or API clients I use `scope='session'` to avoid paying the setup cost on every single test."*

---

### 📚 More Examples

**Example A — Chaining fixtures (an order that depends on a user and a product):**

```python
# tests/conftest.py

import pytest
from django.contrib.auth.models import User
from martify.products.models import Product
from martify.orders.models import Order

@pytest.fixture
def customer(db):
    """A plain, non-admin customer account."""
    return User.objects.create_user(username="customer", password="pass")

@pytest.fixture
def kurta_product(db):
    """A real product row in the test DB."""
    return Product.objects.create(name="Kurta", price=499.0, stock=100)

@pytest.fixture
def pending_order(customer, kurta_product):
    """
    An order for the customer — depends on both fixtures above.
    pytest resolves the dependency graph automatically.
    """
    return Order.objects.create(user=customer, status="pending")
```

```python
# tests/orders/test_order_status.py

@pytest.mark.django_db
def test_pending_order_is_not_shipped(pending_order):
    assert pending_order.status != "shipped"

@pytest.mark.django_db
def test_order_user_is_customer(pending_order, customer):
    assert pending_order.user == customer
```

**Example B — Using pytest's built-in `tmp_path` fixture for file upload tests:**

```python
# martify/products/services.py

import csv, pathlib

class ProductImportService:
    def import_from_csv(self, filepath: str) -> int:
        """Read a CSV and return the count of rows imported."""
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return len(rows)
```

```python
# tests/products/test_import_service.py
# tmp_path is a built-in pytest fixture — no conftest.py needed

from martify.products.services import ProductImportService

def test_import_reads_correct_row_count(tmp_path):
    # Arrange: create a temp CSV file — no real filesystem cleanup needed
    csv_file = tmp_path / "products.csv"
    csv_file.write_text("name,price,stock\nKurta,499,50\nSaree,1299,20\n")

    svc = ProductImportService()
    count = svc.import_from_csv(str(csv_file))

    assert count == 2

def test_import_empty_csv_returns_zero(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("name,price,stock\n")   # header only, no rows

    svc = ProductImportService()
    assert svc.import_from_csv(str(csv_file)) == 0
```

**Example C — Parametrized fixture to test across multiple user roles:**

```python
# tests/conftest.py

@pytest.fixture(params=["anonymous", "customer", "admin"])
def user_by_role(request, db):
    """
    Runs each test THREE TIMES — once per role.
    Useful for permission tests that need to cover all access levels.
    """
    if request.param == "anonymous":
        return None
    if request.param == "customer":
        return User.objects.create_user(username="cust", password="p")
    if request.param == "admin":
        return User.objects.create_superuser(username="adm", email="a@m.com", password="p")
```

```python
# tests/products/test_permissions.py

from rest_framework.test import APIClient

@pytest.mark.django_db
def test_product_list_accessible_by_all_roles(user_by_role):
    client = APIClient()
    if user_by_role:
        client.force_authenticate(user=user_by_role)
    response = client.get("/api/products/")
    # All roles (including anonymous) should be able to list products
    assert response.status_code == 200
    # pytest runs this test 3 times automatically — anonymous, customer, admin
```

---

---

## 3. Mocking & Patching

### 📖 Definition

**Mocking** replaces a real object (DB call, HTTP request, file I/O) with a fake one during a test so that:
- Tests run **fast** (no real network/DB)
- Tests are **deterministic** (no flaky external state)
- You test **your** code, not your dependencies

| Tool | Use case |
|---|---|
| `unittest.mock.patch` | Decorator / context manager to swap out an object by import path |
| `unittest.mock.MagicMock` | A smart fake object that records calls and returns configurable values |
| `pytest-mock` plugin | Provides the `mocker` fixture — cleaner pytest-native API |
| `mocker.patch()` | Same as `unittest.mock.patch` but auto-undone after each test |

**The golden rule of patching:** patch where the object is **used**, not where it is **defined**.

```
# Wrong:  unittest.mock.patch("stripe.Charge.create")
# Right:  unittest.mock.patch("martify.payments.services.stripe.Charge.create")
```

---

### 🎯 Why Python Developers Need This

Without mocking, your test suite becomes an integration test suite — slow, flaky, and expensive:

| External call without a mock | Real-world consequence |
|---|---|
| `stripe.Charge.create(...)` | Charges a real card. Costs money. Fails when Stripe is down. |
| `boto3.client("s3").upload_file(...)` | Uploads to real S3. Costs money. Fails without internet. |
| `openai.ChatCompletion.create(...)` | Costs per token. Rate-limited. Non-deterministic output. |
| `django.core.mail.send_mail(...)` | Sends real emails to real users during test runs. |
| `datetime.now()` | Time-sensitive logic is impossible to test deterministically. |

**The professional mindset:** A good test suite must run in under 60 seconds on any machine, offline, for free. Mocking makes that possible. When an interviewer asks "how do you test your Stripe integration?" — the answer is mocking, not "we have a test Stripe account".

---

### 🛠️ Best Way to Use It

**Rule 1: Prefer `mocker` (pytest-mock) over `@patch` decorator stacking:**

```python
# Bad — stacking @patch decorators reverses the argument order (confusing)
@patch("martify.services.send_mail")
@patch("martify.services.stripe.Charge.create")
def test_checkout(mock_stripe, mock_mail):   # reversed! stripe is first arg
    ...

# Good — mocker fixture: no decorator stacking, no argument order confusion
def test_checkout(mocker):
    mock_stripe = mocker.patch("martify.services.stripe.Charge.create")
    mock_mail   = mocker.patch("martify.services.send_mail")
    ...
```

**Rule 2: Always assert the mock WAS called (not just that it was set up):**

```python
# Weak — you mocked it but never verified it ran
mock_create.return_value = {"id": "ch_123"}
service.charge(500, "tok_visa")
# (no assertion on mock — test doesn't prove charge was attempted)

# Strong — verify it was called with the right arguments
mock_create.assert_called_once_with(amount=50000, currency="inr", ...)
```

**Rule 3: Use `side_effect` for error paths and dynamic responses:**

```python
# Raise an exception
mock.side_effect = stripe.error.CardError(...)

# Return different values on successive calls
mock.side_effect = [first_response, second_response, Exception("third call fails")]
```

**Rule 4: Use `MagicMock` for chained call objects (like ORM querysets):**

```python
# ORM: Order.objects.filter(status="pending").order_by("-created_at")
mock_qs = MagicMock()
mock_objects.filter.return_value = mock_qs
mock_qs.order_by.return_value = [order1, order2]
```

---

### 💡 Educative Example

**Scenario A:** Martify's `PaymentService.charge()` calls Stripe. You must not make real API calls in tests.

```python
# martify/payments/services.py

import stripe

class PaymentService:
    def charge(self, amount_paise: int, token: str) -> dict:
        """
        Charge a customer via Stripe.
        amount_paise: amount in smallest currency unit (paise for INR).
        """
        try:
            charge = stripe.Charge.create(
                amount=amount_paise,
                currency="inr",
                source=token,
                description="Martify Order",
            )
            return {"success": True, "charge_id": charge["id"]}
        except stripe.error.CardError as e:
            return {"success": False, "error": str(e)}
```

**Test with `unittest.mock.patch` (decorator style):**

```python
# tests/test_payment_service.py

from unittest.mock import patch, MagicMock
from martify.payments.services import PaymentService

@patch("martify.payments.services.stripe.Charge.create")   # patch at point of USE
def test_charge_returns_success(mock_stripe_create):
    # Arrange: configure what the fake Stripe should return
    mock_stripe_create.return_value = {"id": "ch_test_123"}

    service = PaymentService()
    result = service.charge(amount_paise=50000, token="tok_visa")

    # Assert on your code's return value
    assert result["success"] is True
    assert result["charge_id"] == "ch_test_123"

    # Assert Stripe was called with the right args
    mock_stripe_create.assert_called_once_with(
        amount=50000,
        currency="inr",
        source="tok_visa",
        description="Martify Order",
    )
```

**Test with `pytest-mock` (cleaner, no decorator stacking):**

```python
# tests/test_payment_service_mocker.py

import stripe
from martify.payments.services import PaymentService

def test_charge_handles_card_error(mocker):
    # Arrange: make Stripe raise a CardError
    mock_create = mocker.patch("martify.payments.services.stripe.Charge.create")
    mock_create.side_effect = stripe.error.CardError(
        message="Your card was declined.",
        param="card",
        code="card_declined",
    )

    service = PaymentService()
    result = service.charge(amount_paise=50000, token="tok_chargeDeclined")

    # Assert graceful degradation
    assert result["success"] is False
    assert "declined" in result["error"].lower()
```

**Scenario B:** Mocking a Django ORM call — no DB needed.

```python
# martify/orders/services.py

from martify.orders.models import Order

class OrderService:
    def get_pending_orders(self, user_id: int):
        return list(Order.objects.filter(user_id=user_id, status="pending"))
```

```python
# tests/test_order_service.py

from unittest.mock import patch, MagicMock
from martify.orders.services import OrderService

@patch("martify.orders.services.Order.objects")
def test_get_pending_orders_filters_correctly(mock_objects):
    # Arrange: fake queryset chain
    fake_orders = [MagicMock(id=1), MagicMock(id=2)]
    mock_objects.filter.return_value = fake_orders

    service = OrderService()
    result = service.get_pending_orders(user_id=7)

    # Assert filter was called with the right kwargs
    mock_objects.filter.assert_called_once_with(user_id=7, status="pending")
    assert len(result) == 2
```

---

### ✅ Test Cases

```python
# tests/test_mocking_suite.py

import pytest
import stripe
from unittest.mock import patch, MagicMock, call
from martify.payments.services import PaymentService

def test_stripe_not_called_twice(mocker):
    mock_create = mocker.patch("martify.payments.services.stripe.Charge.create")
    mock_create.return_value = {"id": "ch_abc"}

    PaymentService().charge(50000, "tok_visa")
    assert mock_create.call_count == 1

def test_amount_passed_correctly(mocker):
    mock_create = mocker.patch("martify.payments.services.stripe.Charge.create")
    mock_create.return_value = {"id": "ch_xyz"}

    PaymentService().charge(amount_paise=99900, token="tok_amex")
    args, kwargs = mock_create.call_args
    assert kwargs["amount"] == 99900

def test_currency_is_always_inr(mocker):
    mock_create = mocker.patch("martify.payments.services.stripe.Charge.create")
    mock_create.return_value = {"id": "ch_inr"}

    PaymentService().charge(10000, "tok_in")
    _, kwargs = mock_create.call_args
    assert kwargs["currency"] == "inr"

def test_failed_charge_returns_success_false(mocker):
    mock_create = mocker.patch("martify.payments.services.stripe.Charge.create")
    mock_create.side_effect = stripe.error.CardError("Declined", "card", "declined")

    result = PaymentService().charge(500, "tok_bad")
    assert result["success"] is False

def test_failed_charge_has_error_key(mocker):
    mock_create = mocker.patch("martify.payments.services.stripe.Charge.create")
    mock_create.side_effect = stripe.error.CardError("Declined", "card", "declined")

    result = PaymentService().charge(500, "tok_bad")
    assert "error" in result
```

> **Interview tip:** *"I always patch at the point of use. If `payments/services.py` imports `stripe`, I patch `martify.payments.services.stripe.Charge.create`, not `stripe.Charge.create`. That's a common mistake that causes patches to not take effect."*

---

### 📚 More Examples

**Example A — Mocking `send_mail` so tests never send real emails:**

```python
# martify/orders/services.py

from django.core.mail import send_mail

class OrderConfirmationService:
    def send_confirmation(self, order_id: int, customer_email: str) -> bool:
        try:
            send_mail(
                subject=f"Order #{order_id} Confirmed — Martify",
                message=f"Thank you! Your order {order_id} has been placed.",
                from_email="noreply@martify.com",
                recipient_list=[customer_email],
            )
            return True
        except Exception:
            return False
```

```python
# tests/orders/test_confirmation_service.py

from martify.orders.services import OrderConfirmationService

def test_sends_email_to_correct_address(mocker):
    mock_send = mocker.patch("martify.orders.services.send_mail")

    svc = OrderConfirmationService()
    svc.send_confirmation(order_id=42, customer_email="sami@martify.com")

    # Verify send_mail was called with the right recipient
    mock_send.assert_called_once()
    _, kwargs = mock_send.call_args
    assert "sami@martify.com" in kwargs["recipient_list"]

def test_subject_contains_order_id(mocker):
    mock_send = mocker.patch("martify.orders.services.send_mail")

    OrderConfirmationService().send_confirmation(99, "buyer@test.com")

    _, kwargs = mock_send.call_args
    assert "99" in kwargs["subject"]

def test_returns_false_when_mail_fails(mocker):
    mock_send = mocker.patch("martify.orders.services.send_mail")
    mock_send.side_effect = Exception("SMTP server down")

    result = OrderConfirmationService().send_confirmation(1, "a@b.com")
    assert result is False
```

**Example B — Mocking `datetime.now()` for time-sensitive logic:**

```python
# martify/orders/utils.py

from datetime import datetime

def is_flash_sale_active() -> bool:
    """Flash sale runs every day from 12:00 to 14:00."""
    now = datetime.now()
    return 12 <= now.hour < 14
```

```python
# tests/orders/test_flash_sale.py

from datetime import datetime
from martify.orders.utils import is_flash_sale_active

def test_flash_sale_active_at_noon(mocker):
    # Freeze time at 12:30
    mock_now = mocker.patch("martify.orders.utils.datetime")
    mock_now.now.return_value = datetime(2024, 6, 1, 12, 30)

    assert is_flash_sale_active() is True

def test_flash_sale_inactive_at_3pm(mocker):
    mock_now = mocker.patch("martify.orders.utils.datetime")
    mock_now.now.return_value = datetime(2024, 6, 1, 15, 0)

    assert is_flash_sale_active() is False

def test_flash_sale_inactive_at_midnight(mocker):
    mock_now = mocker.patch("martify.orders.utils.datetime")
    mock_now.now.return_value = datetime(2024, 6, 1, 0, 0)

    assert is_flash_sale_active() is False
```

**Example C — Mocking S3 boto3 upload (no AWS account needed in tests):**

```python
# martify/products/services.py

import boto3

class ProductImageService:
    def upload_image(self, file_path: str, bucket: str, key: str) -> str:
        s3 = boto3.client("s3")
        s3.upload_file(file_path, bucket, key)
        return f"https://{bucket}.s3.amazonaws.com/{key}"
```

```python
# tests/products/test_image_service.py

from martify.products.services import ProductImageService

def test_upload_returns_correct_url(mocker):
    # Mock the entire boto3.client call
    mock_s3 = mocker.MagicMock()
    mocker.patch("martify.products.services.boto3.client", return_value=mock_s3)

    svc = ProductImageService()
    url = svc.upload_image("/tmp/kurta.jpg", "martify-images", "products/kurta.jpg")

    assert url == "https://martify-images.s3.amazonaws.com/products/kurta.jpg"

def test_upload_file_called_with_correct_args(mocker):
    mock_s3 = mocker.MagicMock()
    mocker.patch("martify.products.services.boto3.client", return_value=mock_s3)

    ProductImageService().upload_image("/tmp/img.jpg", "my-bucket", "img.jpg")

    mock_s3.upload_file.assert_called_once_with("/tmp/img.jpg", "my-bucket", "img.jpg")

def test_upload_uses_s3_client(mocker):
    """Ensure we're connecting to S3 (not SNS, SQS, etc.)"""
    mock_client_factory = mocker.patch("martify.products.services.boto3.client")
    mock_client_factory.return_value = mocker.MagicMock()

    ProductImageService().upload_image("/tmp/a.jpg", "b", "k")

    mock_client_factory.assert_called_once_with("s3")
```

**Example D — Mocking a chained ORM queryset:**

```python
# martify/orders/services.py

from martify.orders.models import Order

def get_recent_pending_orders(user_id: int):
    return list(
        Order.objects.filter(user_id=user_id, status="pending")
                     .order_by("-created_at")[:5]
    )
```

```python
# tests/orders/test_services.py

from unittest.mock import MagicMock, patch
from martify.orders.services import get_recent_pending_orders

@patch("martify.orders.services.Order.objects")
def test_recent_pending_orders_filters_by_user(mock_objects):
    # Build the queryset chain: .filter().order_by()[...]
    mock_qs = MagicMock()
    mock_qs.order_by.return_value.__getitem__ = MagicMock(return_value=[])
    mock_objects.filter.return_value = mock_qs

    get_recent_pending_orders(user_id=7)

    # Confirm the filter used the right arguments
    mock_objects.filter.assert_called_once_with(user_id=7, status="pending")

@patch("martify.orders.services.Order.objects")
def test_recent_pending_orders_limits_to_five(mock_objects):
    fake_orders = [MagicMock() for _ in range(3)]
    mock_qs = MagicMock()
    mock_qs.order_by.return_value.__getitem__ = MagicMock(return_value=fake_orders)
    mock_objects.filter.return_value = mock_qs

    result = get_recent_pending_orders(user_id=1)
    assert len(result) == 3
```

---

---

## 4. Asserting Exceptions

### 📖 Definition

`pytest.raises()` is a **context manager** that asserts a specific exception is raised within its block. If the exception is NOT raised, the test fails.

```python
with pytest.raises(ExceptionType):
    code_that_should_raise()

# Also capture exception info for deeper assertion:
with pytest.raises(ExceptionType) as exc_info:
    code_that_should_raise()

assert "some message" in str(exc_info.value)
```

You can also use the `match` parameter (regex) inline:

```python
with pytest.raises(ValueError, match="must be positive"):
    calculate_discount(-10)
```

---

### 🎯 Why Python Developers Need This

Error handling code is the most under-tested part of any codebase. Developers test "it works when everything is fine" — but production failures almost always happen in the error paths.

| Untested scenario | Production consequence |
|---|---|
| `create_product(price=-50)` not validated | Negative-price products appear in the store |
| `get_order(id="abc")` not guarded with `TypeError` | Unhandled 500 error instead of a clean 400 response |
| DRF serializer `validate_` methods not tested | Invalid data silently accepted |
| Custom exception not raised on auth failure | Wrong HTTP status code returned (200 instead of 403) |

**Key insight:** If you never test your `except` blocks and `raise` statements, they might never run at all — dead code sitting in your codebase giving a false sense of safety.

---

### 🛠️ Best Way to Use It

**Rule 1: Always use `pytest.raises()` as a context manager, never as a decorator.**

**Rule 2: Check the exception message when it is user-facing:**

```python
# Weak — only checks the exception TYPE
with pytest.raises(ValueError):
    create_product(price=-1)

# Strong — checks type AND message (matches a regex)
with pytest.raises(ValueError, match="greater than zero"):
    create_product(price=-1)
```

**Rule 3: Use `exc_info` to inspect the full exception object:**

```python
with pytest.raises(ValueError) as exc_info:
    create_product(price=-1)

error = exc_info.value
assert "greater than zero" in str(error)
assert exc_info.type is ValueError     # EXACTLY ValueError, not a subclass
```

**Rule 4: Write a positive test alongside every exception test** to rule out false positives:

```python
# Together these two tests prove the guard works correctly:
def test_valid_price_does_not_raise():
    svc.create_product("Shirt", 299.0, 10)   # must NOT raise

def test_negative_price_raises():
    with pytest.raises(ValueError):
        svc.create_product("Shirt", -1.0, 10)  # MUST raise
```

---

### 💡 Educative Example

**Scenario:** Martify's `ProductService` raises specific errors for invalid inputs.

```python
# martify/products/services.py

class ProductService:
    def create_product(self, name: str, price: float, stock: int):
        if not name or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock < 0:
            raise TypeError("Stock cannot be negative.")
        return {"name": name, "price": price, "stock": stock}

    def get_product(self, product_id: int):
        if not isinstance(product_id, int):
            raise TypeError(f"product_id must be int, got {type(product_id).__name__}")
        if product_id <= 0:
            raise LookupError(f"No product with id={product_id}")
        return {"id": product_id, "name": "Sample"}
```

```python
# tests/test_product_service_exceptions.py

import pytest
from martify.products.services import ProductService

@pytest.fixture
def svc():
    return ProductService()

# --- Basic exception assertion ---
def test_empty_name_raises_value_error(svc):
    with pytest.raises(ValueError):
        svc.create_product(name="", price=299.0, stock=10)

# --- Assert exception message with match (regex) ---
def test_empty_name_error_message(svc):
    with pytest.raises(ValueError, match="cannot be empty"):
        svc.create_product(name="   ", price=299.0, stock=10)

# --- Capture exc_info for detailed inspection ---
def test_negative_price_error_details(svc):
    with pytest.raises(ValueError) as exc_info:
        svc.create_product(name="Shirt", price=-50.0, stock=5)

    assert "greater than zero" in str(exc_info.value)
    assert exc_info.type is ValueError

# --- Wrong type raises TypeError ---
def test_negative_stock_raises_type_error(svc):
    with pytest.raises(TypeError):
        svc.create_product(name="Shirt", price=299.0, stock=-1)

# --- LookupError for bad ID ---
def test_invalid_product_id_raises(svc):
    with pytest.raises(LookupError, match="No product with id=0"):
        svc.get_product(0)
```

---

### ✅ Test Cases

```python
# tests/test_exceptions_full.py

import pytest
from martify.products.services import ProductService

@pytest.fixture
def svc():
    return ProductService()

def test_whitespace_name_is_also_invalid(svc):
    with pytest.raises(ValueError):
        svc.create_product(name="   ", price=100.0, stock=5)

def test_zero_price_raises(svc):
    with pytest.raises(ValueError, match="greater than zero"):
        svc.create_product(name="Hat", price=0, stock=3)

def test_string_product_id_raises_type_error(svc):
    with pytest.raises(TypeError):
        svc.get_product("abc")

def test_negative_product_id_raises_lookup_error(svc):
    with pytest.raises(LookupError):
        svc.get_product(-5)

def test_valid_product_does_not_raise(svc):
    # Sanity: ensure no false positives
    result = svc.create_product("Kurta", 499.0, 20)
    assert result["name"] == "Kurta"

def test_exception_type_is_exact(svc):
    with pytest.raises(ValueError) as exc_info:
        svc.create_product("", 100, 1)
    # Ensure it's exactly ValueError, not a subclass
    assert exc_info.type is ValueError
```

> **Interview tip:** *"I always check both the exception type AND the message. Catching a broad `Exception` in a test is a smell — it could mask bugs where the wrong error is raised."*

---

### 📚 More Examples

**Example A — Testing a custom exception hierarchy (professional pattern):**

```python
# martify/exceptions.py

class MartifyBaseError(Exception):
    """All Martify custom exceptions inherit from this."""
    pass

class InsufficientStockError(MartifyBaseError):
    def __init__(self, product_name: str, requested: int, available: int):
        self.product_name = product_name
        self.requested = requested
        self.available = available
        super().__init__(
            f"Cannot fulfil {requested} units of '{product_name}' — only {available} in stock."
        )

class PaymentDeclinedError(MartifyBaseError):
    pass
```

```python
# martify/cart/services.py

from martify.exceptions import InsufficientStockError

class CartCheckoutService:
    def checkout(self, product_name: str, quantity: int, stock: int):
        if quantity > stock:
            raise InsufficientStockError(product_name, quantity, stock)
        return {"status": "ok"}
```

```python
# tests/cart/test_checkout_exceptions.py

import pytest
from martify.cart.services import CartCheckoutService
from martify.exceptions import InsufficientStockError, MartifyBaseError

@pytest.fixture
def svc():
    return CartCheckoutService()

def test_raises_insufficient_stock_when_over_limit(svc):
    with pytest.raises(InsufficientStockError):
        svc.checkout("Kurta", quantity=10, stock=5)

def test_error_message_is_descriptive(svc):
    with pytest.raises(InsufficientStockError, match="Kurta"):
        svc.checkout("Kurta", quantity=10, stock=5)

def test_error_attributes_are_correct(svc):
    """Access exception attributes — not just the message string."""
    with pytest.raises(InsufficientStockError) as exc_info:
        svc.checkout("Saree", quantity=3, stock=1)

    err = exc_info.value
    assert err.product_name == "Saree"
    assert err.requested == 3
    assert err.available == 1

def test_custom_exception_is_subclass_of_base(svc):
    """Prove the hierarchy — catch it as MartifyBaseError too."""
    with pytest.raises(MartifyBaseError):   # parent catches child
        svc.checkout("Dupatta", quantity=99, stock=0)

def test_no_exception_when_stock_sufficient(svc):
    result = svc.checkout("Kurta", quantity=2, stock=50)
    assert result["status"] == "ok"
```

**Example B — Testing Django model `clean()` validation:**

```python
# martify/products/models.py

from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name  = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def clean(self):
        if self.price <= 0:
            raise ValidationError({"price": "Price must be greater than zero."})
        if self.stock < 0:
            raise ValidationError({"stock": "Stock cannot be negative."})
```

```python
# tests/products/test_product_model.py

import pytest
from django.core.exceptions import ValidationError
from martify.products.models import Product

@pytest.mark.django_db
def test_negative_price_fails_validation():
    product = Product(name="Kurta", price=-100, stock=10)
    with pytest.raises(ValidationError) as exc_info:
        product.clean()
    assert "price" in exc_info.value.message_dict

@pytest.mark.django_db
def test_negative_stock_fails_validation():
    product = Product(name="Kurta", price=499, stock=-5)
    with pytest.raises(ValidationError) as exc_info:
        product.clean()
    assert "stock" in exc_info.value.message_dict

@pytest.mark.django_db
def test_valid_product_passes_validation():
    product = Product(name="Kurta", price=499, stock=50)
    product.clean()  # Must NOT raise — no assertion needed if no exception = pass
```

**Example C — Testing multiple inputs that ALL should raise (parametrize + raises):**

```python
# tests/orders/test_discount_errors.py

import pytest
from martify.orders.utils import calculate_discount

@pytest.mark.parametrize("bad_input", [
    0,        # zero
    -1,       # negative int
    -0.01,    # negative float
    -500,     # large negative
])
def test_all_non_positive_inputs_raise_value_error(bad_input):
    with pytest.raises(ValueError):
        calculate_discount(bad_input)
```

This runs 4 separate test cases with one function — clean, exhaustive, and readable.

---

---

## 5. DRF API Client Testing

### 📖 Definition

Django REST Framework's **`APIClient`** simulates HTTP requests to your API endpoints **in-process** — no real server, no network. It is the standard tool for integration-testing DRF views.

```python
from rest_framework.test import APIClient

client = APIClient()

# Authenticate (JWT / Session / Token)
client.force_authenticate(user=some_user)

# Make requests
response = client.get("/api/products/")
response = client.post("/api/orders/", data={"product_id": 1}, format="json")
response = client.put("/api/orders/5/", data={...}, format="json")
response = client.delete("/api/orders/5/")

# Assert
assert response.status_code == 200
assert response.data["id"] == 5
```

**Common HTTP status codes to assert:**

| Code | Meaning | Typical scenario |
|---|---|---|
| `200 OK` | Success (GET, PUT) | List or detail retrieved |
| `201 Created` | Resource created (POST) | New order placed |
| `204 No Content` | Deleted (DELETE) | Resource removed |
| `400 Bad Request` | Validation error | Missing required field |
| `401 Unauthorized` | Not authenticated | No/expired token |
| `403 Forbidden` | Authenticated but not allowed | Non-owner accessing resource |
| `404 Not Found` | Resource missing | Product ID does not exist |

---

### 🎯 Why Python Developers Need This

Unit tests (testing functions in isolation) are not enough for a web API. You need **integration tests** that verify the full lifecycle of a request:

```
HTTP request → URL routing → View → Permission check → Serializer → DB → Response
```

A bug in any of those steps ships to production if you only test functions. API Client tests catch:

| Bug type | Example | Caught by API test? |
|---|---|---|
| Wrong URL pattern | `/api/product/` instead of `/api/products/` | ✅ Yes — `404` instead of `200` |
| Missing permission class | Anonymous user can DELETE | ✅ Yes — `200` instead of `401` |
| Serializer field typo | Response has `"pric"` not `"price"` | ✅ Yes — field assertion fails |
| Wrong HTTP method | `GET` handler doing writes | ✅ Yes — wrong status code |
| Missing `format="json"` | POST body not parsed | ✅ Yes — `400` instead of `201` |

**For Calsoft:** The role involves Django + DRF. Every new endpoint you write should have at minimum: a success test, an auth failure test, and a validation failure test. That is the minimum professional bar.

---

### 🛠️ Best Way to Use It

**Rule 1: Always use `APIClient`, not Django's plain `Client`, for DRF:**

```python
# Wrong for DRF — Django's client doesn't handle content negotiation
from django.test import Client
client = Client()

# Right — APIClient speaks DRF's language (JSON, Accept headers, etc.)
from rest_framework.test import APIClient
client = APIClient()
```

**Rule 2: Use `force_authenticate()` to test views, not to test auth:**

```python
# force_authenticate bypasses token mechanics — use it when you're testing the VIEW
client.force_authenticate(user=admin)    # "pretend this user is logged in"

# Use real credentials only when you're specifically testing the AUTH endpoint
client.post("/api/token/", {"username": "sami", "password": "pass"})
```

**Rule 3: Always specify `format="json"` for POST/PUT:**

```python
# Without format="json", DRF may not parse the body correctly
response = client.post("/api/products/", data={"name": "Kurta"})           # fragile
response = client.post("/api/products/", data={"name": "Kurta"}, format="json")  # correct
```

**Rule 4: Assert BOTH the status code AND the response body:**

```python
# Weak — only checks the code
assert response.status_code == 201

# Strong — proves the response contains what the client actually needs
assert response.status_code == 201
assert response.data["name"] == "Kurta"
assert "id" in response.data          # client needs the ID to follow up
```

---

### 💡 Educative Example

**Scenario:** Martify has a `ProductViewSet`. We want to test list, create, and authentication.

```python
# martify/products/views.py (simplified)

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]  # create/update/delete = admin only
```

```python
# tests/test_product_api.py

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin", email="admin@martify.com", password="pass"
    )

@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        username="sami", email="sami@martify.com", password="pass"
    )

@pytest.fixture
def sample_product(db):
    from martify.products.models import Product
    return Product.objects.create(name="Kurta", price=499.0, stock=50)

# --- GET /api/products/ ---
@pytest.mark.django_db
def test_list_products_returns_200(api_client, sample_product):
    response = api_client.get("/api/products/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_list_products_returns_list(api_client, sample_product):
    response = api_client.get("/api/products/")
    assert isinstance(response.data, list)
    assert len(response.data) >= 1

# --- POST /api/products/ (admin only) ---
@pytest.mark.django_db
def test_create_product_as_admin_returns_201(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    payload = {"name": "Saree", "price": 1299.0, "stock": 20}
    response = api_client.post("/api/products/", data=payload, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "Saree"

@pytest.mark.django_db
def test_create_product_as_regular_user_returns_403(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    payload = {"name": "Saree", "price": 1299.0, "stock": 20}
    response = api_client.post("/api/products/", data=payload, format="json")
    assert response.status_code == 403

@pytest.mark.django_db
def test_create_product_unauthenticated_returns_401(api_client):
    payload = {"name": "Dhoti", "price": 599.0, "stock": 10}
    response = api_client.post("/api/products/", data=payload, format="json")
    assert response.status_code == 401

# --- Validation: 400 Bad Request ---
@pytest.mark.django_db
def test_create_product_missing_name_returns_400(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    payload = {"price": 299.0, "stock": 5}  # name is missing
    response = api_client.post("/api/products/", data=payload, format="json")
    assert response.status_code == 400
    assert "name" in response.data  # DRF puts field errors in response.data

# --- DELETE ---
@pytest.mark.django_db
def test_delete_product_returns_204(api_client, admin_user, sample_product):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(f"/api/products/{sample_product.id}/")
    assert response.status_code == 204
```

---

### ✅ Test Cases

```python
# tests/test_product_api_full.py

@pytest.mark.django_db
def test_retrieve_single_product_200(api_client, sample_product):
    response = api_client.get(f"/api/products/{sample_product.id}/")
    assert response.status_code == 200
    assert response.data["id"] == sample_product.id

@pytest.mark.django_db
def test_retrieve_nonexistent_product_404(api_client):
    response = api_client.get("/api/products/99999/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_update_product_as_admin_200(api_client, admin_user, sample_product):
    api_client.force_authenticate(user=admin_user)
    response = api_client.patch(
        f"/api/products/{sample_product.id}/",
        data={"price": 699.0},
        format="json",
    )
    assert response.status_code == 200
    assert response.data["price"] == "699.00"  # DRF serializes Decimal as string

@pytest.mark.django_db
def test_response_contains_expected_fields(api_client, sample_product):
    response = api_client.get(f"/api/products/{sample_product.id}/")
    for field in ["id", "name", "price", "stock"]:
        assert field in response.data

@pytest.mark.django_db
def test_unauthenticated_delete_returns_401(api_client, sample_product):
    response = api_client.delete(f"/api/products/{sample_product.id}/")
    assert response.status_code == 401
```

> **Interview tip:** *"I use `force_authenticate()` in tests instead of going through the login endpoint — it bypasses token mechanics and tests only the view layer. For testing the auth endpoint itself, I use `client.post('/api/token/', credentials)`."*

---

### 📚 More Examples

**Example A — Testing the JWT token endpoint (testing auth itself):**

```python
# tests/api/test_auth.py

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def registered_user(db):
    return User.objects.create_user(username="sami", password="strongpass123")

@pytest.mark.django_db
def test_valid_credentials_return_token_pair(api_client, registered_user):
    response = api_client.post(
        "/api/token/",
        {"username": "sami", "password": "strongpass123"},
        format="json",
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_wrong_password_returns_401(api_client, registered_user):
    response = api_client.post(
        "/api/token/",
        {"username": "sami", "password": "wrongpassword"},
        format="json",
    )
    assert response.status_code == 401

@pytest.mark.django_db
def test_access_token_grants_entry_to_protected_endpoint(api_client, registered_user):
    # Step 1: Get the token
    token_response = api_client.post(
        "/api/token/",
        {"username": "sami", "password": "strongpass123"},
        format="json",
    )
    access_token = token_response.data["access"]

    # Step 2: Use it on a protected endpoint
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = api_client.get("/api/orders/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_no_token_returns_401_on_protected_endpoint(api_client):
    response = api_client.get("/api/orders/")
    assert response.status_code == 401
```

**Example B — Testing query param filtering (search, category filter):**

```python
# martify/products/views.py

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        search = self.request.query_params.get("search")
        if category:
            qs = qs.filter(category=category)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs
```

```python
# tests/api/test_product_filters.py

import pytest
from rest_framework.test import APIClient
from martify.products.models import Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def product_catalog(db):
    Product.objects.create(name="Men's Kurta",  category="men",   price=499)
    Product.objects.create(name="Women's Saree", category="women", price=1299)
    Product.objects.create(name="Men's Pyjama",  category="men",   price=299)

@pytest.mark.django_db
def test_category_filter_returns_only_men(api_client, product_catalog):
    response = api_client.get("/api/products/?category=men")
    assert response.status_code == 200
    assert len(response.data) == 2
    for item in response.data:
        assert item["category"] == "men"

@pytest.mark.django_db
def test_search_filter_is_case_insensitive(api_client, product_catalog):
    response = api_client.get("/api/products/?search=kurta")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert "Kurta" in response.data[0]["name"]

@pytest.mark.django_db
def test_no_filter_returns_all_products(api_client, product_catalog):
    response = api_client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_search_with_no_match_returns_empty(api_client, product_catalog):
    response = api_client.get("/api/products/?search=laptop")
    assert response.status_code == 200
    assert response.data == []
```

**Example C — Testing paginated responses:**

```python
# tests/api/test_pagination.py

@pytest.mark.django_db
def test_paginated_response_has_correct_keys(api_client, db):
    # Create 15 products (more than one page if page_size=10)
    for i in range(15):
        Product.objects.create(name=f"Product {i}", price=100, stock=10)

    response = api_client.get("/api/products/")
    assert response.status_code == 200

    # DRF PageNumberPagination returns: count, next, previous, results
    assert "count" in response.data
    assert "results" in response.data
    assert response.data["count"] == 15

@pytest.mark.django_db
def test_second_page_has_remaining_items(api_client, db):
    for i in range(15):
        Product.objects.create(name=f"Product {i}", price=100, stock=10)

    response = api_client.get("/api/products/?page=2")
    assert response.status_code == 200
    assert len(response.data["results"]) == 5   # 15 total, 10 on page 1, 5 on page 2
```

---

---

## 6. Database Isolation in Django

### 📖 Definition

By default, pytest tests do **not** touch the database. Django's test runner automatically creates a **separate test database** (prefixed with `test_`) that is:

- **Isolated** — never touches your development/production DB
- **Transactional** — each test is wrapped in a transaction that is **rolled back** after the test, so test order doesn't matter
- **Migrated** — Django applies all migrations to the test DB before the suite runs

| Mechanism | Description |
|---|---|
| `@pytest.mark.django_db` | Marks a pytest function as allowed to access the DB |
| `django.test.TestCase` | Base class that wraps each test in a transaction + rollback |
| `@pytest.mark.django_db(transaction=True)` | For tests that need COMMIT behaviour (e.g. testing Celery tasks) |
| `django_db_setup` fixture | Customise the test database bootstrap |
| `django_db_reset_sequences` fixture | Resets auto-increment IDs between tests |

---

### 🎯 Why Python Developers Need This

Without DB isolation, tests are **order-dependent** — which is one of the worst kinds of bugs to track down:

```
Test A creates User "sami"
Test B also tries to create User "sami"
Test B fails with IntegrityError: UNIQUE constraint failed
... but only when tests run in alphabetical order. On CI it works. Locally it fails.
```

| Problem | Django test isolation solution |
|---|---|
| Test A's data bleeds into Test B | Each test is wrapped in a rolled-back transaction |
| Tests accidentally hit production DB | Django creates a separate `test_` prefixed DB |
| Tests fail due to leftover data | Test DB is wiped and re-migrated at the start of every run |
| Two tests create conflicting unique records | Rollback means nothing is actually committed |

**Interview point:** An interviewer might ask *"what happens if you don't clean up DB state between tests?"* Your answer: *"In Django, you don't need to manually clean up. Each test is wrapped in a transaction that rolls back after it completes, so the next test always starts with a clean slate — guaranteed by the `db` fixture or `@pytest.mark.django_db`."*

---

### 🛠️ Best Way to Use It

**Rule 1: Use `db` fixture in `conftest.py` — not `@pytest.mark.django_db` on every individual test:**

```python
# conftest.py — the 'db' fixture propagates to tests that use this fixture
@pytest.fixture
def customer(db):              # 'db' grants DB access and ensures rollback
    return User.objects.create_user(username="sami", password="p")

# test file — no marker needed; the 'customer' fixture carries it
def test_something(customer):
    assert customer.username == "sami"
```

**Rule 2: Use `transaction=True` ONLY when code depends on committed data (e.g. Celery tasks):**

```python
# Regular test — fast, uses transaction rollback (default)
@pytest.mark.django_db
def test_create_order(db): ...

# Celery task test — task runs in a subprocess, needs committed data to see it
@pytest.mark.django_db(transaction=True)
def test_order_confirmation_task(db): ...
```

**Rule 3: Use `django_db_reset_sequences` when your test cares about specific auto-increment IDs:**

```python
@pytest.mark.django_db
def test_first_product_has_id_1(django_db_reset_sequences):
    product = Product.objects.create(name="Kurta", price=499, stock=10)
    assert product.id == 1   # guaranteed — sequences were reset
```

**Rule 4: Override settings temporarily with the `settings` fixture:**

```python
def test_stripe_uses_test_key(settings):
    settings.STRIPE_SECRET_KEY = "sk_test_override"
    # automatically restored after the test ends
```

---

### 💡 Educative Example

**Scenario:** Testing that Martify's `Order` model correctly computes total price.

```python
# martify/orders/models.py

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        return sum(item.line_total() for item in self.orderitem_set.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def line_total(self):
        return self.quantity * self.unit_price
```

```python
# tests/test_order_model.py

import pytest
from django.contrib.auth.models import User
from martify.orders.models import Order, OrderItem

@pytest.mark.django_db                     # grant DB access to this test
def test_order_total_sums_line_items():
    user = User.objects.create_user(username="tester", password="pass")
    order = Order.objects.create(user=user)

    OrderItem.objects.create(order=order, product_name="Kurta",    quantity=2, unit_price=499)
    OrderItem.objects.create(order=order, product_name="Dupatta",  quantity=1, unit_price=299)

    # 2*499 + 1*299 = 998 + 299 = 1297
    assert order.get_total() == 1297

@pytest.mark.django_db
def test_empty_order_total_is_zero():
    user = User.objects.create_user(username="empty_user", password="pass")
    order = Order.objects.create(user=user)
    assert order.get_total() == 0

@pytest.mark.django_db
def test_db_isolation_previous_test_data_not_visible():
    """
    This test proves isolation: the 'tester' user from the test above
    does NOT exist here — the transaction was rolled back.
    """
    assert User.objects.filter(username="tester").count() == 0
```

**Using `conftest.py` fixtures with DB:**

```python
# tests/conftest.py

import pytest
from django.contrib.auth.models import User
from martify.orders.models import Order

@pytest.fixture
def user(db):               # the 'db' fixture grants DB access + auto-rollback
    return User.objects.create_user(username="sami", password="test123")

@pytest.fixture
def pending_order(user):
    return Order.objects.create(user=user, status="pending")
```

```python
# tests/test_order_with_fixtures.py

@pytest.mark.django_db
def test_order_status_default_is_pending(pending_order):
    assert pending_order.status == "pending"

@pytest.mark.django_db
def test_order_belongs_to_correct_user(pending_order, user):
    assert pending_order.user.username == "sami"
```

---

### ✅ Test Cases

```python
# tests/test_db_isolation.py

import pytest
from django.contrib.auth.models import User
from martify.orders.models import Order, OrderItem

@pytest.fixture
def order_with_items(db):
    user = User.objects.create_user(username="buyer", password="p")
    order = Order.objects.create(user=user)
    OrderItem.objects.create(order=order, product_name="Shirt", quantity=3, unit_price=200)
    OrderItem.objects.create(order=order, product_name="Pants", quantity=1, unit_price=800)
    return order

@pytest.mark.django_db
def test_total_with_multiple_items(order_with_items):
    # 3*200 + 1*800 = 600 + 800 = 1400
    assert order_with_items.get_total() == 1400

@pytest.mark.django_db
def test_order_item_count(order_with_items):
    assert order_with_items.orderitem_set.count() == 2

@pytest.mark.django_db
def test_cascade_delete_removes_items(order_with_items):
    order_id = order_with_items.id
    order_with_items.delete()
    assert OrderItem.objects.filter(order_id=order_id).count() == 0

@pytest.mark.django_db
def test_filter_pending_orders(db):
    user = User.objects.create_user(username="filter_test", password="p")
    Order.objects.create(user=user, status="pending")
    Order.objects.create(user=user, status="shipped")
    Order.objects.create(user=user, status="pending")
    pending = Order.objects.filter(status="pending")
    assert pending.count() == 2
```

> **Interview tip:** *"I always use the `db` fixture (or `@pytest.mark.django_db`) rather than `transaction=True` unless I'm testing something that explicitly needs committed data — like a Celery task that's launched in a separate process and queries the DB independently."*

---

### 📚 More Examples

**Example A — Testing a Django `post_save` signal:**

```python
# martify/orders/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from martify.orders.models import Order

@receiver(post_save, sender=Order)
def create_order_analytics_record(sender, instance, created, **kwargs):
    if created:
        from martify.analytics.models import OrderEvent
        OrderEvent.objects.create(order=instance, event_type="order_created")
```

```python
# tests/orders/test_signals.py

import pytest
from django.contrib.auth.models import User
from martify.orders.models import Order
from martify.analytics.models import OrderEvent

@pytest.mark.django_db
def test_creating_order_fires_analytics_event(db):
    user = User.objects.create_user(username="signal_test", password="p")
    order = Order.objects.create(user=user, status="pending")

    # The signal should have run automatically on Order.save()
    event = OrderEvent.objects.filter(order=order, event_type="order_created")
    assert event.exists()

@pytest.mark.django_db
def test_updating_order_does_not_create_duplicate_event(db):
    user = User.objects.create_user(username="signal_test2", password="p")
    order = Order.objects.create(user=user, status="pending")

    # Update (not create) — signal fires but `created=False`
    order.status = "shipped"
    order.save()

    # Only 1 event — the initial creation one
    events = OrderEvent.objects.filter(order=order, event_type="order_created")
    assert events.count() == 1
```

**Example B — Testing a custom Manager method:**

```python
# martify/orders/models.py

class OrderManager(models.Manager):
    def pending_for_user(self, user):
        return self.filter(user=user, status="pending")

    def high_value(self, threshold=1000):
        return self.filter(total_amount__gte=threshold)

class Order(models.Model):
    objects = OrderManager()
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    status  = models.CharField(max_length=20, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
```

```python
# tests/orders/test_manager.py

import pytest
from django.contrib.auth.models import User
from martify.orders.models import Order

@pytest.fixture
def two_users(db):
    u1 = User.objects.create_user(username="alice", password="p")
    u2 = User.objects.create_user(username="bob",   password="p")
    return u1, u2

@pytest.mark.django_db
def test_pending_for_user_excludes_other_users(two_users):
    alice, bob = two_users
    Order.objects.create(user=alice, status="pending", total_amount=500)
    Order.objects.create(user=bob,   status="pending", total_amount=300)

    alice_orders = Order.objects.pending_for_user(alice)
    assert alice_orders.count() == 1
    assert alice_orders.first().user == alice

@pytest.mark.django_db
def test_pending_for_user_excludes_shipped_orders(two_users):
    alice, _ = two_users
    Order.objects.create(user=alice, status="pending", total_amount=200)
    Order.objects.create(user=alice, status="shipped", total_amount=800)

    pending = Order.objects.pending_for_user(alice)
    assert pending.count() == 1   # only the pending one

@pytest.mark.django_db
def test_high_value_returns_only_above_threshold(two_users):
    alice, _ = two_users
    Order.objects.create(user=alice, status="pending", total_amount=500)
    Order.objects.create(user=alice, status="pending", total_amount=1500)
    Order.objects.create(user=alice, status="pending", total_amount=2000)

    high = Order.objects.high_value(threshold=1000)
    assert high.count() == 2
```

**Example C — Testing `bulk_create` and confirming atomicity:**

```python
# martify/products/services.py

from martify.products.models import Product

class ProductBulkImportService:
    def bulk_create_products(self, products_data: list) -> int:
        """
        Create multiple products atomically.
        Returns the count of products created.
        """
        objects = [
            Product(name=d["name"], price=d["price"], stock=d.get("stock", 0))
            for d in products_data
        ]
        created = Product.objects.bulk_create(objects)
        return len(created)
```

```python
# tests/products/test_bulk_import.py

import pytest
from martify.products.services import ProductBulkImportService
from martify.products.models import Product

@pytest.fixture
def svc():
    return ProductBulkImportService()

@pytest.mark.django_db
def test_bulk_create_inserts_all_products(svc):
    data = [
        {"name": "Kurta",  "price": 499, "stock": 50},
        {"name": "Saree",  "price": 1299, "stock": 20},
        {"name": "Pyjama", "price": 299, "stock": 100},
    ]
    count = svc.bulk_create_products(data)

    assert count == 3
    assert Product.objects.count() == 3

@pytest.mark.django_db
def test_bulk_create_sets_correct_prices(svc):
    data = [{"name": "Hat", "price": 199, "stock": 10}]
    svc.bulk_create_products(data)

    hat = Product.objects.get(name="Hat")
    assert float(hat.price) == 199.0

@pytest.mark.django_db
def test_bulk_create_returns_correct_count(svc):
    data = [{"name": f"Item {i}", "price": 100 * i, "stock": i} for i in range(1, 6)]
    result = svc.bulk_create_products(data)
    assert result == 5
```

---

---

## 7. CI/CD Pipeline Integration

### 📖 Definition

CI/CD (**Continuous Integration / Continuous Deployment**) is the practice of automatically running tests every time code is pushed, so bugs are caught before they reach production.

The flow:
```
Developer pushes code → GitHub Actions triggers → Install deps → Run pytest → Pass/Fail
```

If tests fail, the **build is blocked** — the PR cannot be merged.

---

### 🎯 Why Python Developers Need This

Without CI, testing is a *manual, optional, easily skipped* step. With CI, it is automatic and mandatory.

| Without CI | With CI |
|---|---|
| Developer forgets to run tests before pushing | Tests run automatically on every push |
| "It works on my machine" | Tests run on a fresh Ubuntu container — always |
| Broken code merged into `main` | PR merge is blocked until tests pass |
| Nobody checks test coverage | Coverage gate enforced on every PR |
| Secrets hardcoded in scripts | Environment variables managed by GitHub Secrets |

**Calsoft context:** The job description explicitly mentions CI/CD experience. At minimum, you need to be able to:
1. Read and understand an existing `.github/workflows/*.yml` file
2. Add a test step to a pipeline
3. Explain what `--cov-fail-under=80` does and why it matters
4. Know the difference between a **job** (runs in parallel) and a **step** (runs sequentially inside a job)

---

### 🛠️ Best Way to Use It

**Rule 1: Structure your pipeline as separate jobs — fail fast:**

```yaml
jobs:
  lint:     # runs first — if code style is broken, don't waste time running tests
    ...
  test:     # runs only after lint passes
    needs: lint
    ...
  deploy:   # runs only after tests pass, only on main branch
    needs: test
    if: github.ref == 'refs/heads/main'
```

**Rule 2: Cache pip dependencies — shaves 60-90 seconds off every run:**

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
    cache: "pip"              # caches ~/.cache/pip between runs
```

**Rule 3: Use GitHub Secrets for API keys — never hardcode:**

```yaml
env:
  STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}   # set in repo Settings → Secrets
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_ACCESS_KEY }}
```

**Rule 4: Use a matrix build to test across Python versions:**

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

**Rule 5: Set `--tb=short` in CI to keep logs readable — full tracebacks are too noisy in CI output.**

---

### 💡 Educative Example — GitHub Actions Workflow

**File:** `.github/workflows/test.yml`

```yaml
name: Martify — CI Test Suite

# Trigger on every push and pull_request to main
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    # Spin up a Postgres service container (mirrors production)
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: martify_test
          POSTGRES_USER: martify
          POSTGRES_PASSWORD: testpassword
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      DATABASE_URL: postgres://martify:testpassword@localhost:5432/martify_test
      DJANGO_SETTINGS_MODULE: martify.settings.test
      SECRET_KEY: ci-test-secret-key-not-for-production

    steps:
      # Step 1: Checkout code
      - name: Checkout repository
        uses: actions/checkout@v4

      # Step 2: Set up Python
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"                  # Cache pip packages for faster runs

      # Step 3: Install dependencies
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt   # pytest, pytest-django, pytest-cov

      # Step 4: Run database migrations
      - name: Run migrations
        run: python manage.py migrate --settings=martify.settings.test

      # Step 5: Run the test suite with coverage
      - name: Run pytest with coverage
        run: |
          pytest \
            --cov=martify \
            --cov-report=xml \
            --cov-report=term-missing \
            --cov-fail-under=80 \     # QUALITY GATE: fail if coverage < 80%
            -v

      # Step 6: Upload coverage report (optional — for Codecov / PR comments)
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: coverage.xml
          fail_ci_if_error: false
```

**GitLab CI equivalent** (`.gitlab-ci.yml`):

```yaml
stages:
  - test

variables:
  POSTGRES_DB: martify_test
  POSTGRES_USER: martify
  POSTGRES_PASSWORD: testpassword
  DATABASE_URL: "postgres://martify:testpassword@postgres/martify_test"
  DJANGO_SETTINGS_MODULE: martify.settings.test

test:
  stage: test
  image: python:3.11-slim
  services:
    - postgres:15
  before_script:
    - pip install -r requirements.txt -r requirements-dev.txt
    - python manage.py migrate
  script:
    - pytest --cov=martify --cov-fail-under=80 --cov-report=term-missing -v
  coverage: '/TOTAL.*\s+(\d+%)$/'    # Extracts coverage % for GitLab badge
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

---

### ✅ Test Cases (for pipeline validation)

```python
# tests/test_smoke.py
# Smoke tests — first things the CI runs. If these fail, something is very broken.

import pytest
from django.test import TestCase

@pytest.mark.django_db
def test_database_is_reachable(db):
    """CI check: confirm the Postgres service container is up."""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    assert result[0] == 1

def test_settings_module_loaded():
    """CI check: confirm Django settings are correct for test env."""
    from django.conf import settings
    assert settings.DEBUG is False or True   # just ensure settings loaded
    assert "test" in settings.DATABASES["default"]["NAME"].lower()

@pytest.mark.django_db
def test_user_model_accessible(db):
    """CI check: ORM + migrations work."""
    from django.contrib.auth.models import User
    count = User.objects.count()
    assert count == 0   # fresh test DB should be empty
```

> **Interview tip:** *"In the CI YAML I use `--cov-fail-under=80` to enforce a quality gate. If someone submits a PR that drops test coverage below 80%, the pipeline fails and the PR is blocked. This keeps the team honest about testing new features."*

---

### 📚 More Examples

**Example A — Matrix build: test across Python 3.10, 3.11, and 3.12 simultaneously:**

```yaml
# .github/workflows/test.yml

name: Martify — Matrix CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
      fail-fast: false   # don't cancel 3.11 run if 3.10 fails

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"

      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Run tests
        run: pytest --tb=short -q
        env:
          DJANGO_SETTINGS_MODULE: martify.settings.test
          SECRET_KEY: ci-secret
```

This creates **3 parallel jobs** — each on a different Python version. If your library has a compatibility issue with 3.12, this catches it.

**Example B — Separate lint and test jobs (fail fast):**

```yaml
# .github/workflows/ci.yml

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11", cache: "pip" }
      - run: pip install flake8 black isort
      - name: Check formatting
        run: black --check .
      - name: Check imports
        run: isort --check-only .
      - name: Lint
        run: flake8 martify/ --max-line-length=120

  test:
    runs-on: ubuntu-latest
    needs: lint      # test job only runs if lint passes
    services:
      postgres:
        image: postgres:15
        env: { POSTGRES_DB: martify_test, POSTGRES_USER: martify, POSTGRES_PASSWORD: pass }
        options: --health-cmd pg_isready --health-interval 10s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11", cache: "pip" }
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: python manage.py migrate --settings=martify.settings.test
      - run: pytest --cov=martify --cov-fail-under=80 --tb=short

  deploy:
    runs-on: ubuntu-latest
    needs: test                                      # deploy only after tests pass
    if: github.ref == 'refs/heads/main'              # deploy only on main branch
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          echo "Deploying Martify to AWS..."
          # eb deploy / kubectl apply / etc.
```

**Example C — Running only changed tests (faster PR feedback with `--lf`):**

```yaml
# For PRs: run only the tests that failed last time first,
# then run the rest. Gives faster feedback on fixes.

- name: Run previously failed tests first
  run: pytest --lf --tb=short || true   # don't fail if no previous run

- name: Run full suite
  run: pytest --cov=martify --cov-fail-under=80
```

---

---

## 8. Code Coverage & Quality Gates

### 📖 Definition

**Code coverage** measures what percentage of your source code is actually executed during your test suite.

| Tool | Role |
|---|---|
| `coverage.py` | Core library that instruments Python code and tracks execution |
| `pytest-cov` | pytest plugin that wraps `coverage.py` (`--cov` flag) |
| `--cov-report=term-missing` | Shows which lines are NOT covered in the terminal |
| `--cov-report=html` | Generates a browsable HTML report at `htmlcov/index.html` |
| `--cov-fail-under=N` | Fails the test run if coverage is below N% — the **quality gate** |

---

### 🎯 Why Python Developers Need This

Coverage answers a question your test suite cannot answer by itself: **"Is there code I haven't tested at all?"**

| Without coverage | With coverage |
|---|---|
| You think you've tested `checkout()` | Coverage reveals the `CardError` branch at line 47 is never hit |
| A dead `if/else` branch ships with no test | Coverage flags the untested branch in the terminal output |
| PR reviewer asks "did you test the error path?" | You show the coverage diff: `services.py: 100%` |
| Team has no standard for test completeness | `--cov-fail-under=80` is the enforceable standard |

**The nuance to say in an interview:** *"100% coverage does not mean bug-free code. It means every line was executed by at least one test — but a bad test can execute code without asserting anything meaningful. Coverage is a floor, not a ceiling. I aim for 80-90% on business logic and accept lower on configuration and migrations."*

---

### 🛠️ Best Way to Use It

**Rule 1: Use branch coverage, not just line coverage:**

```bash
# Line coverage only — misses untested branches
pytest --cov=martify

# Branch coverage — catches untested if/else paths
pytest --cov=martify --cov-branch
```

```python
def get_discount(total):
    if total > 500:          # line coverage: ✓ (any call covers this line)
        return total * 0.1   # branch coverage: needs a test where total > 500
    return 0                 # branch coverage: ALSO needs a test where total <= 500
```

**Rule 2: Exclude the right things in `.coveragerc`:**

```ini
[run]
source = martify
branch = True                # enable branch coverage globally
omit =
    */migrations/*
    */settings/*
    */tests/*
    manage.py
    */admin.py              # Django admin is usually not unit-tested
    conftest.py
```

**Rule 3: Use `# pragma: no cover` for genuinely untestable lines:**

```python
if __name__ == "__main__":    # pragma: no cover
    app.run()                 # Entry points don't need a test
```

**Rule 4: Set different thresholds for different apps:**

```bash
# Critical business logic — high bar
pytest --cov=martify.orders   --cov-fail-under=90

# Admin UI / config — lower bar acceptable
pytest --cov=martify.admin    --cov-fail-under=60
```

**Rule 5: Check coverage before pushing, not after:**

```bash
# Add this to your pre-commit hook or Makefile:
pytest --cov=martify --cov-fail-under=80 -q
```

---

### 💡 Educative Example

**Running coverage locally:**

```bash
# Basic run — shows coverage summary in terminal
pytest --cov=martify --cov-report=term-missing

# Generate HTML report (open htmlcov/index.html in browser)
pytest --cov=martify --cov-report=html

# Enforce 80% minimum — fails with exit code 2 if under threshold
pytest --cov=martify --cov-fail-under=80

# Only measure coverage for a specific app
pytest martify/orders/tests/ --cov=martify.orders --cov-report=term-missing
```

**Sample terminal output:**

```
---------- coverage: platform linux, python 3.11 ----------
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
martify/orders/models.py             24      2    92%   45-46
martify/orders/services.py           18      4    78%   32, 35, 41, 55
martify/payments/services.py         21      0   100%
martify/products/views.py            30      6    80%   88-93
---------------------------------------------------------------
TOTAL                                93     12    87%

Required test coverage of 80% reached. Total coverage: 87.10%
```

**`.coveragerc` — exclude files you don't want measured:**

```ini
# .coveragerc
[run]
source = martify
omit =
    */migrations/*        # Auto-generated — no point testing these
    */settings/*          # Config, not logic
    */tests/*             # Don't measure the tests themselves
    manage.py
    */wsgi.py
    */asgi.py

[report]
show_missing = True
skip_covered = False
```

**How to answer: "How do you prevent merging untested code?"**

```
1. pytest-cov runs in CI with --cov-fail-under=80
2. If coverage drops below 80%, the pipeline exits with a non-zero code
3. GitHub/GitLab branch protection rules require the CI job to pass before merging
4. For new features, the developer must write tests — otherwise coverage drops and the PR is blocked
5. Optionally, upload to Codecov so the PR shows a coverage diff comment
```

---

### ✅ Test Cases (Coverage self-check pattern)

```python
# tests/test_coverage_helpers.py
# Tests that exist specifically to drive coverage of edge paths

import pytest
from martify.orders.utils import calculate_discount
from martify.products.services import ProductService

# Drives the `order_total > 500` branch
def test_coverage_discount_branch_true():
    assert calculate_discount(600) == 60.0

# Drives the `order_total <= 500` branch
def test_coverage_discount_branch_false():
    assert calculate_discount(300) == 0.0

# Drives the `ValueError` branch
def test_coverage_discount_error_branch():
    with pytest.raises(ValueError):
        calculate_discount(-1)

# Drives ProductService.get_product happy path
@pytest.mark.django_db
def test_coverage_get_product_happy_path():
    svc = ProductService()
    result = svc.get_product(1)
    assert "id" in result
```

@pytest.mark.django_db
def test_coverage_get_product_happy_path():
    svc = ProductService()
    result = svc.get_product(1)
    assert "id" in result
```

---

### 📚 More Examples

**Example A — Branch coverage in practice (testing both sides of every condition):**

```python
# martify/orders/utils.py

def classify_order(total: float) -> str:
    """Classify an order into a tier."""
    if total >= 5000:
        return "platinum"
    elif total >= 2000:
        return "gold"
    elif total >= 500:
        return "silver"
    else:
        return "standard"
```

```python
# tests/orders/test_classify.py
# Without branch coverage you might only test one path.
# With --cov-branch, all 4 branches must be hit.

import pytest
from martify.orders.utils import classify_order

@pytest.mark.parametrize("total, tier", [
    (6000,  "platinum"),   # branch: total >= 5000
    (3000,  "gold"),       # branch: total >= 2000
    (800,   "silver"),     # branch: total >= 500
    (100,   "standard"),   # branch: else
    (5000,  "platinum"),   # boundary: exactly 5000
    (2000,  "gold"),       # boundary: exactly 2000
    (500,   "silver"),     # boundary: exactly 500
    (499,   "standard"),   # boundary: just below silver
])
def test_classify_order_all_branches(total, tier):
    assert classify_order(total) == tier
```

Running with `--cov-branch` on this file will show 100% branch coverage — every `if/elif/else` path exercised.

**Example B — Per-app coverage with a `Makefile` (professional workflow):**

```makefile
# Makefile at Martify project root

.PHONY: test test-orders test-payments coverage-html

# Run all tests with coverage
test:
	pytest --cov=martify --cov-branch --cov-fail-under=80 --cov-report=term-missing -q

# Run only orders app
test-orders:
	pytest tests/orders/ --cov=martify.orders --cov-fail-under=85 --cov-report=term-missing

# Run only payments app (higher bar — money is involved)
test-payments:
	pytest tests/payments/ --cov=martify.payments --cov-fail-under=95 --cov-report=term-missing

# Generate HTML report and open in browser
coverage-html:
	pytest --cov=martify --cov-branch --cov-report=html -q
	open htmlcov/index.html    # macOS; use xdg-open on Linux
```

**Example C — Using `# pragma: no cover` correctly (don't abuse it):**

```python
# martify/core/management/commands/seed_data.py

class Command(BaseCommand):
    help = "Seed the database with sample data"

    def handle(self, *args, **options):    # pragma: no cover
        """
        Management commands are run manually, not in tests.
        Marking with pragma: no cover is acceptable here.
        """
        Product.objects.create(name="Seed Product", price=100, stock=10)
        self.stdout.write("Seeded 1 product.")

# martify/payments/services.py

class PaymentService:
    def charge(self, amount, token):
        try:
            charge = stripe.Charge.create(amount=amount, currency="inr", source=token)
            return {"success": True, "charge_id": charge["id"]}
        except stripe.error.CardError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:            # pragma: no cover
            # Unexpected Stripe errors — log and re-raise.
            # Difficult to reproduce in tests without complex mock setup.
            logger.critical(f"Unexpected Stripe error: {e}")
            raise
```

> **Interview tip:** Using `# pragma: no cover` on a business-critical branch like `except Exception` during an interview would raise red flags. It signals you are hiding untested code. Use it only for genuinely untestable infrastructure code — entry points, management commands, and truly exceptional error paths.

**Example D — Combining coverage reports (HTML + XML for CI + terminal):**

```bash
# Run once, get all three report formats
pytest \
  --cov=martify \
  --cov-branch \
  --cov-fail-under=80 \
  --cov-report=term-missing \   # terminal: see missing lines immediately
  --cov-report=html \           # HTML: browse in browser for deep analysis
  --cov-report=xml              # XML: parsed by GitHub Actions / Codecov badge
```

```yaml
# In GitHub Actions — upload XML to Codecov for PR coverage comments
- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    files: coverage.xml
    flags: unittests
    name: martify-coverage
```

---

### 📌 Quick Reference — Key Commands

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run a specific file
pytest tests/test_product_api.py

# Run a specific test by name
pytest tests/test_product_api.py::test_create_product_as_admin_returns_201

# Run tests matching a keyword
pytest -k "discount or order"

# Run with coverage + quality gate
pytest --cov=martify --cov-report=term-missing --cov-fail-under=80

# Stop after first failure
pytest -x

# Show local variable values on failure
pytest -l
```

---

### 🏁 Interview Cheat Sheet

| Question | One-line answer |
|---|---|
| Why pytest over unittest? | Less boilerplate, native assert with rich diffs, powerful fixture DI |
| What does `yield` do in a fixture? | Separates setup (before) from teardown (after) |
| Where do you put shared fixtures? | `conftest.py` — auto-discovered by pytest |
| Why mock external calls? | Speed + determinism — tests should not depend on Stripe/S3/LLM availability |
| Patch where defined or used? | Where **used** — always patch at the import location of the caller |
| How to test a 403 in DRF? | `force_authenticate(regular_user)` + assert `response.status_code == 403` |
| Why is the test DB isolated? | Django wraps each test in a transaction and rolls it back after |
| How to enforce coverage in CI? | `--cov-fail-under=80` in the pytest step; exit code 2 blocks the merge |
| What does `@pytest.mark.django_db` do? | Grants that test access to the test database with auto-rollback |

---

*Good luck at Calsoft, Sami! Test early, test often. 🚀*
