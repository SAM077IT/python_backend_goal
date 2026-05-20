# 🧩 Object-Oriented Programming — Questions & Answers

> Click ▶ to reveal answers. Covers: Classes · Inheritance · Polymorphism · Dunder methods · Abstract classes · Dataclasses

---

## Classes & Instances

<details>
<summary><strong>Q1. What is the difference between instance attributes and class attributes?</strong></summary>

```python
class Dog:
    species = "Canis lupus familiaris"   # class attribute — shared by ALL instances

    def __init__(self, name, breed):
        self.name = name      # instance attributes — unique per instance
        self.breed = breed

d1 = Dog("Rex", "Labrador")
d2 = Dog("Bella", "Poodle")

print(Dog.species)     # 'Canis lupus familiaris'
print(d1.species)      # 'Canis lupus familiaris' — found on the class
print(d1.name)         # 'Rex'
print(d2.name)         # 'Bella'

# Mutating a mutable class attribute affects all instances
class Counter:
    count = 0
    items = []   # ← danger: mutable class attribute

Counter.count += 1      # modifying via class — fine
c = Counter()
c.count += 1            # creates a NEW instance attribute shadowing the class one
print(Counter.count)    # 1 (class attr unchanged)
print(c.count)          # 2 (instance attr)
```

**Rule:** use instance attributes for data that varies per object, class attributes for constants or shared state.

</details>

---

<details>
<summary><strong>Q2. Explain <code>__init__</code>, <code>__str__</code>, and <code>__repr__</code>. When is each called?</strong></summary>

```python
class Point:
    def __init__(self, x, y):
        """Called when creating an instance: Point(1, 2)"""
        self.x = x
        self.y = y

    def __repr__(self):
        """Called by repr(), in the REPL, and as fallback for str()"""
        return f"Point({self.x!r}, {self.y!r})"

    def __str__(self):
        """Called by str(), print(). Falls back to __repr__ if not defined."""
        return f"({self.x}, {self.y})"

p = Point(1, 2)
print(str(p))    # (1, 2)     ← __str__
print(repr(p))   # Point(1, 2) ← __repr__
print(p)         # (1, 2)     ← print() calls str()

# In collections, __repr__ is always used
points = [Point(1, 2), Point(3, 4)]
print(points)    # [Point(1, 2), Point(3, 4)]
```

**Guideline:**
- `__repr__` should return a string that could recreate the object: `eval(repr(obj)) == obj` ideally
- `__str__` should return a human-friendly description

</details>

---

<details>
<summary><strong>Q3. What other dunder methods should you know? Write examples for comparison and container behaviour.</strong></summary>

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    # Arithmetic
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):   # handles scalar * vector
        return self.__mul__(scalar)

    # Comparison
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x**2 + self.y**2) < (other.x**2 + other.y**2)

    # Container / sequence protocol
    def __len__(self):
        return 2

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    # Callable
    # def __call__(self, ...): makes an instance callable like a function

    # Context manager
    # def __enter__(self) / __exit__(self, ...): enables 'with' statement

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)     # Vector(4, 6)
print(3 * v1)      # Vector(3, 6)
print(len(v1))     # 2
print(v1[0])       # 1
print(v1 == Vector(1, 2))   # True
```

| Dunder | Triggered by |
|--------|-------------|
| `__add__` | `a + b` |
| `__eq__` | `a == b` |
| `__lt__`, `__le__`, `__gt__`, `__ge__` | `<`, `<=`, `>`, `>=` |
| `__len__` | `len(a)` |
| `__getitem__` | `a[i]` |
| `__setitem__` | `a[i] = v` |
| `__contains__` | `x in a` |
| `__iter__` | `for x in a` |
| `__call__` | `a()` |
| `__hash__` | `hash(a)`, using in sets/dicts |

</details>

---

## Inheritance & Polymorphism

<details>
<summary><strong>Q4. How does inheritance work in Python? Explain <code>super()</code> and MRO.</strong></summary>

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)   # calls Animal.__init__ — don't duplicate init logic
        self.breed = breed

    def speak(self):   # method overriding
        return f"{self.name} barks"

class GoldenRetriever(Dog):
    def speak(self):
        return super().speak() + " (friendly!)"

gr = GoldenRetriever("Buddy", "Golden")
print(gr.speak())   # 'Buddy barks (friendly!)'
```

**Method Resolution Order (MRO)** — the order Python searches for a method in the inheritance chain. Uses C3 linearisation.

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass   # multiple inheritance

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
# Python checks D → B → C → A → object, in that order
```

`super()` always delegates to the **next class in the MRO**, not necessarily the direct parent.

</details>

---

<details>
<summary><strong>Q5. What is duck typing? How does it relate to polymorphism in Python?</strong></summary>

> "If it walks like a duck and quacks like a duck, it's a duck."

Python doesn't require a common base class for polymorphic behaviour — it only cares whether the object has the required method or attribute.

```python
class Dog:
    def speak(self):
        return "Woof"

class Cat:
    def speak(self):
        return "Meow"

class Robot:
    def speak(self):
        return "Beep boop"

def make_noise(animal):
    # No isinstance check needed — any object with .speak() works
    print(animal.speak())

for thing in [Dog(), Cat(), Robot()]:
    make_noise(thing)
