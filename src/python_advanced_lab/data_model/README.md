# Python Data Model Reference Guide

Welcome to the **Python Data Model** section of this advanced laboratory. This document serves as a high-level conceptual blueprint and comprehensive reference guide for understanding Pythonic protocols and special methods.

---

## 🧭 Core Concepts

### 1. Protocols: The Informal Contracts
In Python, a **Protocol** is an informal contract required by a specific language operation. 
* **Informal Nature:** There are no abstract base classes to inherit from, nor interfaces to register. It is pure **duck typing** driven by specification.
* **The Universal Promise:** 
  * **IF** your object implements the required special method with the correct signature and expected behavior...
  * **THEN** Python will seamlessly allow your object to participate in that operation.

### 2. The Python Data Model
The **Data Model** is the complete specification of the Python language. It defines the universal API that all objects can implement to integrate with Python's built-in syntax (loops, indexing, operators, context managers).

### 3. Special / Dunder Methods
Special methods (also known as *Dunder* or *Magic* methods) are functions with reserved names wrapped in double underscores (e.g., `__init__`). Python invokes these methods **automatically** under the hood when a native operation is triggered.

---

## 📊 Summary of Main Protocols

This laboratory covers the most important protocols of the Python Data Model. Each row below represents a protocol implemented in this directory:

| Protocol | Operation | Special Method | Purpose / Expected Behavior |
| :--- | :--- | :--- | :--- |
| **Initialization** | `Instance Creation` | `__init__(self, ...)` | Initializes a newly created object instance safely. |
| **Representation** | `repr(obj)` | `__repr__(self)` | Unambiguous string for developers (looks like valid Python code). |
| **String Conversion**| `str(obj)` or `print()`| `__str__(self)` | User-friendly, clean string representation for end-users/logs. |
| **Comparison (Eq)** | `obj == other` | `__eq__(self, other)` | Defines structural equality instead of memory identity. |
| **Ordering (Lt)** | `obj < other` or `min()`| `__lt__(self, other)` | Establishes a natural sorting order between instances. |
| **Container Emulation**| `len(obj)` | `__len__(self)` | Returns the total count of items as an integer $\ge 0$. |
| **Collection Indexing**| `obj[key]` | `__getitem__(self, key)`| Enables element access, slicing, and automatic sequential iteration. |

---

## 🛠️ Code Architecture in this Lab

To keep the learning process organized, the concepts are split into distinct, highly typed production scripts within this module:

* 📄 **`representation.py`**: Practical exploration of object lifetimes, memory separation, and the `__repr__` vs `__str__` duality.
* 📄 **`operators.py`**: Deep dive into operators overloading, implementing relational protocols (`__eq__`, `__lt__`), and leveraging built-in aggregation algorithms like `min()`.
* 📄 **`collections.py`** *(Upcoming)*: Hands-on implementation of custom objects emulating Python's native data structures.

---

> *"The Python Data Model allows your custom objects to look, feel, and behave exactly like Python's built-in types, honoring the principle of least surprise."*
