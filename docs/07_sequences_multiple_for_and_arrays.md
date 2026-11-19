# 07. Sequences II: Multiple `for` Clauses & Typed Arrays

This document covers nested iterations inside comprehensions, Cartesian products, flattening structures, and memory-efficient flat sequences (`array.array`).

---

## 🔄 1. Multiple `for` Clauses in List Comprehensions

A list comprehension can contain multiple `for` clauses in a single expression. Each additional `for` iterates over another iterable, allowing you to combine elements from multiple sequences or traverse nested structures.

### General Syntax
```python
[expression for a in A for b in B]
```

### Equivalent Traditional Nested Loops
```python
result = []
for a in A:
    for b in B:
        result.append(expression)
```

### Key Takeaways
* **Execution Order:** Works like nested `for` loops. The rightmost loop runs completely for each iteration of the leftmost loop.
* **Use Cases:** Generating Cartesian products (e.g., pairing every server with every health check) or flattening nested collections (e.g., extracting all installed services across a fleet of servers).
* **Readability Rule:** If a comprehension exceeds two `for` clauses or becomes hard to read, prefer traditional `for` loops or generator pipelines.

---

## 💾 2. Typed Flat Sequences (`array.array`)

* Unlike `list` (which stores pointers to full Python `int` objects), `array.array` stores raw C-level values contiguously in memory.
* **Typecodes:** Require a single-character typecode upon creation (e.g., `'H'` for unsigned short 2-byte integers `0` to `65535`, ideal for network ports).

---

## 🧪 3. Baseline Setup for Practical Examples

We continue with the inventory. The examples are intended to be executed in order.

```python
from array import array
from inventory import Server

servers = [
    Server("etl-01", "ubuntu", "22.04", ["airflow", "dbt"]),
    Server("db-01", "debian", "12.5", ["postgres"]),
    Server("web-01", "ubuntu", "20.04", ["nginx", "gunicorn", "redis"]),
    Server("bi-01", "rocky", "9.3", []),
]

checks = ("cpu", "disk", "memory")
ports = array("H", [22, 80, 443, 5432, 8080])
```

---

## Multiple `for` Clauses

### The Problem: Two Nested `for` Loops

We want to create a monitoring plan that runs each check (CPU, disk, and memory) on every server.

To accomplish this, we use two nested `for` loops. The outer loop iterates over all servers, while the inner loop iterates over all monitoring checks for each server.

```python
plan = []  # Create an empty list to store the monitoring plan.

for server in servers:  # Iterate over each server in the servers list.
    for check in checks:  # Run through every monitoring check for the current server.
        plan.append((server.name, check))  # Store a tuple containing the server name and the check.

print(len(plan))  # Print the total number of monitoring tasks.
```

How it works:

1. `plan = []`: Creates an empty list where we will store the monitoring tasks.
2. `for server in servers`: Selects each server, one at a time.
3. `for check in checks`: For each selected server, iterates through all available monitoring checks.
4. `plan.append((server.name, check))`: Adds a tuple containing the server's name and the current check to the list.
5. `print(len(plan))`: Counts and displays the total number of monitoring tasks.

Expected output:

```
12
```

There are 4 servers and 3 checks, resulting in 12 monitoring tasks (4 × 3).

### Cartesian Product

A list comprehension can contain multiple `for` clauses. These clauses behave like nested loops and execute in the same order in which they are written: the first `for` is the outer loop, and the second `for` is the inner loop.

```python
# Generate all combinations of servers and monitoring checks.
plan_comprehension = [(s.name, check) for s in servers for check in checks]

# Check whether the list comprehension produces the same result as the traditional loops.
print(plan_comprehension == plan)  # True

# Display the first four monitoring tasks.
print(
    plan_comprehension[:4]
)  # [('etl-01', 'cpu'), ('etl-01', 'disk'), ('etl-01', 'memory'), ('db-01', 'cpu')]
```

How it works:

