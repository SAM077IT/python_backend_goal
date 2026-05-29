# 🐍 Python Advanced Concepts & Coding Problems
### Cognizant Python Developer | 3+ Years Experience

---

## ✅ Advanced Topic Checklist

- [ ] Decorators
- [ ] Generators & `yield`
- [ ] Context Managers
- [ ] Closures
- [ ] `async` / `await` — asyncio basics
- [ ] GIL — Multithreading vs Multiprocessing
- [ ] Memory Management & Garbage Collection
- [ ] Metaclasses (awareness level)
- [ ] `__slots__`
- [ ] Coding: Sorting, Strings, Lists, DSA basics

---

## 1. 🎀 Decorators

A decorator is a function that **wraps another function** to extend its behaviour without modifying the original code.

```python
# Basic decorator structure
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function runs")
        result = func(*args, **kwargs)
        print("After function runs")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Before function runs
# Hello, Alice!
# After function runs
```

### Decorator with Arguments (3-level nesting)

```python
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi!")

say_hi()
# Hi!
# Hi!
# Hi!
```

### Real-World Decorators

```python
import functools
import time

# Timing decorator
def timer(func):
    @functools.wraps(func)          # Preserves original function metadata
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} ran in {end - start:.4f}s")
        return result
    return wrapper

# Retry decorator — asked in senior Python interviews
def retry(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(n):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}")
            raise Exception(f"Failed after {n} attempts")
        return wrapper
    return decorator
```

> **Interview Q:** "What is `@functools.wraps` and why use it?"
> **A:** It preserves the decorated function's metadata (`__name__`, `__doc__`, etc.). Without it, `wrapper.__name__` would return `"wrapper"` instead of the original function name.

---

## 2. ⚡ Generators & `yield`

A generator is a **special function** that produces values **lazily** using `yield` — one at a time, saving memory.

```python
# Normal function — builds entire list in memory
def get_squares_list(n):
    return [x**2 for x in range(n)]

# Generator — produces one value at a time
def get_squares_gen(n):
    for x in range(n):
        yield x**2

# Usage
gen = get_squares_gen(1000000)
print(next(gen))   # 0
print(next(gen))   # 1
# Entire million numbers NOT in memory!
```

### Generator Expression

```python
# List comprehension — all in memory
squares_list = [x**2 for x in range(10)]

# Generator expression — lazy evaluation
squares_gen = (x**2 for x in range(10))

print(sum(squares_gen))   # 285 — computed lazily
```

### `yield from` — Delegating to sub-generator

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

print(list(flatten([1, [2, [3, 4]], 5])))
# [1, 2, 3, 4, 5]
```

> **Key distinction:**
> - `return` → function exits, returns a value
> - `yield` → function pauses, returns a value, resumes on next `next()` call
> - Generators are **iterators** — they implement `__iter__` and `__next__`

---

## 3. 🔒 Context Managers — `with` statement

Context managers handle **setup and teardown** automatically (e.g., opening/closing files, DB connections).

```python
# Using built-in context manager
with open("file.txt", "r") as f:
    content = f.read()
# File is automatically closed after the block, even on error

# Creating your own context manager
class DatabaseConnection:
    def __enter__(self):
        print("Opening DB connection")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing DB connection")
        return False   # Don't suppress exceptions

with DatabaseConnection() as db:
    print("Running queries...")
# Output:
# Opening DB connection
# Running queries...
# Closing DB connection
```

### Using `contextlib`

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("Acquiring resource")
    yield "resource_object"
    print("Releasing resource")

with managed_resource() as res:
    print(f"Using {res}")
```

---

## 4. 🔗 Closures

A closure is a function that **remembers** the variables from its enclosing scope even after the outer function has finished executing.

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor          # 'factor' is captured from outer scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# Inspect closure
print(double.__closure__[0].cell_contents)   # 2
```

> **Q:** "What is the difference between a closure and a class?"
> **A:** Both can maintain state. Closures are lightweight for simple cases; classes are better for complex state with multiple methods.

---

## 5. ⚙️ GIL — Global Interpreter Lock

The **GIL** is a mutex in CPython that allows **only one thread** to execute Python bytecode at a time.

```
GIL Impact:
  CPU-bound tasks (calculations) → GIL is a bottleneck → Use multiprocessing
  I/O-bound tasks (file, network, DB) → GIL released during I/O → Threads work fine
```

### Multithreading vs Multiprocessing

```python
import threading
import multiprocessing

