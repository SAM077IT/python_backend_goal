# 💻 Coding Practice Log

> Track every problem you solve here. The goal is **≥ 10 problems** before the assessment,
> with at least one full timed mock session (45 minutes, 2–3 problems, no lookups).

---

## 🎯 Strategy for the Accenture Coding Round

| Priority | Tactic |
|----------|--------|
| **1st** | Read all problems before starting — pick the easiest one first |
| **2nd** | Write a brute-force solution that works — partial credit is real |
| **3rd** | Optimize only if you have time after all problems are attempted |
| **4th** | Always test edge cases: empty input, single element, duplicates, negatives |
| **Target** | 2 fully correct + 1 partial = sufficient to clear |

**Time budget (45-min session):**
- Problem 1 (easy): ≤ 12 minutes
- Problem 2 (medium): ≤ 20 minutes
- Problem 3 (hard/partial): remaining time

---

## 📚 Pattern 1 — String Manipulation

*Most commonly reported pattern in Accenture coding rounds.*

### Key techniques
- `s.split()`, `s.join()`, `s[::-1]` for reversal
- `s.lower()`, `s.upper()`, `s.isalpha()`, `s.isdigit()`
- `collections.Counter(s)` for frequency maps
- Sliding window for substrings

### Template problems

```python
# 1. Reverse words in a string
def reverse_words(s: str) -> str:
    return " ".join(s.split()[::-1])

# 2. Check if two strings are anagrams
from collections import Counter
def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

# 3. Password validation
def is_valid_password(s: str) -> int:
    if (len(s) >= 4 and
        any(c.isupper() for c in s) and
        any(c.islower() for c in s) and
        any(c.isdigit() for c in s)):
        return 1
    return 0

# 4. First non-repeating character
def first_unique(s: str) -> int:
    freq = Counter(s)
    for i, c in enumerate(s):
        if freq[c] == 1:
            return i
    return -1
```

### Practice log — String problems

| # | Problem | Difficulty | Solved? | Time taken | Notes |
|---|---------|------------|---------|------------|-------|
| 1 | Reverse words in a string | Easy | [ ] | | |
| 2 | Check anagram | Easy | [ ] | | |
| 3 | Password validation | Easy | [ ] | | |
| 4 | Longest substring without repeating chars | Medium | [ ] | | |
| 5 | Count vowels and consonants | Easy | [ ] | | |
| 6 | Check if string is palindrome | Easy | [ ] | | |
| 7 | Find all permutations of a string | Medium | [ ] | | |
| 8 | _(add your own)_ | | [ ] | | |

---

## 📚 Pattern 2 — Arrays & Math

### Key techniques
- `sorted()` with `set()` for unique elements
- `enumerate()` for index + value together
- Two-pointer for sorted arrays
- Modulo (`%`) and integer division (`//`) for digit/base problems

### Template problems

```python
# 1. Second largest element
def second_largest(arr: list) -> int:
    unique = sorted(set(arr), reverse=True)
    return unique[1] if len(unique) > 1 else None

# 2. Max value and its index
def max_with_index(arr: list) -> tuple:
    m = max(arr)
    return m, arr.index(m)

# 3. Base conversion (decimal → base N)
def dec_to_base(num: int, base: int) -> str:
    if num == 0:
        return "0"
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    while num > 0:
        result = chars[num % base] + result
        num //= base
    return result

# 4. Sum of digits
def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

# 5. Check prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```

### Practice log — Array & math problems

| # | Problem | Difficulty | Solved? | Time taken | Notes |
|---|---------|------------|---------|------------|-------|
| 1 | Second largest element | Easy | [ ] | | |
| 2 | Max value and index | Easy | [ ] | | |
| 3 | Base conversion | Medium | [ ] | | |
| 4 | Sum of digits | Easy | [ ] | | |
| 5 | Check prime | Easy | [ ] | | |
| 6 | Rotate array by K positions | Medium | [ ] | | |
| 7 | Find missing number in 1..N | Medium | [ ] | | |
| 8 | _(add your own)_ | | [ ] | | |

