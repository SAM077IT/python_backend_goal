# 🐍 Python Core — Questions & Answers

> Click the triangle ▶ next to any question to reveal the answer.
> Covers: Decorators · Closures · Generators · Memory · Types · Comprehensions · Functional tools

---

## Decorators & Closures

<details>
<summary><strong>Q1. What is a decorator in Python? Explain with an example.</strong></summary>

A decorator is a function that takes another function as input, wraps it with additional behaviour, and returns the modified function — without changing the original function's code.

```python
import functools

def log_calls(func):
    @functools.wraps(func)  # preserves __name__, __doc__ of original
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(2, 3)
# Calling add with args=(2, 3), kwargs={}
# add returned 5
```

**Key points:**
- `@log_calls` is syntactic sugar for `add = log_calls(add)`
- `functools.wraps` is essential — without it, `add.__name__` would be `"wrapper"`, breaking introspection and debugging
- `*args, **kwargs` in the wrapper makes the decorator work with any function signature

</details>

---

<details>
<summary><strong>Q2. Write a decorator that takes arguments — e.g. <code>@retry(times=3)</code>.</strong></summary>

When a decorator itself needs arguments, you need an extra layer of nesting: a factory function that returns the actual decorator.

```python
import functools
import time

def retry(times=3, delay=0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < times:
                        time.sleep(delay)
            raise RuntimeError(f"{func.__name__} failed after {times} attempts")
        return wrapper
    return decorator

@retry(times=3, delay=1)
def fetch_data(url):
    # simulates a flaky network call
    raise ConnectionError("timeout")

fetch_data("https://example.com")
```

**Layers:**
1. `retry(times=3)` → returns `decorator`
2. `decorator(func)` → returns `wrapper`
3. `wrapper(*args, **kwargs)` → actual execution logic

</details>

---

<details>
<summary><strong>Q3. What is a closure? How does it differ from a regular function?</strong></summary>

A closure is a function that **remembers the variables from its enclosing scope** even after that scope has finished executing.

```python
def make_multiplier(factor):
    # 'factor' lives in the enclosing scope of 'multiply'
    def multiply(x):
        return x * factor   # 'factor' is a "free variable" — captured by the closure
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# The closure stores the captured variable
print(double.__closure__[0].cell_contents)  # 2
```

**Key difference from a regular function:** a regular function can only access its own local variables and globals. A closure retains a reference to the enclosing function's local variables via `__closure__`.

**Common use:** decorators themselves are closures — `wrapper` captures `func` from the enclosing `decorator` scope.

</details>

---

<details>
<summary><strong>Q4. What does <code>@functools.wraps</code> do and why is it important?</strong></summary>

`@functools.wraps(func)` copies the metadata of the original function (`__name__`, `__doc__`, `__module__`, `__qualname__`, `__annotations__`, `__dict__`) onto the wrapper function.

**Without `wraps`:**
```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Says hello."""
    return f"Hello, {name}"

print(greet.__name__)   # 'wrapper'  ← WRONG
print(greet.__doc__)    # None       ← WRONG
```

**With `wraps`:**
```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """Says hello."""
    return f"Hello, {name}"

print(greet.__name__)   # 'greet'        ← correct
print(greet.__doc__)    # 'Says hello.'  ← correct
```

This matters for debugging, logging, testing frameworks (pytest uses `__name__`), and introspection tools.

</details>

---

<details>
<summary><strong>Q5. What are the built-in decorators <code>@staticmethod</code>, <code>@classmethod</code>, and <code>@property</code>? When do you use each?</strong></summary>

```python
class Circle:
    PI = 3.14159

    def __init__(self, radius):
        self._radius = radius

    # @property — computed attribute, accessed like an attribute not a method call
    @property
    def area(self):
        return self.PI * self._radius ** 2

    @area.setter
    def area(self, value):
        self._radius = (value / self.PI) ** 0.5

    # @classmethod — receives the class (cls) as first arg, not the instance
    # Use for alternative constructors or factory methods
    @classmethod
    def from_diameter(cls, diameter):
        return cls(diameter / 2)

    # @staticmethod — no access to class or instance; a plain utility function
    # grouped inside the class for logical organisation only
    @staticmethod
    def validate_radius(r):
        return r > 0


c1 = Circle(5)
print(c1.area)              # 78.53975  (no parentheses needed)
c2 = Circle.from_diameter(10)   # alternative constructor
print(Circle.validate_radius(-1))  # False
```