# Threading — shared memory, limited by GIL
def task():
    result = sum(range(1000000))

threads = [threading.Thread(target=task) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
# Good for I/O-bound, NOT great for CPU-bound

# Multiprocessing — separate processes, bypasses GIL
processes = [multiprocessing.Process(target=task) for _ in range(4)]
for p in processes:
    p.start()
for p in processes:
    p.join()
# Great for CPU-bound tasks
```

| | Threading | Multiprocessing | asyncio |
|---|-----------|----------------|---------|
| **Memory** | Shared | Separate | Shared |
| **GIL** | Limited by GIL | Bypasses GIL | Single-threaded |
| **Best for** | I/O-bound | CPU-bound | Async I/O |
| **Overhead** | Low | High | Low |

---

## 6. 🔄 Async / Await — asyncio

```python
import asyncio

async def fetch_data(url):
    print(f"Fetching {url}...")
    await asyncio.sleep(1)      # Simulates async I/O (non-blocking)
    return f"Data from {url}"

async def main():
    # Run concurrently
    results = await asyncio.gather(
        fetch_data("api.example.com/users"),
        fetch_data("api.example.com/orders"),
    )
    for r in results:
        print(r)

asyncio.run(main())
# Both fetches run concurrently — total ~1s, not 2s
```

> **Key concept:** `await` suspends the current coroutine and allows other tasks to run.
> - `async def` → defines a coroutine function
> - `await` → yields control back to the event loop

---

## 7. 🧠 Memory Management

Python uses **reference counting** + **cyclic garbage collector**.

```python
import gc
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))   # Reference count (usually count + 1 for the call itself)

# Garbage collection generations
print(gc.get_count())       # (gen0, gen1, gen2) — new objects start in gen0

# Circular reference — reference counting alone can't handle this
a = []
b = [a]
a.append(b)   # a → b → a — circular! GC handles this
del a, b
gc.collect()   # Force GC to clean up
```

### `__slots__` — Memory Optimization

```python
# Without __slots__ — uses __dict__ for each instance (heavy)
class PointNormal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# With __slots__ — fixed attribute set, no __dict__ (lighter)
class PointSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

# PointSlots uses significantly less memory
```

---

## 8. 🧩 Metaclasses (Awareness Level)

```python
# A metaclass is a "class of a class"
# type is the default metaclass in Python

# Custom metaclass
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected"

db1 = Database()
db2 = Database()
print(db1 is db2)   # True — same instance!
```

---

## 9. 💻 Coding Problems — Must Practice

### Problem 1: Find duplicates in a list
```python
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))   # [2, 3]
```

### Problem 2: Check if a string is a palindrome
```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

print(is_palindrome("racecar"))   # True
print(is_palindrome("A man a plan a canal Panama"))   # True
```

### Problem 3: FizzBuzz (classic)
```python
def fizzbuzz(n):
    for i in range(1, n+1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)
```

### Problem 4: Two Sum
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
```

### Problem 5: Fibonacci with generator
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
print([next(fib) for _ in range(10)])
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Problem 6: Find most frequent element
```python
from collections import Counter

def most_frequent(lst):
    counter = Counter(lst)
    return counter.most_common(1)[0][0]

print(most_frequent([1, 2, 2, 3, 3, 3, 4]))   # 3
```

### Problem 7: Flatten nested list
```python
def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, [4]], 5]]))   # [1, 2, 3, 4, 5]
```

### Problem 8: Anagram check *(common at Cognizant)*
```python
def is_anagram(s1, s2):
    return Counter(s1.lower()) == Counter(s2.lower())

print(is_anagram("listen", "silent"))   # True
print(is_anagram("hello", "world"))     # False
```

---

## 10. 🎤 Quick-Fire Q&A

| Question | Answer |
|----------|--------|
| `list` vs `tuple` performance | Tuples are faster for iteration; lists are faster for modification |
| When to use a generator? | When processing large datasets; saves memory with lazy evaluation |
| What is monkey patching? | Dynamically modifying a class or module at runtime (testing, hot-fixes) |
| What is memoization? | Caching function results for the same inputs (use `functools.lru_cache`) |
| Deep copy vs shallow copy? | Deep: independent clone. Shallow: shares nested objects |
| `__getattr__` vs `__getattribute__`? | `__getattribute__` is called always; `__getattr__` is a fallback for missing attributes |

```python
# Memoization example
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

print(fib(50))   # 12586269025 — instant, even for large n
```

---

*Next: SQL Interview Prep → `04_sql_interview_prep.md`*