1. `(s.name, check)`: Defines the tuple that will be created for each combination.
2. `for s in servers`: Iterates over every server (outer loop).
3. `for check in checks`: Iterates over every monitoring check for the current server (inner loop).
4. `plan_comprehension == plan`: Compares both lists to verify that they contain exactly the same elements in the same order.
5. `plan_comprehension[:4]`: Uses list slicing to retrieve the first four elements.

Expected output:

```
True
[('etl-01', 'cpu'), ('etl-01', 'disk'), ('etl-01', 'memory'), ('db-01', 'cpu')]
```

> Cartesian product: The result contains every possible combination of elements from the input sequences. In this example, every server is paired with every monitoring check.

Key takeaway: Multiple `for` clauses in a list comprehension are a concise alternative to nested loops. They produce the same iteration order and results when the expression and loop structure are equivalent.

---

## Multiple `for` Loops

### Cartesian Product

4 servers × 3 checks = 12

This is called a Cartesian product: every element from one sequence is combined with every element from another sequence.

For each server, the inner `for` loop iterates through all the monitoring checks. This is why the total number of combinations is calculated through multiplication.

Example:

```python
# 4 servers × 3 checks = 12 combinations
plan = [(s.name, check) for s in servers for check in checks]
```

### When the Second `for` Loop Depends on the First

The second `for` loop can use the variable defined in the first loop. This allows us to access each server's installed services and create a pair `(server, service)` for every installed service.

Unlike the Cartesian product, the number of iterations in the second loop depends on the current server.

```python
# Create a list containing each server and its installed services.
installed = [
    (s.name, service)  # Create a tuple with the server name and service.
    for s in servers  # Iterate over every server.
    for service in s.services  # Iterate over the services installed on the current server.
]

print(len(installed))  # Print the total number of installed services: 6.

# Display all server-service combinations.
print(installed)
# [('etl-01', 'airflow'), ('etl-01', 'dbt'),
#  ('db-01', 'postgres'),
#  ('web-01', 'nginx'), ('web-01', 'gunicorn'), ('web-01', 'redis')]
```

How it works:

1. `for s in servers`: Selects each server.
2. `for service in s.services`: Retrieves each service installed on the current server.
3. `(s.name, service)`: Creates a tuple containing the server name and the installed service.
4. Servers with empty service lists produce no elements because their inner loop has nothing to iterate over.

Key difference: The Cartesian product combines every element from two independent sequences. Here, the second iteration depends on the first because each server has its own list of services.

### Equivalent to `UNNEST` and `explode`

This process is known as flattening: converting nested collections, such as a list of lists, into a single flat list.

In data processing, similar operations include:

- SQL (BigQuery): `UNNEST()` expands an array into individual rows.
- Apache Spark: `explode()` creates a separate row for each element in an array or map column.

Simple example:

Imagine a table containing servers and their installed services:

| server | services             |
| ------ | -------------------- |
| etl-01 | `["airflow", "dbt"]` |
| db-01  | `["postgres"]`       |
| web-01 | `["nginx", "redis"]` |

After flattening, each service becomes an individual row:

| server | service  |
| ------ | -------- |
| etl-01 | airflow  |
| etl-01 | dbt      |
| db-01  | postgres |
| web-01 | nginx    |
| web-01 | redis    |

BigQuery example:

```SQL
SELECT
    server,
    service
FROM inventory,
UNNEST(services) AS service;
```

PySpark example:

```python
from pyspark.sql.functions import explode

df_exploded = df.select("server", explode("services").alias("service"))
```

> Key takeaway: Flattening transforms nested data into individual records, making it easier to filter, analyze, aggregate, and process each element independently.

## Generator Expressions

Generator expressions are a way to create iterators in Python that produce values one at a time, on demand, instead of creating and storing an entire list in memory.

They are particularly useful when working with large datasets or when you only need to process values sequentially.

### List Comprehension vs. Generator Expression

Both approaches use a similar syntax, but they behave differently.

List comprehension

```python
squares = [x**2 for x in range(1, 6)]

print(squares)  # [1, 4, 9, 16, 25]
```

