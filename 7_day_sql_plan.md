# 🗄️ 7-Day SQL Learning Plan

> **Goal:** Go from zero to confident in SQL — one concept per day.  
> **Time required:** 2–4 hours/day | **Tool:** [SQLiteOnline.com](https://sqliteonline.com) *(free, no install)*  
> **Sample dataset:** [Chinook DB](https://github.com/lerocha/chinook-database) or [Northwind DB](https://github.com/jpwhite3/northwind-SQLite3)

---

## 📊 Progress Tracker

| Day | Theme | Status |
|-----|-------|--------|
| Day 1 | Foundation — First queries | `[ ] Not started` |
| Day 2 | Filtering & Logic | `[ ] Not started` |
| Day 3 | Aggregations & Grouping | `[ ] Not started` |
| Day 4 | JOINs — Connecting tables | `[ ] Not started` |
| Day 5 | Subqueries & CTEs | `[ ] Not started` |
| Day 6 | Window Functions & Advanced SQL | `[ ] Not started` |
| Day 7 | Real Project & Best Practices | `[ ] Not started` |

> ✏️ **How to use:** Replace `[ ]` with `[x]` as you complete each day's tasks.

---

## 📅 Day 1 — What is SQL? Setup & First Queries

**Level:** Beginner | **Time:** 2–3 hours | **Theme:** Foundation

### Concepts to learn

- [ ] What is a relational database? (tables, rows, columns, relationships)
- [ ] Setting up your environment (SQLiteOnline.com or DB Browser for SQLite)
- [ ] `SELECT` and `FROM` — fetching all data from a table
- [ ] `WHERE` clause — filtering rows by condition
- [ ] `ORDER BY` — sorting results ascending/descending
- [ ] `LIMIT` — restricting the number of rows returned

### Key SQL to practice

```sql
-- Select all columns from a table
SELECT * FROM employees;

-- Select specific columns
SELECT first_name, last_name, salary FROM employees;

-- Filter with WHERE
SELECT * FROM employees WHERE department = 'Sales';

-- Sort results
SELECT * FROM employees ORDER BY salary DESC;

-- Limit output
SELECT * FROM employees ORDER BY salary DESC LIMIT 10;

-- Combine all three
SELECT first_name, salary
FROM employees
WHERE department = 'Engineering'
ORDER BY salary DESC
LIMIT 5;
```

### 💡 Tip
> Don't just read — type every query yourself. Muscle memory matters in SQL.

### Resources
- [SQLBolt — Lessons 1–4](https://sqlbolt.com)
- [Mode SQL Tutorial — Basics](https://mode.com/sql-tutorial/)
- [W3Schools SQL — SELECT](https://www.w3schools.com/sql/sql_select.asp)

---

## 📅 Day 2 — Filtering, Logic & Data Types

**Level:** Beginner | **Time:** 2–3 hours | **Theme:** Filtering

### Concepts to learn

- [ ] `AND`, `OR`, `NOT` — combining multiple conditions
- [ ] `LIKE` and wildcards (`%`, `_`) — pattern matching
- [ ] `IN` — match against a list of values
- [ ] `BETWEEN` — filter within a range (numbers, dates)
- [ ] `IS NULL` / `IS NOT NULL` — handling missing data
- [ ] Data types overview: `INT`, `VARCHAR`, `DATE`, `FLOAT`, `BOOLEAN`

### Key SQL to practice

```sql
-- AND, OR, NOT
SELECT * FROM orders
WHERE status = 'Shipped' AND total > 100;

SELECT * FROM customers
WHERE country = 'USA' OR country = 'Canada';

-- LIKE (% = any number of chars, _ = one char)
SELECT * FROM customers WHERE name LIKE 'A%';       -- starts with A
SELECT * FROM customers WHERE email LIKE '%@gmail%'; -- contains @gmail
SELECT * FROM products WHERE code LIKE 'AB_123';    -- exact pattern

-- IN
SELECT * FROM employees WHERE department IN ('Sales', 'Marketing', 'HR');

-- BETWEEN (inclusive on both ends)
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';
SELECT * FROM products WHERE price BETWEEN 10 AND 50;

-- NULL handling
SELECT * FROM employees WHERE manager_id IS NULL;     -- no manager (CEO!)
SELECT * FROM employees WHERE phone IS NOT NULL;      -- has a phone number
```

### 💡 Tip
> Practice on a real dataset. Download the Chinook or Northwind database — both are free with good variety of columns and data types.

### Resources
- [SQLBolt — Lessons 5–7](https://sqlbolt.com/lesson/select_queries_with_constraints)
- [W3Schools SQL — WHERE & LIKE](https://www.w3schools.com/sql/sql_where.asp)
- [Chinook Database (download)](https://github.com/lerocha/chinook-database)

---

## 📅 Day 3 — Aggregations & Grouping

**Level:** Intermediate | **Time:** 3 hours | **Theme:** Aggregations

### Concepts to learn

- [ ] Aggregate functions: `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()`
- [ ] `GROUP BY` — grouping rows to summarize by category
- [ ] `HAVING` — filtering after grouping (like `WHERE` but for groups)
- [ ] `DISTINCT` — removing duplicate values
- [ ] Combining `GROUP BY` with `ORDER BY`

### Key SQL to practice

```sql
-- Aggregate functions
SELECT COUNT(*) FROM orders;                      -- total number of orders
SELECT COUNT(DISTINCT customer_id) FROM orders;   -- unique customers
SELECT SUM(total) FROM orders;                    -- total revenue
SELECT AVG(total) FROM orders;                    -- average order value
SELECT MIN(price), MAX(price) FROM products;      -- price range

-- GROUP BY — sales by department
SELECT department, COUNT(*) AS employee_count, AVG(salary) AS avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;

-- HAVING — only show departments with more than 5 employees
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 5
ORDER BY employee_count DESC;

-- DISTINCT
SELECT DISTINCT country FROM customers;
```

### 🧠 Key concept to memorize
```
WHERE  → filters rows BEFORE grouping
HAVING → filters groups AFTER aggregation
```

### Mini-project: answer these 5 questions on your sample DB
1. How many customers are in each country?
2. What is the total revenue per product category?
3. Which month had the highest number of orders?
4. What is the average order value per customer?
5. Which customers have placed more than 3 orders?

### 💡 Tip
> `WHERE` filters rows before grouping; `HAVING` filters groups after. Write this on a sticky note.

### Resources
- [SQLBolt — Lessons 10–12](https://sqlbolt.com/lesson/select_queries_with_aggregates)
- [Mode SQL — Aggregations](https://mode.com/sql-tutorial/sql-aggregate-functions/)
- [pgexercises.com — Aggregations](https://pgexercises.com/questions/aggregates/)

---

## 📅 Day 4 — JOINs: Connecting Tables

**Level:** Intermediate | **Time:** 3–4 hours | **Theme:** JOINs

### Concepts to learn

- [ ] Why JOINs exist (primary keys, foreign keys, relationships)
- [ ] `INNER JOIN` — rows matching in BOTH tables
- [ ] `LEFT JOIN` — all rows from left + matches from right (NULL if no match)
- [ ] `RIGHT JOIN` — mirror of LEFT JOIN
- [ ] `FULL OUTER JOIN` — everything from both tables
- [ ] Joining 3+ tables in a single query

### Visual reference

```
Table A     Table B
  ┌───┐       ┌───┐
  │   │       │   │
  │ ■─┼───────┼─■ │  ← INNER JOIN (only overlap)
  │   │       │   │
  └───┘       └───┘

LEFT JOIN  = All of A + matching B (NULLs where no match)
RIGHT JOIN = All of B + matching A (NULLs where no match)
FULL JOIN  = Everything from both
```

### Key SQL to practice

```sql
-- INNER JOIN — only customers who have placed orders
SELECT c.name, o.order_date, o.total
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

-- LEFT JOIN — all customers, even those with no orders
SELECT c.name, o.order_date, o.total
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- Find customers who have NEVER placed an order
SELECT c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Multi-table JOIN — customers, orders, and products
SELECT c.name, o.order_date, p.product_name, oi.quantity
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id;
```

### 💡 Tip
> Draw the tables on paper and trace which rows match before writing code. Venn diagrams are your best friend here.

### Resources
- [SQLBolt — Lesson 6 (JOINs)](https://sqlbolt.com/lesson/select_queries_with_joins)
- [Visual JOIN explainer (Coding Horror)](https://blog.codinghorror.com/a-visual-explanation-of-sql-joins/)
- [pgexercises.com — Joins](https://pgexercises.com/questions/joins/)

---

## 📅 Day 5 — Subqueries & CTEs

**Level:** Intermediate | **Time:** 3 hours | **Theme:** Subqueries

### Concepts to learn

- [ ] Subquery in `WHERE` — filter using a nested query result
- [ ] Subquery in `FROM` — use a query as a derived table
- [ ] Subquery in `SELECT` — scalar subqueries
- [ ] `WITH` (CTE) — Common Table Expressions for cleaner code
- [ ] Correlated subqueries — subqueries that reference the outer query
- [ ] `EXISTS` vs `IN` — when to use each

### Key SQL to practice

```sql
-- Subquery in WHERE — find customers who have ordered more than the average
SELECT name FROM customers
WHERE customer_id IN (
  SELECT customer_id FROM orders
  WHERE total > (SELECT AVG(total) FROM orders)
);

-- Subquery in FROM (derived table)
SELECT dept_name, avg_salary
FROM (
  SELECT department AS dept_name, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department
) AS dept_summary
WHERE avg_salary > 60000;

-- CTE — same as above but much cleaner
WITH dept_summary AS (
  SELECT department, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY department
)
SELECT department, avg_salary
FROM dept_summary
WHERE avg_salary > 60000;

-- Multiple CTEs chained together
WITH
  high_value_orders AS (
    SELECT customer_id, SUM(total) AS lifetime_value
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total) > 1000
  ),
  customer_details AS (
    SELECT c.name, c.email, hvo.lifetime_value
    FROM customers c
    INNER JOIN high_value_orders hvo ON c.customer_id = hvo.customer_id
  )
SELECT * FROM customer_details ORDER BY lifetime_value DESC;

-- EXISTS (often faster than IN for large datasets)
SELECT name FROM customers c
WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
);
```

### 💡 Tip
> CTEs are just named subqueries that sit at the top. Always prefer CTEs over deeply nested subqueries for readability.

### Resources
- [Mode SQL — Subqueries](https://mode.com/sql-tutorial/sql-sub-queries/)
- [StrataScratch — Practice problems](https://platform.stratascratch.com/coding?code_type=1)
- [SQLBolt — Advanced](https://sqlbolt.com/lesson/select_queries_with_expressions)

---

## 📅 Day 6 — Window Functions & Advanced SQL

**Level:** Advanced | **Time:** 3–4 hours | **Theme:** Advanced

### Concepts to learn

- [ ] `OVER()` clause — the foundation of all window functions
- [ ] `PARTITION BY` — like GROUP BY but without collapsing rows
- [ ] `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` — ranking rows
- [ ] `LAG()` and `LEAD()` — compare current row to previous/next
- [ ] Running totals with `SUM() OVER(ORDER BY ...)`
- [ ] `CASE WHEN` — if/else logic inside SQL

### Key SQL to practice

```sql
-- ROW_NUMBER — unique rank per partition
SELECT
  employee_id,
  department,
  salary,
  ROW_NUMBER() OVER(PARTITION BY department ORDER BY salary DESC) AS rank_in_dept
FROM employees;

-- RANK vs DENSE_RANK (difference: how ties are handled)
-- RANK:       1, 2, 2, 4  (skips 3)
-- DENSE_RANK: 1, 2, 2, 3  (no gap)
SELECT
  name, salary,
  RANK()       OVER(ORDER BY salary DESC) AS rank,
  DENSE_RANK() OVER(ORDER BY salary DESC) AS dense_rank
FROM employees;

-- Running total (cumulative sum)
SELECT
  order_date,
  total,
  SUM(total) OVER(ORDER BY order_date) AS running_revenue
FROM orders;

-- LAG — compare to previous row (month-over-month growth)
SELECT
  month,
  revenue,
  LAG(revenue, 1) OVER(ORDER BY month) AS prev_month_revenue,
  revenue - LAG(revenue, 1) OVER(ORDER BY month) AS growth
FROM monthly_revenue;

-- Top N per group (e.g., top 3 earners per department)
SELECT * FROM (
  SELECT
    name, department, salary,
    ROW_NUMBER() OVER(PARTITION BY department ORDER BY salary DESC) AS rn
  FROM employees
) ranked
WHERE rn <= 3;

-- CASE WHEN — conditional columns
SELECT
  name,
  salary,
  CASE
    WHEN salary >= 100000 THEN 'Senior'
    WHEN salary >= 60000  THEN 'Mid-level'
    ELSE                       'Junior'
  END AS level
FROM employees;
```

### 💡 Tip
> Window functions are the #1 skill that separates beginner from intermediate SQL analysts. They're worth every extra hour you spend on them.

### Resources
- [Mode SQL — Window Functions](https://mode.com/sql-tutorial/sql-window-functions/)
- [StrataScratch — Medium/Hard problems](https://platform.stratascratch.com)
- [LeetCode SQL — Medium difficulty](https://leetcode.com/problemset/database/)

---

## 📅 Day 7 — Real Project & Best Practices

**Level:** Practical | **Time:** 4 hours | **Theme:** Capstone

### Concepts to learn

- [ ] `INSERT INTO` — add new rows to a table
- [ ] `UPDATE ... SET` — modify existing rows
- [ ] `DELETE FROM` — remove rows safely
- [ ] `CREATE TABLE` — define a schema with data types and constraints
- [ ] Query optimization basics (indexes, avoid `SELECT *`, filter early)
- [ ] SQL formatting and style guide

### Key SQL to practice

```sql
-- INSERT
INSERT INTO customers (name, email, country)
VALUES ('Jane Doe', 'jane@example.com', 'USA');

-- INSERT multiple rows
INSERT INTO products (name, price, category)
VALUES
  ('Widget A', 9.99, 'Electronics'),
  ('Widget B', 14.99, 'Electronics'),
  ('Gadget C', 4.99, 'Accessories');

-- UPDATE (always use WHERE to avoid updating every row!)
UPDATE employees
SET salary = salary * 1.10
WHERE department = 'Engineering' AND performance_rating = 'Excellent';

-- DELETE (always test with SELECT first!)
-- Step 1: Test
SELECT * FROM orders WHERE order_date < '2020-01-01';
-- Step 2: Delete once you're sure
DELETE FROM orders WHERE order_date < '2020-01-01';

-- CREATE TABLE
CREATE TABLE projects (
  project_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name         VARCHAR(100) NOT NULL,
  start_date   DATE,
  budget       DECIMAL(10, 2),
  manager_id   INTEGER REFERENCES employees(employee_id)
);
```

### ✅ SQL best practices

```sql
-- ✅ DO: Name columns explicitly
SELECT customer_id, name, email FROM customers;

-- ❌ DON'T: SELECT * in production queries
SELECT * FROM customers;  -- slow, fragile, unclear

-- ✅ DO: Filter early, let the DB do the work
SELECT * FROM orders WHERE status = 'Active' AND total > 500;

-- ✅ DO: Use CTEs for readability over nested subqueries
WITH active_users AS ( ... )
SELECT * FROM active_users;

-- ✅ DO: Use consistent formatting
SELECT
    c.customer_id,
    c.name,
    COUNT(o.order_id)  AS order_count,
    SUM(o.total)       AS lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY lifetime_value DESC;
```

### 🏆 Capstone project instructions

Pick **one** free dataset and answer all 10 questions using SQL only.

**Recommended datasets:**
- [Maven Analytics — Free Datasets](https://www.mavenanalytics.io/data-playground)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Mode Public Warehouse](https://mode.com/sql-tutorial/sql-in-mode/)

**10 questions to answer (adapt to your dataset):**
1. How many total records are in the dataset?
2. What are the top 10 values by your primary metric?
3. What is the breakdown by category/group?
4. Which groups have above-average performance?
5. What is the month-over-month or year-over-year trend?
6. Are there any records with missing values? Which columns?
7. Who are the top 5 performers within each category?
8. What is the running cumulative total over time?
9. What percentage of total does each category represent?
10. Find a meaningful insight that surprises you — and explain it.

### 💡 Tip
> Upload your queries and findings to GitHub. It's your first SQL portfolio piece — employers love seeing real applied work.

### Resources
- [sqlstyle.guide — SQL formatting](https://www.sqlstyle.guide)
- [Use The Index, Luke — SQL performance](https://use-the-index-luke.com)
- [LeetCode SQL problems](https://leetcode.com/problemset/database/)
- [StrataScratch — Interview prep](https://platform.stratascratch.com)

---

## 📚 Complete Resource List

### Free practice platforms
| Platform | Best for |
|----------|----------|
| [SQLBolt](https://sqlbolt.com) | Interactive beginner lessons |
| [pgexercises.com](https://pgexercises.com) | Structured exercises by topic |
| [StrataScratch](https://platform.stratascratch.com) | Real interview questions |
| [LeetCode SQL](https://leetcode.com/problemset/database/) | Interview prep (Easy → Hard) |
| [Mode SQL Tutorial](https://mode.com/sql-tutorial/) | Analytics-focused SQL |
| [SQLiteOnline.com](https://sqliteonline.com) | Browser-based SQL sandbox |

### Sample databases
| Database | Description | Download |
|----------|-------------|----------|
| Chinook | Music store (artists, albums, invoices) | [GitHub](https://github.com/lerocha/chinook-database) |
| Northwind | Retail orders & suppliers | [GitHub](https://github.com/jpwhite3/northwind-SQLite3) |
| Sakila | DVD rental store | [MySQL docs](https://dev.mysql.com/doc/sakila/en/) |

### Reference docs
- [W3Schools SQL Reference](https://www.w3schools.com/sql/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQL Style Guide](https://www.sqlstyle.guide)

---

## 🗺️ What comes next (after day 7)

Once you've finished this plan, here's where to go next:

- [ ] **Intermediate:** Window functions mastery, query optimization, indexes
- [ ] **Database design:** Normalization, ER diagrams, schema design
- [ ] **Advanced SQL:** Recursive CTEs, pivoting, JSON in SQL
- [ ] **Pick a dialect:** PostgreSQL (most versatile), MySQL (most common), BigQuery (data analytics)
- [ ] **Connect to real tools:** Connect SQL to Python (pandas + SQLAlchemy), Tableau, Power BI, or Metabase
- [ ] **Interview prep:** Do 30 LeetCode SQL problems (10 Easy, 10 Medium, 10 Hard)

---

*Generated with Claude · [sqlstyle.guide](https://www.sqlstyle.guide) · Happy querying! 🎉*