| Decorator | First arg | Access to instance? | Access to class? |
|-----------|-----------|---------------------|------------------|
| _(none)_ | `self` | ✅ | via `self.__class__` |
| `@classmethod` | `cls` | ❌ | ✅ |
| `@staticmethod` | _(none)_ | ❌ | ❌ |
| `@property` | `self` | ✅ | via `self.__class__` |

</details>

---

## Generators & Iterators

<details>
<summary><strong>Q6. What is the difference between an iterable, an iterator, and a generator?</strong></summary>

| Concept | Has `__iter__`? | Has `__next__`? | Lazy? |
|---------|----------------|-----------------|-------|
| Iterable | ✅ | ❌ | ❌ |
| Iterator | ✅ | ✅ | ✅ |
| Generator | ✅ | ✅ | ✅ |

```python
# Iterable — can be looped, but not an iterator itself
my_list = [1, 2, 3]
it = iter(my_list)   # creates an iterator from the iterable

# Iterator — stateful, one-directional, exhausted after use
print(next(it))  # 1
print(next(it))  # 2

# Generator — a function with yield; creates an iterator automatically
def count_up(n):
    for i in range(n):
        yield i          # pauses here, resumes on next()

gen = count_up(3)
print(next(gen))   # 0
print(next(gen))   # 1
```

**Why generators matter:** they produce values **lazily** — one at a time — so they use O(1) memory regardless of the sequence size. Processing a 10 GB log file line-by-line with a generator uses barely any RAM.

</details>

---

<details>
<summary><strong>Q7. Write a generator that yields Fibonacci numbers indefinitely.</strong></summary>

```python
def fibonacci():
    a, b = 0, 1
    while True:          # infinite generator — fine because it's lazy
        yield a
        a, b = b, a + b

# Usage — take first 10
from itertools import islice
print(list(islice(fibonacci(), 10)))
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**Contrast with a list version:**
```python
def fibonacci_list(n):
    result = []
    a, b = 0, 1
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result
```

The generator version holds only `a` and `b` in memory regardless of how many values you consume. The list version holds all `n` values.

</details>

---

<details>
<summary><strong>Q8. What is a generator expression? How does it differ from a list comprehension?</strong></summary>

```python
# List comprehension — evaluates immediately, stores all values in memory
squares_list = [x**2 for x in range(1_000_000)]   # ~8 MB in memory

# Generator expression — lazy, produces one value at a time
squares_gen = (x**2 for x in range(1_000_000))    # ~120 bytes in memory