- Creates the complete list immediately.
- Stores all generated elements in memory.
- Allows direct access to elements using indexes.

Generator expression

```python
squares = (x**2 for x in range(1, 6))

print(squares)  # <generator object ...>
```

- Creates a generator object instead of a complete list.
- Produces one value at a time, only when requested.
- Does not store all generated elements simultaneously.
- Is generally more memory-efficient when processing large sequences.

Retrieving values from a generator:

```python
squares = (x**2 for x in range(1, 6))

print(next(squares))  # 1
print(next(squares))  # 4
print(next(squares))  # 9
```

Each call to `next()` requests the next available value from the generator.

> Key takeaway: List comprehensions create all elements immediately, while generator expressions produce elements on demand. Both are useful, but generators are especially beneficial when memory efficiency matters.

---

### Why Are Generator Expressions Useful? Memory Efficiency

Generator expressions are especially useful because they consume significantly less memory than list comprehensions when working with large sequences.

A list comprehension generates and stores all its elements in memory immediately. A generator expression creates an iterator that produces each value only when requested.

Example: Comparing Memory Usage

```python
import sys

# Create a list containing 10 million squared numbers.
# All elements are generated and stored in memory immediately.
print(sys.getsizeof([n**2 for n in range(10_000_000)]))  # Approximately 89 MB

# Create a generator that produces the same values on demand.
# Only the generator object is stored, not all the generated values.
print(sys.getsizeof((n**2 for n in range(10_000_000))))  # Approximately 208 bytes
```

Expected output (approximately):

```
89095160
208
```

How it works:

1. `import sys`: Imports Python's system module, which provides access to interpreter-related information and utilities.
2. `sys.getsizeof()`: Returns the shallow memory size of an object in bytes.
3. `[n**2 for n in range(10_000_000)]`: Creates a list containing 10 million squared numbers, storing all elements in memory.
4. `(n**2 for n in range(10_000_000))`: Creates a generator expression that calculates each squared number only when requested.

Important distinction: `sys.getsizeof()` measures the size of the object itself, not necessarily the total memory occupied by everything it references. For a list, it does not include the full memory footprint of all its elements. For a generator, it does not include the memory needed to produce future values.

> Key takeaway: Generators are memory-efficient because they avoid storing an entire collection of results. Instead, they produce values one at a time, making them particularly useful for processing large datasets.

---

## **Short-Circuiting**

### **Stopping evaluation once the result is known**

Short-circuiting is a behavior in Python where logical expressions stop being evaluated as soon as the final result is determined.

- **With**`and`**:** If any value is `False`, the entire expression is `False`. Python stops evaluating as soon as it finds the first `False`.
- **With**`or`**:** If any value is `True`, the entire expression is `True`. Python stops evaluating as soon as it finds the first `True`.

### **Examples**

**Using** `and`**:**

```python
True and True and True and True
# True

False and True and True and True
# False
```

**Using** `or`**:**

```python
False or False or False or False
# False

False or True or False or False
# True
```

### **Key idea**

Python evaluates logical expressions from left to right and skips the remaining parts whenever the result is already known. This improves efficiency and can prevent unnecessary operations.

---

### **Seeing Short-Circuiting in Action with**`check()`

We can use a function to see how Python evaluates logical expressions and skips unnecessary operations.

```python
def check(check_name, result):
    print(f"Checking {check_name}...")
    return result

print(check("Disk", False) and check("CPU", True))
# Checking Disk...
# False

print(check("Disk", True) or check("CPU", False))
# Checking Disk...
# True
```

**What's happening?**

1. **Using **`and`**:** Python evaluates `check("Disk", False)` first. Since it returns `False`, the entire expression must be `False`. Therefore, `check("CPU", True)` is never executed.
2. **Using **`or`**:** Python evaluates `check("Disk", True)` first. Since it returns `True`, the entire expression must be `True`. Therefore, `check("CPU", False)` is never executed.

### **Real-World Example: Filtering Outdated Versions**

