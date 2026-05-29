# 🐍 Python Core Concepts — Interview Prep
### Cognizant Python Developer | 3+ Years Experience

---

## ✅ Topic Checklist

- [ ] Python basics & data types
- [ ] Mutable vs Immutable
- [ ] Lists, Tuples, Sets, Dictionaries
- [ ] OOP — Classes, Inheritance, Polymorphism, Encapsulation
- [ ] Exception Handling
- [ ] File I/O
- [ ] List Comprehensions & Lambda
- [ ] Built-in functions (map, filter, zip, enumerate)
- [ ] Scope (LEGB rule)
- [ ] Shallow vs Deep Copy

---

## 1. 🔢 Python Data Types — Quick Reference

| Type | Mutable? | Ordered? | Duplicates? | Example |
|------|----------|----------|-------------|---------|
| `list` | ✅ Yes | ✅ Yes | ✅ Yes | `[1, 2, 2]` |
| `tuple` | ❌ No | ✅ Yes | ✅ Yes | `(1, 2, 2)` |
| `set` | ✅ Yes | ❌ No | ❌ No | `{1, 2, 3}` |
| `dict` | ✅ Yes | ✅ Yes (3.7+) | Keys: No | `{"a": 1}` |
| `str` | ❌ No | ✅ Yes | ✅ Yes | `"hello"` |
| `frozenset` | ❌ No | ❌ No | ❌ No | `frozenset({1,2})` |

> **Interview Q:** "What is the difference between a list and a tuple?"
> **Answer:** A list is mutable (can be changed after creation), while a tuple is immutable. Tuples are faster and can be used as dictionary keys; lists cannot.

---

## 2. 🔗 Mutable vs Immutable

```python
# Immutable — strings, int, float, tuple
x = "hello"
x[0] = "H"  # ❌ TypeError — strings are immutable

# Mutable — lists, dicts, sets
lst = [1, 2, 3]
lst[0] = 99  # ✅ Works fine
```

> **Why it matters:** Passing mutable objects to functions can have side effects. Interviewers often test this with a list vs a string argument.

---

## 3. 🏛️ Object-Oriented Programming (OOP)

### 4 Pillars — Must Know

| Pillar | Definition | Python Example |
|--------|-----------|----------------|
| **Encapsulation** | Binding data + methods into one unit (class) | Private `__attr`, getters/setters |
| **Abstraction** | Hiding internal complexity, exposing only what's needed | `ABC`, abstract methods |
| **Inheritance** | Child class inherits from parent class | `class Dog(Animal)` |
| **Polymorphism** | Same method name, different behaviour | Method overriding |

### Class Example (covers all 4 pillars)

```python
from abc import ABC, abstractmethod

# Abstraction
class Animal(ABC):
    def __init__(self, name):
        self.__name = name          # Encapsulation — private attribute

    def get_name(self):             # Encapsulation — controlled access
        return self.__name

    @abstractmethod
    def speak(self):                # Abstraction — must be implemented
        pass

# Inheritance
class Dog(Animal):
    def speak(self):                # Polymorphism — overriding
        return f"{self.get_name()} says: Woof!"

class Cat(Animal):
    def speak(self):                # Polymorphism — different behaviour
        return f"{self.get_name()} says: Meow!"

# Usage
animals = [Dog("Rex"), Cat("Whiskers")]
for a in animals:
    print(a.speak())
# Rex says: Woof!
# Whiskers says: Meow!
```

---

### `__init__`, `__str__`, `__repr__` — Dunder Methods

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):              # For print() / str()
        return f"Point({self.x}, {self.y})"

    def __repr__(self):             # For debugging / repr()
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other):        # For == comparison
        return self.x == other.x and self.y == other.y

p = Point(3, 4)
print(p)        # Point(3, 4)
repr(p)         # Point(x=3, y=4)
```

---

## 4. 🧬 Inheritance Types

```python
# Single Inheritance
class B(A): pass

# Multiple Inheritance
class C(A, B): pass

# Multilevel Inheritance
class C(B):   # B inherits A
    pass
```

### Method Resolution Order (MRO)

```python
class A:
    def hello(self): return "A"

class B(A):
    def hello(self): return "B"

class C(A):
    def hello(self): return "C"

