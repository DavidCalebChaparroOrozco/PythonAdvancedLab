## `__dunder__`

**Dunder methods** are special methods in Python that connect built-in Python operations and syntax to the behavior of your objects.

**Dunder** is short for **double underscore**, because these methods have two underscores before and after their names:

```python
__method__
```

### Python Data Model

Dunder methods are part of Python's **Data Model**.

The Data Model defines **protocols**—rules that allow your objects to work with Python's built-in syntax and operations.

For example:

| Python operation | Dunder method | Protocol / behavior |
|---|---|---|
| `object()` | `__call__` | Make an object callable |
| `with object:` | `__enter__` / `__exit__` | Context manager |
| `object[something]` | `__getitem__` | Collection / item access |
| `x in object` | `__contains__` | Membership |
| `if object:` | `__bool__` | Truthiness |

### The Core Idea

Instead of Python knowing every custom class you create, it defines **protocols** that your class can follow.

For example:

```python
object[something]
```

Python looks for:

```python
object.__getitem__(something)
```

And:

```python
x in object
```

Python can use:

```python
object.__contains__(x)
```

So the general pattern is:

> **Python syntax → dunder method → behavior defined by your class**

Dunder methods are what allow custom objects to **feel like normal Python objects**.

---

## What Is a Dunder Method?

A **dunder method** is a special Python method whose name starts and ends with **two underscores** (`__`).

“Dunder” means **double underscore**.

Dunder methods let you define how your objects behave with Python’s built-in functions and operators.

For example:

- `__init__`: initializes a newly created object.
- `__str__`: defines the human-readable text shown by `print(obj)` or `str(obj)`.
- `__repr__`: defines the developer-oriented representation of an object, mainly used for debugging and in the interactive Python console.
- `__len__`: defines what `len(obj)` should return.
- `__add__`: defines what happens when you use `obj + other`.
- `__eq__`: defines what happens when you compare objects with `obj == other`.

### Complete Example

```python
class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Person: {self.name}"

    def __len__(self):
        return len(self.name)


person = Person("Caleb")

print(person)       # Person: Caleb
print(str(person))  # Person: Caleb
print(len(person))  # 5
```

### What Happens Here?

```python
person = Person("Caleb")
```

Python calls:

```python
__init__
```

to initialize the new `Person` object.

When you write:

```python
print(person)
```

Python uses:

```python
__str__
```

to determine what text to display.

When you write:

```python
len(person)
```

Python uses:

```python
__len__
```

to determine the object's length.

In short:

> **Dunder methods allow your classes to work naturally with Python's built-in functions, operators, and syntax.**

---

## Six Operations, Six Protocols

Python defines **protocols** that allow your objects to work with built-in syntax and operations. You implement these protocols using special **dunder methods**.

The basic pattern is:

**Python syntax → dunder method → behavior of your object**

---

### 1. `object()` → `__call__`

When you write:

```python
object()
```

you are **calling** something.

If a class defines `__call__`, its instances can also be called like functions:

```python
object()
```

This allows an object to behave like a function while still **storing its own state**.

> **Protocol:** Callable

Example:

```python
class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count


counter = Counter()

print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

Here, `counter` is an object, but `counter()` works because it implements `__call__`.

---

### 2. `with object:` → `__enter__` / `__exit__`

The `with` statement is used to **automatically set up and clean up resources**.

For example:

```python
with object:
    ...
```

A class can support this behavior by implementing:

```python
__enter__
__exit__
```

`__enter__` prepares the resource before entering the block.

`__exit__` cleans it up when leaving the block, **even if an exception occurs**.

> **Protocol:** Context manager

Example:

```python
class Resource:
    def __enter__(self):
        print("Resource opened")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Resource closed")


with Resource():
    print("Using resource")
