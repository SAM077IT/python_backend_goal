# NumPy & pandas Interview Questions and Answers

## Table of Contents
1. NumPy Basics
2. NumPy Intermediate
3. pandas Basics
4. pandas Intermediate
5. Advanced pandas
6. Scenario-Based Questions

---

# NumPy Basics

## Q1. What is NumPy?
**Answer:** NumPy is the fundamental numerical computing library in Python. It provides the ndarray object for fast, memory-efficient array operations.

## Q2. Why is NumPy faster than Python lists?
**Answer:**
- Homogeneous data types
- Contiguous memory allocation
- Vectorized operations implemented in C

## Q3. What is an ndarray?
**Answer:** A multidimensional array object that stores elements of the same type.

```python
import numpy as np
arr = np.array([1,2,3])
```

## Q4. Difference between list and ndarray?
| Feature | List | ndarray |
|----------|------|---------|
| Speed | Slow | Fast |
| Type | Mixed | Homogeneous |
| Memory | Higher | Lower |

## Q5. What are shape, ndim and size?

**shape** → dimensions

**ndim** → number of axes

**size** → total elements

---

# NumPy Intermediate

## Q6. What is broadcasting?

**Answer:** Broadcasting allows NumPy to perform arithmetic on arrays of different shapes.

```python
arr = np.array([1,2,3])
arr + 10
```

## Q7. What is vectorization?

Replacing loops with array operations.

```python
arr * 2
```

## Q8. Difference between copy() and view()?

### copy()
Creates independent data.

### view()
Shares memory with original array.

## Q9. What is fancy indexing?

Selecting elements using arrays of indices.

```python
arr[[0,2,4]]
```

## Q10. What is boolean indexing?

```python
arr[arr > 5]
```

## Q11. Explain reshape().

Changes array dimensions without changing data.

## Q12. Difference between flatten() and ravel()?

- flatten() → returns copy
- ravel() → returns view when possible

## Q13. How do you handle missing values in NumPy?

```python
np.nan
np.isnan(arr)
```

## Q14. Common aggregation functions?

- sum()
- mean()
- median()
- std()
- max()
- min()

## Q15. Explain axis parameter.

axis=0 → columns

axis=1 → rows

---

# pandas Basics

## Q16. What is pandas?

A data analysis library built on top of NumPy.

## Q17. What are Series and DataFrame?

### Series
1-D labeled array

### DataFrame
2-D tabular structure

```python
import pandas as pd
```

## Q18. Read CSV file

```python
df = pd.read_csv("data.csv")
```

## Q19. Display first rows

```python
df.head()
```

## Q20. Display last rows

```python
df.tail()
```

## Q21. Get dataframe information

```python
df.info()
```

## Q22. Statistical summary

```python
df.describe()
```

## Q23. Select a column

```python
df["salary"]
```

## Q24. Multiple columns

```python
df[["name","salary"]]
```

## Q25. What is index?

Row labels used for data access.

---

# pandas Intermediate

## Q26. Difference between loc and iloc?

### loc
Label-based

```python
df.loc[0]
```

### iloc
Position-based

```python
df.iloc[0]
```

## Q27. Filtering rows

```python
df[df["salary"] > 50000]
```

## Q28. Sort data

```python
df.sort_values("salary")
```

## Q29. Rename columns

```python
df.rename(columns={"old":"new"})
```

## Q30. Drop columns

```python
df.drop("salary", axis=1)
```

## Q31. Handle missing values

```python
df.isnull()
df.fillna(0)
df.dropna()
```

## Q32. Unique values

```python
df["city"].unique()
```

## Q33. Value counts

```python
df["city"].value_counts()
```

## Q34. Apply function

```python
df["salary"].apply(lambda x: x*1.1)
```

## Q35. Map function

```python
df["gender"].map({"M":"Male","F":"Female"})
```

---

# Advanced pandas

## Q36. What is GroupBy?

Used for split-apply-combine operations.

```python
df.groupby("department")["salary"].mean()
```

## Q37. What is pivot table?

```python
pd.pivot_table(df,index="department")
```

## Q38. Merge vs Join

### Merge
SQL-style joins

### Join
Index-based joining

## Q39. Types of joins

- Inner
- Left
- Right
- Outer

## Q40. Concatenation

```python
pd.concat([df1,df2])
```

## Q41. What is MultiIndex?

Hierarchical indexing system.

## Q42. Working with dates

```python
pd.to_datetime(df["date"])
```

## Q43. Set index

```python
df.set_index("id")
```

## Q44. Reset index

```python
df.reset_index()
```

## Q45. Duplicate rows

```python
df.duplicated()
df.drop_duplicates()
```

---

# Scenario-Based Questions

## Q46. How do you find null values?

```python
df.isnull().sum()
```

## Q47. How do you replace null values?

```python
df.fillna(df.mean(numeric_only=True))
```

## Q48. How do you remove outliers?

Using IQR or Z-score methods.

## Q49. How do you merge two datasets?

```python
pd.merge(df1, df2, on="id")
```

## Q50. How do you optimize pandas performance?

- Use proper dtypes
- Avoid loops
- Use vectorization
- Use categorical variables
- Use chunk processing

---

# Frequently Asked Interview Questions

1. Why NumPy instead of lists?
2. Explain broadcasting.
3. What is vectorization?
4. Difference between loc and iloc?
5. Explain merge and join.
6. Explain GroupBy.
7. What is MultiIndex?
8. How do you handle missing values?
9. Difference between copy and view?
10. Difference between Series and DataFrame?

---

# 1-Day Revision Checklist

- ndarray
- Broadcasting
- Vectorization
- Reshape
- Copy vs View
- Series
- DataFrame
- loc vs iloc
- Filtering
- Missing Values
- GroupBy
- Merge
- Pivot Table
- Datetime Operations
- Performance Optimization

Good luck with your NumPy and pandas interviews!
