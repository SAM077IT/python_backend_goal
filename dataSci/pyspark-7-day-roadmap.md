# PySpark 7-Day Roadmap (21 Jun → 27 Jun)

> Built on top of your existing numpy/pandas knowledge. The fastest way to learn PySpark when you already know pandas is to constantly map "how would I do this in pandas?" → "how do I do this in PySpark?" — that mapping is woven into every day below.

**Target:** Comfortable enough to read/write PySpark ETL code, explain Spark architecture, and answer interview-level questions by Jun 27.

**Daily time budget:** ~2–3 hrs (1 hr theory/docs, 1–1.5 hr hands-on code).

---

## Week at a Glance

| Day | Date | Focus | Output |
|---|---|---|---|
| 1 | Jun 21 (Sat) | Spark architecture + environment setup | Working local PySpark shell |
| 2 | Jun 22 (Sun) | DataFrame API basics (pandas → PySpark) | Cheat sheet + practice notebook |
| 3 | Jun 23 (Mon) | GroupBy, Joins, Window functions | Aggregation + join exercises |
| 4 | Jun 24 (Tue) | Spark SQL + UDFs | Hybrid SQL/DataFrame queries |
| 5 | Jun 25 (Wed) | Performance: partitions, caching, broadcast joins | Explain-plan reading |
| 6 | Jun 26 (Thu) | Mini ETL project (e-commerce data, Martify-style) | End-to-end pipeline script |
| 7 | Jun 27 (Fri) | Revision + interview prep | Cheat sheet + Q&A drill |

---

## Day 1 (Jun 21) — Architecture & Setup

### Why this matters
PySpark interview questions almost always start with "explain Spark's architecture" — driver, executors, cluster manager, lazy evaluation. Get this right before touching code.

### Topics
- Spark architecture: Driver, Executors, Cluster Manager, Tasks/Stages/Jobs
- RDD vs DataFrame vs Dataset (Python only has RDD + DataFrame)
- **Lazy evaluation** — transformations vs actions (this trips up everyone coming from pandas, where every line executes immediately)
- SparkSession (the entry point — replaces `SparkContext` + `SQLContext` from old Spark)