We've already used short-circuiting without explicitly calling it that.

In the previous lesson, we had this condition:

```python
s.so == system and s < reference
```

Python first checks whether `s.so == system`.

- If the systems don't match (`False`), Python skips the second comparison.
- If the systems match (`True`), Python evaluates `s < reference`.

**Key idea:** Short-circuiting avoids unnecessary comparisons and operations by stopping as soon as the result is known.

---

### `any()` **and** `all()`

Python provides two built-in functions that apply logical checks to an entire iterable (such as a list, tuple, or generator).

- `any()`**:** Returns `True` if at least one element is truthy. It stops evaluating as soon as it finds the first truthy element. Returns `False` if all elements are falsy or the iterable is empty.
- `all()`**:** Returns `True` if every element is truthy. It stops evaluating as soon as it finds the first falsy element. Returns `False` if at least one element is falsy or the iterable is empty.

### **Examples**

```python
print(any([False, True, False]))
# True
print(all([True, False, True]))
# False
```

### **More examples**

```python
print(any([False, False, False]))
# False
print(all([True, True, True]))
# True
```

### **Key idea**

- `any()` works like a chain of `or` operations.
- `all()` works like a chain of `and` operations.

Both use short-circuiting, meaning they stop as soon as the final result is known.

---

## **Short-Circuiting + Generator Expressions**

Generator expressions work particularly well with `any()` and `all()` because they allow Python to evaluate elements one at a time and stop as soon as the result is known.

### **Example: Checking Remote Servers**

Imagine we have multiple servers and want to check whether at least one of them has Redis installed.

```python
def has_service(server, service):
    print(f"Querying {server.name}...")
    return service in server.services

print(any(has_service(s, "redis") for s in servers))
# Querying etl-01...
# Querying db-01...
# Querying web-01...
# True
```

**What's happening?**

1. The generator expression checks one server at a time.
2. `any()` evaluates each result as it receives it.
3. Once it finds a server with Redis, it returns `True`.
4. The remaining servers are never checked.

### **Now, using square brackets**

```python
print(any([has_service(s, "redis") for s in servers]))
# Querying etl-01...
# Querying db-01...
# Querying web-01...
# Querying bi-01...
# True
```

**What's happening?**

The list comprehension builds the entire list before passing it to `any()`.

This means:

- Every server is checked first.
- Only after the list is complete does `any()` start evaluating its elements.
- Short-circuiting cannot prevent the unnecessary queries because they have already happened.

### **Why does this matter?**

Imagine checking 1,000 servers:

- **Generator expression:** Stops as soon as Redis is found.
- **List comprehension:** Checks all 1,000 servers before `any()` starts.

If the match is found on the first server, the list comprehension performs 999 unnecessary queries.



Best practice: Use generator expressions with `any()` and `all()` when you don't need to store the results.

```python
any(has_service(s, "redis") for s in servers)
all(has_service(s, "redis") for s in servers)
```

### **Ruff C419: Unnecessary List Comprehension**

Ruff flags `any([...])` as an unnecessary list comprehension because the list doesn't need to be created.

Instead of:

```python
any([x > 0 for x in numbers])
```

Use:

```python
any(x > 0 for x in numbers)
```

The second version is more memory-efficient and allows short-circuiting during iteration.

## **A Brief Summary**

| Concept              | What it does                                                  |
| -------------------- | ------------------------------------------------------------- |
| Short-circuiting     | Stops evaluating once the result is known.                    |
| `and`                | Stops at the first falsy value.                               |
| `or`                 | Stops at the first truthy value.                              |
| `any()`              | Returns `True` if at least one element is truthy.             |
| `all()`              | Returns `True` if every element is truthy.                    |
| Generator expression | Evaluates elements lazily, one at a time.                     |
| List comprehension   | Builds the entire list before passing it to another function. |

**Key takeaway:** Combine generator expressions with `any()` and `all()` to avoid unnecessary computations, reduce memory usage, and take full advantage of short-circuiting.