# 💻 Coding Problems — Questions & Solutions

> Each problem includes: the question, approach explanation, full Python solution, complexity analysis, and edge cases.
> Difficulty mirrors Accenture's coding round (easy to medium).

---

## Strings

<details>
<summary><strong>P1. Reverse words in a string</strong><br><code>"Accenture is great" → "great is Accenture"</code></summary>

**Approach:** Split by whitespace, reverse the list, rejoin with spaces. Python's `split()` handles multiple spaces and leading/trailing whitespace automatically.

```python
def reverse_words(s: str) -> str:
    return " ".join(s.split()[::-1])

# Tests
print(reverse_words("Accenture is great"))    # "great is Accenture"
print(reverse_words("  hello   world  "))     # "world hello"  (handles extra spaces)
print(reverse_words("single"))                # "single"
print(reverse_words(""))                      # ""
```

**Complexity:** O(n) time, O(n) space

**Edge cases:**
- Multiple spaces between words → `split()` with no args handles this
- Leading/trailing spaces → `split()` handles this
- Single word → returns the word unchanged
- Empty string → returns empty string

</details>

---

<details>
<summary><strong>P2. Check if a string is a palindrome</strong><br><code>"racecar" → True, "hello" → False</code></summary>

**Approach:** Compare the string to its reverse. For a "real" palindrome check (ignoring non-alphanumeric and case), clean the string first.

```python
# Simple version
def is_palindrome(s: str) -> bool:
    return s == s[::-1]

# Real-world version (ignores spaces, punctuation, case)
def is_palindrome_clean(s: str) -> bool:
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]

# Two-pointer version (no extra space)
def is_palindrome_two_ptr(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

# Tests
print(is_palindrome("racecar"))             # True
print(is_palindrome_clean("A man a plan a canal Panama"))  # True
print(is_palindrome("hello"))               # False
print(is_palindrome(""))                    # True
print(is_palindrome("a"))                   # True
```

**Complexity:** O(n) time, O(n) space for slice approach; O(1) space for two-pointer

</details>

---

<details>
<summary><strong>P3. Check if two strings are anagrams</strong><br><code>"listen", "silent" → True</code></summary>

**Approach:** Two strings are anagrams if they contain the same characters with the same frequencies. Compare sorted strings or frequency maps.

```python
from collections import Counter

# Method 1: Sort (O(n log n))
def is_anagram_sort(s: str, t: str) -> bool:
    return sorted(s.lower()) == sorted(t.lower())

# Method 2: Counter (O(n)) — preferred
def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    return Counter(s.lower()) == Counter(t.lower())

# Method 3: Manual frequency dict (shows understanding)
def is_anagram_manual(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    for c in t:
        freq[c] = freq.get(c, 0) - 1
        if freq[c] < 0:
            return False
    return True

print(is_anagram("listen", "silent"))   # True
print(is_anagram("hello", "world"))     # False
print(is_anagram("Astronomer", "Moon starer"))  # True (if spaces ignored)
```

**Note:** Accenture interviewers specifically ask for **multiple approaches** for problems like this — always mention at least two.

</details>

---

<details>
<summary><strong>P4. Password validation</strong><br>Return 1 if valid, 0 if not. Rules: ≥ 4 chars, at least one uppercase, one lowercase, one digit.</summary>

```python
def is_valid_password(s: str) -> int:
    if len(s) < 4:
        return 0
    has_upper = any(c.isupper() for c in s)
    has_lower = any(c.islower() for c in s)
    has_digit = any(c.isdigit() for c in s)
    return 1 if (has_upper and has_lower and has_digit) else 0

# Extended version with special character requirement
def is_valid_password_ext(s: str, min_len=8) -> int:
    import string
    if len(s) < min_len:
        return 0
    checks = [
        any(c.isupper() for c in s),
        any(c.islower() for c in s),
        any(c.isdigit() for c in s),
        any(c in string.punctuation for c in s),
    ]
    return 1 if all(checks) else 0

print(is_valid_password("Ab3d"))   # 1
print(is_valid_password("abc"))    # 0 — too short
print(is_valid_password("abcd"))   # 0 — no uppercase or digit
print(is_valid_password("ABCD1"))  # 0 — no lowercase
```

</details>

---

<details>
<summary><strong>P5. Longest substring without repeating characters</strong><br><code>"abcabcbb" → 3 ("abc")</code></summary>

**Approach:** Sliding window with a set tracking characters in the current window. Expand right pointer; when duplicate found, shrink from left.

```python
def length_of_longest_substring(s: str) -> int:
    char_set = set()
    left = 0
    max_len = 0

    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len

# Optimised: store last index of each char for O(n) jumps
def length_of_longest_substring_opt(s: str) -> int:
    last_seen = {}
    left = 0
    max_len = 0

    for right, char in enumerate(right, s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len

print(length_of_longest_substring("abcabcbb"))   # 3
print(length_of_longest_substring("bbbbb"))      # 1
print(length_of_longest_substring("pwwkew"))     # 3
print(length_of_longest_substring(""))           # 0
```

**Complexity:** O(n) time, O(min(n, alphabet)) space

