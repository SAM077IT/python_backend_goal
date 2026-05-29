# 🗄️ SQL Interview Prep
### Cognizant Python Developer | 3+ Years Experience

---

## ✅ SQL Topic Checklist

- [ ] DDL, DML, DCL, TCL commands
- [ ] All JOIN types with examples
- [ ] Aggregate functions + GROUP BY + HAVING
- [ ] Subqueries (nested & correlated)
- [ ] Window Functions (ROW_NUMBER, RANK, LAG, LEAD)
- [ ] CTEs (Common Table Expressions)
- [ ] Indexes — types and when to use
- [ ] Normalization (1NF, 2NF, 3NF)
- [ ] SQL vs NoSQL
- [ ] Query Optimisation basics
- [ ] Classic problems (2nd highest salary, etc.)

---

## 1. 🏗️ SQL Command Categories

| Category | Commands | Purpose |
|----------|----------|---------|
| **DDL** — Data Definition | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | Structure |
| **DML** — Data Manipulation | `SELECT`, `INSERT`, `UPDATE`, `DELETE` | Data |
| **DCL** — Data Control | `GRANT`, `REVOKE` | Permissions |
| **TCL** — Transaction Control | `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Transactions |

---

## 2. 🔗 JOINs — Must Know All Types

### Sample Tables Used Throughout

```sql
-- employees table
| emp_id | name    | dept_id | salary |
|--------|---------|---------|--------|
| 1      | Alice   | 10      | 60000  |
| 2      | Bob     | 20      | 75000  |
| 3      | Charlie | 10      | 80000  |
| 4      | Diana   | 30      | 55000  |
| 5      | Eve     | NULL    | 70000  |

-- departments table
| dept_id | dept_name   |
|---------|-------------|
| 10      | Engineering |
| 20      | Marketing   |
| 40      | Finance     |
```

### JOIN Types with Results

```sql
-- INNER JOIN — only matching rows from both tables
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
-- Returns: Alice-Engineering, Bob-Marketing, Charlie-Engineering

-- LEFT JOIN — all from left + matches from right (NULL if no match)
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;
-- Returns: All 5 employees. Diana→Finance dept, Eve→NULL, Diana has dept 30 (no dept)

-- RIGHT JOIN — all from right + matches from left
SELECT e.name, d.dept_name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.dept_id;
-- Returns: All departments. Finance (id 40) has NULL employee

-- FULL OUTER JOIN — all rows from both, NULL where no match
SELECT e.name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.dept_id;
-- Returns: All combinations, NULLs where no match

-- CROSS JOIN — Cartesian product (every row × every row)
SELECT e.name, d.dept_name
FROM employees e
CROSS JOIN departments d;
-- Returns: 5 × 4 = 20 rows
```

### Anti-Join — Rows in A NOT in B

```sql
-- Employees with NO department
SELECT e.name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_id IS NULL;

-- Same using NOT EXISTS (often faster)
SELECT e.name
FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM departments d WHERE d.dept_id = e.dept_id
);
```

---

## 3. 📊 Aggregate Functions + GROUP BY + HAVING

```sql
-- Basic aggregations
SELECT
    dept_id,
    COUNT(*)          AS employee_count,
    AVG(salary)       AS avg_salary,
    MAX(salary)       AS max_salary,
    MIN(salary)       AS min_salary,
    SUM(salary)       AS total_salary
FROM employees
GROUP BY dept_id;

-- HAVING — filter after grouping (WHERE filters before grouping)
SELECT dept_id, AVG(salary) AS avg_sal
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 65000;

-- ORDER OF CLAUSES (must know):
-- SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
```

> **⚠️ Common mistake:** Using WHERE to filter aggregates. Always use HAVING for aggregate conditions.

---

## 4. 🏆 Classic Problem: Employees Earning Above Dept Average
*(Asked at Cognizant!)*

```sql
-- Using a subquery (correlated)
SELECT e.name, e.salary, e.dept_id
FROM employees e
WHERE e.salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE dept_id = e.dept_id
);

