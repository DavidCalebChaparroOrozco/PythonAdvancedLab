# Tuples & Unpacking in Depth

This document covers the dual nature of Python tuples (immutable lists vs. structural records), hashability boundaries, and advanced sequence unpacking patterns.

---

## 📦 1. Tuples: Dual Purpose Architecture

In Python, tuples serve two distinct roles depending on context:
1. **Immutable Lists:** Storing a collection of items where the length and order should never change (e.g., configuration constants, ports, or coordinates).
2. **Records Without Field Names:** Holding heterogeneous data where the **position** determines the meaning of each field (e.g., `("etl-01", "ubuntu", "22.04")`).

### Immutability vs. Hashability
* A tuple's references are immutable (you cannot add, remove, or reassign slots).
* However, a tuple is only **hashable** (usable as a `dict` key or inside a `set`) if **all** of its contained elements are also hashable (e.g., `(1, "a")` is hashable, whereas `(1, ["a"])` raises a `TypeError: unhashable type: 'list'`).

---

## 🧩 2. Sequence & Iterable Unpacking

Unpacking works with **any iterable** (tuples, lists, generators, strings, files), not just tuples.

### A. Parallel Assignment
```python
host, os_name, version = ("etl-01", "ubuntu", "22.04")
```

### B. Swapping Variables Without Temporary Storage
```python
a, b = b, a
```

### C. Prefixing Arguments with `*` (Function Calls)
```python
server_data = ("db-01", "debian", "12", ["postgresql"])
server = Server(*server_data)
```

---

## 🌟 3. Extended Iterable Unpacking (`*` Star Expressions)

Introduced in PEP 3132, the `*` operator captures excess elements into a `list` during assignment:

* **At the end:** `first, second, *rest = [10, 20, 30, 40, 50]` → `rest == [30, 40, 50]`
* **At the beginning:** `*head, last = [10, 20, 30, 40]` → `head == [10, 20, 30]`
* **In the middle:** `first, *middle, last = [10, 20, 30, 40]` → `middle == [20, 30]`
* **Rule:** Only **one** starred expression is allowed per unpacking level, and it always evaluates to a `list` (even if empty `[]`).

---

## 🔍 4. Nested Unpacking & Ignoring Values

* **Nested Unpacking:** Mirrors the exact structure of nested tuples/lists:
  ```python
  server_name, (major, minor) = ("web-01", (20, 4))
  ```
* **Dummy Variables (`_`):** By convention, `_` (or `*_`) signals that a value is intentionally ignored:
  ```python
  name, *_, services = ("etl-01", "ubuntu", "22.04", ["airflow", "dbt"])
  ```

---

## A tuple, two uses

A tuple is an ordered, unchangeable (immutable) sequence of items. Like a list, you can loop over it with a `for` loop and access its items by their index position. The main difference lies in how you use it.

In Python, a tuple has two distinct uses:

- **As a record:** `("db-01", 5432)` (groups different attributes of one item)
- **As an immutable list:** `("cpu", "disk", "memory")` (a fixed collection of similar items that cannot be modified)

---

## What is a record?

A record is a data structure that groups several related pieces of information to describe a single entity. In a record, every position has a specific meaning.

For example, you can represent a student with a tuple:

```python
student = ("Caleb", 29, "Medellin")
```

Here, each index holds a specific field:

- **Position 0:** `"Caleb"` (name)
- **Position 1:** `29` (age)
- **Position 2:** `"Medellin"` (city)

Together, these values form a single record representing one student.

---

## A record in practice: a server address

Using a server address as an example:

```python
address = ("db-01", 5432)

print(address[0])   # Output: db-01
print(address[1])   # Output: 5432
print(len(address)) # Output: 2
```

---

## Three implications of using a tuple as a record

1. **The length is fixed:** A server address requires exactly two pieces of data (host and port). Adding or removing an element changes what the data represents.
2. **The order is strict:** `(5432, "db-01")` is no longer a valid address because the host and port are swapped. Sorting a record (for example, with `sorted()`) destroys its meaning.
3. **Data types can vary:** A record often mixes different data types—such as a `str` (string) for the hostname and an `int` (integer) for the port—because each position represents a different attribute.

> **Tuple (Record) vs. List:** A list like `["postgresql", "redis"]` typically holds multiple items of the same type. You can add, remove, or reorder items in a list without changing the fact that every element is still a service name.

---

## You see them every day

If you work with data, you encounter tuple records constantly. For example, each row returned by a SQL database query in Python is represented as a tuple:

```python
import sqlite3

connection = sqlite3.connect(":memory:")
row = connection.execute("SELECT 'db-01', 5432").fetchone()

print(row)       # Output: ('db-01', 5432)
print(type(row)) # Output: <class 'tuple'>
```

---

## What you cannot do (Immutability)

The second use case for a tuple is acting as an immutable list—a sequence whose size and contents cannot be modified after creation.

Because tuples are immutable, you cannot replace an existing element or add a new one:

```python
address[1] = 5433      # Raises TypeError: 'tuple' object does not support item assignment
address.append("tcp")  # Raises AttributeError: 'tuple' object has no attribute 'append'
```

---

## Tuples only retain read-only methods

Comparing the built-in methods of tuples and lists shows that tuples only keep methods that inspect data without changing it:

```python
print([m for m in dir(tuple) if not m.startswith('_')])
print([m for m in dir(list) if not m.startswith('_')])
```

- **Tuple methods:** `'count'`, `'index'`
- **List methods:** `'append'`, `'clear'`, `'copy'`, `'count'`, `'extend'`, `'index'`, `'insert'`, `'pop'`, `'remove'`, `'reverse'`, `'sort'`