</details>

---

<details>
<summary><strong>P6. First non-repeating character — return its index</strong><br><code>"leetcode" → 0, "loveleetcode" → 2</code></summary>

```python
from collections import Counter

def first_unique_char(s: str) -> int:
    freq = Counter(s)
    for i, c in enumerate(s):
        if freq[c] == 1:
            return i
    return -1

# Two-pass manual version
def first_unique_char_manual(s: str) -> int:
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    for i, c in enumerate(s):
        if count[c] == 1:
            return i
    return -1

print(first_unique_char("leetcode"))        # 0
print(first_unique_char("loveleetcode"))    # 2
print(first_unique_char("aabb"))            # -1
```

**Complexity:** O(n) time, O(1) space (at most 26 lowercase letters in the dict)

</details>

---

## Arrays & Math

<details>
<summary><strong>P7. Find the second-largest element in an array</strong><br><code>[3, 1, 4, 1, 5, 9, 2, 6] → 6</code></summary>

```python
# Method 1: Sort + deduplicate (clean, easy to explain)
def second_largest_sort(arr: list):
    unique = sorted(set(arr), reverse=True)
    return unique[1] if len(unique) >= 2 else None

# Method 2: Single pass O(n) — preferred in interviews
def second_largest(arr: list):
    if len(arr) < 2:
        return None
    first = second = float('-inf')
    for n in arr:
        if n > first:
            second = first
            first = n
        elif first > n > second:
            second = n
    return second if second != float('-inf') else None

print(second_largest([3, 1, 4, 1, 5, 9, 2, 6]))   # 6
print(second_largest([5, 5, 5]))                   # None — all same
print(second_largest([10]))                        # None — only one element
print(second_largest([-1, -2, -3]))                # -2
```

**Note:** Accenture problems often ask for second-largest from even/odd positions specifically — adapt the single-pass approach by filtering indices first.

</details>

---

<details>
<summary><strong>P8. Find the missing number in an array of 1 to N</strong><br><code>[1, 2, 4, 5] → 3 (N=5)</code></summary>

```python
# Method 1: Formula — O(n) time, O(1) space
def missing_number(arr: list) -> int:
    n = len(arr) + 1
    expected_sum = n * (n + 1) // 2
    return expected_sum - sum(arr)

# Method 2: XOR — avoids integer overflow for very large N
def missing_number_xor(arr: list) -> int:
    n = len(arr) + 1
    xor = 0
    for i in range(1, n + 1):
        xor ^= i
    for num in arr:
        xor ^= num
    return xor  # all paired numbers cancel out, leaving the missing one

print(missing_number([1, 2, 4, 5]))    # 3
print(missing_number([2, 3, 4, 5]))    # 1
print(missing_number([1, 2, 3, 4]))    # 5
```

</details>

---

<details>
<summary><strong>P9. Rotate an array to the right by K steps</strong><br><code>[1,2,3,4,5], k=2 → [4,5,1,2,3]</code></summary>

```python
# Method 1: Slice (Pythonic, O(n) space)
def rotate(arr: list, k: int) -> list:
    k = k % len(arr)   # handle k > len
    return arr[-k:] + arr[:-k]

# Method 2: Reverse algorithm — O(1) space (in-place)
def rotate_inplace(arr: list, k: int) -> None:
    n = len(arr)
    k = k % n

    def reverse(left, right):
        while left < right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

    reverse(0, n - 1)   # reverse entire array
    reverse(0, k - 1)   # reverse first k elements
    reverse(k, n - 1)   # reverse remaining

arr = [1, 2, 3, 4, 5]
print(rotate(arr, 2))   # [4, 5, 1, 2, 3]

rotate_inplace(arr, 2)
print(arr)              # [4, 5, 1, 2, 3]
```

</details>

---

<details>
<summary><strong>P10. Decimal to base N conversion</strong><br><code>dec_to_base(10, 2) → "1010"</code></summary>

```python
def dec_to_base(num: int, base: int) -> str:
    if num == 0:
        return "0"
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    negative = num < 0
    num = abs(num)
    while num > 0:
        result = chars[num % base] + result
        num //= base
    return ("-" + result) if negative else result

# Python built-ins for common bases
print(bin(10))    # '0b1010' — binary
print(oct(10))    # '0o12'   — octal
print(hex(255))   # '0xff'   — hexadecimal

print(dec_to_base(10, 2))    # '1010'
print(dec_to_base(255, 16))  # 'FF'
print(dec_to_base(8, 8))     # '10'
print(dec_to_base(0, 2))     # '0'
```

</details>

---

## Dictionaries & Frequency

<details>
<summary><strong>P11. Two Sum — find indices of two numbers that add up to target</strong><br><code>[2,7,11,15], target=9 → [0,1]</code></summary>

```python
# Method 1: Brute force O(n²)
def two_sum_brute(nums: list, target: int) -> list:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# Method 2: Hash map O(n) — always use this
def two_sum(nums: list, target: int) -> list:
    seen = {}   # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))    # [0, 1]
print(two_sum([3, 2, 4], 6))         # [1, 2]
print(two_sum([3, 3], 6))            # [0, 1]
```