-- Using window functions (more efficient)
SELECT name, salary, dept_id
FROM (
    SELECT
        name,
        salary,
        dept_id,
        AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
    FROM employees
) sub
WHERE salary > dept_avg;
```

---

## 5. 🪟 Window Functions — High Priority

Window functions perform calculations **across related rows** WITHOUT collapsing them like GROUP BY.

```sql
-- Syntax
function_name() OVER (
    PARTITION BY column    -- Group rows (optional)
    ORDER BY column        -- Order within partition
    ROWS BETWEEN ... AND ...  -- Frame (optional)
)
```

### ROW_NUMBER, RANK, DENSE_RANK

```sql
SELECT
    name,
    dept_id,
    salary,
    ROW_NUMBER()   OVER (PARTITION BY dept_id ORDER BY salary DESC) AS row_num,
    RANK()         OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rank,
    DENSE_RANK()   OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dense_rank
FROM employees;

-- If salaries are 80000, 80000, 60000:
-- ROW_NUMBER:  1, 2, 3   (always unique)
-- RANK:        1, 1, 3   (skips 2)
-- DENSE_RANK:  1, 1, 2   (no skipping)
```

### LAG and LEAD — Access Adjacent Rows

```sql
SELECT
    name,
    salary,
    LAG(salary, 1, 0) OVER (ORDER BY salary) AS prev_salary,
    LEAD(salary, 1, 0) OVER (ORDER BY salary) AS next_salary,
    salary - LAG(salary) OVER (ORDER BY salary) AS salary_diff