> Any method that adds, removes, or reorders elements in place does not exist on a tuple.

---

## What exactly does "immutable" mean?

Immutability means the tuple's structure—the references it holds—cannot be changed after creation. You cannot reassign any slot in the tuple to point to a different object. However, if a slot holds a mutable object (like a list), that inner object can still be modified in place:

```python
record = ("web-01", ["nginx", "redis"])
before = id(record)

record.append("haproxy")
print(record)                 # Output: ('web-01', ['nginx', 'redis', 'haproxy'])
print(id(record) == before) # Output: True (it is still the exact same list object)
```

---

## The comma creates the tuple, not the parentheses

In Python, it is the trailing comma—not the parentheses—that defines a tuple:

```python
a = ("db-01")
b = ("db-01",)
c = "db-01", 5432

print(type(a)) # Output: <class 'str'>
print(type(b)) # Output: <class 'tuple'>
print(type(c)) # Output: <class 'tuple'>
```

Keep three rules in mind:

1. **`("db-01")` is a `str`:** Without a comma, parentheses only group expressions, just like in math (`(2 + 3) * 4`).
2. **Single-item tuples require a trailing comma:** You must write `("db-01",)` or `"db-01",` to create a tuple with one element.
3. **Parentheses are optional except where syntax requires them:** `"db-01", 5432` is already a valid tuple. Parentheses are added for readability and are mandatory when commas would otherwise act as separators—such as passing a tuple as a single argument to a function: `create_connection((host, port))`.

---

## How are two tuples compared?

Python compares tuples **lexicographically** (element by element, from left to right). The first pair of elements that differ determines the result, and Python stops checking the remaining elements.

This makes tuples ideal for comparing version numbers or multi-part values where plain text comparison fails:

```python
# Comparing as text (alphabetical order: '4' comes after '1')
"22.4" < "22.10"   # Output: False

# Comparing as tuples (numerical order: 22 == 22, then 4 < 10)
(22, 4) < (22, 10) # Output: True
```

---

## What does Python gain from using a tuple?

Because a tuple cannot change in size or content, CPython (the standard Python interpreter) does not need to reserve extra space for future growth or track modifications. This results in two measurable performance benefits:

1. **It consumes less memory.**
2. **Copying it costs nothing.**

---

## It consumes less memory

Lists allocate extra memory behind the scenes so that `.append()` operations remain fast without resizing on every addition. Tuples allocate only the exact amount of memory needed for their elements:

```python
import sys

ports_tuple = (22, 80, 443)
ports_list = [22, 80, 443]

print(sys.getsizeof(ports_tuple)) # Output: 64 (or 72 depending on Python version/architecture)
print(sys.getsizeof(ports_list))  # Output: 88
```

---

## Copying it costs nothing

Passing an existing tuple to `tuple()` returns a reference to the exact same object in memory instead of creating a duplicate:

```python
print(tuple(ports_tuple) is ports_tuple) # Output: True
print(list(ports_list) is ports_list)    # Output: False
```

> `list(...)` must allocate and copy all elements into a brand-new list so that modifying one copy does not accidentally alter the original. Calling `tuple(...)` on an existing tuple simply returns the original object because neither can ever be modified.

---

## When to use each

1. **A record (fixed fields where each position has a specific meaning) → `tuple`**  
   *Example:* `address = ("db-01", 5432)` or `version = (22, 4)`
2. **A fixed collection of items that should never change → `tuple`**  
   *Example:* `checks = ("cpu", "disk", "memory")`
3. **A collection that grows, shrinks, needs sorting, or requires filtering → `list`**  
   *Example:* `servers = ["web-01", "web-02"]` or `active_services = ["nginx", "redis"]`

---

## The problem

To use values stored inside a tuple record, accessing them one by one using index positions is repetitive and makes code harder to read:

```python
host = address[0]
port = address[1]
```

---

## What is unpacking?

Unpacking is a Python feature that extracts the elements of a sequence and assigns them to multiple variables in a single statement. Python matches elements from left to right—assigning the first element to the first variable, the second element to the second variable, and so on:

```python
host, port = address
print(host) # Output: db-01
print(port) # Output: 5432
```

*(Note: The number of variables on the left must match the number of elements on the right, otherwise Python raises a `ValueError`.)*

---

## It works with any iterable

Unpacking is not limited to tuples. The expression on the right-hand side can be any iterable—such as a list returned by `.split()`, a string, or a generator expression:

```python
# Unpacking a list of strings
major, minor = "22.04".split(".")
print(major, minor) # Output: 22 04

# Unpacking a generator expression
major, minor = (int(part) for part in "22.04".split("."))
print(major, minor) # Output: 22 4
```

---

## Swapping two variables

Python evaluates the entire right-hand side as a temporary tuple before assigning any values to the left-hand side. This lets you swap the values of two variables cleanly in one line without needing a temporary placeholder variable:

```python
primary = "db-01"
replica = "db-02"

primary, replica = replica, primary
print(primary, replica) # Output: db-02 db-01
```

---

## Discarding unwanted data: `_`

When unpacking a record, you may only need certain fields. By Python convention, any value you want to ignore is assigned to an underscore (`_`):

```python
import socket

with socket.create_server(("127.0.0.1", 0)) as local_server:
    print(local_server.getsockname()) # Output: ('127.0.0.1', 41273)
    _, port = local_server.getsockname()

print(port) # Output: 41273
```

> Technically, `_` is a valid, ordinary variable name in Python—using it simply signals to other developers that the value is intentionally ignored.