```

Output:

```text
Resource opened
Using resource
Resource closed
```

---

### 3. `__exit__` → `exc_type`, `exc_value`, `traceback`

How does `__exit__` know whether the `with` block finished successfully or an exception occurred?

Python automatically passes three arguments to `__exit__`:

```python
__exit__(self, exc_type, exc_value, traceback)
```

They contain information about an exception, if one occurred:

- `exc_type`: the type of the exception, such as `ValueError`
- `exc_value`: the actual exception object and its message
- `traceback`: information about where the exception occurred

If no exception occurred, all three are:

```python
None
```

Example:

```python
class Resource:
    def __enter__(self):
        print("Opened")

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print("Finished successfully")
        else:
            print(f"An error occurred: {exc_value}")


with Resource():
    print("Working")
```

The important idea is:

> **`__exit__` receives exception information so it can clean up the resource and optionally handle the exception.**

---

### 4. `object[something]` → `__getitem__`

When you write:

```python
object[something]
```

Python calls:

```python
__getitem__
```

This allows your class to behave like a collection.

You can use it to support:

- Indexing: `obj[0]`
- Slicing: `obj[1:4]`
- Keys: `obj["name"]`

> **Protocol:** Container / sequence / mapping behavior

Example:

```python
class Person:
    def __init__(self, name, age):
        self.data = [name, age]

    def __getitem__(self, index):
        return self.data[index]


person = Person("Caleb", 27)

print(person[0])  # Caleb
print(person[1])  # 27
```

The syntax:

```python
person[0]
```

is translated conceptually into:

```python
person.__getitem__(0)
```

---

### 5. `x in object` → `__contains__`

When you write:

```python
x in object
```

Python can use:

```python
__contains__
```

to determine whether `x` exists inside the object.

This allows you to define how membership searches work.

> **Protocol:** Container / membership

Example:

```python
class Team:
    def __init__(self, members):
        self.members = members

    def __contains__(self, name):
        return name in self.members


team = Team(["Caleb", "John", "Maria"])

print("Caleb" in team)  # True
print("David" in team)  # False
```

The expression:

```python
"Caleb" in team
```

can call:

```python
team.__contains__("Caleb")
```

---

### 6. `if object:` → `__bool__`

When Python evaluates an object in a Boolean context:

```python
if object:
    ...
```

Python uses `__bool__` to determine whether the object should be considered **true or false**.

> **Protocol:** Truthiness

Example:

```python
class User:
    def __init__(self, name):
        self.name = name

    def __bool__(self):
        return bool(self.name)


user = User("Caleb")

if user:
    print("User has a name")
```

Since `"Caleb"` is a non-empty string, `bool(self.name)` returns `True`.

If the name were empty:

```python
user = User("")
```

then:

```python
bool(user)
```

would return `False`.

The key idea is:

> **`__bool__` lets you decide when an object should be considered truthy or falsy.**

If `__bool__` is not defined, Python can fall back to `__len__`: an object with length `0` is considered falsy, while an object with a non-zero length is truthy.

---

## `__call__`: Two Distinct Moments in an Object's Life

`__init__` and `__call__` may look similar because both can receive arguments, but they answer **different questions**.

```python
filter = Filter(10)  # __init__ runs ONCE, when the object is created

filter(15)           # True
filter(5)            # False
```

Every time `filter(...)` is used, `__call__` runs again.

---

### `__init__`: Configure the Object

`__init__` is triggered when an object is created:

> **"I just created this object. How should I configure it?"**

```python
def __init__(self, minimum):
    self.minimum = minimum
```

Key points:

- Receives **constructor arguments**: `Filter(10)` → `minimum = 10`
- Stores state in `self`
- Does not explicitly return a value
- Runs once for each new instance

---

### `__call__`: Use the Object

`__call__` is triggered when `()` is placed after an object:

> **"Someone called this object. What should I do?"**

```python
def __call__(self, number):
    return number > self.minimum
```

Key points:

- Receives **call arguments**: `filter(15)` → `number = 15`
- Uses the state already stored in `self`
- Returns a result
- Can be called as many times as needed

### Complete Example

```python
class Filter:
    def __init__(self, minimum):
        self.minimum = minimum

    def __call__(self, number):
        return number > self.minimum


filter = Filter(10)

print(filter(15))  # True
print(filter(5))   # False
print(filter(20))  # True
```

The important distinction is:

```text
Filter(10)
   ↓