FROM employees;
-- Great for trend analysis, month-over-month comparisons
```

### Running Total

```sql
SELECT
    name,
    salary,
    SUM(salary) OVER (ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    AS running_total
FROM employees;
```

---

## 6. 📝 CTEs — Common Table Expressions

CTEs make complex queries readable and reusable. Think of them as **temporary named result sets**.

```sql
-- Basic CTE
WITH dept_stats AS (
    SELECT
        dept_id,
        AVG(salary) AS avg_salary,
        COUNT(*) AS emp_count
    FROM employees
    GROUP BY dept_id
)
SELECT e.name, e.salary, d.avg_salary
FROM employees e
JOIN dept_stats d ON e.dept_id = d.dept_id
WHERE e.salary > d.avg_salary;

-- Multiple CTEs
WITH
high_earners AS (
    SELECT * FROM employees WHERE salary > 70000
),
dept_info AS (
    SELECT dept_id, dept_name FROM departments
)
SELECT h.name, h.salary, d.dept_name
FROM high_earners h
JOIN dept_info d ON h.dept_id = d.dept_id;
```

### Recursive CTE — Hierarchical Data

```sql
-- Org chart: employees with manager references
WITH RECURSIVE org_chart AS (
    -- Base case: top-level manager
    SELECT emp_id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: employees with managers
    SELECT e.emp_id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    INNER JOIN org_chart oc ON e.manager_id = oc.emp_id
)
SELECT * FROM org_chart ORDER BY level;
```

---

## 7. 🥈 Classic: Nth Highest Salary

```sql
-- 2nd highest salary using subquery
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Nth highest using DENSE_RANK (n = 2)
SELECT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 2;

-- Using OFFSET-LIMIT (MySQL/PostgreSQL)
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;   -- 0-indexed: OFFSET 1 = 2nd highest
```

---

## 8. 🔧 Subqueries

```sql
-- Nested subquery (runs once)
SELECT name FROM employees
WHERE dept_id = (SELECT dept_id FROM departments WHERE dept_name = 'Engineering');

-- Correlated subquery (runs for each row — slower but powerful)
SELECT name, salary
FROM employees e1
WHERE salary > (
    SELECT AVG(salary) FROM employees e2
    WHERE e2.dept_id = e1.dept_id
);

-- Subquery in FROM (inline view / derived table)
SELECT dept_id, AVG(salary)
FROM (SELECT * FROM employees WHERE salary > 50000) AS filtered
GROUP BY dept_id;

-- EXISTS vs IN
-- EXISTS stops at first match — often faster for large datasets
SELECT name FROM employees e
WHERE EXISTS (
    SELECT 1 FROM departments d WHERE d.dept_id = e.dept_id
);
```

---

## 9. 📚 Indexes

```sql
-- Create index
CREATE INDEX idx_salary ON employees(salary);

-- Composite index
CREATE INDEX idx_dept_salary ON employees(dept_id, salary);

-- Unique index
CREATE UNIQUE INDEX idx_unique_email ON users(email);
```

| Index Type | When to Use |
|-----------|-------------|
| **B-Tree** (default) | Range queries, equality checks, ORDER BY |
| **Hash** | Equality-only checks |
| **Composite** | Queries filtering on multiple columns |
| **Unique** | Enforce uniqueness + speed up lookups |

> **Index tips:**
> - Index columns used in WHERE, JOIN, ORDER BY
> - Avoid indexing columns with low cardinality (e.g., boolean columns)
> - Indexes speed up reads but slow down writes

---

## 10. 🗃️ Normalization

| Form | Rule | Eliminates |
|------|------|-----------|
| **1NF** | Atomic values, no repeating groups | Multivalued cells |
| **2NF** | 1NF + no partial dependency | Dependency on part of composite key |
| **3NF** | 2NF + no transitive dependency | Column depending on non-key column |

```
Example:
- Table: (StudentID, CourseID, CourseName, InstructorName)
- 1NF ✅ — atomic values
- Violates 2NF ❌ — CourseName depends only on CourseID (partial dependency)
- Fix: Split into Students, Courses, Enrollment tables
```

---

## 11. ⚡ SQL vs NoSQL

| Factor | SQL (Relational) | NoSQL |
|--------|-----------------|-------|
| **Structure** | Fixed schema, tables | Flexible schema |
| **Scaling** | Vertical | Horizontal |
| **Transactions** | ACID compliant | Eventually consistent (BASE) |
| **Best for** | Complex queries, relationships | Large-scale, unstructured data |
| **Examples** | MySQL, PostgreSQL, SQL Server | MongoDB, Cassandra, Redis |

> **When to choose NoSQL:**
> - Huge volumes of rapidly changing, unstructured data
> - Need horizontal scaling across many servers
> - Simple queries without complex JOINs

---

## 12. 🔍 Query Optimisation Tips

```sql
-- ❌ Avoid SELECT * — fetches unnecessary columns
SELECT * FROM employees;

-- ✅ Select only needed columns
SELECT name, salary FROM employees;

-- ❌ Avoid functions on indexed columns in WHERE
SELECT * FROM employees WHERE YEAR(created_at) = 2024;

-- ✅ Use range comparison instead
SELECT * FROM employees WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- ❌ Avoid correlated subqueries when window functions can be used
-- ✅ Use CTEs for readability in complex queries
-- ✅ Use EXPLAIN / EXPLAIN ANALYZE to review the query execution plan
```

---

## 13. 🎤 Common Interview Q&A

### Q: Difference between DELETE, TRUNCATE, and DROP?

| Command | Removes | Rollback? | WHERE clause? | Auto-increment reset? |
|---------|---------|-----------|---------------|----------------------|
| `DELETE` | Rows | ✅ Yes | ✅ Yes | ❌ No |
| `TRUNCATE` | All rows | ❌ Usually No | ❌ No | ✅ Yes |
| `DROP` | Entire table | ❌ No | ❌ No | ✅ Yes (table gone) |

### Q: UNION vs UNION ALL?
```sql
-- UNION — removes duplicates (slower)
SELECT name FROM employees_2023
UNION
SELECT name FROM employees_2024;

-- UNION ALL — keeps duplicates (faster)
SELECT name FROM employees_2023
UNION ALL
SELECT name FROM employees_2024;
```

### Q: Primary Key vs Unique Key?
- **Primary Key:** Uniquely identifies each row. NOT NULL. Only one per table.
- **Unique Key:** Ensures uniqueness. Can have NULL. Multiple per table.

### Q: WHERE vs HAVING?
```sql
-- WHERE: filter rows BEFORE grouping
SELECT dept_id, COUNT(*) FROM employees WHERE salary > 50000 GROUP BY dept_id;

-- HAVING: filter groups AFTER aggregation
SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id HAVING COUNT(*) > 2;
```

---

## 14. 🧪 Practice Queries

```sql
-- 1. Find employees in Engineering department with salary > 60000
SELECT e.name, e.salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_name = 'Engineering' AND e.salary > 60000;

-- 2. List department with highest average salary
SELECT dept_id, AVG(salary) AS avg_sal
FROM employees
GROUP BY dept_id
ORDER BY avg_sal DESC
LIMIT 1;

-- 3. Find employees who joined in same month as another employee
SELECT DISTINCT e1.name
FROM employees e1
JOIN employees e2
  ON e1.emp_id <> e2.emp_id
  AND MONTH(e1.join_date) = MONTH(e2.join_date);

-- 4. Running total of salaries ordered by salary
SELECT name, salary,
  SUM(salary) OVER (ORDER BY salary) AS running_total
FROM employees;

-- 5. Rank employees within each department by salary
SELECT name, dept_id, salary,
  RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank
FROM employees;
```

---

*Next: HR & Behavioural Prep → `05_hr_and_behavioral.md`*
