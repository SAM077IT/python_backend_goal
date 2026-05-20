# ⏱️ 48-Hour Study Plan

> **Tip:** GitHub renders `- [ ]` as clickable checkboxes. Check items off directly in the GitHub UI, or edit this file locally.

---

## 📅 Day 1 — Foundation & Coding Patterns (Hours 0–24)

### 🕐 Hours 0–3 · Python Core Review
> Goal: Nail the most-reported Python interview concepts

- [ ] Decorators — write one from scratch, understand `functools.wraps`
- [ ] Closures — understand captured variables, `nonlocal`
- [ ] Context managers — `with` statement, `__enter__`/`__exit__`, `contextlib`
- [ ] `*args` and `**kwargs` — how they work, when to use each
- [ ] List / dict / set comprehensions with conditions
- [ ] Mutable vs immutable types — know which built-ins are which
- [ ] Shallow vs deep copy — `copy.copy()` vs `copy.deepcopy()`, where each matters

**Resources:**
- [Real Python — Decorators](https://realpython.com/primer-on-python-decorators/)
- [Python docs — `copy` module](https://docs.python.org/3/library/copy.html)

---

### 🕓 Hours 3–6 · OOP Deep Dive
> Goal: Be able to write a class hierarchy and explain every concept

- [ ] Classes and instances — `__init__`, instance vs class attributes
- [ ] Inheritance — `super()`, MRO (Method Resolution Order)
- [ ] Polymorphism — method overriding, duck typing
- [ ] Dunder methods — `__str__`, `__repr__`, `__len__`, `__eq__`, `__hash__`
- [ ] Abstract classes — `abc.ABC`, `@abstractmethod`
- [ ] Dataclasses — `@dataclass`, `field()`, `frozen=True`
- [ ] Class methods vs static methods vs instance methods

**Practice:** Write a `Shape → Circle / Rectangle` hierarchy with area/perimeter methods.

---

### 🕕 Hours 6–9 · DSA Patterns — Strings & Arrays
> Goal: Solve typical Accenture coding problems fluently

- [ ] Two-pointer technique
- [ ] Sliding window
- [ ] Frequency map with `collections.Counter`
- [ ] Sorting with custom key (`sorted(arr, key=lambda x: ...)`)
- [ ] Solve ≥ 5 problems (track in [`coding-practice.md`](./coding-practice.md))

**Problem targets:**
- [ ] Reverse words in a string
- [ ] Check if string is an anagram
- [ ] Longest substring without repeating characters
- [ ] Find second-largest element in array
- [ ] Password validation with multiple conditions

---

### 🕗 Hours 9–12 · Pandas & NumPy
> Goal: Handle the data library coding challenges Accenture is known for

**Pandas:**
- [ ] Create a DataFrame from dict / list
- [ ] `.groupby()` + aggregation (`sum`, `mean`, `count`)
- [ ] `.merge()` — inner, left, right joins
- [ ] `.apply()` with lambda
- [ ] `.fillna()`, `.dropna()`, `.isna()`
- [ ] Boolean indexing / `.query()`
- [ ] `.pivot_table()`

**NumPy:**
- [ ] Array creation: `np.array`, `np.zeros`, `np.arange`, `np.linspace`
- [ ] Indexing and slicing: `arr[1:3]`, `arr[:, 0]`
- [ ] Broadcasting rules
- [ ] `np.argmax`, `np.argsort`, `np.unique`
- [ ] Matrix operations: `np.dot`, `np.linalg.inv`

---

### 🕙 Hours 12–15 · SQL
> Goal: Write joins, aggregations, and window functions confidently

- [ ] `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`
- [ ] `GROUP BY` + `HAVING`
- [ ] Subqueries in `WHERE` and `FROM`
- [ ] `ORDER BY` with `ASC`/`DESC`
- [ ] Window functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `PARTITION BY`
- [ ] `CASE WHEN` statements
- [ ] `DISTINCT`, `LIMIT`, `OFFSET`

**Practice:** [SQLZoo](https://sqlzoo.net/) — complete the SELECT basics + joins sections.

---

### 🕛 Hours 15–20 · Timed Mock Coding Session
> Simulate the real test environment

- [ ] Set a **45-minute timer**
- [ ] Pick 2–3 problems from [HackerRank Accenture practice](https://www.hackerrank.com/)
- [ ] No looking things up during the session
- [ ] After: review mistakes and note weak areas below

**Weak areas identified:**
> _(fill in after the mock)_

---

### 🕑 Hours 20–24 · Light Review + Rest
- [ ] Skim networking basics: OSI model (7 layers), HTTP vs HTTPS, TCP vs UDP
- [ ] Cloud terminology: IaaS / PaaS / SaaS, containers, CI/CD pipelines
- [ ] Review any notes from today's sessions
- [ ] **Sleep** — critical for performance

---

## 📅 Day 2 — Consolidation & Confidence (Hours 24–48)

### 🕑 Hours 24–27 · Flask / Django REST API Concepts
> Goal: Answer "design a secure, scalable REST API" confidently

- [ ] Flask routes — `@app.route`, HTTP methods
- [ ] Request/response cycle — `request.json`, `jsonify`
- [ ] Authentication — JWT basics, `flask-jwt-extended`
- [ ] Error handling — custom error handlers, HTTP status codes
- [ ] Blueprints for modular Flask apps
- [ ] Django vs Flask — when to use which
- [ ] Django: MVT pattern, ORM, migrations

---

### 🕓 Hours 27–30 · Pythonic Code & Error Handling
> Goal: Impress in code review scenario questions

- [ ] `try` / `except` / `else` / `finally` structure
- [ ] Custom exception classes (inherit from `Exception`)
- [ ] Logging — `logging` module, log levels, formatting
- [ ] Type hints — `def fn(x: int) -> str:`
- [ ] PEP 8 — naming conventions, line length, imports order
- [ ] `f-strings` vs `.format()` vs `%` formatting

---

### 🕔 Hours 30–33 · AI/ML Awareness
> Goal: Speak knowledgeably about AI/ML — now explicitly tested at Accenture

- [ ] Supervised vs unsupervised vs reinforcement learning
- [ ] Common models: linear regression, logistic regression, decision tree, random forest, SVM
- [ ] Overfitting / underfitting — bias-variance tradeoff
- [ ] `scikit-learn` basics: `fit()`, `predict()`, `train_test_split`, `Pipeline`
- [ ] What an LLM is — transformer architecture at a high level
- [ ] AI ethics / responsible AI (Accenture's focus area)
- [ ] Pandas + scikit-learn integration for data preprocessing

---

### 🕗 Hours 33–40 · Full Mock Assessment (Timed)
> Simulate the entire OA back to back

- [ ] 30 minutes — MCQ: verbal + pseudo-code + networking (use PrepInsta Accenture mock)
- [ ] 45 minutes — Coding: 2 full problems, no external lookup
- [ ] Score yourself and record below

**Mock results:**
| Metric | Result |
|--------|--------|
| Problems fully solved | `/2` |
| Problems partially solved | `/1` |
| Estimated MCQ score | `%` |
| Weak spots to address | |

---

### 🕙 Hours 40–44 · Behavioral Interview Prep
> Goal: Have 3–4 strong STAR stories ready

**STAR = Situation · Task · Action · Result**

- [ ] Story 1 — Complex technical problem I debugged / solved
- [ ] Story 2 — System or feature I designed end-to-end
- [ ] Story 3 — Difficult team situation / conflict I navigated
- [ ] Story 4 — Time I learned a new technology quickly under pressure

**Accenture values to weave in:**
- Stewardship, Best people, Client value creation, One global network, Respect for individuals, Integrity

---

### 🕑 Hours 44–48 · Final Review + Setup
- [ ] Re-read notes on decorators, OOP, and your identified weak spots
- [ ] Set up your physical exam environment (see [`day-of-checklist.md`](./day-of-checklist.md))
- [ ] Confirm assessment link and login work
- [ ] **No new topics** — just consolidate what you know
- [ ] Early sleep

---

## 📝 Notes & Observations

> Use this space to jot down anything important during prep.

```
Day 1 notes:


Day 2 notes:


```