# Both are iterable
print(sum(squares_gen))   # works fine, evaluates lazily
```

**Syntax:** replace `[` with `(`.

**When to use which:**
- List comprehension: when you need to **index**, **iterate multiple times**, or know the **length**
- Generator expression: when you need to **iterate once** (e.g. `sum()`, `max()`, `any()`, `all()`) or when the data is very large

</details>

---

## Types, Memory & the Data Model

<details>
<summary><strong>Q9. What is the difference between mutable and immutable types? Give examples.</strong></summary>

**Immutable** — the object's value cannot be changed after creation. Any "modification" creates a new object.

`int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `bytes`

**Mutable** — the object's value can be changed in place.

`list`, `dict`, `set`, `bytearray`, user-defined class instances (by default)

```python
# Immutable
s = "hello"
id_before = id(s)
s += " world"
print(id(s) == id_before)   # False — a NEW string object was created

# Mutable
lst = [1, 2, 3]
id_before = id(lst)
lst.append(4)
print(id(lst) == id_before)  # True — same object, modified in place
```

**Why this matters in practice:**
```python
# Mutable default argument — classic bug
def append_to(element, target=[]):   # target is created ONCE at function definition
    target.append(element)
    return target

print(append_to(1))   # [1]
print(append_to(2))   # [1, 2]  ← BUG: shares state across calls

# Correct approach
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target
```

</details>

---

<details>
<summary><strong>Q10. Explain shallow copy vs deep copy with a concrete example of where each goes wrong.</strong></summary>

```python
import copy

original = [[1, 2], [3, 4]]

# Shallow copy — new outer list, but inner lists are shared references
shallow = copy.copy(original)
shallow[0].append(99)
print(original)   # [[1, 2, 99], [3, 4]]  ← original is affected!

# Deep copy — completely independent at all levels
original2 = [[1, 2], [3, 4]]
deep = copy.deepcopy(original2)
deep[0].append(99)
print(original2)  # [[1, 2], [3, 4]]  ← original is NOT affected
```

**Rule of thumb:**
- Use `copy.copy()` for flat (non-nested) objects
- Use `copy.deepcopy()` whenever the object contains other mutable objects
- `list[:]` and `list.copy()` are both shallow copies

</details>

---

<details>
<summary><strong>Q11. How does Python manage memory? Explain reference counting and the garbage collector.</strong></summary>

Python uses **two mechanisms** together:

**1. Reference counting (primary)**

Every object has a counter tracking how many references point to it. When the counter hits 0, the memory is freed immediately.

```python
import sys
a = [1, 2, 3]
print(sys.getrefcount(a))   # 2 (a + the temporary ref from getrefcount itself)

b = a
print(sys.getrefcount(a))   # 3

del b
print(sys.getrefcount(a))   # 2 again
```

**2. Cyclic garbage collector (secondary)**

Reference counting alone cannot handle **reference cycles**:
```python
a = []
b = [a]
a.append(b)   # a → b → a: cycle; neither reaches refcount 0
del a, b      # Python's GC detects and cleans this up
```

Python's `gc` module runs periodically to detect and collect cycles.

**The GIL (Global Interpreter Lock):**
- A mutex that allows only one thread to execute Python bytecode at a time
- Makes reference counting thread-safe without per-object locks
- Means CPU-bound multithreaded Python code does NOT run in parallel
- I/O-bound threads (network calls, file I/O) release the GIL while waiting, so threading still helps there
- Solution for CPU-bound parallelism: `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`

</details>

---

<details>
<summary><strong>Q12. What is the difference between <code>is</code> and <code>==</code>?</strong></summary>

- `==` checks **value equality** — do the objects have the same content?
- `is` checks **identity** — are they the same object in memory (same `id()`)?

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  — same content
print(a is b)   # False — different objects

print(a == c)   # True
print(a is c)   # True — c points to the same object as a
```

**Integer interning (CPython):**
```python
x = 256
y = 256
print(x is y)   # True — CPython caches small integers (-5 to 256)

x = 257
y = 257
print(x is y)   # False (in most contexts) — not cached
```

**Rule:** always use `is` for `None`, `True`, `False` comparisons. Use `==` for everything else.

```python
# Correct
if result is None:
    ...

# Incorrect (but works — bad practice)
if result == None:
    ...
```

</details>

---

## Functions & Arguments

<details>
<summary><strong>Q13. Explain <code>*args</code> and <code>**kwargs</code>. What types do they produce inside the function?</strong></summary>

```python
def demo(*args, **kwargs):
    print(type(args))    # <class 'tuple'>
    print(type(kwargs))  # <class 'dict'>
    print(args)
    print(kwargs)

demo(1, 2, 3, name="Alice", age=30)
# (1, 2, 3)
# {'name': 'Alice', 'age': 30}
```

**Full argument ordering rule:**

```python
def full_example(pos1, pos2, *args, kw_only, **kwargs):
    pass
#   positional  │ var-positional │ keyword-only │ var-keyword
```

```python
# Unpacking at call site
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))          # 6 — unpacks list as positional args

opts = {'a': 1, 'b': 2, 'c': 3}
print(add(**opts))         # 6 — unpacks dict as keyword args
```

</details>

---

<details>
<summary><strong>Q14. What are keyword-only arguments? How do you enforce them?</strong></summary>

Any parameter **after a bare `*`** (or after `*args`) can only be passed by keyword, never positionally.

```python
def create_user(name, *, role="user", active=True):
    #                 ^ bare * forces everything after to be keyword-only
    return {"name": name, "role": role, "active": active}

create_user("Alice", role="admin")    # ✅
create_user("Alice", "admin")         # ❌ TypeError: too many positional arguments
```

**Why use this?** It makes function calls self-documenting and prevents argument-order bugs:

```python
# Without keyword-only: easy to mix up argument order
send_email("alice@example.com", True, False)   # What does True mean?