__init__(10)
   ↓
Store minimum = 10
```

Then:

```text
filter(15)
   ↓
__call__(15)
   ↓
Compare 15 > 10
   ↓
True
```

---

## Standard Method vs. `__call__`

### Using a Standard Method

You can achieve the same behavior with a regular method:

```python
class Filter:
    def __init__(self, minimum):
        self.minimum = minimum

    def check(self, number):
        return number > self.minimum


filter = Filter(10)

print(filter.check(15))  # True
print(filter.check(5))   # False
```

Here, you explicitly call the `check()` method.

### Using `__call__`

```python
class Filter:
    def __init__(self, minimum):
        self.minimum = minimum

    def __call__(self, number):
        return number > self.minimum


filter = Filter(10)

print(filter(15))  # True
print(filter(5))   # False
```

Here, the object itself behaves like a function.

---

## When Should You Use `__call__`?

Use a **standard method** when the object has several different operations and you want each operation to have a clear name:

```python
user.save()
user.delete()
user.validate()
```

Use `__call__` when the **main purpose of the object is to perform one operation**, especially when the object needs to remember some configuration or state.

For example:

```python
filter = Filter(10)

filter(15)
filter(20)
filter(3)
```

This is useful for things such as:

- Filters
- Validators
- Predictors
- Callbacks
- Function-like objects
- Configurable processing steps

### Simple Rule

> **`__init__` configures the object. `__call__` makes the object do something.**

```text
Filter(10)   → __init__  → configure the object
filter(15)   → __call__  → use the configured object
```

---

## `__enter__` / `__exit__`: The Protocol You Were Already Using Without Realizing It

Every time you write `with`, two dunder methods are involved:

```python
with open("file.txt") as file:
    content = file.read()
```

You may have used this pattern many times without thinking about what happens behind the scenes.

The file is opened, you use it inside the `with` block, and Python automatically closes it when the block ends—even if an exception occurs while reading the file.

The object returned by `open()` supports the context manager protocol by implementing `__enter__` and `__exit__`.

---

## What Does `with` Actually Do?

Conceptually, this:

```python
with open("file.txt") as file:
    content = file.read()
```

works roughly like this:

```text
1. Create the file object
        ↓
2. Call __enter__()
        ↓
3. Assign the returned value to file
        ↓
4. Execute the with block
        ↓
5. Call __exit__()
        ↓
6. Clean up the resource
```

The important part is that `__exit__` is called when Python leaves the `with` block, **whether the block finishes normally or an exception occurs**.

---

## Complete Example Using `__enter__` and `__exit__`

```python
class Resource:
    def __enter__(self):
        print("Opening resource")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing resource")


with Resource() as resource:
    print("Using resource")
```

Output:

```text
Opening resource
Using resource
Closing resource
```

Here:

```python
__enter__()
```

runs when Python enters the `with` block.

```python
__exit__()
```

runs when Python leaves the block.

The value returned by `__enter__` is assigned to the variable after `as`:

```python
with Resource() as resource:
```

So:

```python
resource
```

refers to the value returned by:

```python
__enter__()
```

---

## What Happens If an Exception Occurs?

`__exit__` is still called:

```python
class Resource:
    def __enter__(self):
        print("Opening resource")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Closing resource")
        print(f"Exception: {exc_value}")


with Resource() as resource:
    print("Using resource")
    raise ValueError("Something went wrong")
```

Output:

```text
Opening resource
Using resource
Closing resource
Exception: Something went wrong
```

This is one of the main reasons context managers are useful: **cleanup happens reliably even when something goes wrong.**

---

## What Are `__enter__` and `__exit__` Actually For?

They are used to **automatically set up and clean up resources or temporary states**.

### `__enter__`

Runs when entering the `with` block.

Typical responsibilities:

- Open a resource
- Acquire a lock
- Start a transaction
- Establish a connection
- Prepare a temporary state

### `__exit__`

Runs when leaving the `with` block.

Typical responsibilities:

- Close a resource
- Release a lock
- Roll back or commit a transaction
- Close a connection
- Restore or clean up temporary state

A simple way to remember it:

> `__enter__` → **Set things up**  
> `__exit__` → **Clean things up**

---

## Why Is `__enter__` / `__exit__` a Protocol?

It is a **protocol** because Python does not require you to inherit from a specific class.

The `with` statement does not care what your class is called or how it is implemented.

It only cares whether the object follows the expected contract:

```python
__enter__()
__exit__()
```

If an object provides these methods, Python can use it as a context manager.

For example, both of these can work with `with`:

```python
with open("file.txt") as file:
    ...