---

## 📚 Pattern 3 — Dictionary & Collections

*Glassdoor (Mumbai, Feb 2025) specifically confirmed: dictionary problems asked with multiple solution approaches expected.*

### Key techniques
- `collections.Counter` — frequency counting
- `collections.defaultdict` — auto-initializing dicts
- `dict.get(key, default)` — safe access
- Dict comprehensions for transformation

### Template problems

```python
from collections import Counter, defaultdict

# 1. Word frequency count
def word_freq(text: str) -> dict:
    return dict(Counter(text.lower().split()))

# 2. Group anagrams together
def group_anagrams(words: list) -> list:
    groups = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())

# 3. Two-sum using a dict (O(n))
def two_sum(nums: list, target: int) -> list:
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []

# 4. Invert a dictionary
def invert_dict(d: dict) -> dict:
    return {v: k for k, v in d.items()}

# 5. Most common element
def most_common(lst: list):
    return Counter(lst).most_common(1)[0][0]
```

### Practice log — Dictionary problems

| # | Problem | Difficulty | Solved? | Time taken | Notes |
|---|---------|------------|---------|------------|-------|
| 1 | Word frequency count | Easy | [ ] | | |
| 2 | Group anagrams | Medium | [ ] | | |
| 3 | Two sum (dict approach) | Medium | [ ] | | |
| 4 | Invert a dictionary | Easy | [ ] | | |
| 5 | Most common element | Easy | [ ] | | |
| 6 | _(add your own)_ | | [ ] | | |

---

## 📚 Pattern 4 — Sorting & Searching

### Key techniques
- `sorted(arr, key=lambda x: ...)` — custom sort key
- `bisect` module for binary search on sorted lists
- `heapq` for top-K problems

### Template problems

```python
import heapq

# 1. Sort by multiple keys
students = [("Alice", 90), ("Bob", 85), ("Charlie", 90)]
sorted_students = sorted(students, key=lambda x: (-x[1], x[0]))

# 2. Top K frequent elements
def top_k_frequent(nums: list, k: int) -> list:
    return [x for x, _ in Counter(nums).most_common(k)]

# 3. Merge two sorted lists
def merge_sorted(a: list, b: list) -> list:
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    return result + a[i:] + b[j:]
```

### Practice log — Sorting & searching

| # | Problem | Difficulty | Solved? | Time taken | Notes |
|---|---------|------------|---------|------------|-------|
| 1 | Sort by multiple keys | Easy | [ ] | | |
| 2 | Top K frequent elements | Medium | [ ] | | |
| 3 | Merge two sorted lists | Medium | [ ] | | |
| 4 | Binary search | Easy | [ ] | | |
| 5 | _(add your own)_ | | [ ] | | |

---

## 🕐 Mock Sessions Log

Record your timed mock sessions here.

### Mock Session 1
- **Date:** 
- **Time limit:** 45 minutes
- **Problems attempted:**
  1. 
  2. 
  3. 
- **Results:** ___ / ___ fully solved
- **What went wrong:**
- **What to fix:**

---

### Mock Session 2
- **Date:** 
- **Time limit:** 45 minutes
- **Problems attempted:**
  1. 
  2. 
  3. 
- **Results:** ___ / ___ fully solved
- **What went wrong:**
- **What to fix:**

---

## 📊 Overall Coding Progress

- [ ] ≥ 5 string problems solved
- [ ] ≥ 5 array/math problems solved
- [ ] ≥ 4 dictionary problems solved
- [ ] ≥ 3 sorting problems solved
- [ ] ≥ 1 timed mock session completed (45 min, no lookups)
- [ ] ≥ 2 mock sessions completed
- [ ] Reviewed all mistakes and weak patterns

**Total problems solved:** `0`
*(update this manually)*
