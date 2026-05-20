# 🐍 Python Topics Checklist

> Topics ordered by frequency in Accenture Python Developer interview reports (Glassdoor India & global, 2025–2026).
> Mark each topic as you feel confident — `[ ]` → `[x]`.

---

## 🔴 Must-Know — High Frequency

*These appear in almost every Python developer interview at Accenture.*

### Decorators & Functional Patterns
- [ ] What a decorator is and how it works (function wrapping)
- [ ] Writing a decorator from scratch without `functools`
- [ ] `@functools.wraps` — why it matters
- [ ] Decorator with arguments (`@retry(times=3)`)
- [ ] Class-based decorators
- [ ] Common built-in decorators: `@staticmethod`, `@classmethod`, `@property`
- [ ] Closures and captured variables (`nonlocal` keyword)

```python
# Minimal decorator example — know this cold
def my_decorator(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper
```

---

### OOP — Object-Oriented Programming
- [ ] `__init__` — instance initialization
- [ ] Instance attributes vs class attributes
- [ ] `self` — what it is and why it's needed
- [ ] Inheritance — single and multiple (`super()`)
- [ ] Method Resolution Order (MRO) — `ClassName.__mro__`
- [ ] Polymorphism — method overriding, duck typing
- [ ] Encapsulation — `_protected`, `__private` name mangling
- [ ] `__str__` vs `__repr__` — when each is called
- [ ] `__eq__`, `__hash__`, `__lt__` — comparison dunder methods
- [ ] `__len__`, `__getitem__`, `__setitem__` — container dunders
- [ ] Abstract base classes — `from abc import ABC, abstractmethod`
- [ ] `@dataclass` — fields, defaults, `frozen=True`, `__post_init__`

---

### Types, Memory & Data Model
- [ ] Mutable types: `list`, `dict`, `set`, `bytearray`
- [ ] Immutable types: `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`
- [ ] How Python passes arguments (pass by object reference)
- [ ] Shallow copy vs deep copy — `copy.copy()` vs `copy.deepcopy()`
- [ ] Reference counting — how Python tracks object lifetimes
- [ ] Garbage collection — cyclic reference detection
- [ ] The GIL (Global Interpreter Lock) — what it is, implications for threading
- [ ] `id()` and object identity vs equality (`is` vs `==`)
- [ ] Interning — why small integers and short strings are cached

---

### Iterables, Generators & Comprehensions
- [ ] Iterables vs iterators — `__iter__` and `__next__`
- [ ] `yield` — turning a function into a generator
- [ ] `yield from` — delegating to a sub-generator
- [ ] Generator expressions: `(x**2 for x in range(10))`
- [ ] List comprehensions with conditions: `[x for x in lst if x > 0]`
- [ ] Dict comprehensions: `{k: v for k, v in pairs}`
- [ ] Set comprehensions: `{x**2 for x in range(5)}`
- [ ] `map()`, `filter()`, `zip()`, `enumerate()`
- [ ] `itertools` — `chain`, `product`, `combinations`, `permutations`

---

### Functions & Arguments
- [ ] Positional, keyword, default arguments
- [ ] `*args` — variable positional arguments (tuple inside)
- [ ] `**kwargs` — variable keyword arguments (dict inside)
- [ ] Keyword-only arguments (after `*` or `*args`)
- [ ] Argument ordering rules: positional → `*args` → keyword-only → `**kwargs`
- [ ] Lambda functions — syntax and limitations
- [ ] `functools.partial` — partially applying arguments

---

### Exception Handling
- [ ] `try` / `except` / `else` / `finally` — when each block runs
- [ ] Catching multiple exceptions: `except (TypeError, ValueError)`
- [ ] Re-raising exceptions: `raise` (bare) vs `raise e`
- [ ] Exception chaining: `raise NewError() from original`
- [ ] Custom exception classes — inheriting from `Exception`
- [ ] `with` statement — context managers, `__enter__` / `__exit__`
- [ ] `contextlib.contextmanager` decorator
- [ ] Logging — `logging.getLogger`, levels, `basicConfig`

---

## 🟡 Important — Medium Frequency

### Pandas
- [ ] `pd.DataFrame()` creation from dict, list, CSV
- [ ] `.head()`, `.info()`, `.describe()`, `.shape`, `.dtypes`
- [ ] Boolean indexing: `df[df['col'] > 0]`
- [ ] `.loc[]` (label-based) vs `.iloc[]` (integer-based)
- [ ] `.groupby()` + `.agg({'col': 'sum'})`
- [ ] `.merge(left, right, on='key', how='inner')`
- [ ] `.apply()` with a lambda or named function
- [ ] `.fillna()`, `.dropna()`, `.isna()`, `.notna()`
- [ ] `.sort_values()`, `.reset_index()`
- [ ] `.pivot_table(values, index, columns, aggfunc)`
- [ ] String operations: `df['col'].str.upper()`, `.str.contains()`

