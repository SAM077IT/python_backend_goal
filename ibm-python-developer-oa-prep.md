# IBM Python Developer — Online Assessment Practice Set
*3+ years experience track — evening cram session*

---

## What to Expect (confirmed structure)

Your invite breaks the test down into two graded sections:

| # | Section | Questions |
|---|---|---|
| 1 | Coding (Standard) | 1 |
| 2 | REST API | 1 |

That's two coding questions total, no separate MCQ block based on this breakdown — so the priority tonight is **one solid Standard DSA problem** and **one REST API consumption problem**, not broad MCQ trivia. (A condensed MCQ appendix is still included at the bottom as a low-priority backup, in case a pretest section shows up that wasn't itemized in the table.)

- **Coding (Standard)** = a classic algorithmic problem — arrays/strings/hashmaps are IBM's most common territory, LeetCode Easy–Medium difficulty.
- **REST API** = a HackerRank-specific question type: you're given a live (or described) JSON API endpoint and asked to write a Python function that calls it, parses the response, and returns a computed answer — not to build/host an API yourself.
- **Language:** take both sections in Python — it's your strongest language and the posting's preferred one.

---

## Section A — Coding (Standard) Practice

<details>
<summary><strong>1. Two Sum (Hashmap — highest-yield pattern)</strong></summary>

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# two_sum([2, 7, 11, 15], 9) -> [0, 1]
```
**Complexity:** O(n) time, O(n) space.

</details>

<details>
<summary><strong>2. Maximum Subarray Sum — Kadane's Algorithm</strong></summary>

```python
def max_subarray(nums):
    max_sum = curr_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)
        max_sum = max(max_sum, curr_sum)
    return max_sum

# max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) -> 6  ([4, -1, 2, 1])
```
**Complexity:** O(n) time, O(1) space. Very common in IBM's array-heavy set — know it cold.

</details>

<details>
<summary><strong>3. Valid Palindrome (Two Pointers)</strong></summary>

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True

# is_palindrome("A man, a plan, a canal: Panama") -> True
```
**Complexity:** O(n) time, O(1) space.

</details>

<details>
<summary><strong>4. First Non-Repeating Character (Hashmap)</strong></summary>

```python
def first_unique_char(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1

# first_unique_char("swiss") -> 1  ('w')
```
**Complexity:** O(n) time, O(k) space.

</details>

<details>
<summary><strong>5. Rotate Array In-Place (O(1) space trick)</strong></summary>

```python
def rotate(nums, k):
    n = len(nums)
    k %= n

    def reverse(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
    return nums

# rotate([1, 2, 3, 4, 5, 6, 7], 3) -> [5, 6, 7, 1, 2, 3, 4]
```
**Complexity:** O(n) time, O(1) space — the "reverse three times" trick is the answer interviewers are fishing for over an extra-array approach.

</details>

<details>
<summary><strong>6. Climbing Stairs — Bottom-Up DP</strong></summary>

```python
def climb_stairs(n):
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1

# climb_stairs(5) -> 8
```
**Complexity:** O(n) time, O(1) space — jump straight to iterative bottom-up rather than naive recursion.

</details>

<details>
<summary><strong>7. Low-Stock Categories (Dict/List, Martify-flavored)</strong></summary>

```python
def low_stock_categories(products, threshold):
    """
    products: [{"name": "Mug", "category": "Kitchen", "stock": 4}, ...]
    Returns category names whose total stock is below threshold.
    """
    totals = {}
    for p in products:
        totals[p["category"]] = totals.get(p["category"], 0) + p["stock"]
    return [cat for cat, total in totals.items() if total < threshold]

products = [
    {"name": "Mug", "category": "Kitchen", "stock": 4},
    {"name": "Pan", "category": "Kitchen", "stock": 2},
    {"name": "Lamp", "category": "Home", "stock": 15},
]
# low_stock_categories(products, 10) -> ["Kitchen"]
```
**Complexity:** O(n) time, O(k) space. Good rehearsal for when the "array" in a question turns out to be a list of dicts, which is exactly what the REST API section below will hand you.

</details>

**Rapid-fire, no solutions (self-test first):**
1. Reverse a singly linked list, iteratively.
2. Check if two strings are anagrams of each other.
3. Find the missing number in an array containing `1` to `n` with one missing.
4. Merge two already-sorted arrays without using `sort()`.
5. Count word frequency in a paragraph, case-insensitive, ignoring punctuation.

---

## Section B — REST API Practice

This is the section worth the most fresh prep tonight since it's a distinct skill from general DSA.

**What it actually tests:** not designing/hosting an API — *consuming* one. You'll be given (or told about) a live JSON endpoint and asked to write a function that calls it with `requests`, parses the JSON, and returns a computed value. HackerRank's own public sandbox for this lives at `jsonmock.hackerrank.com` — worth hitting a couple of its endpoints in a local Python shell tonight just to get a feel for typical response shapes (a `data` array plus pagination metadata) before the timer starts.

Four patterns cover almost everything this section throws at you:

<details>
<summary><strong>R1. Basic Consume + Safe Field Extraction</strong></summary>

*Given a search term, call an endpoint that returns a JSON object with a `data` array of matches, and return one field from the first match — or a sentinel if nothing matches.*