# Woof / Meow / Beep boop
```

**Contrast with Java/C#:** those require all three classes to implement a common interface. Python's duck typing is more flexible but less explicitly documented — hence why type hints and `abc.ABC` are used when you want to enforce a contract.

</details>

---

<details>
<summary><strong>Q6. What are abstract base classes? Write an example using <code>abc.ABC</code>.</strong></summary>

An abstract base class (ABC) defines a **contract** — subclasses must implement certain methods, or Python raises `TypeError` at instantiation time.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """Must be implemented by every subclass."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self):   # concrete method — subclasses inherit this
        return f"Area: {self.area():.2f}, Perimeter: {self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)

# Shape()        # ← TypeError: Can't instantiate abstract class
c = Circle(5)
print(c.describe())   # Area: 78.54, Perimeter: 31.42
```

**Key points:**
- `ABC` is shorthand for `class Shape(metaclass=ABCMeta)`
- Any class with at least one unimplemented `@abstractmethod` **cannot be instantiated**
- Subclasses that implement all abstract methods can be instantiated normally

</details>

---

## Encapsulation

<details>
<summary><strong>Q7. Explain name mangling — what are single underscore and double underscore prefixes?</strong></summary>

Python has **convention-based** encapsulation, not enforced access control like Java.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner         # public — access freely
        self._balance = balance    # protected — convention: "don't touch from outside"
        self.__pin = "1234"        # private — name-mangled to _BankAccount__pin

    def get_balance(self):
        return self._balance       # access via method

    def _validate(self):           # protected method
        return True

    def __check_pin(self, pin):    # private method
        return pin == self.__pin

acc = BankAccount("Alice", 1000)
print(acc.owner)              # 'Alice'
print(acc._balance)           # 1000 (works, but conventionally "don't do this")
# print(acc.__pin)            # AttributeError
print(acc._BankAccount__pin)  # '1234' — mangled name is accessible if you know it
```

| Prefix | Name | Accessible from outside? |
|--------|------|--------------------------|
| `name` | public | ✅ freely |
| `_name` | protected | ✅ but conventional "please don't" |
| `__name` | private (mangled) | Only via `_ClassName__name` |

</details>

---

## Dataclasses

<details>
<summary><strong>Q8. What are dataclasses and when should you use them instead of a regular class?</strong></summary>

`@dataclass` auto-generates `__init__`, `__repr__`, and `__eq__` based on annotated fields, eliminating boilerplate.

```python
from dataclasses import dataclass, field
from typing import List

# Regular class — lots of boilerplate
class PersonOld:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

# Dataclass — same result, much less code
@dataclass
class Person:
    name: str
    age: int
    tags: List[str] = field(default_factory=list)  # mutable default must use field()

    def greet(self):           # you can still add methods
        return f"Hi, I'm {self.name}"

p1 = Person("Alice", 30)
p2 = Person("Alice", 30)
print(p1)           # Person(name='Alice', age=30, tags=[])
print(p1 == p2)     # True — __eq__ compares all fields

# frozen=True — makes the instance immutable (hashable too)
@dataclass(frozen=True)
class Point:
    x: float
    y: float

pt = Point(1.0, 2.0)
# pt.x = 5  # ← FrozenInstanceError

# order=True — generates __lt__, __le__, __gt__, __ge__
@dataclass(order=True)
class Employee:
    salary: float
    name: str

employees = [Employee(50000, "Bob"), Employee(75000, "Alice")]
print(sorted(employees))   # sorted by salary first (field order matters)
```

**Use dataclasses when:** the primary purpose of the class is to hold data, and you'd otherwise write a tedious `__init__` by hand.

**Don't use dataclasses when:** you need complex initialisation logic, inheritance chains where `super().__init__()` ordering matters, or when the class has few fields and no need for `__eq__`/`__repr__`.

</details>

---

<details>
<summary><strong>Q9. What is <code>__post_init__</code> in a dataclass?</strong></summary>

`__post_init__` runs after the auto-generated `__init__`, allowing validation or computed fields.

```python
from dataclasses import dataclass, field

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)   # not a constructor parameter

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be positive")
        self.area = self.width * self.height   # computed field

r = Rectangle(3.0, 4.0)
print(r.area)   # 12.0

Rectangle(-1, 4)  # ← ValueError: Dimensions must be positive
```

</details>

---

## Design Patterns (common at Accenture)

<details>
<summary><strong>Q10. Implement the Singleton pattern in Python.</strong></summary>

A Singleton ensures only **one instance** of a class exists.

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value

s1 = Singleton(10)
s2 = Singleton(20)
print(s1 is s2)    # True — same object
print(s1.value)    # 20 — __init__ ran again on the same instance

# Thread-safe version
import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
```

</details>

---

<details>
<summary><strong>Q11. Implement the Factory pattern in Python.</strong></summary>

A Factory creates objects without the caller needing to know the exact class.

```python
class Dog:
    def speak(self): return "Woof"

class Cat:
    def speak(self): return "Meow"

class Bird:
    def speak(self): return "Tweet"

class AnimalFactory:
    _registry = {
        "dog": Dog,
        "cat": Cat,
        "bird": Bird,
    }

    @classmethod
    def create(cls, animal_type: str):
        klass = cls._registry.get(animal_type.lower())
        if klass is None:
            raise ValueError(f"Unknown animal type: {animal_type!r}")
        return klass()

    @classmethod
    def register(cls, name: str, klass):
        """Extensible — add new types without changing existing code."""
        cls._registry[name] = klass

animal = AnimalFactory.create("dog")
print(animal.speak())   # Woof
```

</details>

---

*See also: [`qa-python-core.md`](./qa-python-core.md) · [`qa-coding-problems.md`](./qa-coding-problems.md)*