### NumPy
- [ ] `np.array()`, `np.zeros()`, `np.ones()`, `np.arange()`, `np.linspace()`
- [ ] Array slicing: `arr[1:5]`, `arr[:, 0]`, `arr[arr > 0]`
- [ ] Broadcasting — rules for shape compatibility
- [ ] `np.argmax()`, `np.argmin()`, `np.argsort()`
- [ ] `np.unique()`, `np.where()`
- [ ] `np.dot()`, `np.matmul()`, `np.linalg.inv()`
- [ ] `np.reshape()`, `np.flatten()`, `np.concatenate()`

---

### Web Frameworks — Flask / Django
- [ ] Flask: `@app.route`, `methods=['GET','POST']`, `request.json`, `jsonify`
- [ ] Flask: Blueprints for modular app structure
- [ ] Flask: Error handlers — `@app.errorhandler(404)`
- [ ] Authentication patterns — JWT (`flask-jwt-extended`), session-based
- [ ] Django: MVT (Model-View-Template) architecture
- [ ] Django: ORM — `models.py`, `migrate`, `makemigrations`
- [ ] Django: URL routing (`urls.py`), views, templates
- [ ] REST API design principles — stateless, resource-based URLs
- [ ] HTTP status codes — 200, 201, 400, 401, 403, 404, 422, 500

---

### SQL
- [ ] `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`
- [ ] `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`
- [ ] `GROUP BY` + `HAVING`
- [ ] Subqueries in `WHERE` clause and `FROM` clause
- [ ] `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`
- [ ] `RANK()`, `DENSE_RANK()`
- [ ] `CASE WHEN ... THEN ... ELSE ... END`
- [ ] `DISTINCT`, `COUNT(*)`, `SUM()`, `AVG()`, `MAX()`, `MIN()`
- [ ] Indexes — what they are, when they help

---

### Code Quality & Testing
- [ ] Type hints — basic (`int`, `str`, `List[int]`, `Optional[str]`, `Union`)
- [ ] PEP 8 — naming (snake_case, UPPER_CASE constants), 79-char line limit
- [ ] `unittest` — `TestCase`, `setUp`, `assertEqual`, `assertRaises`
- [ ] `pytest` — fixtures, parametrize, `conftest.py`
- [ ] Mocking — `unittest.mock.patch`, `MagicMock`
- [ ] Docstrings — Google style vs NumPy style

---

## 🔵 Good to Cover — Lower Frequency

### AI/ML Awareness
- [ ] Supervised learning: regression, classification
- [ ] Unsupervised learning: clustering (k-means), dimensionality reduction (PCA)
- [ ] Common algorithms: linear regression, logistic regression, decision tree, random forest, SVM, KNN
- [ ] Overfitting vs underfitting — bias-variance tradeoff
- [ ] `scikit-learn` workflow: `fit()`, `predict()`, `score()`, `Pipeline`
- [ ] `train_test_split`, cross-validation
- [ ] LLMs at a high level — tokens, transformers, context window, prompting
- [ ] AI ethics and responsible AI (Accenture's core focus)

### Concurrency
- [ ] `threading` module — `Thread`, `Lock`, `Event`
- [ ] GIL limitations for CPU-bound tasks
- [ ] `multiprocessing` — bypasses GIL, separate memory
- [ ] `asyncio` — `async def`, `await`, event loop, `gather()`
- [ ] When to use threading vs multiprocessing vs async

### Cloud & DevOps Basics
- [ ] IaaS / PaaS / SaaS — examples of each
- [ ] Containers vs virtual machines
- [ ] Docker basics — `Dockerfile`, `image`, `container`, `docker-compose`
- [ ] CI/CD pipeline — build → test → deploy stages
- [ ] Git workflows — feature branches, PRs, merge vs rebase

### Networking
- [ ] OSI model — 7 layers and what each does
- [ ] TCP vs UDP — connection-oriented vs connectionless
- [ ] HTTP vs HTTPS — TLS handshake basics
- [ ] DNS — how domain resolution works
- [ ] REST vs GraphQL — key trade-offs

---

## 📝 Personal Notes

```
Concepts I find tricky:


Things to re-read the morning of the test:


```