**Always offer both approaches.** Accenture specifically asks for multiple ways to solve dictionary-based problems.

</details>

---

<details>
<summary><strong>P12. Group anagrams together</strong><br><code>["eat","tea","tan","ate","nat","bat"] → [["eat","tea","ate"],["tan","nat"],["bat"]]</code></summary>

```python
from collections import defaultdict

def group_anagrams(words: list) -> list:
    groups = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))   # sorted letters = canonical key
        groups[key].append(word)
    return list(groups.values())

# Alternative key: tuple of character counts (avoids sorting)
def group_anagrams_count(words: list) -> list:
    groups = defaultdict(list)
    for word in words:
        count = [0] * 26
        for c in word:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(word)
    return list(groups.values())

print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

</details>

---

<details>
<summary><strong>P13. Top K frequent elements</strong><br><code>[1,1,1,2,2,3], k=2 → [1, 2]</code></summary>

```python
from collections import Counter
import heapq

# Method 1: Counter.most_common — O(n log k)
def top_k_frequent(nums: list, k: int) -> list:
    return [num for num, _ in Counter(nums).most_common(k)]

# Method 2: Bucket sort — O(n), clever approach to impress
def top_k_frequent_bucket(nums: list, k: int) -> list:
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
    return result

print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))   # [1, 2]
print(top_k_frequent([1], 1))                   # [1]
```

</details>

---

## Sorting & Searching

<details>
<summary><strong>P14. Sort a list of tuples by multiple keys</strong><br>Sort students by score descending, then name ascending.</summary>

```python
students = [("Alice", 90), ("Bob", 85), ("Charlie", 90), ("Dave", 85)]

# Sort by score descending (-score), then name ascending
sorted_students = sorted(students, key=lambda s: (-s[1], s[0]))
print(sorted_students)
# [('Alice', 90), ('Charlie', 90), ('Bob', 85), ('Dave', 85)]

# Using operator.itemgetter (faster than lambda for large data)
from operator import itemgetter
# Can't negate with itemgetter alone, but useful for ascending sorts:
sorted_by_name = sorted(students, key=itemgetter(0))

# sort() vs sorted()
# sorted() — returns a NEW list; original unchanged
# .sort() — sorts IN PLACE; returns None
```

</details>

---

<details>
<summary><strong>P15. Merge two sorted lists into one sorted list</strong></summary>

```python
# Method 1: Merge step from merge sort — O(n+m) time, O(n+m) space
def merge_sorted(a: list, b: list) -> list:
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    return result + a[i:] + b[j:]

# Method 2: Pythonic one-liner (less efficient but concise)
def merge_sorted_simple(a: list, b: list) -> list:
    return sorted(a + b)  # O((n+m) log(n+m))

# Method 3: heapq.merge — lazy iterator (memory efficient)
import heapq
def merge_sorted_lazy(a, b):
    return list(heapq.merge(a, b))

print(merge_sorted([1, 3, 5], [2, 4, 6]))   # [1, 2, 3, 4, 5, 6]
print(merge_sorted([], [1, 2]))              # [1, 2]
print(merge_sorted([1], []))                 # [1]
```

</details>

---

## Accenture-specific patterns

<details>
<summary><strong>P16. Sum of second-largest from even positions and second-smallest from odd positions</strong><br>(Reported in Accenture Glassdoor coding round)</summary>

```python
def even_odd_second(arr: list) -> int:
    """
    arr is 0-indexed.
    Even positions: indices 0, 2, 4, ...
    Odd positions: indices 1, 3, 5, ...
    """
    even_vals = sorted(set(arr[i] for i in range(0, len(arr), 2)), reverse=True)
    odd_vals  = sorted(set(arr[i] for i in range(1, len(arr), 2)))

    second_largest_even = even_vals[1] if len(even_vals) >= 2 else even_vals[0]
    second_smallest_odd = odd_vals[1]  if len(odd_vals)  >= 2 else odd_vals[0]

    return second_largest_even + second_smallest_odd

arr = [5, 3, 8, 1, 6, 9, 2, 4]
# Even positions (0,2,4,6): [5,8,6,2] → sorted desc: [8,6,5,2] → 2nd largest: 6
# Odd positions (1,3,5,7):  [3,1,9,4] → sorted asc: [1,3,4,9] → 2nd smallest: 3
print(even_odd_second(arr))  # 9
```

</details>

---

<details>
<summary><strong>P17. Count lucky numbers — digit counts match digit value</strong><br>(Reported in Accenture OA — PrepInsta pattern Q20)</summary>

A digit `d` at position `i` in string `s` is "lucky" if the **count** of the character `str(i)` in `s` equals `int(s[i])`.

```python
def lucky_digits(s: str) -> list:
    result = []
    for i in range(len(s)):
        digit = int(s[i])
        if s.count(str(i)) == digit:
            result.append(digit)
    # return unique values
    return list(set(result))

print(lucky_digits("2020"))   # example
```

</details>

---

*See also: [`qa-pandas-numpy.md`](./qa-pandas-numpy.md) · [`qa-sql.md`](./qa-sql.md)*