### Docs to read
- [Spark Overview](https://spark.apache.org/docs/latest/) — skim the cluster mode overview section
- [PySpark Getting Started](https://spark.apache.org/docs/latest/api/python/getting_started/index.html)
- [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html) — read the "Overview" + "RDD Operations" sections only, don't go deep into RDDs (DataFrames are what you'll actually use)

### Setup (pick ONE)
<details>
<summary><b>Option A: Local install (recommended — fastest to start coding)</b></summary>

```bash
# Java is required (Spark runs on the JVM)
java -version   # need Java 11 or 17

pip install pyspark --break-system-packages
```

Test it:
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Day1Test") \
    .master("local[*]") \
    .getOrCreate()

print(spark.version)
df = spark.createDataFrame([(1, "a"), (2, "b")], ["id", "val"])
df.show()
spark.stop()
```
</details>

<details>
<summary><b>Option B: Databricks Community Edition (free, zero install, closest to real-world job setup)</b></summary>

[Sign up here](https://community.cloud.databricks.com/) — free tier gives you a notebook + a small cluster. Good if you want to skip local Java/env headaches and just write code. Most companies hiring for "PySpark" run on Databricks, so this also gets you UI familiarity.
</details>

<details>
<summary><b>Option C: Google Colab</b></summary>

```python
!pip install pyspark
```
Works fine for single-day exercises, no persistence between sessions though.
</details>

### Hands-on
1. Get `spark.version` printed in your environment of choice.
2. Create a DataFrame from a Python list (like above) and call `.show()`, `.printSchema()`, `.count()`.
3. Read about lazy evaluation, then prove it to yourself:
```python
df2 = df.filter(df.id > 1)   # transformation — nothing happens yet
print("filter defined, no execution yet")
df2.show()                    # action — NOW it executes
```

---

## Day 2 (Jun 22) — DataFrame API (pandas → PySpark)

### Topics
- Reading data: CSV, JSON, Parquet
- Schema: inferred vs explicit (`StructType`)
- Core transformations: `select`, `filter`/`where`, `withColumn`, `drop`, `withColumnRenamed`, `distinct`, `orderBy`
- `.show()`, `.collect()`, `.toPandas()` — and why you almost never call `.collect()` on big data

### Docs to read
- [DataFrame API docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html)
- [pyspark.sql.functions reference](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html) — bookmark this, you'll use it constantly

### pandas → PySpark cheat sheet
<details>
<summary><b>Click to expand mapping table</b></summary>

| pandas | PySpark |
|---|---|
| `pd.read_csv("f.csv")` | `spark.read.csv("f.csv", header=True, inferSchema=True)` |
| `df.head()` | `df.show(5)` |
| `df.shape` | `(df.count(), len(df.columns))` |
| `df['col']` | `df['col']` or `df.col` (column object, not data — lazy) |
| `df[df.col > 5]` | `df.filter(df.col > 5)` or `df.where(df.col > 5)` |
| `df.col.unique()` | `df.select('col').distinct()` |
| `df['new'] = df.a + df.b` | `df.withColumn('new', df.a + df.b)` |
| `df.drop(columns=['c'])` | `df.drop('c')` |
| `df.rename(columns={'a':'b'})` | `df.withColumnRenamed('a', 'b')` |
| `df.sort_values('col')` | `df.orderBy('col')` |
| `df.dtypes` | `df.dtypes` or `df.printSchema()` |
| `df.isnull().sum()` | `df.filter(df.col.isNull()).count()` |
| `df.fillna(0)` | `df.fillna(0)` |
| `df.to_csv()` | `df.write.csv("path")` |

**Key mental shift:** pandas is *eager* (every line runs immediately, fits in one machine's RAM). PySpark is *lazy* (builds a plan, only executes on an action like `.show()`, `.count()`, `.collect()`, `.write()`) and is designed for data spread across a cluster.
</details>

### Hands-on
```python
df = spark.read.csv("sample.csv", header=True, inferSchema=True)
df.printSchema()
df.select("col1", "col2").show()
df.filter(df.col1 > 100).show()
df.withColumn("col3", df.col1 * 2).show()
```
Use any CSV you have lying around (even export one from Martify's product/order data) or grab a sample dataset from [Kaggle](https://www.kaggle.com/datasets) since you're already comfortable navigating it from your pandas learning.

---

## Day 3 (Jun 23) — GroupBy, Joins, Window Functions

### Topics
- `groupBy().agg()` with multiple aggregations
- Join types: `inner`, `left`, `right`, `outer`, `left_semi`, `left_anti`
- Window functions: `row_number`, `rank`, `dense_rank`, `lag`, `lead`, partitioned aggregates
- `pyspark.sql.Window` spec

### Docs to read
- [GroupedData docs](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/grouped_data.html)
- [Window functions guide](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/window.html)

### Code examples
<details>
<summary><b>GroupBy + agg</b></summary>

```python
from pyspark.sql import functions as F

df.groupBy("category").agg(
    F.count("*").alias("total_orders"),
    F.sum("amount").alias("total_revenue"),
    F.avg("amount").alias("avg_order_value")
).show()
```
</details>

<details>
<summary><b>Joins</b></summary>

```python
orders.join(customers, on="customer_id", how="inner").show()
orders.join(customers, orders.customer_id == customers.id, how="left").show()
```
</details>

<details>
<summary><b>Window functions</b></summary>

```python
from pyspark.sql import Window
from pyspark.sql import functions as F

w = Window.partitionBy("category").orderBy(F.desc("amount"))

df.withColumn("rank", F.rank().over(w)) \
  .withColumn("prev_amount", F.lag("amount").over(w)) \
  .show()
```
This is the PySpark equivalent of pandas `df.groupby('category')['amount'].rank()` — but far more flexible since you control partitioning and ordering explicitly.
</details>

### Hands-on
Build a small "top N per group" query — e.g., top 3 highest-value orders per category — using `rank()` + `filter()`. This exact pattern shows up constantly in interviews.

---

## Day 4 (Jun 24) — Spark SQL + UDFs

### Topics
- Registering a DataFrame as a temp view and querying with SQL
- When to use SQL vs DataFrame API (mostly style preference, SQL is often more readable for complex joins/aggregations)
- User-Defined Functions (UDFs) — and **why to avoid them when a built-in function exists** (UDFs break Spark's optimizations; this is a common interview gotcha)
- `pandas_udf` (vectorized UDFs) as the faster alternative when you need custom Python logic

### Docs to read
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [pyspark.sql.functions.udf](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.udf.html)
- [pandas UDFs](https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html)

### Code examples
<details>
<summary><b>Spark SQL</b></summary>

```python
df.createOrReplaceTempView("orders")

spark.sql("""
    SELECT category, COUNT(*) as total, SUM(amount) as revenue
    FROM orders
    WHERE amount > 100
    GROUP BY category
    ORDER BY revenue DESC
""").show()
```
</details>

<details>
<summary><b>UDF (and why to be careful with it)</b></summary>

```python
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf

def categorize(amount):
    return "high" if amount > 500 else "low"

categorize_udf = udf(categorize, StringType())
df.withColumn("tier", categorize_udf(df.amount)).show()

# Better when possible — built-in functions are optimized by Catalyst:
from pyspark.sql import functions as F
df.withColumn("tier", F.when(df.amount > 500, "high").otherwise("low")).show()
```
</details>

### Hands-on
Rewrite your Day 3 groupBy query as a SQL string instead, and confirm you get the same result both ways.

---

## Day 5 (Jun 25) — Performance Tuning

This is the day that separates "knows PySpark syntax" from "can be trusted with production data" — and it's a very common interview deep-dive topic for 3+ years experience level.

### Topics
- Partitions: `repartition()` vs `coalesce()` (and why `coalesce` is cheaper for reducing partitions)
- `.cache()` / `.persist()` — when caching helps vs wastes memory
- **Broadcast joins** — joining a small table against a huge one without a full shuffle
- Reading `.explain()` output (physical plan) at a basic level
- Shuffle operations and why they're expensive (`groupBy`, `join`, `distinct`, `orderBy` all trigger shuffles)

### Docs to read
- [Performance Tuning Guide](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
- [RDD Programming Guide — Performance section](https://spark.apache.org/docs/latest/rdd-programming-guide.html#rdd-persistence)

### Code examples
<details>
<summary><b>Broadcast join</b></summary>

```python
from pyspark.sql.functions import broadcast

large_df.join(broadcast(small_df), "id").show()
```
</details>

<details>
<summary><b>Partitions & caching</b></summary>

```python
df.rdd.getNumPartitions()
df2 = df.repartition(8)          # increases/redistributes partitions (full shuffle)
df3 = df.coalesce(2)             # reduces partitions (no full shuffle, cheaper)

df.cache()        # keep in memory across multiple actions
df.count()        # first action triggers caching
df.filter(...).show()   # reuses cached data, faster
```
</details>

<details>
<summary><b>Reading an explain plan</b></summary>

```python
df.groupBy("category").count().explain()
```
Look for `Exchange` in the plan output — that's a shuffle. Minimizing unnecessary `Exchange` steps is the core of Spark performance tuning.
</details>

### Hands-on
Take your Day 3 join query, run `.explain()` on it before and after wrapping the smaller side in `broadcast()`. Note the difference in the plan.

---

## Day 6 (Jun 26) — Mini ETL Project

### Goal
Build a small end-to-end pipeline, framed like a Martify-style e-commerce dataset (orders, customers, products) — since that's a context you already know well from your Django project.

### Project structure
<details>
<summary><b>Sample task spec</b></summary>

1. **Extract:** Read `orders.csv`, `customers.csv`, `products.csv` into DataFrames.
2. **Transform:**
   - Join orders → customers → products
   - Add a `order_month` column derived from a date column
   - Compute monthly revenue per category using `groupBy`
   - Flag top-5 customers by total spend using a window function
   - Clean nulls / dedupe
3. **Load:** Write the final aggregated result out as Parquet (and optionally a CSV summary):

```python
result.write.mode("overwrite").partitionBy("order_month").parquet("output/monthly_revenue")
```
</details>

### Why Parquet
Worth understanding *why* — columnar format, compressed, schema-preserving, and far faster to read back into Spark than CSV. This is a near-guaranteed interview question ("why would you use Parquet over CSV").

### Hands-on
Write this as a single `etl_pipeline.py` script you could run with `spark-submit etl_pipeline.py`. Treat it like a real deliverable — this is the kind of script you'd actually be asked to walk through in an interview.

---

## Day 7 (Jun 27) — Revision + Interview Prep

### Morning: Cheat sheet pass
<details>
<summary><b>Quick-fire concept review</b></summary>

- Spark architecture: Driver → Executors → Tasks, Cluster Manager (YARN/K8s/Standalone)
- Lazy evaluation: transformations build a DAG, actions trigger execution
- DataFrame vs RDD: DataFrames have schema + Catalyst optimizer, use them by default
- `repartition` (shuffle, more partitions) vs `coalesce` (no shuffle, fewer partitions)
- Broadcast join: avoids shuffle when one side is small
- `cache()`/`persist()`: avoid recomputation across multiple actions
- Avoid UDFs when a built-in `pyspark.sql.functions` equivalent exists
- Parquet > CSV for intermediate/output storage (columnar, compressed, schema-aware)
- Narrow vs wide transformations: narrow = no shuffle (`map`, `filter`), wide = shuffle (`groupBy`, `join`, `distinct`)
</details>

### Likely interview questions to rehearse out loud
<details>
<summary><b>Click to expand question list</b></summary>

1. Explain Spark's architecture in your own words.
2. What's the difference between `repartition()` and `coalesce()`?
3. What is lazy evaluation and why does Spark use it?
4. When would you use a broadcast join?
5. Why avoid UDFs? What's a `pandas_udf` and when would you reach for one anyway?
6. How would you debug a slow Spark job? (→ talk about `.explain()`, Spark UI, shuffle stages)
7. Difference between `cache()` and `persist()`?
8. How does PySpark handle schema — inferred vs explicit, and why explicit is safer in production?
9. Walk me through how you'd build an ETL pipeline reading from S3 and writing to a data warehouse.
10. Given your Django/PostgreSQL background — how would you decide whether a task needs Spark vs just pandas/PostgreSQL?
   - *Your honest answer:* Spark earns its complexity at data volumes that don't fit comfortably in memory on one machine, or when you need distributed/parallel processing across a cluster. For anything that fits in pandas comfortably, pandas is simpler and faster to iterate on.
</details>

### Afternoon: Timed practice
Pick 2–3 medium LeetCode/HackerRank-style data problems and solve them in PySpark instead of pandas, timing yourself. This is the fastest way to surface gaps before an actual interview.

---

## Bonus Resources
- [Spark by Examples — PySpark Tutorial](https://sparkbyexamples.com/pyspark-tutorial/) — good for quick syntax lookups
- [Databricks PySpark documentation](https://docs.databricks.com/en/pyspark/index.html) — useful since many job postings specifically say "Databricks experience"
- [Official PySpark API Reference](https://spark.apache.org/docs/latest/api/python/reference/index.html) — your source of truth when stuck

---

**Note:** If your week gets tight, the highest-leverage days to protect are **Day 2 (DataFrame basics)**, **Day 3 (joins/groupBy/window)**, and **Day 5 (performance)** — those three cover the bulk of both real usage and interview questions. Day 6 (project) and Day 1 (architecture) can compress if needed.