# With keyword-only: impossible to mix up
send_email("alice@example.com", html=True, urgent=False)   # Clear
```

</details>

---

## Comprehensions & Functional Tools

<details>
<summary><strong>Q15. Write examples of list, dict, and set comprehensions with conditions.</strong></summary>

```python
numbers = range(1, 11)

# List comprehension
evens = [x for x in numbers if x % 2 == 0]
# [2, 4, 6, 8, 10]

squares_of_odds = [x**2 for x in numbers if x % 2 != 0]
# [1, 9, 25, 49, 81]

# Nested comprehension (flatten a 2D list)
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6]

# Dict comprehension
word_lengths = {word: len(word) for word in ["apple", "bat", "cherry"]}
# {'apple': 5, 'bat': 3, 'cherry': 6}

inverted = {v: k for k, v in word_lengths.items()}
# {5: 'apple', 3: 'bat', 6: 'cherry'}

# Set comprehension (automatically deduplicates)
unique_lengths = {len(word) for word in ["apple", "bat", "cherry", "ant"]}
# {5, 3, 6}
```

</details>

---

<details>
<summary><strong>Q16. When would you use <code>map()</code> and <code>filter()</code> vs a comprehension?</strong></summary>

```python
nums = [1, 2, 3, 4, 5]

# map() — apply a function to every element
doubled_map = list(map(lambda x: x * 2, nums))
doubled_comp = [x * 2 for x in nums]
# Both: [2, 4, 6, 8, 10]

# filter() — keep elements where function returns True
evens_filter = list(filter(lambda x: x % 2 == 0, nums))
evens_comp = [x for x in nums if x % 2 == 0]
# Both: [2, 4]
```

**In practice:** comprehensions are almost always preferred — they are more readable and Pythonic. Use `map()`/`filter()` when:
- Applying an already-named function (avoids a redundant lambda): `list(map(str, nums))`
- Working with itertools pipelines where you want lazy evaluation without parentheses overhead

```python
# Idiomatic: map with a named function
str_nums = list(map(str, [1, 2, 3]))   # cleaner than [str(x) for x in [1,2,3]]
```

</details>

---

<details>
<summary><strong>Q17. What does <code>zip()</code> do? Give a practical example.</strong></summary>

`zip()` takes multiple iterables and produces tuples of corresponding elements, stopping at the shortest iterable.

```python
names = ["Alice", "Bob", "Charlie"]
scores = [92, 87, 95]

# Pair them up
for name, score in zip(names, scores):
    print(f"{name}: {score}")
# Alice: 92
# Bob: 87
# Charlie: 95

# Create a dict from two lists
grade_dict = dict(zip(names, scores))
# {'Alice': 92, 'Bob': 87, 'Charlie': 95}

# Unzip (transpose) — * unpacks the list of tuples
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
numbers, letters = zip(*pairs)
# numbers = (1, 2, 3), letters = ('a', 'b', 'c')

# zip_longest from itertools — fills missing values
from itertools import zip_longest
list(zip_longest([1, 2, 3], [10, 20], fillvalue=0))
# [(1, 10), (2, 20), (3, 0)]
```

</details>

---

## Context Managers

<details>
<summary><strong>Q18. How does the <code>with</code> statement work? Write a custom context manager two ways.</strong></summary>

The `with` statement calls `__enter__` on entry and `__exit__` on exit — even if an exception occurs. This guarantees resource cleanup.

**Method 1: Class-based**
```python
class Timer:
    import time

    def __enter__(self):
        self.start = self.time.time()
        return self   # value assigned to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = self.time.time() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False   # False = don't suppress exceptions

with Timer() as t:
    sum(range(1_000_000))
# Elapsed: 0.0312s
```

**Method 2: `@contextlib.contextmanager` (simpler)**
```python
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    try:
        yield   # code inside 'with' block runs here
    finally:
        print(f"Elapsed: {time.time() - start:.4f}s")

with timer():
    sum(range(1_000_000))
```

`__exit__` receives exception info — return `True` to suppress the exception, `False` (or `None`) to let it propagate.

</details>

---

*See also: [`qa-oop.md`](./qa-oop.md) · [`qa-coding-problems.md`](./qa-coding-problems.md) · [`qa-pandas-numpy.md`](./qa-pandas-numpy.md)*