```python
import requests

def get_field_for_match(search_term: str, field: str, base_url: str) -> str:
    """
    Calls base_url with a `name` query param and returns `field`
    from the first matching record. Returns "-1" if nothing is found
    or the request fails.
    """
    try:
        response = requests.get(base_url, params={"name": search_term}, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return "-1"

    records = response.json().get("data", [])
    if not records:
        return "-1"

    return str(records[0].get(field, "-1"))
```
**Key skill:** pass filters via `params=` (not manual string concatenation), use `.get()` everywhere instead of `[]` so a missing key doesn't crash the function, and always define a fallback for "not found."

</details>

<details>
<summary><strong>R2. Pagination Aggregation (the most common gotcha)</strong></summary>

*An endpoint returns paginated results (`page`, `total_pages`, `data`). Loop through every page and aggregate something across the full dataset.*

```python
import requests

def count_matching_records(base_url: str, **filters) -> int:
    """
    Walks every page of base_url (filters + a `page` param) and
    counts how many records come back in total.
    """
    page = 1
    total_count = 0

    while True:
        response = requests.get(base_url, params={**filters, "page": page}, timeout=10)
        response.raise_for_status()
        payload = response.json()

        total_count += len(payload.get("data", []))
        total_pages = payload.get("total_pages", 1)

        if page >= total_pages:
            break
        page += 1

    return total_count
```
**Key skill:** read `total_pages` from the response itself and loop until you've covered them all. Forgetting that results span multiple pages — and only reading page 1 — is the single most common way people lose points on this question type.

</details>

<details>
<summary><strong>R3. Filter / Sort / Top-N</strong></summary>

*Fetch records, then filter and sort to answer a specific question ("top 3 by X").*

```python
def top_n_by_field(records: list[dict], field: str, n: int, reverse: bool = True) -> list[dict]:
    """
    Sorts already-fetched records by `field` and returns the top n.
    """
    return sorted(records, key=lambda r: r.get(field, 0), reverse=reverse)[:n]
```
**Key skill:** read the problem statement carefully to know whether filtering/sorting should happen **server-side** (via query params like `sort=` or `filter=`) or **client-side** (in Python, after fetching) — IBM's REST API questions test both variants, and using the wrong one against hidden test cases is an easy way to fail silently.

</details>

<details>
<summary><strong>R4. Defensive Error-Handling Wrapper</strong></summary>

*Wrap any API call so a timeout, network failure, or bad status code returns a clean sentinel instead of crashing.*

```python
import requests

def safe_get_json(url: str, params: dict | None = None):
    """
    Returns the parsed JSON body, or None if the call fails for any reason.
    """
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None
```
**Key skill:** `raise_for_status()` catches 4xx/5xx responses, `timeout=` stops the function from hanging indefinitely, and catching `ValueError` covers malformed/non-JSON bodies. This is the difference between code that only passes the happy-path visible test case and code that survives the hidden edge cases.

</details>

**REST API test-day specifics:**
- Confirm outbound network access actually works in the sandbox *before* you start solving — try a throwaway `requests.get()` first. Some locked-down coding environments block outbound calls entirely and expect you to use a pre-loaded mock client instead; if your first real call hangs, that's the signal.
- Read the field schema in the problem statement closely before coding — most bugs in this section come from a mistyped key name (`"capital"` vs `"Capital"`), not logic errors.
- Default to handling pagination even if the visible sample looks like it fits on one page. Hidden test cases usually don't.
- Keep debug/test calls during scratch work minimal — repeated hammering of the same endpoint can trip rate limits on some sandboxes.

---

## Section C — Test-Day Tips

- **Time-box each question.** Don't let one section eat the other's time — if Standard is dragging, bank partial credit and move to REST API, then come back if time allows.
- **Handle edge cases explicitly** in both sections — empty input, no matches found, single-page vs multi-page responses.
- **Run visible test cases before submitting.** A passed visible case doesn't guarantee hidden ones pass, but a failed visible case is a free, fast signal something's wrong.
- Write clean, readable code — meaningful names, no dead code. IBM's grading rubric reportedly weighs this alongside correctness, not just pass/fail on test cases.

---

## Appendix — MCQ Backup (optional, lower priority given the confirmed 2-section structure)

<details>
<summary><strong>Python Core Quick Hits</strong></summary>

- `is` = identity, `==` = value equality.
- Mutable: `list`, `dict`, `set`. Immutable: `int`, `str`, `tuple`. Watch for mutable default arguments (`def f(x=[])`).
- `copy.copy()` = shallow (nested refs shared); `copy.deepcopy()` = fully independent.
- Generators (`yield`) are lazy and stateful; every generator is an iterator, not vice versa.
- `@staticmethod` (no self/cls) vs `@classmethod` (gets cls, common for alt constructors) vs `@property` (attribute-style access).

</details>

<details>
<summary><strong>Complexity Quick Table</strong></summary>

| Operation | list | dict | set |
|---|---|---|---|
| Access | O(1) | O(1) avg | — |
| Search (`in`) | O(n) | O(1) avg | O(1) avg |
| Insert/append | O(1) amortized | O(1) avg | O(1) avg |
| Delete | O(n) | O(1) avg | O(1) avg |

</details>

---

Good luck tonight — the Standard section leans on the same arrays/hashmap muscle memory you've already built from Martify and interview prep, and the REST API section is really just `requests` + careful JSON parsing wrapped in the shape of a coding challenge.