class D(B, C): pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
# D looks: D → B → C → A (left to right)
```

---

## 5. 🚫 Exception Handling

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Caught: {e}")
except (ValueError, TypeError) as e:
    print(f"Value or Type error: {e}")
else:
    print("No exception occurred")   # Runs only if no exception
finally:
    print("Always runs — cleanup here")   # Always executes

# Custom Exception
class InsufficientFundsError(Exception):
    def __init__(self, amount):
        self.amount = amount
        super().__init__(f"Insufficient funds: need {amount} more")

raise InsufficientFundsError(500)
```

> **Common Q:** "What is the difference between `else` and `finally` in try-except?"
> - `else`: runs **only when no exception** occurred
> - `finally`: runs **always**, whether exception happened or not (used for cleanup)

---

## 6. 📋 List Comprehensions & Functional Tools

```python
# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# Dict comprehension
word_len = {word: len(word) for word in ["hello", "world"]}
# {'hello': 5, 'world': 5}

# Lambda
double = lambda x: x * 2

# map() — apply function to each element
result = list(map(lambda x: x**2, [1, 2, 3, 4]))
# [1, 4, 9, 16]

# filter() — keep elements that satisfy condition
evens = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]))
# [2, 4]

# zip() — pair elements from two iterables
names = ["Alice", "Bob"]
scores = [90, 85]
paired = list(zip(names, scores))
# [('Alice', 90), ('Bob', 85)]

# enumerate() — iterate with index
for i, name in enumerate(["Alice", "Bob"], start=1):
    print(f"{i}. {name}")
```

---

## 7. 🔭 Scope — LEGB Rule

Python resolves variable names in this order:

```
L → Local       (inside current function)
E → Enclosing   (outer function, for closures)
G → Global      (module-level)
B → Built-in    (Python built-ins: len, print, etc.)
```

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)        # local

    inner()
    print(x)            # enclosing

outer()
print(x)                # global
```

---

## 8. 📑 Shallow vs Deep Copy

```python
import copy

original = [[1, 2], [3, 4]]

# Shallow copy — copies the outer list, inner lists are still shared
shallow = copy.copy(original)
shallow[0][0] = 99
print(original)  # [[99, 2], [3, 4]] — AFFECTED!

# Deep copy — recursively copies everything
deep = copy.deepcopy(original)
deep[0][0] = 99
print(original)  # [[1, 2], [3, 4]] — NOT affected
```

> **Quick answer:** Shallow copy creates a new container but shares nested objects. Deep copy creates completely independent copies.

---

## 9. 🎤 Common Interview Q&A

### Q1: What is Python? Why is it popular?
**A:** Python is a high-level, interpreted, dynamically-typed, general-purpose language. It's popular for its readable syntax, vast library ecosystem (NumPy, Django, Pandas, etc.), and versatility across web, data science, automation, and AI.

### Q2: Is Python interpreted or compiled?
**A:** Python is interpreted — it executes line by line via the CPython interpreter. However, it first compiles source code to bytecode (`.pyc`), then the Python Virtual Machine (PVM) executes it.

### Q3: What is the difference between `is` and `==`?
```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)   # True  — same VALUE
print(a is b)   # False — different OBJECTS in memory

c = a
print(a is c)   # True  — same object reference
```

### Q4: What are `*args` and `**kwargs`?
```python
def func(*args, **kwargs):
    print(args)    # tuple of positional arguments
    print(kwargs)  # dict of keyword arguments

func(1, 2, 3, name="Alice", age=30)
# (1, 2, 3)
# {'name': 'Alice', 'age': 30}
```

### Q5: What is the difference between `append()` and `extend()`?
```python
lst = [1, 2]
lst.append([3, 4])   # [1, 2, [3, 4]] — adds as single element
lst.extend([3, 4])   # [1, 2, 3, 4]   — adds each element
```

---

## 🧪 Practice Problems

### Problem 1: Reverse a string without slicing
```python
def reverse_string(s):
    result = ""
    for char in s:
        result = char + result
    return result

print(reverse_string("hello"))  # "olleh"
```

### Problem 2: Find permutations of a string *(asked at Cognizant!)*
```python
from itertools import permutations

def get_permutations(s):
    return [''.join(p) for p in permutations(s)]

print(get_permutations("abc"))
# ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
```

### Problem 3: Count character frequency
```python
from collections import Counter

def char_freq(s):
    return dict(Counter(s))

print(char_freq("banana"))
# {'b': 1, 'a': 3, 'n': 2}
```

---

*Next: Advanced Python → `03_python_advanced_and_coding.md`*
