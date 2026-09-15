# Protocols

A protocol is a **set of requirements that an object must satisfy to participate in a specific operation**.

In simple terms:

> **If an object provides the required methods with the expected behavior, Python allows that object to be used with the operation.**

## It is informal

A protocol is usually **not something you explicitly inherit from or register with**. It is a specification of behavior.

For example, the protocol behind `len(obj)` requires the object to provide:

```python
__len__(self)
```

The method must return a **non-negative integer** representing the object's length.

## The promise it makes

Every protocol can be understood as:

* **IF** your object provides these methods, with the expected signatures and behavior...
* **THEN** your object can participate in this operation.

For example:

```text
IF   object provides __len__(self)
AND  it returns a non-negative integer
THEN len(object) works
```

## One protocol per operation

Different operations rely on different protocols:

| Operation      | Main special method      | Purpose                 |
| -------------- | ------------------------ | ----------------------- |
| `len(obj)`     | `__len__`                | Get the object's length |
| `obj[0]`       | `__getitem__`            | Access an item          |
| `for x in obj` | `__iter__`               | Iterate over the object |
| `obj == other` | `__eq__`                 | Compare objects         |
| `obj()`        | `__call__`               | Call the object         |
| `with obj`     | `__enter__` / `__exit__` | Manage a context        |

So, a protocol is essentially the **agreement between Python and an object about how that operation should work**.

## Complete example: the `len()` protocol

### The operation

```python
len(obj)
```

For example:

```python
len("hello")
len([1, 2, 3])
len(box)
```

`len()` is a built-in function. It does not need to know the object's class. It only needs the object to satisfy the requirements of the `len()` protocol.

### The specification

Informally, the protocol says:

* Provide a `__len__(self)` method.
* The method receives `self`.
* It returns a non-negative integer.

That is enough for the object to participate in `len()`.

### The implementation

```python
class Box:
    def __len__(self):
        return 5


box = Box()

print(len(box))  # 5
```

`Box` satisfies the requirements of the `len()` protocol, so `len(box)` works.

The important idea is:

> **Python cares about whether the object provides the required behavior, not what class the object belongs to.**

A `list`, a `str`, a `Deck`, or an `Aquarium` object can all work with `len()` as long as they satisfy the protocol.

---

# Python Data Model

The **Python Data Model** is the set of rules that defines **how Python objects interact with the language and its built-in operations**.

In simple terms:

> **The Data Model is the overall specification for how objects can behave like Python objects.**

It covers things such as:

```python
len(obj)       # __len__
obj[0]         # __getitem__
obj + other    # __add__
obj == other   # __eq__
obj()          # __call__
for x in obj   # __iter__
with obj       # __enter__ / __exit__
```

Each operation has its own rules describing what an object must provide to participate in that operation.

## The relationship between the Data Model and protocols

Think of the Data Model as the **big picture**:

```text
Python Data Model
│
├── len(obj)       → __len__       → length protocol
├── obj[0]         → __getitem__   → indexing protocol
├── obj + other    → __add__       → addition protocol
├── obj == other   → __eq__        → comparison protocol
├── obj()          → __call__      → calling protocol
├── for x in obj   → __iter__      → iteration protocol
└── with obj       → __enter__/__exit__ → context manager protocol
```

So:

> **The Data Model defines the rules, and each protocol defines the requirements for a particular kind of operation.**

---

# Special Methods

A **special method** is a method with a name defined by Python's Data Model that Python uses to implement specific language operations.

They are usually recognized by their **double underscores**:

```python
__len__
__getitem__
__add__
__eq__
__str__
__iter__
```

They are commonly called:

* **Special methods** — the official/general term.
* **Dunder methods** — short for "double underscore methods."
* **Magic methods** — an informal term.

For practical purposes, these terms usually refer to the same group of methods.

## Example: `__str__`

`__str__` defines the **human-readable string representation** of an object.

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"A dog named {self.name}"


my_dog = Dog("Buddy")

print(my_dog)
# A dog named Buddy
```

When Python evaluates:

```python
print(my_dog)
```

it uses the object's `__str__` method to obtain the text representation.

Conceptually:

```python
print(my_dog)
        ↓
str(my_dog)
        ↓
my_dog.__str__()
        ↓
"A dog named Buddy"
```

Without a custom `__str__`, Python uses the default string representation provided by the object's class, which typically looks something like:

```text
<__main__.Dog object at 0x...>
```

So the key relationship is:

> **The protocol defines what behavior is required; the special method is the method that provides that behavior; the Python Data Model defines the overall system of these rules.**
