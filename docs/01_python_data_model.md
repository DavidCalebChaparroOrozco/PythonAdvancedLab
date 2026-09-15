# Protocols

The contract required by an operation.

A list of **requirements** an object must meet to participate in a specific **operation**.

## It is informal:
There is no class to inherit from and no file to import. It is a **specification**, usually described only in the documentation.

> ``` python
> object.__len__(self)
> ```
> Invoked to implement `len()`. It must return the object's length—an integer ≥ 0.

## The promise it makes
Every protocol follows the same pattern, filling in the blanks:

- **IF**: Your object has *these methods*, with this signature and this expected behavior...

- **THEN**: It can be used in **this operation**.

## One per operation:
- len(obj) → length
- obj[0] → indexing
- for x in obj → iteration
- obj == other → comparison
- obj() → calling
- with obj → context

## A complete, end-to-end example
The protocol acts as the bridge between the operation you write and the method you implement.

### The operation
```python
len(obj)
```
- len("hello")
- len([1, 2, 3])
- len(box)

A built-in function. It doesn't know what `obj` is; it only knows what it requires from it.

### The specification
Informally, it states:
- Provide a `__len__(self)` method
- That accepts only `self`
- And returns an integer >= 0
> Nothing else. No inheritance, no imports, no registering anywhere.

That is the **entire** protocol.

### The special method
```python
class Box:
    def __len__(self):
        return 5


box = Box()
print(len(box))  # Result: 5
```

It meets all three requirements. From that point on, `len(box)` works.

> Any object that satisfies that condition works with `len()`. It doesn't matter if it's a `list`, a `str`, your `Deck` class, or one that models an aquarium.
---

# Python Data Model

All the rules for all the operations

The set of **ALL** rules for **ALL** operations across all of Python.

- It is the **complete specification:** it defines how objects can interact with language features.

- It describes—**for every existing language feature**—the behavior an object must provide to participate in it.

> These are the rules that allow your objects to behave like Python objects.

## Data Model
defines how an object should behave when...
- len() → __len__
- [] → __getitem__
- + → __add__
- == → __eq__
- ...

> Each row in this table is a protocol.

---

# Special Methods

The actual code that implements the protocol
A method with a **name reserved** by Python, which the language invokes **automatically** when you perform an operation on your object.
- special method
- dunder method
- magic method
> Three names for exactly the same thing

## Example: `__str__`
The __str__ method controls what text appears when you print an object. 

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"A dog named {self.name}"


my_dog = Dog("Buddy")
print(my_dog)  # Automatically calls my_dog.__str__()

# Output: A dog named Buddy
```

Without __str__, printing my_dog would just output a messy memory address like `<__main__.Dog object at 0x...>`.

---

