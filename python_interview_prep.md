# Python Interview Preparation — 3+ Years Experience

> 160+ questions covering Core Python, Scenario-Based problems, Coding challenges, and additional Backend-specific topics. All answers are tailored for a Python backend developer with 3+ years of experience.

---

## Table of Contents

- [Part 1 — Core Python (120 Questions)](#part-1--core-python-120-questions)
  - [I. Python Basics](#i-python-basics)
  - [II. Data Types & Variables](#ii-data-types--variables)
  - [III. Strings & Formatting](#iii-strings--formatting)
  - [IV. Lists, Tuples, Sets & Dicts](#iv-lists-tuples-sets--dicts)
  - [V. Functions, Lambdas & Scope](#v-functions-lambdas--scope)
  - [VI. OOP in Python](#vi-oop-in-python)
  - [VII. Exception Handling](#vii-exception-handling)
  - [VIII. File Handling & OS](#viii-file-handling--os)
  - [IX. Iterators & Generators](#ix-iterators--generators)
  - [X. Decorators & Context Managers](#x-decorators--context-managers)
  - [XI. Modules, Packages & Virtual Environments](#xi-modules-packages--virtual-environments)
  - [XII. Memory, Garbage Collection & Optimization](#xii-memory-garbage-collection--optimization)
  - [XIII. Multithreading, Multiprocessing & Async](#xiii-multithreading-multiprocessing--async)
  - [XIV. Python Collections Module](#xiv-python-collections-module)
  - [XV. Database, APIs & Misc](#xv-database-apis--misc)
- [Part 2 — Scenario-Based Questions (20)](#part-2--scenario-based-questions-20)
- [Part 3 — Coding Problems with Solutions (25)](#part-3--coding-problems-with-solutions-25)
- [Part 4 — Additional Backend Developer Questions](#part-4--additional-backend-developer-questions)

---

## Part 1 — Core Python (120 Questions)

---

### I. Python Basics

<details>
<summary><strong>1. What are the main features of Python?</strong></summary>

### Answer

Python is a high-level, general-purpose programming language with several defining characteristics:

| Feature | Description |
|---|---|
| **Interpreted** | Executed line-by-line via the Python Virtual Machine (PVM); no manual compilation step |
| **Dynamically typed** | Variable types are resolved at runtime, not at declaration |
| **Multi-paradigm** | Supports OOP, functional, and procedural programming styles |
| **Garbage collected** | Automatic memory management via reference counting + cyclic GC |
| **Batteries included** | Rich standard library (os, sys, json, re, collections, asyncio, etc.) |
| **Readable syntax** | Indentation-based blocks enforce clean, consistent code structure |
| **Extensive ecosystem** | PyPI has 500,000+ packages for virtually any domain |
| **Portability** | Runs on Windows, macOS, Linux without code changes |

> 💡 **Interview tip:** At 3+ years level, go beyond listing features. Mention tradeoffs — Python's dynamic typing speeds development but can hide bugs that static languages catch at compile time. The GIL limits CPU-bound parallelism.

</details>

---

<details>
<summary><strong>2. Explain Python's execution model.</strong></summary>

### Answer

```
Source Code (.py)
       ↓
   [Compiler]          ← Python's internal compiler (not exposed)
       ↓
  Bytecode (.pyc)      ← Stored in __pycache__/ directory
       ↓
Python Virtual Machine (PVM)
       ↓
   Execution
```

1. **Source → Bytecode:** Python parses and compiles `.py` files into platform-independent bytecode (`.pyc`). This happens automatically.
2. **Bytecode → Execution:** The PVM (an interpreter loop) reads and executes bytecode instructions one by one.
3. **Caching:** `.pyc` files are cached in `__pycache__/`. Python only recompiles if the source file's modification time changes.

```python
# View bytecode yourself
import dis

def add(a, b):
    return a + b

dis.dis(add)
# LOAD_FAST, LOAD_FAST, BINARY_ADD, RETURN_VALUE
```

Different Python implementations exist: **CPython** (default, written in C), **PyPy** (JIT-compiled, faster), **Jython** (runs on JVM), **IronPython** (.NET).

> 💡 **Interview tip:** Mention that CPython's bytecode is not machine code — it still needs the PVM to run. PyPy compiles bytecode further to native machine code via JIT, making it 3–10x faster for CPU-bound tasks.

</details>

---

<details>
<summary><strong>3. What is PEP 8 and why is it important?</strong></summary>

### Answer

PEP 8 is Python's official **style guide** — a set of conventions for writing readable, consistent Python code. It was written by Guido van Rossum (Python's creator).

**Key conventions:**

```python
# Naming
variable_name = "snake_case"
CONSTANT_VALUE = 42
class MyClassName:          # PascalCase
    def method_name(self):  # snake_case
        pass

# Indentation — 4 spaces, never tabs
def function():
    if True:
        pass

# Line length — max 79 chars (99 in many modern projects)
# Two blank lines between top-level definitions
# One blank line between methods in a class

# Imports — one per line, grouped: stdlib → third-party → local
import os
import sys

import requests
import django

from myapp import models

# Spaces around operators
x = 5 + 3       # correct
x=5+3           # wrong

# No space before colon in slices
my_list[1:5]    # correct
my_list[1 : 5]  # wrong
```

**Why it matters:**
- Code is read far more often than written
- Consistent style reduces cognitive load during code reviews
- Most professional teams enforce it via linters (`flake8`, `pylint`, `ruff`)
- Formatters like `black` and `autopep8` auto-enforce it

> 💡 **Interview tip:** Mention that you use `black` (opinionated formatter) + `ruff` (fast linter) in CI pipelines to automatically enforce PEP 8 on every commit.

</details>

---

<details>
<summary><strong>4. What is the difference between a script and a module?</strong></summary>

### Answer

| | Script | Module |
|---|---|---|
| **Purpose** | Meant to be **run directly** | Meant to be **imported** by other code |
| **Entry point** | Has `if __name__ == '__main__':` block | Typically doesn't |
| **`__name__`** | Set to `'__main__'` when run directly | Set to the module's filename when imported |

```python
# utils.py — can be both a script AND a module
def greet(name):
    return f"Hello, {name}"

# This block only runs when executed directly, not when imported
if __name__ == '__main__':
    print(greet("World"))

# When imported: __name__ == 'utils'
# When run directly: __name__ == '__main__'
```

```bash
python utils.py       # __name__ == '__main__', prints "Hello, World"
python -c "import utils; print(utils.greet('Alice'))"  # __name__ == 'utils'
```

> 💡 **Interview tip:** The `if __name__ == '__main__':` guard is a crucial pattern in backend code — it lets you write modules that are both importable libraries and runnable scripts (e.g., management commands, migration scripts).

</details>

---

<details>
<summary><strong>5. What are Python namespaces?</strong></summary>

### Answer

A **namespace** is a mapping from names (identifiers) to objects. It's essentially a dictionary that Python uses to track variable bindings.

**Types of namespaces:**

| Namespace | When Created | When Destroyed | Example |
|---|---|---|---|
| **Built-in** | Python starts | Python exits | `len`, `print`, `None` |
| **Global** | Module is imported/run | Program exits | Module-level variables |
| **Enclosing** | Outer function is called | Outer function returns | Variables in `def outer()` |
| **Local** | Function is called | Function returns | Variables inside a function |

```python
x = "global"          # Global namespace

def outer():
    x = "enclosing"   # Enclosing namespace

    def inner():
        x = "local"   # Local namespace
        print(x)      # "local" — LEGB lookup stops here

    inner()

# Each module has its own global namespace
# You can inspect it:
print(globals())      # all global names in current module
print(locals())       # all local names in current scope
```

> 💡 **Interview tip:** Namespaces prevent naming conflicts across modules. Two modules can both define `connect()` without colliding because they live in separate namespaces. This is why `import module; module.connect()` is safer than `from module import *`.

</details>

---

<details>
<summary><strong>6. Explain the LEGB rule.</strong></summary>

### Answer

LEGB defines Python's **scope resolution order** — the sequence in which Python searches for a name:

**L → E → G → B**

```
L — Local        Variables defined inside the current function
E — Enclosing    Variables in the enclosing function's scope (closures)
G — Global       Module-level variables
B — Built-in     Python's built-in names (len, print, range, etc.)
```

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        # x = "local"   ← uncomment to demonstrate L
        print(x)        # Without local x, finds "enclosing" (E)

    inner()

outer()  # prints "enclosing"

# Modifying outer scope variables
def counter():
    count = 0
    def increment():
        nonlocal count   # tells Python to use the enclosing 'count'
        count += 1
        return count
    return increment

c = counter()
print(c())  # 1
print(c())  # 2

# Modifying global scope
total = 0
def add(n):
    global total    # tells Python to use the module-level 'total'
    total += n
```

> 💡 **Interview tip:** Overusing `global` is a code smell. Prefer returning values or using class instances to share state. `nonlocal` is acceptable in closures and decorators.

</details>

---

<details>
<summary><strong>7. What are Python keywords?</strong></summary>

### Answer

Keywords are **reserved words** with special syntactic meaning. They cannot be used as identifiers.

```python
import keyword
print(keyword.kwlist)
# ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
#  'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
#  'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
#  'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
#  'try', 'while', 'with', 'yield']

# Soft keywords (Python 3.10+) — context-dependent
# 'match', 'case', 'type' — not reserved, can still be used as identifiers
```

**Commonly asked in interviews:**

| Keyword | Purpose |
|---|---|
| `yield` | Turns a function into a generator |
| `nonlocal` | Bind to enclosing function scope |
| `async`/`await` | Define/call coroutines |
| `with` | Context manager protocol |
| `lambda` | Anonymous single-expression function |
| `pass` | No-op placeholder |

</details>

---

<details>
<summary><strong>8. Difference between Python 2 and Python 3.</strong></summary>

### Answer

Python 2 reached **end of life on January 1, 2020**. All new projects use Python 3.

| Feature | Python 2 | Python 3 |
|---|---|---|
| `print` | Statement: `print "hello"` | Function: `print("hello")` |
| Division | `5/2 = 2` (integer) | `5/2 = 2.5` (float), `5//2 = 2` |
| `unicode` | Separate `unicode` type | All strings are Unicode by default |
| `range()` | Returns a list | Returns a lazy iterator (like Python 2's `xrange`) |
| `input()` | Evaluates input as Python code | Reads as string (safe) |
| `super()` | `super(ClassName, self)` | `super()` with no args |
| Type hints | Not supported | Full support via `typing` module |
| `async`/`await` | Not available | Native syntax |
| `f-strings` | Not available | Available (Python 3.6+) |
| Dictionary order | Not guaranteed | Insertion order preserved (3.7+) |

> 💡 **Interview tip:** If asked about Python 2 in 2025+, you can briefly acknowledge it but focus on Python 3. Any production system still on Python 2 is a serious technical debt issue.

</details>

---

<details>
<summary><strong>9. Explain pass, break, continue.</strong></summary>

### Answer

```python
# pass — syntactic placeholder, does absolutely nothing
class MyException(Exception):
    pass   # empty class body — valid syntax

def not_implemented_yet():
    pass   # placeholder until you write the body

# break — immediately exits the nearest enclosing loop
for i in range(10):
    if i == 5:
        break      # loop stops, i never reaches 6-9
print(i)           # 5

# continue — skips the rest of this iteration, jumps to the next
for i in range(10):
    if i % 2 == 0:
        continue   # skip even numbers
    print(i)       # prints 1, 3, 5, 7, 9

# Real-world usage
def process_records(records):
    for record in records:
        if not record.get('active'):
            continue               # skip inactive records
        if record.get('poison'):
            break                  # stop entirely on poison pill
        process(record)
```

</details>

---

<details>
<summary><strong>10. Difference between == and is.</strong></summary>

### Answer

| Operator | Checks | Returns True When |
|---|---|---|
| `==` | **Value equality** | Objects have the same value |
| `is` | **Identity (memory address)** | Both variables point to the exact same object in memory |

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  — same values
print(a is b)   # False — different objects in memory
print(a is c)   # True  — c references the same object as a

# Gotcha: Python interns small integers (-5 to 256) and some strings
x = 256
y = 256
print(x is y)   # True — interned (same object)

x = 257
y = 257
print(x is y)   # False — not interned (separate objects)

# Correct usage of 'is'
# ONLY use 'is' for None, True, False comparisons
if result is None:    # correct
    pass
if result == None:    # works, but style guideline says use 'is'
    pass
```

> 💡 **Interview tip:** Never use `is` to compare strings or integers in production — integer interning is an implementation detail of CPython and is not guaranteed. Always use `==` for value comparisons.

</details>

---

### II. Data Types & Variables

<details>
<summary><strong>11. Mutable vs Immutable types with examples.</strong></summary>

### Answer

| Category | Types | Can change in-place? |
|---|---|---|
| **Immutable** | `int`, `float`, `complex`, `str`, `tuple`, `frozenset`, `bytes` | No — "changes" create new objects |
| **Mutable** | `list`, `dict`, `set`, `bytearray` | Yes — modified in-place |

```python
# Immutable — reassignment creates a new object
s = "hello"
id_before = id(s)
s += " world"
print(id(s) == id_before)   # False — new string object created

# Mutable — modified in-place
lst = [1, 2, 3]
id_before = id(lst)
lst.append(4)
print(id(lst) == id_before)  # True — same object

# Dangerous default argument (common interview gotcha)
def append_to(val, lst=[]):   # WRONG — mutable default is shared across calls
    lst.append(val)
    return lst

print(append_to(1))   # [1]
print(append_to(2))   # [1, 2] ← not what you expected!

def append_to(val, lst=None):  # CORRECT
    if lst is None:
        lst = []
    lst.append(val)
    return lst

# Mutability and function arguments
def modify(lst, num):
    lst.append(99)   # mutates the original list — side effect!
    num += 1         # creates a new int — no effect on caller's variable

my_list = [1, 2]
my_num = 5
modify(my_list, my_num)
print(my_list)  # [1, 2, 99] — modified!
print(my_num)   # 5 — unchanged
```

</details>

---

<details>
<summary><strong>12. What is interning in Python?</strong></summary>

### Answer

**Interning** is a memory optimization where Python reuses existing objects instead of creating new ones for certain values. Python maintains a pool of interned objects.

**What gets interned automatically:**
- Small integers: `-5` to `256`
- String literals that look like identifiers (no spaces, special chars)
- Compile-time string constants

```python
# Integer interning
a = 100; b = 100
print(a is b)   # True — interned

a = 300; b = 300
print(a is b)   # False — not interned (beyond -5..256)

# String interning
s1 = "hello"
s2 = "hello"
print(s1 is s2)   # True — interned (simple identifier-like string)

s1 = "hello world"
s2 = "hello world"
print(s1 is s2)   # May be False — space means not auto-interned

# Manual interning
import sys
s1 = sys.intern("hello world")
s2 = sys.intern("hello world")
print(s1 is s2)   # True — manually interned
```

**Backend use case:** `sys.intern()` is useful for large dictionaries with repeated string keys — reduces memory and speeds up key lookups since identity comparison (`is`) is faster than value comparison (`==`).

</details>

---

<details>
<summary><strong>13. What is object identity?</strong></summary>

### Answer

Every object in Python has a unique **identity** — an integer that is guaranteed to be unique and constant during the object's lifetime. In CPython, this is the memory address.

```python
x = [1, 2, 3]
print(id(x))       # e.g., 140234567890
print(id(x) == id(x))   # True — same object

# id() can be reused after an object is garbage collected
a = [1, 2]
id_a = id(a)
del a
b = [3, 4]
print(id(b) == id_a)   # Possibly True — CPython may reuse the address
```

</details>

---

<details>
<summary><strong>14. What happens when you modify a string?</strong></summary>

### Answer

Strings are **immutable** — you cannot change them in place. Any operation that appears to "modify" a string actually creates a **new string object**.

```python
s = "hello"
print(id(s))        # e.g., 140000001

s = s + " world"    # Creates a NEW string — s now points to the new object
print(id(s))        # Different id

s += "!"            # Same as above — creates yet another new string

# This is why string concatenation in a loop is O(n²)
# Bad:
result = ""
for word in words:
    result += word   # creates a new string each iteration

# Good:
result = "".join(words)  # O(n) — builds one string at the end

# You can use bytearray for mutable byte sequences
ba = bytearray(b"hello")
ba[0] = ord('H')
print(ba)   # bytearray(b'Hello')
```

</details>

---

<details>
<summary><strong>15. How are integers stored?</strong></summary>

### Answer

In CPython, **integers are arbitrary-precision objects** — they can be any size limited only by available memory (no overflow like C's `int`).

Small integers (`-5` to `256`) are pre-allocated and cached (interned) by the interpreter. Larger integers are heap-allocated objects with a variable-length digit array internally.

```python
# No integer overflow in Python
print(2 ** 1000)   # works fine — very large integer

# Check size
import sys
print(sys.getsizeof(0))    # 24 bytes — minimum overhead for an int object
print(sys.getsizeof(2**30))  # 28 bytes
print(sys.getsizeof(2**60))  # 32 bytes — grows with magnitude

# Python integers include a reference count, type pointer, size field, and digit array
```

> 💡 **Interview tip:** This is why Python integers never overflow but are slower than C/Java fixed-width integers. For performance-critical numeric code, use `numpy` arrays which store fixed-width C integers.

</details>

---

<details>
<summary><strong>16. What is a bytearray?</strong></summary>

### Answer

`bytearray` is a **mutable sequence of bytes** (integers 0–255). It's like `bytes` but you can modify it in-place.

```python
# bytes — immutable
b = b"hello"
# b[0] = 72  ← TypeError: 'bytes' object does not support item assignment

# bytearray — mutable
ba = bytearray(b"hello")
ba[0] = 72    # ASCII for 'H'
print(ba)     # bytearray(b'Hello')

# Creating bytearray
ba1 = bytearray(10)           # 10 zero bytes
ba2 = bytearray([65, 66, 67]) # [A, B, C]
ba3 = bytearray(b"data")      # from bytes literal

# Use cases in backend
# - Building binary protocols (network packets, file formats)
# - Efficient in-place manipulation of binary data
# - Reading chunks from binary streams and modifying them

# Conversion
print(bytes(ba))       # b'Hello' — back to immutable bytes
print(ba.decode())     # 'Hello' — to string
```

</details>

---

<details>
<summary><strong>17. Explain tuple packing and unpacking.</strong></summary>

### Answer

```python
# Packing — multiple values automatically grouped into a tuple
point = 3, 4          # tuple (3, 4)
coordinates = 1, 2, 3

# Unpacking — tuple values assigned to individual variables
x, y = 3, 4
a, b, c = (10, 20, 30)

# Extended unpacking (Python 3+) — * collects remaining items
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

*start, last = [1, 2, 3, 4, 5]
# start = [1, 2, 3, 4], last = 5

first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2,3,4], last=5

# Swap without temp variable
a, b = 1, 2
a, b = b, a   # Python evaluates right side first, then unpacks

# Nested unpacking
matrix = [(1, 2), (3, 4), (5, 6)]
for x, y in matrix:
    print(x, y)

# Function returning multiple values (tuple under the hood)
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 4, 1, 5, 9])
```

</details>

---

<details>
<summary><strong>18. What is a frozenset?</strong></summary>

### Answer

`frozenset` is an **immutable version of a set**. Once created, its elements cannot be added or removed.

```python
fs = frozenset([1, 2, 3, 4])

# frozenset supports all read operations of set
print(2 in fs)                    # True
print(fs & frozenset([2, 3]))     # frozenset({2, 3}) — intersection

# But not mutation operations
# fs.add(5)      ← AttributeError
# fs.discard(1)  ← AttributeError

# Key property: frozensets are hashable — can be used as dict keys or set elements
my_dict = {frozenset([1, 2]): "pair", frozenset([3]): "single"}
set_of_sets = {frozenset([1, 2]), frozenset([3, 4])}

# Use cases
# 1. Representing immutable collections of tags, permissions
# 2. Caching/memoization keys when the key is a set of things
# 3. Graph edges (undirected) — frozenset({u, v}) is order-independent
```

</details>

---

<details>
<summary><strong>19. Why are lists not hashable?</strong></summary>

### Answer

Lists are **mutable**. Hashing requires that an object's hash value never changes during its lifetime. If a list were hashable and you mutated it after using it as a dict key, the key would be unfindable (wrong bucket) — breaking dictionary invariants.

```python
my_dict = {}
key = [1, 2, 3]
# my_dict[key] = "value"   ← TypeError: unhashable type: 'list'

# Only immutable types are safely hashable
my_dict[(1, 2, 3)] = "value"          # tuple — OK
my_dict[frozenset([1, 2, 3])] = "v"  # frozenset — OK

# How Python hashing works
# hash(obj) must satisfy: a == b → hash(a) == hash(b)
# Since list mutation can change equality, hash would need to change too
# Changing hash after insertion corrupts the dict/set structure

# Workaround: convert list to tuple for use as key
data = [1, 2, 3]
my_dict[tuple(data)] = "value"
```

</details>

---

<details>
<summary><strong>20. Explain negative indexing.</strong></summary>

### Answer

Python sequences support **negative indices** which count from the end. Index `-1` is the last element, `-2` is second-to-last, etc.

```python
lst = [10, 20, 30, 40, 50]
#       0   1   2   3   4   ← positive indices
#      -5  -4  -3  -2  -1   ← negative indices

print(lst[-1])    # 50 — last element
print(lst[-2])    # 40 — second to last
print(lst[-5])    # 10 — same as lst[0]

# Negative slicing
print(lst[-3:])   # [30, 40, 50] — last 3 elements
print(lst[:-2])   # [10, 20, 30] — all but last 2

# Works on strings too
s = "Python"
print(s[-1])      # 'n'
print(s[-6:])     # 'Python'
print(s[::-1])    # 'nohtyP' — reversed

# Equivalent: lst[-n] == lst[len(lst) - n]
```

</details>

---

### III. Strings & Formatting

<details>
<summary><strong>21. Difference between str() and repr().</strong></summary>

### Answer

| | `str()` | `repr()` |
|---|---|---|
| **Goal** | Human-readable output | Unambiguous, developer-friendly representation |
| **Audience** | End users | Developers / debuggers |
| **`eval(repr(x)) == x`** | Not required | Should hold (when possible) |
| **Dunder method** | `__str__` | `__repr__` |

```python
from datetime import datetime

dt = datetime(2024, 1, 15, 10, 30)
print(str(dt))    # '2024-01-15 10:30:00'       ← readable
print(repr(dt))   # 'datetime.datetime(2024, 1, 15, 10, 30)'  ← reconstructable

# Strings show the difference clearly
s = "hello\nworld"
print(str(s))     # hello
                  # world           ← newline rendered
print(repr(s))    # 'hello\nworld'  ← shows escape sequence

# Custom class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"   # !r applies repr()

    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(3, 4)
print(str(p))    # (3, 4)
print(repr(p))   # Point(3, 4)
```

> 💡 **Interview tip:** Always define `__repr__` in your classes — it's what you see in the Python shell, in logs, and in debuggers. If you only define one, define `__repr__`.

</details>

---

<details>
<summary><strong>22. Explain string interning.</strong></summary>

### Answer

See [Question 12 — Interning](#12-what-is-interning-in-python). String interning is a subset of the general interning mechanism.

Python automatically interns:
- String literals that look like valid Python identifiers
- Strings created at compile time

```python
a = "hello"
b = "hello"
print(a is b)       # True — auto-interned

a = "hello world"   # has a space
b = "hello world"
print(a is b)       # May be False in some contexts

# Force interning
import sys
a = sys.intern("any string whatsoever")
b = sys.intern("any string whatsoever")
print(a is b)       # True — guaranteed

# Use case: large dictionaries with repeated string keys
# Interned strings use identity check (pointer comparison) instead of char-by-char
```

</details>

---

<details>
<summary><strong>23. Methods to reverse a string.</strong></summary>

### Answer

```python
s = "Python Backend"

# 1. Slicing — most Pythonic, O(n)
reversed_s = s[::-1]       # "dnekcaB nohtyP"

# 2. reversed() + join
reversed_s = "".join(reversed(s))

# 3. List reverse
lst = list(s)
lst.reverse()
reversed_s = "".join(lst)

# Reverse words (not characters)
sentence = "Hello World Backend"
reversed_words = " ".join(sentence.split()[::-1])   # "Backend World Hello"

# Performance: slicing is fastest for simple reversal
import timeit
timeit.timeit(lambda: s[::-1], number=100000)
```

</details>

---

<details>
<summary><strong>24. What are f-strings?</strong></summary>

### Answer

F-strings (formatted string literals) were introduced in Python 3.6. They allow embedding expressions directly inside string literals, evaluated at runtime.

```python
name = "Alice"
age = 30
pi = 3.14159

# Basic usage
print(f"Name: {name}, Age: {age}")

# Expressions inside braces
print(f"In 5 years: {age + 5}")
print(f"Upper: {name.upper()}")

# Format specifiers
print(f"Pi: {pi:.2f}")              # "3.14"
print(f"Large: {1000000:,}")        # "1,000,000"
print(f"Hex: {255:#x}")             # "0xff"
print(f"Padded: {name:>10}")        # "     Alice"
print(f"Padded: {name:<10}|")       # "Alice     |"

# Python 3.8+ — self-documenting expressions
x = 42
print(f"{x=}")          # "x=42" — great for debugging!

# Python 3.12+ — nested f-strings
items = ["a", "b", "c"]
print(f"Joined: {', '.join(f'{i}' for i in items)}")

# Multiline f-strings
query = (
    f"SELECT * FROM users "
    f"WHERE id = {user_id} "
    f"AND active = true"
)
```

**Performance:** F-strings are the fastest string formatting method — faster than `.format()` and `%` formatting because they're compiled to efficient bytecode.

</details>

---

<details>
<summary><strong>25. .strip() vs .split().</strong></summary>

### Answer

```python
s = "  hello world  "

# strip() — removes leading/trailing whitespace (or specified chars)
print(s.strip())          # "hello world"
print(s.lstrip())         # "hello world  "
print(s.rstrip())         # "  hello world"
print("###hello###".strip('#'))  # "hello"

# split() — splits string into a list by delimiter
print("a,b,c".split(','))         # ['a', 'b', 'c']
print("hello world".split())      # ['hello', 'world'] — splits on any whitespace
print("a::b::c".split('::'))      # ['a', 'b', 'c']
print("a,b,c".split(',', 1))      # ['a', 'b,c'] — maxsplit=1
print("a,b,c".rsplit(',', 1))     # ['a,b', 'c'] — split from right

# splitlines() — splits on line boundaries
text = "line1\nline2\r\nline3"
print(text.splitlines())   # ['line1', 'line2', 'line3']

# Common pattern — strip then split
csv_line = "  Alice, 30, Engineer  "
parts = [p.strip() for p in csv_line.split(',')]
# ['Alice', '30', 'Engineer']
```

</details>

---

<details>
<summary><strong>26. Explain join().</strong></summary>

### Answer

`str.join(iterable)` joins elements of an iterable into a single string, using the calling string as the separator. The iterable must contain strings.

```python
# Basic usage
words = ["Python", "is", "great"]
print(" ".join(words))    # "Python is great"
print("-".join(words))    # "Python-is-great"
print("".join(words))     # "Pythonisgreat"

# Why join() is faster than concatenation in loops
# Bad — O(n²) due to repeated string creation
result = ""
for word in words:
    result += word + " "

# Good — O(n), builds list then joins once
result = " ".join(words)

# Works with any iterable of strings
print(", ".join(str(x) for x in [1, 2, 3]))   # "1, 2, 3"
print("\n".join(["line1", "line2", "line3"]))  # multiline string

# Common use case — building CSV rows
row = ["Alice", "30", "Engineer"]
csv_line = ",".join(row)
```

</details>

---

<details>
<summary><strong>27. Substring membership check.</strong></summary>

### Answer

```python
text = "Python is a great backend language"

# 'in' operator — O(n), most readable
print("backend" in text)     # True
print("java" in text)        # False
print("Python" not in text)  # False

# str.find() — returns index or -1
idx = text.find("great")    # 15
idx = text.find("java")     # -1

# str.index() — returns index or raises ValueError
text.index("great")         # 15
# text.index("java")        # ValueError

# str.count() — number of non-overlapping occurrences
print("hello".count("l"))   # 2

# str.startswith() / str.endswith()
print("api_key".startswith("api"))    # True
print("image.png".endswith(".png"))   # True
print("file.py".endswith((".py", ".pyx")))  # True — tuple of suffixes

# Case-insensitive check
print("BACKEND" in text.lower())    # check with .lower() or .casefold()
```

</details>

---

<details>
<summary><strong>28. Why strings are immutable.</strong></summary>

### Answer

String immutability is a design choice with several benefits:

1. **Safety:** Strings can be safely shared across multiple references without defensive copying.
2. **Hashability:** Immutable strings can be used as dictionary keys and set elements.
3. **Interning:** Python can maintain a pool of string objects and safely reuse them.
4. **Thread safety:** Immutable strings need no locks for concurrent reads.
5. **Predictability:** No function can accidentally mutate a string you passed to it.

```python
# Strings are safe to share
def process(s):
    s = s.upper()   # creates a NEW string — caller's string unchanged
    return s

original = "hello"
result = process(original)
print(original)   # "hello" — unchanged
print(result)     # "HELLO"

# Immutability enforces a contract: strings you receive won't change under you
# This is especially important in multi-threaded backends
```

</details>

---

<details>
<summary><strong>29. Explain Unicode support.</strong></summary>

### Answer

In Python 3, all strings (`str`) are Unicode by default — specifically UTF-32 internally (or a compact representation). This means Python can handle any character from any language.

```python
# Unicode string literals
s = "Hello, 世界 🌍"
print(len(s))     # 10 — counts Unicode code points, not bytes

# Encoding — convert str to bytes
encoded = s.encode('utf-8')        # b'Hello, \xe4\xb8\x96\xe7\x95\x8c \xf0\x9f\x8c\x8d'
encoded = s.encode('utf-16')
encoded = s.encode('ascii', errors='ignore')   # drops non-ASCII

# Decoding — convert bytes back to str
decoded = encoded.decode('utf-8')

# Unicode escape sequences
print("\u0041")   # 'A' — Unicode code point
print("\U0001F30D")  # '🌍'

# Normalize for comparison (important for user input)
import unicodedata
s1 = "café"
s2 = "cafe\u0301"  # 'e' + combining accent
print(s1 == s2)    # False — different representations!
n1 = unicodedata.normalize('NFC', s1)
n2 = unicodedata.normalize('NFC', s2)
print(n1 == n2)    # True

# Backend best practice: always decode input at boundaries, work with str internally, encode at output
```

</details>

---

<details>
<summary><strong>30. Number formatting options.</strong></summary>

### Answer

```python
n = 1234567.89123

# f-string format specifiers
print(f"{n:,.2f}")        # 1,234,567.89  — thousands separator, 2 decimal
print(f"{n:.0f}")         # 1234568       — round to integer
print(f"{n:e}")           # 1.234568e+06  — scientific notation
print(f"{n:g}")           # 1.23457e+06   — general format (auto)
print(f"{255:#x}")        # 0xff          — hex with prefix
print(f"{255:#o}")        # 0o377         — octal with prefix
print(f"{255:#b}")        # 0b11111111    — binary with prefix
print(f"{0.00123:.2%}")   # 0.12%         — percentage

# format() function — same specifiers
print(format(n, ',.2f'))

# Locale-aware formatting
import locale
locale.setlocale(locale.LC_ALL, '')
print(locale.format_string("%.2f", n, grouping=True))

# Decimal for financial precision
from decimal import Decimal, ROUND_HALF_UP
price = Decimal('19.995')
rounded = price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
print(rounded)    # 20.00 — never use float for money!
```

</details>

---

### IV. Lists, Tuples, Sets & Dicts

<details>
<summary><strong>31. List vs Tuple differences.</strong></summary>

### Answer

| | List | Tuple |
|---|---|---|
| **Mutability** | Mutable | Immutable |
| **Syntax** | `[1, 2, 3]` | `(1, 2, 3)` or `1, 2, 3` |
| **Hashable** | No | Yes (if all elements are hashable) |
| **Performance** | Slightly slower | Slightly faster to create/iterate |
| **Memory** | More (dynamic resizing overhead) | Less |
| **Use case** | Homogeneous sequences that change | Heterogeneous records, dict keys |

```python
# Tuples communicate intent — "these values belong together and won't change"
point = (3.0, 4.0)           # a coordinate pair
rgb = (255, 128, 0)          # a color
person = ("Alice", 30, "eng") # a record

# Lists communicate "a collection of similar things that might change"
names = ["Alice", "Bob", "Charlie"]

# Tuple as dict key
distances = {(0, 0): 0, (1, 0): 1, (0, 1): 1}

# Named tuples — best of both worlds
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(p.x, p.y)    # attribute access
print(p[0], p[1])  # index access still works
```

</details>

---

<details>
<summary><strong>32. List comprehension usage.</strong></summary>

### Answer

```python
# Basic: [expression for item in iterable]
squares = [x**2 for x in range(10)]

# With condition: [expression for item in iterable if condition]
evens = [x for x in range(20) if x % 2 == 0]

# Nested loops
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]

# Equivalent to:
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]    # flatten

# Dict and set comprehensions
word_lengths = {word: len(word) for word in ["python", "is", "great"]}
unique_lengths = {len(word) for word in ["python", "is", "great"]}

# Real-world example
# Filter and transform API response data
active_users = [
    {"id": u["id"], "name": u["name"].title()}
    for u in api_response["users"]
    if u["active"] and u["role"] != "guest"
]

# When NOT to use comprehensions
# If logic is complex (3+ conditions), a regular loop is more readable
# If you need to handle exceptions per-item, use a loop
```

</details>

---

<details>
<summary><strong>33. Tuple immutability advantages.</strong></summary>

### Answer

See [Question 31](#31-list-vs-tuple-differences). Additional advantages:

```python
# 1. Can be used as dictionary keys
cache = {}
cache[(1, 2, 3)] = "result"

# 2. Thread-safe by design — no locks needed for reads
# 3. Slightly faster iteration and access
import timeit
list_time = timeit.timeit(lambda: sum([1,2,3,4,5]), number=1000000)
tuple_time = timeit.timeit(lambda: sum((1,2,3,4,5)), number=1000000)
# tuple is typically 5-15% faster

# 4. Memory efficient
import sys
print(sys.getsizeof([1,2,3,4,5]))   # 120 bytes (Python 3.10)
print(sys.getsizeof((1,2,3,4,5)))   # 80 bytes

# 5. Tuple unpacking is highly optimized
x, y, z = 1, 2, 3   # common pattern in Python, efficient
```

</details>

---

<details>
<summary><strong>34. How dictionary hashing works.</strong></summary>

### Answer

Python dictionaries are **hash tables** — they use hashing to achieve O(1) average-case lookups.

```
Key → hash(key) → index in internal array → check for collision → value
```

1. `hash(key)` computes an integer hash.
2. The hash is reduced to an index: `index = hash(key) % table_size`.
3. Python stores `(hash, key, value)` at that index.
4. On **collision** (two keys map to same index), Python uses open addressing with probing.
5. When the table is ~2/3 full, Python resizes (doubles) the table.

```python
# You can see the hash
print(hash("hello"))      # some integer
print(hash(42))           # 42 (integers hash to themselves for small values)
print(hash((1, 2, 3)))    # hash of tuple — works
# hash([1, 2, 3])         # TypeError — list not hashable

# Custom hashable class — must implement both __hash__ AND __eq__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))   # hash of tuple of fields

p1 = Point(1, 2)
d = {p1: "origin"}
print(d[Point(1, 2)])    # "origin" — equal points, same hash
```

</details>

---

<details>
<summary><strong>35. What is a dict view?</strong></summary>

### Answer

Dict views are **dynamic objects** that provide a live view into a dictionary's keys, values, or items. They update automatically when the dictionary changes.

```python
d = {"a": 1, "b": 2, "c": 3}

keys   = d.keys()    # dict_keys(['a', 'b', 'c'])
values = d.values()  # dict_values([1, 2, 3])
items  = d.items()   # dict_items([('a', 1), ('b', 2), ('c', 3)])

# Views are dynamic — they reflect dictionary changes
d["d"] = 4
print(keys)    # dict_keys(['a', 'b', 'c', 'd']) — updated automatically!

# Keys view supports set-like operations
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print(d1.keys() & d2.keys())   # {'b'} — intersection
print(d1.keys() | d2.keys())   # {'a', 'b', 'c'} — union
print(d1.keys() - d2.keys())   # {'a'} — difference

# Iterating items() is the idiomatic way to loop over key-value pairs
for key, value in d.items():
    print(f"{key}: {value}")
```

</details>

---

<details>
<summary><strong>36. What is defaultdict and OrderedDict?</strong></summary>

### Answer

```python
from collections import defaultdict, OrderedDict

# defaultdict — provides a default value for missing keys
# instead of raising KeyError
word_count = defaultdict(int)      # default factory: int → 0
for word in "the quick brown fox the fox".split():
    word_count[word] += 1          # no KeyError on first access

# defaultdict with list — great for grouping
grouped = defaultdict(list)
for name, dept in [("Alice", "Eng"), ("Bob", "HR"), ("Carol", "Eng")]:
    grouped[dept].append(name)
# {"Eng": ["Alice", "Carol"], "HR": ["Bob"]}

# defaultdict with defaultdict — nested structure
nested = defaultdict(lambda: defaultdict(int))
nested["2024"]["jan"] += 5

# OrderedDict — maintains insertion order
# In Python 3.7+, regular dicts also maintain insertion order
# OrderedDict is still useful for:
# 1. move_to_end() method
# 2. Equality comparison considers order
od = OrderedDict()
od["first"] = 1
od["second"] = 2
od.move_to_end("first")       # move to end
od.move_to_end("second", last=False)  # move to beginning

# OrderedDict equality is order-sensitive
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print(od1 == od2)   # False — different order
print(dict(od1) == dict(od2))   # True — regular dict comparison
```

</details>

---

<details>
<summary><strong>37. Set vs frozenset.</strong></summary>

### Answer

| | `set` | `frozenset` |
|---|---|---|
| **Mutable** | Yes | No |
| **Hashable** | No | Yes |
| **Can be dict key** | No | Yes |
| **Operations** | All set operations + `add`, `discard`, `remove`, `update` | Read-only set operations |

```python
s = {1, 2, 3}
s.add(4)
s.discard(2)

fs = frozenset([1, 2, 3])
# fs.add(4)   ← AttributeError

# frozenset as dict key
permissions_cache = {
    frozenset(["read", "write"]): "editor",
    frozenset(["read"]): "viewer",
}

# Both support set operations
print(s & fs)     # intersection
print(s | fs)     # union
print(s - fs)     # difference
```

</details>

---

<details>
<summary><strong>38. How lists are stored internally.</strong></summary>

### Answer

CPython lists are implemented as **dynamic arrays of pointers** to PyObjects.

- Internally: an array of `(PyObject*)` — each element is a pointer to an object
- Supports O(1) random access by index
- Appending is **amortized O(1)** — the array over-allocates (grows by ~12.5% extra) to avoid resizing on every append
- Inserting/removing at the front or middle is O(n) — requires shifting pointers

```python
import sys

lst = []
for i in range(10):
    lst.append(i)
    print(f"len={len(lst)}, size={sys.getsizeof(lst)}")
# You'll see the allocated size jump in powers of ~2

# List memory contains:
# - PyListObject header (reference count, type, size, allocated)
# - Array of (void*) pointers to elements
# - The elements themselves are stored separately on the heap

# Consequence: all elements are the same "size" in the list (pointer size)
# A list of 1000 integers vs 1000 strings has same list overhead
```

</details>

---

<details>
<summary><strong>39. append() vs extend().</strong></summary>

### Answer

```python
lst = [1, 2, 3]

# append() — adds a SINGLE item (even if it's a list)
lst.append(4)           # [1, 2, 3, 4]
lst.append([5, 6])      # [1, 2, 3, 4, [5, 6]] ← nested list!

lst = [1, 2, 3]

# extend() — adds ALL elements from an iterable
lst.extend([4, 5])      # [1, 2, 3, 4, 5]
lst.extend("ab")        # [1, 2, 3, 4, 5, 'a', 'b'] — iterates string

# + operator — creates a new list (doesn't modify in-place)
new_lst = [1, 2] + [3, 4]   # [1, 2, 3, 4]

# Performance
lst = [1, 2, 3]
lst += [4, 5]    # equivalent to extend — modifies in-place for lists
# (because __iadd__ calls extend for lists)

# insert() — at a specific position (O(n))
lst.insert(0, 0)    # [0, 1, 2, 3, 4, 5] — insert at index 0
```

</details>

---

<details>
<summary><strong>40. Shallow vs Deep copy.</strong></summary>

### Answer

```python
import copy

original = [[1, 2, 3], [4, 5, 6], {"key": "value"}]

# Shallow copy — new outer container, but references to SAME inner objects
shallow = copy.copy(original)
# OR: shallow = original[:] or list(original) or original.copy()

shallow[0].append(99)      # modifies the SAME inner list!
print(original[0])         # [1, 2, 3, 99] — original changed too!
shallow.append([7, 8])     # only modifies shallow (outer container is new)
print(original)            # no [7, 8] — outer was not shared

# Deep copy — recursively clones everything
deep = copy.deepcopy(original)
deep[1].append(99)
print(original[1])   # [4, 5, 6] — unchanged!

# When to use which:
# Shallow: when inner objects are immutable (ints, strings, tuples)
#          or when you intentionally want shared inner objects
# Deep: when you need complete independence from the original

# deepcopy handles circular references
a = []
a.append(a)   # circular!
b = copy.deepcopy(a)   # works — deepcopy tracks visited objects
```

</details>

---

<details>
<summary><strong>41. List iteration vs enumeration.</strong></summary>

### Answer

```python
fruits = ["apple", "banana", "cherry"]

# Basic iteration — when you don't need the index
for fruit in fruits:
    print(fruit)

# enumerate() — when you need index AND value
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# enumerate with custom start index
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")   # 1. apple, 2. banana, 3. cherry

# Anti-pattern — never use range(len(...)) when you can enumerate
# Bad:
for i in range(len(fruits)):
    print(fruits[i])

# Good:
for fruit in fruits:
    print(fruit)

# zip() — iterate multiple lists in parallel
names = ["Alice", "Bob", "Carol"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip_longest — pad shorter iterables with fillvalue
from itertools import zip_longest
for a, b in zip_longest([1, 2, 3], [4, 5], fillvalue=0):
    print(a, b)   # (1,4), (2,5), (3,0)
```

</details>

---

<details>
<summary><strong>42. Methods to merge two dictionaries.</strong></summary>

### Answer

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}   # "b" exists in both — d2 wins in all methods below

# 1. Python 3.9+ — merge operator |
merged = d1 | d2            # {"a": 1, "b": 3, "c": 4}
d1 |= d2                    # in-place update

# 2. {**d1, **d2} — dict unpacking (Python 3.5+)
merged = {**d1, **d2}       # {"a": 1, "b": 3, "c": 4}

# 3. dict.update() — modifies d1 in-place
d1.update(d2)               # d1 is now {"a": 1, "b": 3, "c": 4}

# 4. dict() constructor
merged = dict(d1, **d2)

# 5. ChainMap — no copy, lookup chained
from collections import ChainMap
cm = ChainMap(d1, d2)   # reads from d1 first, then d2

# For custom merge logic (e.g., sum values for shared keys)
from collections import Counter
c1 = Counter({"a": 1, "b": 2})
c2 = Counter({"b": 3, "c": 4})
print(c1 + c2)   # Counter({'b': 5, 'c': 4, 'a': 1})
```

</details>

---

### V. Functions, Lambdas & Scope

<details>
<summary><strong>43–46. Positional-only, keyword-only args, *args, **kwargs, recursion.</strong></summary>

### Answer

```python
# Positional-only arguments (Python 3.8+) — before /
def greet(name, age, /, greeting="Hello"):
    return f"{greeting}, {name}, age {age}"

greet("Alice", 30)           # OK
# greet(name="Alice", age=30)  # TypeError — must be positional

# Keyword-only arguments — after *
def connect(host, *, port=5432, timeout=30):
    pass

connect("localhost")              # OK
connect("localhost", port=5433)   # OK
# connect("localhost", 5433)      # TypeError — port must be keyword

# *args and **kwargs
def log(level, *messages, **metadata):
    print(f"[{level}]", *messages)
    print("metadata:", metadata)

log("INFO", "Server started", "Port 8080", env="prod", version="2.1")

# Recursion
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Python's default recursion limit
import sys
print(sys.getrecursionlimit())   # 1000
sys.setrecursionlimit(5000)      # can increase

# Tail recursion is NOT optimized in Python — prefer iteration for deep recursion
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

</details>

---

<details>
<summary><strong>47. What is a closure?</strong></summary>

### Answer

A **closure** is a function that "closes over" variables from its enclosing scope — it retains access to those variables even after the enclosing function has returned.

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor   # 'factor' is a free variable — closed over
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# Each closure has its own cell containing 'factor'
print(double.__closure__[0].cell_contents)  # 2
print(triple.__closure__[0].cell_contents)  # 3

# Real-world use case — function factories, decorators, callbacks
def make_validator(min_val, max_val):
    def validate(value):
        if not (min_val <= value <= max_val):
            raise ValueError(f"Value {value} out of range [{min_val}, {max_val}]")
        return value
    return validate

validate_age = make_validator(0, 120)
validate_score = make_validator(0, 100)

# Classic gotcha — loop variable capture
# Bad:
funcs = [lambda: i for i in range(5)]
print([f() for f in funcs])   # [4, 4, 4, 4, 4] — all capture same 'i'

# Fix: use default argument to capture value at definition time
funcs = [lambda i=i: i for i in range(5)]
print([f() for f in funcs])   # [0, 1, 2, 3, 4]
```

</details>

---

<details>
<summary><strong>48–54. Lambda, Memoization, Decorators, functools.wraps, Partial, First-class, Currying.</strong></summary>

### Answer

```python
# Lambda — anonymous single-expression function
square = lambda x: x ** 2
sort_key = lambda item: (item["priority"], item["name"])
items.sort(key=lambda x: x["created_at"], reverse=True)

# Memoization — cache results of expensive function calls
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(100))       # instant — cached
print(fibonacci.cache_info())  # CacheInfo(hits=..., misses=..., ...)

# Manual memoization with dict
def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# Decorators
def timer(func):
    import time
    from functools import wraps

    @wraps(func)   # preserves __name__, __doc__, __wrapped__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_query():
    import time; time.sleep(0.1)

# functools.wraps — why it matters
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_func():
    """My docstring."""
    pass

print(my_func.__name__)   # 'wrapper' — WRONG without @wraps

# Partial functions — fix some arguments
from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)
print(square(5))   # 25
print(cube(3))     # 27

# First-class functions — functions are objects
def apply(func, value):
    return func(value)

print(apply(str.upper, "hello"))   # "HELLO"
functions = [str.upper, str.lower, str.title]
print([f("python") for f in functions])

# Currying — transform f(a, b, c) into f(a)(b)(c)
def curry(func):
    from inspect import signature
    n = len(signature(func).parameters)
    def curried(*args):
        if len(args) >= n:
            return func(*args)
        return lambda *more: curried(*(args + more))
    return curried

@curry
def add(a, b, c):
    return a + b + c

print(add(1)(2)(3))   # 6
print(add(1, 2)(3))   # 6
```

</details>

---

### VI. OOP in Python

<details>
<summary><strong>55–66. OOP Pillars, __init__, Dunder methods, MRO, super(), Abstract classes, Encapsulation.</strong></summary>

### Answer

```python
# OOP Pillars
# 1. Encapsulation — bundling data + methods, controlling access
# 2. Inheritance — subclass inherits from parent
# 3. Polymorphism — different classes implement the same interface
# 4. Abstraction — hiding complexity behind simple interfaces

from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name: str, age: int):
        self._name = name          # protected (convention)
        self.__age = age           # private (name-mangled to _Animal__age)

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self.__age = value

    @abstractmethod
    def speak(self) -> str:       # must be overridden by subclasses
        pass

    def __repr__(self):
        return f"{type(self).__name__}(name={self._name!r}, age={self.__age})"

    def __str__(self):
        return f"{self._name} (age {self.__age})"

    def __eq__(self, other):
        return isinstance(other, type(self)) and self._name == other._name

    def __hash__(self):
        return hash(self._name)

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)   # super() calls parent __init__
        self.breed = breed

    def speak(self):
        return f"{self._name} says: Woof!"

    @staticmethod
    def is_good_boy():
        return True    # doesn't access instance or class

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["age"], data["breed"])

# Multiple Inheritance + MRO (Method Resolution Order)
class A:
    def method(self): return "A"

class B(A):
    def method(self): return "B"

class C(A):
    def method(self): return "C"

class D(B, C):   # Diamond inheritance
    pass

print(D.__mro__)
# [D, B, C, A, object] — C3 linearization algorithm
print(D().method())   # "B" — follows MRO

# Composition vs Inheritance
# Prefer composition when "has-a" relationship
class Engine:
    def start(self): return "engine started"

class Car:
    def __init__(self):
        self.engine = Engine()   # composition — Car HAS-AN engine

    def start(self):
        return self.engine.start()
```

</details>

---

### VII. Exception Handling

<details>
<summary><strong>67–76. Exception handling, custom exceptions, chaining, context managers.</strong></summary>

### Answer

```python
# Error vs Exception
# BaseException — root of all exceptions
# Exception — root of "normal" exceptions (inherits BaseException)
# SystemExit, KeyboardInterrupt, GeneratorExit — directly under BaseException

# try-except-else-finally
def parse_config(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {path}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {path}") from e   # exception chaining
    else:
        # Runs only if NO exception was raised in try block
        validate_config(data)
        return data
    finally:
        # ALWAYS runs — cleanup goes here
        logger.info(f"Config load attempt for {path}")

# Custom exceptions
class AppError(Exception):
    """Base exception for this application."""
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field = field
        super().__init__(f"Validation error on '{field}': {message}")

class DatabaseError(AppError):
    pass

# raise vs assert
# raise — for runtime error conditions (user input, API failures)
# assert — for debugging invariants (should never fail in production)
def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")   # correct
    assert isinstance(a, (int, float))         # debugging only

# Exception chaining
try:
    result = db.query()
except DatabaseConnectionError as e:
    raise ServiceUnavailableError("DB unreachable") from e
    # preserves original traceback in __cause__

# Suppress exception chaining
raise ServiceUnavailableError("DB unreachable") from None

# Context manager with exceptions
class ManagedResource:
    def __enter__(self):
        self.resource = acquire()
        return self.resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        release(self.resource)
        # Return True to suppress the exception
        # Return None/False to let it propagate
        if exc_type is ResourceWarning:
            return True    # suppress warnings
        return False       # propagate everything else

# Why avoid bare except:
try:
    risky()
except:           # catches KeyboardInterrupt, SystemExit — NEVER do this!
    pass

try:
    risky()
except Exception:   # catches all normal exceptions — acceptable but broad
    pass

try:
    risky()
except (ValueError, TypeError) as e:   # preferred — explicit exceptions
    handle(e)
```

</details>

---

### VIII. File Handling & OS

<details>
<summary><strong>77–84. File handling, OS module, serialization.</strong></summary>

### Answer

```python
import os
import json
import pickle
import shutil

# Open and read files — always use context manager
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()        # entire file as string
    # OR
    lines = f.readlines()     # list of lines including \n
    # OR
    for line in f:            # iterate line by line (memory efficient)
        process(line.rstrip('\n'))

# Write modes
# 'r'  — read (default)
# 'w'  — write (overwrites)
# 'a'  — append
# 'x'  — exclusive create (fails if file exists)
# 'rb' — read binary
# 'wb' — write binary

# Text vs binary
with open("image.png", "rb") as f:   # binary
    data = f.read()

with open("data.txt", "r", encoding="utf-8") as f:   # text — handles line endings and encoding
    data = f.read()

# File seeking
with open("data.bin", "rb") as f:
    f.seek(100)       # move to byte position 100
    f.seek(0, 2)      # seek to end (0 bytes from end)
    size = f.tell()   # current position = file size

# Check file existence
os.path.exists("file.txt")
os.path.isfile("file.txt")
os.path.isdir("mydir")
from pathlib import Path
Path("file.txt").exists()

# OS module — common operations
os.getcwd()                    # current directory
os.listdir(".")                # list directory contents
os.makedirs("a/b/c", exist_ok=True)
os.environ.get("DATABASE_URL")
os.path.join("path", "to", "file")   # cross-platform path joining
os.path.abspath("relative")

# Prefer pathlib (Python 3.4+) — object-oriented, cleaner
from pathlib import Path

p = Path("/home/user/data")
p.mkdir(parents=True, exist_ok=True)
for f in p.glob("*.json"):
    print(f.name, f.stat().st_size)

# shutil — high-level file operations
shutil.copy("src.txt", "dst.txt")
shutil.copytree("src_dir", "dst_dir")
shutil.move("old.txt", "new.txt")
shutil.rmtree("old_dir")
shutil.make_archive("backup", "zip", ".", "my_folder")

# Serialization
# JSON — human-readable, interoperable
data = {"key": "value", "nums": [1, 2, 3]}
json_str = json.dumps(data, indent=2)
json.dump(data, open("out.json", "w"))
loaded = json.loads(json_str)

# Pickle — Python-specific, not safe for untrusted data
with open("data.pkl", "wb") as f:
    pickle.dump(obj, f)
with open("data.pkl", "rb") as f:
    obj = pickle.load(f)
```

</details>

---

### IX. Iterators & Generators

<details>
<summary><strong>85–94. Iterators, generators, yield, itertools, lazy evaluation.</strong></summary>

### Answer

```python
# Iterator Protocol — any object with __iter__ and __next__
class CountUp:
    def __init__(self, start, stop):
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        val = self.current
        self.current += 1
        return val

for n in CountUp(1, 5):
    print(n)   # 1 2 3 4

# Generator — simpler iterator using yield
def count_up(start, stop):
    while start < stop:
        yield start
        start += 1

gen = count_up(1, 5)
print(next(gen))   # 1
print(next(gen))   # 2

# Generator vs Iterator
# Generator:    function with yield, creates iterator automatically
# Iterator:     object with __iter__ + __next__ (generator IS an iterator)
# Iterable:     object with __iter__ (list, tuple, dict, generator, etc.)

# Generator expressions — lazy, memory efficient
squares_gen = (x**2 for x in range(1000000))  # no memory allocated yet
total = sum(x for x in squares_gen if x % 2 == 0)

# Real-world generator — stream large datasets
def read_large_file(path, chunk_size=8192):
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk

def parse_jsonl(path):
    """Yield one JSON object per line — memory efficient."""
    with open(path) as f:
        for line in f:
            yield json.loads(line.strip())

# yield from — delegate to sub-generator
def chain(*iterables):
    for it in iterables:
        yield from it

# itertools — powerful lazy combinatorics
import itertools

list(itertools.islice(count_up(1, 1000), 5))  # first 5 items
list(itertools.takewhile(lambda x: x < 5, count_up(1, 100)))
list(itertools.dropwhile(lambda x: x < 5, [1, 3, 5, 7, 2]))
list(itertools.chain([1, 2], [3, 4], [5, 6]))
list(itertools.product([1, 2], [3, 4]))   # Cartesian product
list(itertools.combinations([1,2,3], 2))
list(itertools.groupby(sorted_data, key=lambda x: x["dept"]))

# map vs list comprehension
# map is lazy (returns iterator), comprehension is eager (returns list)
squared = map(lambda x: x**2, range(10))   # lazy
squared = [x**2 for x in range(10)]        # eager
```

</details>

---

### X. Decorators & Context Managers

<details>
<summary><strong>95–104. Decorators, context managers, contextlib.</strong></summary>

### Answer

```python
import functools
import contextlib
import time

# Decorator with arguments — requires three levels of nesting
def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def call_api(url):
    return requests.get(url)

# Class-based decorator
class RateLimit:
    def __init__(self, calls_per_second):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - self.last_call
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_call = time.time()
            return func(*args, **kwargs)
        return wrapper

@RateLimit(calls_per_second=5)
def api_call():
    pass

# Context Managers
# Method 1: __enter__ / __exit__
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False   # don't suppress exceptions

with Timer() as t:
    slow_operation()
print(t.elapsed)

# Method 2: contextlib.contextmanager — simpler
@contextlib.contextmanager
def managed_transaction(db):
    tx = db.begin()
    try:
        yield tx
        tx.commit()
    except Exception:
        tx.rollback()
        raise

with managed_transaction(db) as tx:
    tx.execute("INSERT ...")

# contextlib utilities
@contextlib.suppress(FileNotFoundError)   # silently ignore specific exceptions
def maybe_delete(path):
    os.remove(path)

with contextlib.suppress(FileNotFoundError):
    os.remove("maybe_exists.txt")

# contextlib.ExitStack — dynamic context managers
with contextlib.ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in file_paths]
    process_files(files)
```

</details>

---

### XI. Modules, Packages & Virtual Environments

<details>
<summary><strong>105–112. Modules, packages, virtualenv, pip.</strong></summary>

### Answer

```
# Module — single .py file
# Package — directory with __init__.py containing multiple modules

mypackage/
    __init__.py          # makes directory a package; can expose public API
    models.py
    utils.py
    api/
        __init__.py
        endpoints.py
        auth.py
```

```python
# __init__.py — control public API
# mypackage/__init__.py
from .models import User, Product    # expose at package level
from .utils import format_date

__all__ = ["User", "Product", "format_date"]  # controls 'from pkg import *'

# Relative imports (inside packages)
from .models import User          # same package
from ..utils import helper        # parent package

# PYTHONPATH — directories Python searches for modules
import sys
sys.path.append("/path/to/my/libs")
# Or set PYTHONPATH environment variable

# Virtual environments
# venv — built-in (Python 3.3+), lightweight
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# pip — package manager
pip install requests
pip install requests==2.31.0     # pinned version
pip install -r requirements.txt

# requirements.txt
pip freeze > requirements.txt    # capture current environment

# Comparison
# venv:   built-in, simple, one Python version
# pipenv: Pipfile + lock file, manages virtualenv + packages together
# conda:  manages non-Python deps too, good for data science
# poetry: modern dependency resolution, lock file, publishing support

# Recommended for backend: venv + pip-tools or poetry
```

</details>

---

### XII. Memory, Garbage Collection & Optimization

<details>
<summary><strong>113–124. Memory management, GIL, GC, weak references.</strong></summary>

### Answer

```python
import gc
import sys
import weakref

# Reference Counting — CPython's primary GC mechanism
# Every object has ob_refcnt
# When refcount drops to 0, object is immediately freed

import ctypes

a = [1, 2, 3]
print(sys.getrefcount(a))    # 2 — local + getrefcount's argument

b = a                        # refcount → 3
del b                        # refcount → 2

# Cyclic GC — handles reference cycles
# Reference counting alone can't free these
import gc

class Node:
    def __init__(self):
        self.child = None

a = Node()
b = Node()
a.child = b
b.child = a   # cycle!
del a, b      # refcount still > 0 because of cycle
gc.collect()  # finds and frees cycles

# GC generations — objects survive collection → promoted to older generation
print(gc.get_count())       # (gen0, gen1, gen2) counts
gc.disable()                # disable GC (careful — leaks cycles)
gc.enable()

# GIL — Global Interpreter Lock
# Only ONE thread executes Python bytecode at a time
# Impact:
#   CPU-bound multithreading → no speedup (GIL prevents parallelism)
#   I/O-bound multithreading → works fine (GIL released during I/O)

# Memory leaks — common causes
# 1. Global containers growing unboundedly
# 2. Circular references (handled by gc, but delayed)
# 3. Caches without eviction policies
# 4. Callbacks/closures keeping large objects alive

# Weak references — reference without preventing GC
cache = {}
def get_cached(key, factory):
    ref = cache.get(key)
    obj = ref() if ref is not None else None
    if obj is None:
        obj = factory()
        cache[key] = weakref.ref(obj)
    return obj

# sys.getsizeof() — size of object itself (not children)
print(sys.getsizeof([1, 2, 3]))   # 88 bytes — list overhead only

# Total size including contents
def total_size(obj, seen=None):
    """Recursively calculate total size of object."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum(total_size(v, seen) for v in obj.values())
        size += sum(total_size(k, seen) for k in obj.keys())
    elif hasattr(obj, '__iter__') and not isinstance(obj, str):
        size += sum(total_size(i, seen) for i in obj)
    return size

# Python is slow because:
# 1. Dynamic typing — type checks at runtime
# 2. Everything is an object — even integers
# 3. GIL prevents true parallelism
# 4. Interpreted bytecode vs native machine code

# Optimization strategies
# - Use built-ins (implemented in C) — sum, map, filter
# - NumPy for numerical computation
# - Use generators instead of lists where possible
# - Profile first (cProfile, line_profiler) before optimizing
# - Consider PyPy for CPU-bound tasks
# - Cython or ctypes for C extensions
```

</details>

---

### XIII. Multithreading, Multiprocessing & Async

<details>
<summary><strong>125–136. Threading, multiprocessing, asyncio, coroutines.</strong></summary>

### Answer

```python
import threading
import multiprocessing
import asyncio
import concurrent.futures

# Thread vs Process
# Thread:  shares memory with other threads, lightweight, GIL-limited for CPU tasks
# Process: separate memory space, heavier, true parallelism, no GIL issue

# Threading — best for I/O-bound tasks
def download(url):
    response = requests.get(url)
    return response.text

urls = ["http://example.com/1", "http://example.com/2"]
threads = [threading.Thread(target=download, args=(url,)) for url in urls]
for t in threads: t.start()
for t in threads: t.join()

# Thread safety — Lock, Semaphore, Event
lock = threading.Lock()
counter = 0

def increment():
    global counter
    with lock:         # prevents race condition
        counter += 1

# Semaphore — limit concurrent access
semaphore = threading.Semaphore(5)   # max 5 threads at once
with semaphore:
    limited_resource()

# Event — signal between threads
event = threading.Event()
event.set()           # signal
event.wait()          # block until set
event.clear()         # reset

# Deadlock — two threads waiting on each other's lock
# Prevention: always acquire locks in the same order

# Multiprocessing — true parallelism for CPU-bound tasks
def cpu_heavy(n):
    return sum(i**2 for i in range(n))

with multiprocessing.Pool(processes=4) as pool:
    results = pool.map(cpu_heavy, [10**6, 10**6, 10**6, 10**6])

# Share data between processes
manager = multiprocessing.Manager()
shared_dict = manager.dict()
shared_list = manager.list()

# concurrent.futures — high-level API (preferred)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(download, url) for url in urls]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_heavy, [10**6] * 4))

# Asyncio — single-threaded concurrent I/O
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)   # concurrent execution

asyncio.run(main())

# Coroutine vs Thread:
# Coroutine: cooperative (explicitly yields with await), single-threaded, no race conditions
# Thread:    preemptive (OS switches), multi-threaded, needs synchronization

# Event loop concept
# asyncio maintains an event loop that runs coroutines
# When a coroutine hits 'await', it suspends and lets others run
# The loop picks up the next ready coroutine

# async vs await
# async def — defines a coroutine function
# await expr — suspends coroutine until expr completes
```

</details>

---

### XIV. Python Collections Module

<details>
<summary><strong>137–146. defaultdict, Counter, namedtuple, deque, ChainMap, heapq, bisect.</strong></summary>

### Answer

```python
from collections import (
    defaultdict, Counter, namedtuple, deque, ChainMap, OrderedDict
)
import heapq
import bisect

# Counter — count hashable objects
words = "the quick brown fox jumps over the lazy dog the".split()
c = Counter(words)
print(c.most_common(3))      # [('the', 3), ('quick', 1), ...]
print(c["the"])              # 3
print(c["missing"])          # 0 — no KeyError

# Counter arithmetic
c1 = Counter({"a": 3, "b": 2})
c2 = Counter({"a": 1, "c": 4})
print(c1 + c2)    # Counter({'c': 4, 'a': 4, 'b': 2})
print(c1 - c2)    # Counter({'a': 2, 'b': 2}) — only positive
print(c1 & c2)    # Counter({'a': 1}) — min of each
print(c1 | c2)    # Counter({'c': 4, 'a': 3, 'b': 2}) — max of each

# namedtuple — lightweight immutable record
Point = namedtuple('Point', ['x', 'y'])
Person = namedtuple('Person', ['name', 'age', 'role'])

p = Point(3.0, 4.0)
print(p.x, p.y)    # attribute access
print(p[0], p[1])  # index access
print(p._asdict())  # OrderedDict

# Python 3.6+ — typing.NamedTuple (supports type hints + defaults)
from typing import NamedTuple

class Employee(NamedTuple):
    name: str
    department: str
    salary: float = 0.0

emp = Employee("Alice", "Engineering", 95000)

# deque — double-ended queue, O(1) append/pop from both ends
dq = deque(maxlen=5)   # bounded deque — auto-discards oldest
dq.append(1)
dq.appendleft(0)
dq.pop()
dq.popleft()
dq.rotate(2)           # rotate elements

# ChainMap — multiple dicts, lookup in order
defaults = {"color": "blue", "size": "medium"}
user_settings = {"color": "red"}
settings = ChainMap(user_settings, defaults)
print(settings["color"])   # "red" — user_settings first
print(settings["size"])    # "medium" — falls through to defaults

# heapq — min-heap (binary heap on a list)
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)
print(heapq.heappop(heap))   # 2 — smallest

# nlargest / nsmallest
data = [3, 1, 4, 1, 5, 9, 2, 6]
print(heapq.nlargest(3, data))    # [9, 6, 5]
print(heapq.nsmallest(3, data))   # [1, 1, 2]

# Max heap — negate values
max_heap = []
for val in data:
    heapq.heappush(max_heap, -val)
print(-heapq.heappop(max_heap))   # 9

# bisect — binary search on sorted lists
sorted_list = [1, 3, 5, 7, 9, 11]
idx = bisect.bisect_left(sorted_list, 7)    # 3 — insertion point, 7 found
idx = bisect.bisect_right(sorted_list, 7)   # 4 — after 7
bisect.insort(sorted_list, 6)               # insert maintaining sort order
```

</details>

---

### XV. Database, APIs & Misc

<details>
<summary><strong>147–156. SQL, ORM, JSON, requests, logging, scheduling, argparse, serialization.</strong></summary>

### Answer

```python
# Python + SQL — sqlite3 (built-in)
import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))   # parameterized!
rows = cursor.fetchall()
conn.commit()
conn.close()

# With context manager
with sqlite3.connect("mydb.db") as conn:
    rows = conn.execute("SELECT * FROM users").fetchall()

# ORM concept — SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

engine = create_engine("postgresql://user:pass@localhost/db")
with Session(engine) as session:
    users = session.query(User).filter(User.name == "Alice").all()

# JSON
import json
data = {"key": "value", "nums": [1, 2, 3]}
json_str = json.dumps(data, indent=2, default=str)   # default=str handles non-serializable
loaded = json.loads(json_str)

# HTTP requests
import requests

response = requests.get("https://api.example.com/users", params={"page": 1})
response.raise_for_status()   # raises HTTPError for 4xx/5xx
data = response.json()

# Session for connection reuse
session = requests.Session()
session.headers.update({"Authorization": "Bearer token"})
response = session.get("https://api.example.com/data")

# Logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)
logger.info("Server started")
logger.error("Failed to connect", exc_info=True)   # includes traceback

# Argparse
import argparse

parser = argparse.ArgumentParser(description="My CLI tool")
parser.add_argument("input", help="Input file path")
parser.add_argument("--output", "-o", default="out.txt")
parser.add_argument("--verbose", "-v", action="store_true")
parser.add_argument("--count", type=int, default=10)
args = parser.parse_args()

# Scheduling with APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_task, 'cron', hour=3, minute=0)   # daily at 3am
scheduler.add_job(health_check, 'interval', minutes=5)
scheduler.start()

# Serialization: JSON vs Pickle vs msgpack
# JSON — human readable, interoperable, slow for binary data
# Pickle — Python only, supports arbitrary objects, NOT safe for untrusted data
# msgpack — binary, fast, compact, cross-language

import pickle
serialized = pickle.dumps(complex_object)
restored = pickle.loads(serialized)
```

</details>

---

## Part 2 — Scenario-Based Questions (20)

<details>
<summary><strong>157. You have a huge list of dictionaries; how do you sort efficiently?</strong></summary>

### Answer

```python
employees = [
    {"name": "Alice", "dept": "Eng", "salary": 95000, "age": 30},
    {"name": "Bob",   "dept": "HR",  "salary": 75000, "age": 25},
    # ... millions more
]

# 1. Single key — use key= parameter (Timsort, O(n log n))
by_salary = sorted(employees, key=lambda e: e["salary"], reverse=True)

# 2. Multiple keys — tuple key (stable sort)
by_dept_salary = sorted(employees, key=lambda e: (e["dept"], -e["salary"]))

# 3. operator.itemgetter — faster than lambda for dict access
from operator import itemgetter
by_name = sorted(employees, key=itemgetter("name"))
by_dept_name = sorted(employees, key=itemgetter("dept", "name"))

# 4. In-place sort — doesn't create a new list (saves memory)
employees.sort(key=itemgetter("salary"), reverse=True)

# 5. Schwartzian transform (Decorate-Sort-Undecorate) — for expensive key computation
# Pre-compute sort key once
decorated = [(expensive_key(e), e) for e in employees]
decorated.sort()
sorted_employees = [e for _, e in decorated]

# 6. Partial sort — only need top N (use heapq)
import heapq
top_5 = heapq.nlargest(5, employees, key=itemgetter("salary"))
```

> 💡 **Interview tip:** Python's `sorted()` uses Timsort, which is O(n log n) and stable (equal elements keep their relative order). For very large datasets that don't fit in memory, mention external sorting or database-level ORDER BY.

</details>

---

<details>
<summary><strong>158. A function is slow; how do you profile and optimize it?</strong></summary>

### Answer

```python
# Step 1: Measure first — never optimize without profiling
import cProfile
import pstats

# cProfile — function-level profiling
cProfile.run("my_slow_function()", "profile_output")
stats = pstats.Stats("profile_output")
stats.sort_stats("cumulative")
stats.print_stats(20)    # top 20 slowest functions

# line_profiler — line-level profiling (pip install line_profiler)
@profile   # add @profile decorator, then run: kernprof -l -v script.py
def my_slow_function():
    ...

# timeit — micro-benchmarking
import timeit
t = timeit.timeit(lambda: my_function(), number=1000)
print(f"Average: {t/1000:.6f}s")

# memory_profiler — memory usage per line
from memory_profiler import profile

# Step 2: Common optimizations
# - Replace loops with vectorized NumPy operations
# - Use built-in functions (implemented in C)
# - Cache repeated calculations with @lru_cache
# - Use generators instead of building full lists
# - Profile I/O — is the bottleneck in DB/network, not CPU?
# - Use sets for O(1) membership instead of lists (O(n))

# Example: finding common elements
# Slow: O(n*m)
common = [x for x in list1 if x in list2]

# Fast: O(n+m) with sets
common = list(set(list1) & set(list2))

# Step 3: Advanced
# - PyPy for CPU-bound pure Python
# - Cython, C extensions for hot paths
# - asyncio for I/O-bound
# - multiprocessing for CPU-bound parallelism
```

</details>

---

<details>
<summary><strong>159. API request taking too long — steps to troubleshoot?</strong></summary>

### Answer

```python
# Systematic approach:

# 1. Add timing at each layer
import time

@contextmanager
def timed(label):
    start = time.perf_counter()
    yield
    print(f"{label}: {time.perf_counter()-start:.3f}s")

with timed("DB query"):
    results = db.execute(query)

with timed("Serialization"):
    data = serialize(results)

# 2. Check if it's the DB
# - EXPLAIN ANALYZE the slow query
# - Add missing indexes
# - Optimize N+1 queries

# 3. Check if it's external API calls
import requests
response = requests.get(url, timeout=5)
print(response.elapsed.total_seconds())

# 4. Add HTTP connection pooling
session = requests.Session()   # reuses connections
adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=20)
session.mount('https://', adapter)

# 5. Add caching
from functools import lru_cache
import redis

r = redis.Redis()
def get_user(user_id):
    cached = r.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    user = db.fetch_user(user_id)
    r.setex(f"user:{user_id}", 300, json.dumps(user))
    return user

# 6. Move slow work to background tasks (Celery)
# 7. Add pagination — don't return 10k records at once
# 8. Use async for concurrent I/O
# 9. Check network latency (is DB in same datacenter?)
```

</details>

---

<details>
<summary><strong>160. You need 1000+ IO tasks concurrently — what do you use?</strong></summary>

### Answer

```python
# Answer: asyncio (best for I/O-bound concurrency at scale)

import asyncio
import aiohttp

async def fetch(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            return await resp.json()
    except Exception as e:
        return {"error": str(e), "url": url}

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        # Limit concurrency to avoid overwhelming the server
        semaphore = asyncio.Semaphore(100)

        async def bounded_fetch(url):
            async with semaphore:
                return await fetch(session, url)

        tasks = [bounded_fetch(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

results = asyncio.run(fetch_all(urls))

# ThreadPoolExecutor — if you must use sync libraries
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = {executor.submit(requests.get, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        result = future.result()

# Rule of thumb:
# asyncio     — I/O-bound, 1000+ tasks, when async-compatible libraries exist
# ThreadPool  — I/O-bound, when you need to use sync libraries
# ProcessPool — CPU-bound, limited by CPU cores
```

</details>

---

<details>
<summary><strong>161. Process a 10GB file without loading it entirely.</strong></summary>

### Answer

```python
# 1. Iterate line by line — most common, O(1) memory
def process_large_file(path):
    with open(path, encoding="utf-8") as f:
        for line in f:              # Python buffers reads automatically
            process_line(line.rstrip('\n'))

# 2. Read in chunks — for binary data
def process_binary(path, chunk_size=65536):  # 64KB chunks
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            process_chunk(chunk)

# 3. Generator pipeline — memory-efficient transformation chain
def read_lines(path):
    with open(path) as f:
        yield from f

def parse_csv_rows(lines):
    for line in lines:
        yield line.split(',')

def filter_rows(rows, predicate):
    for row in rows:
        if predicate(row):
            yield row

# Compose the pipeline — none of these load the full file
lines = read_lines("huge.csv")
rows = parse_csv_rows(lines)
active = filter_rows(rows, lambda r: r[2] == "active")
for row in active:
    write_to_db(row)

# 4. pandas chunked reading
import pandas as pd

for chunk in pd.read_csv("huge.csv", chunksize=10000):
    process_chunk(chunk)

# 5. Memory-mapped files — random access without loading
import mmap

with open("huge.bin", "rb") as f:
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    # access arbitrary positions without reading entire file
    mm.seek(1_000_000)
    data = mm.read(1024)
    mm.close()
```

</details>

---

<details>
<summary><strong>162. Share data between processes efficiently.</strong></summary>

### Answer

```python
import multiprocessing
from multiprocessing import Manager, Value, Array, Queue, Pipe

# 1. Manager — shared Python objects (slowest, most flexible)
with Manager() as manager:
    shared_dict = manager.dict()
    shared_list = manager.list()
    # Processes can read/write these objects

# 2. Value and Array — shared C types (fastest for simple data)
counter = Value('i', 0)   # 'i' = signed int
arr = Array('d', range(10))   # 'd' = double

def increment(counter):
    with counter.get_lock():   # thread-safe increment
        counter.value += 1

# 3. Queue — message passing (safe, recommended)
q = multiprocessing.Queue()

def producer(q):
    for item in data:
        q.put(item)
    q.put(None)   # sentinel

def consumer(q):
    while (item := q.get()) is not None:
        process(item)

# 4. Pipe — bidirectional, two endpoints
parent_conn, child_conn = Pipe()

# 5. Redis/memcached — for distributed processes across machines
import redis
r = redis.Redis()
r.set("key", json.dumps(data))
data = json.loads(r.get("key"))
```

</details>

---

<details>
<summary><strong>163. Implement caching in Python.</strong></summary>

### Answer

```python
# 1. functools.lru_cache — simplest, in-memory
from functools import lru_cache, cache

@lru_cache(maxsize=256)
def expensive_compute(n: int) -> int:
    return sum(i**2 for i in range(n))

@cache   # Python 3.9+ — unbounded cache
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

# 2. TTL cache with expiry (cachetools library)
from cachetools import TTLCache, cached

cache_store = TTLCache(maxsize=100, ttl=300)   # 100 items, 5min TTL

@cached(cache=cache_store)
def get_user(user_id):
    return db.fetch_user(user_id)

# 3. Redis cache — distributed, survives restarts
import redis, json, hashlib, functools

r = redis.Redis(decode_responses=True)

def redis_cache(ttl=300):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()}"
            cached = r.get(key)
            if cached is not None:
                return json.loads(cached)
            result = func(*args, **kwargs)
            r.setex(key, ttl, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

@redis_cache(ttl=600)
def get_product(product_id):
    return db.fetch_product(product_id)

# 4. Cache invalidation
def invalidate_product_cache(product_id):
    r.delete(f"get_product:{product_id}")  # targeted
    # OR: r.flushdb()  — nuclear option
```

</details>

---

<details>
<summary><strong>164. Make a class iterable.</strong></summary>

### Answer

```python
class NumberRange:
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        """Returns an iterator object."""
        return NumberRangeIterator(self.start, self.stop, self.step)

    def __len__(self):
        return max(0, (self.stop - self.start + self.step - 1) // self.step)

class NumberRangeIterator:
    def __init__(self, start, stop, step):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        val = self.current
        self.current += self.step
        return val

# Simpler: use generator
class NumberRange:
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        current = self.start
        while current < self.stop:
            yield current
            current += self.step

r = NumberRange(0, 10, 2)
print(list(r))        # [0, 2, 4, 6, 8]
print(list(r))        # [0, 2, 4, 6, 8] — reusable! (new iterator each time)
```

</details>

---

<details>
<summary><strong>165. Repeated code in multiple modules — how to fix?</strong></summary>

### Answer

```python
# Extract to a shared utility module
# mypackage/
#   utils/
#       __init__.py
#       decorators.py    ← shared decorators
#       validators.py    ← shared validators
#       helpers.py       ← general helpers

# Decorators for cross-cutting concerns
# utils/decorators.py
def require_auth(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionError("Authentication required")
        return func(request, *args, **kwargs)
    return wrapper

# Mixin classes for shared behavior
class TimestampMixin:
    created_at: datetime
    updated_at: datetime

    def touch(self):
        self.updated_at = datetime.utcnow()

class SoftDeleteMixin:
    deleted_at: Optional[datetime] = None

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()

    @property
    def is_deleted(self):
        return self.deleted_at is not None

class User(TimestampMixin, SoftDeleteMixin, Base):
    pass

# Abstract base class — enforce interface across modules
from abc import ABC, abstractmethod

class NotificationProvider(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool: ...

    @abstractmethod
    def bulk_send(self, recipients: list, message: str) -> dict: ...
```

</details>

---

<details>
<summary><strong>166–167. Thread safety and sharing resources between threads.</strong></summary>

### Answer

```python
import threading

# Thread-safe counter using Lock
class SafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    def get(self):
        with self._lock:
            return self._value

# RLock — re-entrant lock (same thread can acquire multiple times)
class SafeAccount:
    def __init__(self, balance):
        self.balance = balance
        self._lock = threading.RLock()

    def transfer_to(self, other, amount):
        with self._lock:              # acquires lock
            self.withdraw(amount)     # also acquires self._lock — OK with RLock
            other.deposit(amount)

    def withdraw(self, amount):
        with self._lock:
            if amount > self.balance:
                raise ValueError("Insufficient funds")
            self.balance -= amount

# Thread-local storage — per-thread data
local = threading.local()

def worker():
    local.request_id = generate_id()   # unique per thread
    process()

# Queue — thread-safe producer/consumer
from queue import Queue

work_queue = Queue(maxsize=100)

def producer():
    for item in data_source():
        work_queue.put(item)
    work_queue.put(None)   # poison pill

def consumer():
    while (item := work_queue.get()) is not None:
        process(item)
        work_queue.task_done()

# queue.join() — wait until all items are processed
work_queue.join()
```

</details>

---

<details>
<summary><strong>168. Automatically retry API calls on failure.</strong></summary>

### Answer

```python
import time
import functools
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 1. Manual retry decorator with exponential backoff
def retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    jitter = delay * 0.1 * (2 * __import__('random').random() - 1)
                    time.sleep(delay + jitter)
                    delay *= 2    # exponential backoff
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(requests.RequestException,))
def call_payment_api(payload):
    r = requests.post("https://api.payment.com/charge", json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

# 2. requests built-in retry (urllib3)
session = requests.Session()
retry = Retry(
    total=3,
    backoff_factor=1,          # wait 1s, 2s, 4s between retries
    status_forcelist=[429, 500, 502, 503, 504],  # retry on these status codes
    allowed_methods=["GET", "POST"],
)
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

# 3. tenacity library — most powerful
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
    reraise=True
)
def call_api():
    ...
```

</details>

---

<details>
<summary><strong>169–171. Handle malformed JSON, log exceptions, large JSON files.</strong></summary>

### Answer

```python
import json
import logging

logger = logging.getLogger(__name__)

# 169. Handle malformed JSON gracefully
def safe_parse_json(raw: str, default=None):
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        logger.warning(f"Malformed JSON at position {e.pos}: {e.msg}")
        return default

def parse_api_response(response):
    try:
        data = response.json()
    except json.JSONDecodeError:
        # Try to extract partial data or return error info
        return {"error": "Invalid JSON", "raw": response.text[:200]}
    return data

# 170. Log exceptions without stopping execution
def process_batch(items):
    results = []
    for item in items:
        try:
            results.append(process_item(item))
        except Exception:
            logger.exception(f"Failed to process item {item!r}")
            # logger.exception automatically includes traceback
            # execution continues to next item
    return results

# 171. Load a very large JSON file efficiently
# Option 1: ijson — streaming JSON parser
import ijson

def stream_large_json_array(path):
    with open(path, "rb") as f:
        for item in ijson.items(f, "item"):   # "item" = each element of root array
            yield item

# Process without loading entire file
for user in stream_large_json_array("10gb_users.json"):
    insert_to_db(user)

# Option 2: JSONL (JSON Lines) — one JSON object per line, easily streamable
def read_jsonl(path):
    with open(path) as f:
        for line in f:
            if line.strip():
                yield json.loads(line)

# JSONL is the preferred format for large datasets in data pipelines
```

</details>

---

<details>
<summary><strong>172–176. Global state, memoization, prevent override, Singleton, 10M unique items.</strong></summary>

### Answer

```python
# 172. Multiple functions need shared global state — best practice
# Prefer: class with instance state, or a configuration object
class AppConfig:
    _instance = None

    def __init__(self):
        self.db_url = os.environ["DATABASE_URL"]
        self.redis_url = os.environ["REDIS_URL"]
        self.debug = os.environ.get("DEBUG", "false").lower() == "true"

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# 173. Memoize expensive functions
from functools import lru_cache

@lru_cache(maxsize=None)
def expensive(n):
    return heavy_computation(n)

# Clear cache when needed
expensive.cache_clear()

# 174. Prevent subclass from overriding certain methods
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "critical_method" in cls.__dict__:
            raise TypeError(f"{cls.__name__} cannot override critical_method")

    def critical_method(self):
        return "important logic"

# 175. Singleton pattern — multiple approaches
# Thread-safe Singleton
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:   # double-checked locking
                    cls._instance = super().__new__(cls)
        return cls._instance

# Module-level singleton — simplest and most Pythonic
# myapp/database.py
# db_connection = create_connection()
# Just import this module — Python imports are singletons by design

# 176. Handle 10 million unique items efficiently
# Use a set — O(1) average lookup, ~200MB for 10M strings
unique_items = set()
for item in data_stream:
    unique_items.add(item)

# If memory is tight — use a Bloom filter (probabilistic, ~10x smaller)
from pybloom_live import BloomFilter
bf = BloomFilter(capacity=10_000_000, error_rate=0.001)
for item in data_stream:
    if item not in bf:
        bf.add(item)
        process_unique(item)

# For exact count with fixed memory — HyperLogLog
import redis
r = redis.Redis()
for item in data_stream:
    r.pfadd("unique_items", item)
print(r.pfcount("unique_items"))   # approximate count ±0.81%
```

</details>

---

## Part 3 — Coding Problems with Solutions (25)

<details>
<summary><strong>1. Reverse words in a sentence.</strong></summary>

```python
def reverse_words(s: str) -> str:
    return " ".join(s.split()[::-1])

# Handles multiple spaces and leading/trailing spaces
print(reverse_words("Hello World"))        # "World Hello"
print(reverse_words("  the quick  fox  "))# "fox quick the"
```

</details>

<details>
<summary><strong>2. Check palindrome.</strong></summary>

```python
def is_palindrome(s: str) -> bool:
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

# Two-pointer approach (O(1) space, O(n) time)
def is_palindrome_two_pointer(s: str) -> bool:
    s = s.lower().replace(" ", "")
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("A man a plan a canal Panama"))  # True
print(is_palindrome("race a car"))                   # False
```

</details>

<details>
<summary><strong>3. Find second largest number.</strong></summary>

```python
def second_largest(nums: list) -> int:
    # O(n) — single pass, no sorting
    first = second = float('-inf')
    for n in nums:
        if n > first:
            second = first
            first = n
        elif n > second and n != first:
            second = n
    if second == float('-inf'):
        raise ValueError("No second distinct element")
    return second

print(second_largest([3, 1, 4, 1, 5, 9, 2, 6]))  # 6
```

</details>

<details>
<summary><strong>4. FizzBuzz.</strong></summary>

```python
def fizzbuzz(n: int) -> list:
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result

# One-liner (clever but less readable)
def fizzbuzz_oneliner(n):
    return ["FizzBuzz" if not i%15 else "Fizz" if not i%3 else "Buzz" if not i%5 else str(i) for i in range(1, n+1)]
```

</details>

<details>
<summary><strong>5. Fibonacci Generator.</strong></summary>

```python
def fibonacci(n: int):
    """Generator that yields first n Fibonacci numbers."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Infinite generator
def fib_infinite():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice
print(list(islice(fib_infinite(), 10)))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# With memoization for arbitrary index
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2: return n
    return fib(n-1) + fib(n-2)
```

</details>

<details>
<summary><strong>6. Rotate array.</strong></summary>

```python
def rotate(arr: list, k: int) -> list:
    if not arr: return arr
    k %= len(arr)
    return arr[-k:] + arr[:-k]

def rotate_inplace(arr: list, k: int) -> None:
    n = len(arr)
    k %= n
    arr.reverse()
    arr[:k] = arr[:k][::-1]
    arr[k:] = arr[k:][::-1]

print(rotate([1, 2, 3, 4, 5], 2))   # [4, 5, 1, 2, 3]
```

</details>

<details>
<summary><strong>7. Merge two sorted lists.</strong></summary>

```python
def merge_sorted(a: list, b: list) -> list:
    """O(n+m) time, O(n+m) space."""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result

# Using heapq.merge (lazy, memory efficient)
import heapq
merged = list(heapq.merge([1, 3, 5], [2, 4, 6]))
```

</details>

<details>
<summary><strong>8–12. Counter, Flatten, Anagram, Missing number, Remove duplicates.</strong></summary>

```python
from collections import Counter

# 8. Count frequency
def count_frequency(items):
    return Counter(items)

freq = count_frequency([1, 2, 3, 1, 1, 2])
print(freq.most_common())   # [(1, 3), (2, 2), (3, 1)]

# 9. Flatten nested list — recursive
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Generator version — memory efficient
def flatten_gen(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten_gen(item)
        else:
            yield item

print(flatten([1, [2, [3, [4]], 5], 6]))   # [1, 2, 3, 4, 5, 6]

# 10. Anagram check — O(n log n) sort, or O(n) Counter
def is_anagram(a: str, b: str) -> bool:
    return Counter(a.lower()) == Counter(b.lower())

# 11. Find missing number — O(n), O(1) space with math formula
def find_missing(nums: list) -> int:
    n = len(nums) + 1
    return n * (n + 1) // 2 - sum(nums)

# XOR approach — also O(n), O(1) space
def find_missing_xor(nums: list) -> int:
    n = len(nums) + 1
    xor = 0
    for i in range(1, n + 1):
        xor ^= i
    for num in nums:
        xor ^= num
    return xor

# 12. Remove duplicates preserving order
def remove_duplicates(lst: list) -> list:
    return list(dict.fromkeys(lst))   # preserves order (Python 3.7+)

# Using seen set — more explicit
def remove_duplicates_v2(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]
```

</details>

<details>
<summary><strong>13. Longest substring without repeating characters.</strong></summary>

```python
def longest_unique_substring(s: str) -> int:
    """Sliding window — O(n) time, O(min(n, charset)) space."""
    seen = {}
    left = max_len = 0

    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len

def longest_unique_with_substring(s: str) -> tuple:
    """Returns (length, substring)."""
    seen = {}
    left = max_len = 0
    start = 0

    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        if right - left + 1 > max_len:
            max_len = right - left + 1
            start = left

    return max_len, s[start:start + max_len]

print(longest_unique_substring("abcabcbb"))   # 3 ("abc")
print(longest_unique_substring("pwwkew"))     # 3 ("wke")
```

</details>

<details>
<summary><strong>14–16. Binary search, LRU Cache, Find duplicates.</strong></summary>

```python
# 14. Binary search — O(log n)
def binary_search(arr: list, target: int) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2   # avoids overflow (matters in other languages)
        if arr[mid] == target: return mid
        if arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1

import bisect
idx = bisect.bisect_left(arr, target)
found = idx < len(arr) and arr[idx] == target

# 15. LRU Cache — OrderedDict implementation
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # mark as recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)   # evict LRU (first item)

# Python 3.9+ — use @functools.lru_cache for function memoization

# 16. Find duplicates
def find_duplicates(arr: list) -> list:
    seen = set()
    return list({x for x in arr if x in seen or seen.add(x) is not None and False or x in seen})

# Cleaner version
def find_duplicates(arr: list) -> list:
    seen, duplicates = set(), set()
    for x in arr:
        if x in seen:
            duplicates.add(x)
        seen.add(x)
    return list(duplicates)

print(find_duplicates([1, 2, 3, 1, 2, 4]))   # [1, 2]
```

</details>

<details>
<summary><strong>17–21. Matrix transpose, Prime check, Least frequent, Two Sum, Valid parentheses.</strong></summary>

```python
# 17. Matrix transpose
def transpose(matrix: list) -> list:
    return list(map(list, zip(*matrix)))
    # Or: [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

# 18. Prime check — O(sqrt(n))
def is_prime(n: int) -> bool:
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

# Sieve of Eratosthenes — all primes up to n
def sieve(n: int) -> list:
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n + 1, i):
                is_p[j] = False
    return [i for i, p in enumerate(is_p) if p]

# 19. Least frequent element
from collections import Counter
def least_frequent(lst: list):
    return min(Counter(lst), key=Counter(lst).get)

def least_frequent_efficient(lst: list):
    c = Counter(lst)
    return min(c, key=c.get)   # compute Counter once

# 20. Two Sum — O(n) with hashmap
def two_sum(nums: list, target: int) -> tuple:
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return (seen[complement], i)
        seen[n] = i
    return None

print(two_sum([2, 7, 11, 15], 9))   # (0, 1)

# 21. Valid parentheses — O(n) with stack
def is_valid_parens(s: str) -> bool:
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for ch in s:
        if ch in "({[":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack

print(is_valid_parens("()[]{}"))   # True
print(is_valid_parens("([)]"))     # False
```

</details>

<details>
<summary><strong>22–25. Majority element, Remove Nth node, Large file reading, Async example.</strong></summary>

```python
# 22. Majority element — Boyer-Moore Voting O(n) time O(1) space
def majority_element(nums: list) -> int:
    candidate, count = None, 0
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
    return candidate

print(majority_element([3, 2, 3]))         # 3
print(majority_element([2, 2, 1, 1, 2]))   # 2

# 23. Remove Nth node from end of linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def remove_nth_from_end(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):   # move fast n+1 steps ahead
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next   # skip the nth node
    return dummy.next

# 24. Large file reading — line by line
def process_large_file(path: str, process_fn=print):
    with open(path, encoding="utf-8") as f:
        for line in f:
            process_fn(line.rstrip('\n'))

# With progress tracking
from itertools import islice

def read_in_batches(path: str, batch_size: int = 1000):
    with open(path) as f:
        while batch := list(islice(f, batch_size)):
            yield batch

# 25. Async example — concurrent HTTP fetches
import asyncio
import aiohttp

async def fetch(session: aiohttp.ClientSession, url: str) -> dict:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            return {"url": url, "status": resp.status, "data": await resp.json()}
    except Exception as e:
        return {"url": url, "error": str(e)}

async def fetch_all(urls: list) -> list:
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(50)   # limit to 50 concurrent requests
        async def bounded(url):
            async with semaphore:
                return await fetch(session, url)
        return await asyncio.gather(*[bounded(url) for url in urls])

results = asyncio.run(fetch_all(["https://httpbin.org/get"] * 10))
```

</details>

---

## Part 4 — Additional Backend Developer Questions

> These questions are commonly asked for Python backend developers with 3+ years of experience and cover topics beyond the PDF.

---

<details>
<summary><strong>B1. What is the difference between synchronous, multi-threaded, and asynchronous servers? When would you choose each?</strong></summary>

### Answer

| Model | How | Best For |
|---|---|---|
| Sync (WSGI) | One request at a time per worker | CPU-heavy, simple apps |
| Multi-threaded | Multiple threads per process | Mixed I/O + CPU workloads |
| Async (ASGI) | Event loop, non-blocking I/O | High concurrency I/O-bound (WebSockets, chat, APIs) |

```python
# WSGI — synchronous (Gunicorn, uWSGI)
# app.py
def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Hello, World!"]

# gunicorn --workers 4 app:application

# ASGI — asynchronous (Uvicorn, Hypercorn)
# Works with FastAPI, Starlette, Django Channels

# FastAPI example
from fastapi import FastAPI
app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await db.fetch_one("SELECT * FROM users WHERE id = :id", {"id": user_id})
    return user

# uvicorn app:app --workers 4

# Gunicorn + Uvicorn workers (production recommendation)
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

</details>

---

<details>
<summary><strong>B2. Explain Python type hints and the typing module. How do you use them in a real backend project?</strong></summary>

### Answer

```python
from typing import Optional, Union, List, Dict, Tuple, Any, Callable, TypeVar, Generic
from typing import TypedDict, Protocol, Literal, Final
from dataclasses import dataclass

# Basic type hints
def get_user(user_id: int) -> Optional[dict]:
    ...

# TypedDict — typed dict structure
class UserResponse(TypedDict):
    id: int
    name: str
    email: str
    role: Literal["admin", "user", "guest"]

# Dataclass — typed + auto-generated __init__, __repr__, __eq__
@dataclass
class Order:
    id: int
    user_id: int
    items: List[Dict[str, Any]]
    total: float
    status: Literal["pending", "paid", "shipped"] = "pending"

# Protocol — structural subtyping (duck typing + type safety)
class Serializable(Protocol):
    def to_dict(self) -> dict: ...
    def to_json(self) -> str: ...

def serialize_response(obj: Serializable) -> str:
    return obj.to_json()   # works with any class implementing the protocol

# Generic types
T = TypeVar('T')

class Repository(Generic[T]):
    def get(self, id: int) -> Optional[T]: ...
    def save(self, obj: T) -> T: ...
    def delete(self, id: int) -> None: ...

class UserRepository(Repository[User]):
    def get(self, id: int) -> Optional[User]:
        return db.query(User).filter_by(id=id).first()

# Runtime enforcement with Pydantic
from pydantic import BaseModel, validator, EmailStr

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    age: int

    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v

# Type checking tool: mypy
# mypy app.py --strict
```

</details>

---

<details>
<summary><strong>B3. How do you handle environment configuration in a Python backend application?</strong></summary>

### Answer

```python
# Best practice: 12-factor app — config via environment variables

# 1. python-dotenv — load .env file in development
from dotenv import load_dotenv
load_dotenv()   # loads .env into os.environ

import os
DATABASE_URL = os.environ["DATABASE_URL"]   # raises KeyError if missing
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
PORT = int(os.environ.get("PORT", "8000"))

# 2. pydantic-settings — typed, validated settings
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn

class Settings(BaseSettings):
    database_url: PostgresDsn
    redis_url: RedisDsn
    secret_key: str
    debug: bool = False
    allowed_hosts: list[str] = ["*"]
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()   # reads from env + .env file, validates types

# 3. Multiple environments
class DevelopmentSettings(Settings):
    debug: bool = True
    log_level: str = "DEBUG"

class ProductionSettings(Settings):
    debug: bool = False

def get_settings():
    env = os.environ.get("ENVIRONMENT", "development")
    if env == "production":
        return ProductionSettings()
    return DevelopmentSettings()

# .env file (never commit to git)
# DATABASE_URL=postgresql://user:pass@localhost/mydb
# SECRET_KEY=your-secret-key-here
# REDIS_URL=redis://localhost:6379/0
```

</details>

---

<details>
<summary><strong>B4. Explain Python's dataclasses vs Pydantic vs NamedTuple — when to use each.</strong></summary>

### Answer

| | `dataclass` | `pydantic.BaseModel` | `NamedTuple` |
|---|---|---|---|
| **Mutability** | Mutable (frozen optional) | Immutable by default | Immutable |
| **Validation** | No (use `__post_init__`) | Yes — automatic | No |
| **Serialization** | Manual | Built-in (`.dict()`, `.json()`) | Manual |
| **Type coercion** | No | Yes (`"5"` → `5`) | No |
| **Performance** | Fast | Slower (validation overhead) | Fastest |
| **Use case** | Internal data objects | API request/response, config | Simple records, DB rows |

```python
from dataclasses import dataclass, field
from typing import List

# dataclass — internal domain objects
@dataclass
class Order:
    id: int
    items: List[str] = field(default_factory=list)
    total: float = 0.0

    def __post_init__(self):
        if self.total < 0:
            raise ValueError("Total cannot be negative")

# Pydantic — API boundaries (request/response validation)
from pydantic import BaseModel, Field, validator

class CreateOrderRequest(BaseModel):
    items: List[str] = Field(min_items=1)
    total: float = Field(gt=0)
    customer_id: int

    class Config:
        frozen = True   # immutable

# NamedTuple — simple, immutable, lightweight
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
    z: float = 0.0
```

</details>

---

<details>
<summary><strong>B5. How do you write clean, testable Python backend code? What patterns do you use?</strong></summary>

### Answer

```python
# 1. Dependency Injection — makes testing easy
class OrderService:
    def __init__(self, db: Database, email: EmailService, cache: CacheService):
        self.db = db
        self.email = email
        self.cache = cache

    def create_order(self, user_id: int, items: list) -> Order:
        order = Order(user_id=user_id, items=items)
        self.db.save(order)
        self.email.send_confirmation(order)
        self.cache.invalidate(f"user:{user_id}:orders")
        return order

# Easy to test — mock dependencies
from unittest.mock import MagicMock
def test_create_order():
    mock_db = MagicMock()
    mock_email = MagicMock()
    mock_cache = MagicMock()

    service = OrderService(mock_db, mock_email, mock_cache)
    order = service.create_order(user_id=1, items=["item1"])

    mock_db.save.assert_called_once()
    mock_email.send_confirmation.assert_called_once_with(order)

# 2. Repository pattern — abstract data access
class UserRepository(Protocol):
    def get(self, user_id: int) -> Optional[User]: ...
    def save(self, user: User) -> User: ...

class SQLUserRepository:
    def get(self, user_id: int) -> Optional[User]:
        return db.query(User).get(user_id)

class InMemoryUserRepository:   # for tests
    def __init__(self):
        self._store = {}
    def get(self, user_id: int):
        return self._store.get(user_id)
    def save(self, user: User):
        self._store[user.id] = user
        return user

# 3. Result pattern — explicit error handling without exceptions
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Result(Generic[T]):
    value: T = None
    error: str = None
    success: bool = True

    @classmethod
    def ok(cls, value: T):
        return cls(value=value, success=True)

    @classmethod
    def fail(cls, error: str):
        return cls(error=error, success=False)

def parse_user_input(data: dict) -> Result:
    if not data.get("email"):
        return Result.fail("Email is required")
    if not data.get("name"):
        return Result.fail("Name is required")
    return Result.ok(User(**data))
```

</details>

---

<details>
<summary><strong>B6. How does Python handle memory for large-scale backend applications? What are common pitfalls?</strong></summary>

### Answer

```python
# Common memory pitfalls in backend apps:

# 1. Unbounded in-memory caches
cache = {}   # grows forever!
# Fix: use maxsize, TTL, or Redis

from functools import lru_cache
@lru_cache(maxsize=1000)   # bounded
def get_config(key): ...

# 2. Holding DB result sets in memory
# Bad:
all_users = session.query(User).all()   # 1M users in memory!
for user in all_users:
    process(user)

# Good: yield_per for SQLAlchemy
for user in session.query(User).yield_per(1000):
    process(user)

# 3. String concatenation in loops
# Bad: O(n²)
result = ""
for item in items:
    result += str(item) + ","
# Good: O(n)
result = ",".join(str(item) for item in items)

# 4. Keeping large DataFrames in global scope
# Use explicit deletion
import pandas as pd
df = pd.read_csv("huge.csv")
process(df)
del df   # explicitly free memory

# 5. Circular references in long-lived objects
# Use weakref for back-references
import weakref

class Parent:
    def __init__(self):
        self.children = []

class Child:
    def __init__(self, parent):
        self.parent = weakref.ref(parent)   # weak reference — won't prevent GC

# Memory profiling tools
# memory_profiler — line-by-line memory usage
# tracemalloc — Python built-in, tracks allocations
import tracemalloc
tracemalloc.start()
# ... run code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

</details>

---

## Interview Tips for Python Backend Developers (3+ Years)

### What interviewers look for at this level

- **Not just "what"** — explain *why* you made design choices and what tradeoffs you considered
- **Real-world application** — connect every concept to a backend use case (APIs, DBs, queues, caching)
- **Code quality awareness** — mention testing, linting, type hints, code reviews
- **Operational thinking** — performance, memory, logging, monitoring, deployment

### Key topics to revise beyond this guide

- `asyncio` with `aiohttp` / `httpx` for async HTTP clients
- SQLAlchemy ORM — sessions, lazy vs eager loading, migrations with Alembic
- Redis — pub/sub, sorted sets, rate limiting patterns
- Celery — task queues, chords, chains, monitoring with Flower
- FastAPI — Pydantic models, dependency injection, background tasks
- Docker basics — containerizing a Python app, multi-stage builds
- REST API design — versioning, pagination, error response formats
- Database connection pooling — `SQLALCHEMY_POOL_SIZE`, `asyncpg`

### Useful commands every Python developer should know

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v --cov=app --cov-report=html
python -m mypy app/ --strict
python -m black . && python -m ruff check .
python -m cProfile -s cumulative app.py
python -c "import dis; dis.dis(lambda x: x+1)"
```

---

*Good luck with your interview! You've got this.*