```

and:

```python
with Resource() as resource:
    ...
```

They are completely different objects, but they follow the same **context manager protocol**.

### The Key Idea

> **A protocol is a set of methods and behaviors that an object must provide to work with a particular Python operation.**

For the `with` statement:

```text
with object:
      ↓
__enter__() → set up
      ↓
execute block
      ↓
__exit__() → clean up
```

So you can think of `__enter__` and `__exit__` as the **contract that allows an object to work with `with`**.

---

## `__getitem__` Allows Your Object to Use `[ ]`

The `__getitem__` method allows your custom object to respond to the `[]` operator.

Conceptually:

```python
object[something]
```

becomes:

```python
object.__getitem__(something)
```

This lets you decide what should happen when someone puts something inside the brackets.

### Example

```python
class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __getitem__(self, index):
        return self.songs[index]


playlist = Playlist(["Song A", "Song B", "Song C"])

print(playlist[0])  # Song A
print(playlist[1])  # Song B
```

Here:

```python
playlist[0]
```

calls:

```python
playlist.__getitem__(0)
```

---

## `__getitem__` Treats Your Class Like a Collection

You decide what the brackets mean for your object.

`__getitem__` can support indexes, slices, keys, or other types of access depending on how you implement it.

### Example with a Dictionary

```python
class Person:
    def __init__(self, name, age):
        self.data = {
            "name": name,
            "age": age
        }

    def __getitem__(self, key):
        return self.data[key]


person = Person("Caleb", 27)

print(person["name"])  # Caleb
print(person["age"])   # 27
```

Now your object behaves somewhat like a dictionary:

```python
person["name"]
```

calls:

```python
person.__getitem__("name")
```

> **Key idea:** `__getitem__` lets you define what `object[...]` means for your class.

---

## `__contains__` Defines What `"in"` Means for Your Object

The `__contains__` method allows you to define how membership checking works.

Conceptually:

```python
x in object
```

becomes:

```python
object.__contains__(x)
```

### Example

```python
class Team:
    def __init__(self, members):
        self.members = members

    def __contains__(self, name):
        return name in self.members


team = Team(["Caleb", "Maria", "John"])

print("Caleb" in team)  # True
print("David" in team)  # False
```

When Python evaluates:

```python
"Caleb" in team
```

it uses:

```python
team.__contains__("Caleb")
```

The method decides whether the value is considered a member of the object.

> **Key idea:** `__contains__` lets you define what membership means for your class.

---

## `__bool__` Defines What It Means for Your Object to Be True

The `__bool__` method controls whether an object is considered **truthy or falsy** when Python evaluates it in a Boolean context.

For example:

```python
if object:
    ...
```

uses the object's Boolean value.

If `__bool__` is defined, Python calls:

```python
object.__bool__()
```

### Example

```python
class ShoppingCart:
    def __init__(self, items):
        self.items = items

    def __bool__(self):
        return len(self.items) > 0


cart = ShoppingCart(["Laptop"])

if cart:
    print("The cart has items")
```

Since the cart contains an item, `__bool__` returns `True`.

If the cart is empty:

```python
empty_cart = ShoppingCart([])

if empty_cart:
    print("The cart has items")
else:
    print("The cart is empty")
```

Output:

```text
The cart is empty
```

> **Key idea:** `__bool__` lets you define when an object should be considered **True or False**.

### Quick Map

| Python syntax | Dunder method | Purpose |
|---|---|---|
| `object[something]` | `__getitem__` | Define bracket access |
| `x in object` | `__contains__` | Define membership |
| `if object` | `__bool__` | Define truthiness |

