---
title: Classes and Objects
tags: 
  - name: Python Classes
    link: https://docs.python.org/3/tutorial/classes.html
  - name: Dataclasses Documentation
    link: https://docs.python.org/3/library/dataclasses.html
  - name: Understanding Dataclasses
    link: https://www.geeksforgeeks.org/understanding-python-dataclasses/
  - name: Decorator
    link: https://pythonbasics.org/decorators/
---
Here I'll go into the basics of working with classes and objects in Python. This is not an exhaustive treatment, but should be enough to give you the basics, and should be enough to make my AoC solutions easier to follow.

## Page Contents

- [What is a Class? What is an Object?](#what-is-a-class-what-is-an-object)
- [Object-Oriented Programming (OOP)](#object-oriented-programming-oop)
- [Defining a Class](#defining-a-class)
- [Comparing Objects](#comparing-objects)
- [Dataclass](#dataclass)

## What is a Class? What is an Object?

Think of a _class_ as a blueprint.  It is the blueprint of a _thing_, where that thing has:

- State - called _attributes_.
- Behaviour - called _methods_.

So a class is kind of an abstract concept. But we can create an _instance_ of the class; think of it as building something according to the blueprint. The instance is called an _object_.

Time for an analogy:

- The _Ford Motor Company_ have a blueprint for creating a _Ford Mustang_. It is a design. A specification. This is analagous to a **class**.
- I own a _Ford Mustang_.  It is a real, physical thing.  I can sit in it and drive it.  So, _my_ Mustang is an _instance_ of the Ford Mustang class.  My Ford Mustang is an **object**.

### Attributes

The Ford Mustang class has some **attributes**, e.g.

- It has four wheels.
- It has two doors.
- It has a 5L V8 engine.
- It is right-hand-drive.

Attributes are just variables.  But they are variables that scoped to the class or object. The attributes above would typically be defined as _class attributes_, because any instance of this class will have these same attributes.

_My_ Ford Mustang has some additional **attributes**, e.g.

- It is three years old.
- It has 10000 miles on the clock.
- It has a service due in June.

These are called _instance attributes_ or _object attributes_, because they are unique to _my Mustang_.

### Methods

A _Mustang_ can do some things...

- It can accelerate.
- It can break.
- It can turn.

All of these would be implemented as _methods_. Methods are just functions; but they are functions that are scoped to the object (or class).

## Object-Oriented Programming (OOP)

In simplistic terms, this is simply a way of programming where we primarily use classes and objects to represent _things_, and we interact with classes and objects using the methods they expose.

In OOP, there are some standard concepts:

- **Inheritance** - I.e. where an object can inherit - and override - the properties and methods from some sort of ancester, called a _base class_.  Using our simple analogy again:
  - `Vehicle` is a very abstract thing. It can accelerate, decelerate, and turn.
  - `Car` is a **subclass** (i.e. inherits from or **extends**) Vehicle.  A `Car` adds some additional attributes and methods.  E.g. a `Car` has four wheels.  Whereas a `Bike` has two.
  - `Mustang` is a **subclass** (i.e. inherits from or **extends**) of `Car`.  It adds some additional attributes and methods.  For example, it has two doors.  It is made by _Ford_.
  - `Mustang 5.0GT`  is a **subclass** (i.e. inherits from or **extends**) of `Mustang`.  It adds some additional attributes and methods.  For example, it has a 5L V8 engine.
- **Polymorphism** - the idea that different objects can have the same _method signatures_, and exhibit different behavours at runtime, depending on the specific type of class that was instantiated.
- **Encapsulation** - the idea that an object can hide its internal implementation, so that we only interact with the object using its publicly accessible interface.  In Python, _encapsulation_ is not enforced, but there are _conventions_ we should follow.  E.g. if an _attribute_ or _method_ should not be used by anything other than the object itself, then we prefix the _attribute_ or _method_ with an `_` (underscore) character.

## Defining a Class

Here we use the simple example of a `Dog` class:

```python
class Dog():
    """ A Dog class """
    
    def __init__(self, name: str) -> None:
        """ How we create an instance of Dog.

        Args:
            name (str): The name of the dog
        """
        
        self._name = name   # note how this is intended to be a private instance attribute
        
    # Use the @property decorator to provide a public interface to a method, that resembles an attribute.
    # E.g. we can just reference my_dog.name, rather than my_dog.name().
    @property
    def name(self):
        """ The dog's name """
        return self._name
    
    def bark(self):
        return "Woof!"
    
    def __repr__(self) -> str:
        """ Unambiguously identify an instance. """
        return f"Dog(name={self._name})"
    
    def __str__(self) -> str:
        """ Friendly humand-readable representation of the instance """
        return f"Dog {self._name}"
```

Some notes:

- The class definition starts with \
`class SomeClassName():`
- Whilst Python typically uses _snake_case_ for all names (e.g. `my_variable_name`), _upper camel case_ is used for class names (e.g. `MyClassName`).
- Note that **ALL** instance variables and instance methods must be prefixed with `self`, in the class.
- Method definitions must always have `self` as the first argument. However, when we call these methods, the `self` is implicit.
- We use the `__init__()` method to initialise any new instances of a class. I.e. whenever we create a new `Dog`, this is the method that gets called. We can define which attributes are required (or are optional) to the initialiser.
- In our Dog's `__init__()`, we expect a single explicit parameter to be passed, which is the `name` of the `Dog`. We're using _type hinting_ to tell the Python compiler that the `name` argument should be a `str`.  If we try to run code that passes anything else, our _linter_ will warn us we've probably done something wrong.
- The `__init__()` method initialises a single instance variable when an instance (object) is created. This is the `_name` instance variable.  Note that it is intended to be a private variable.
- We provide a method called `name()` which returns the name of a Dog instance. However, to make it easier to get our Dog's name, we can use the `@property` decorator to expose the name as if it were a public attribute.
- We define a `__repr__()` method that can be used to unambiguously identify a given instance.  This can be useful in debugging.
- We define a `__str__()` method, which is used to generate a friendly, human-readable representation of our `Dog`.

To exercise our `Dog` class:

```python
dog_a = Dog("Fido") # Create a new dog
dog_b = Dog("Henry") # Create another dog

print(dog_a)    # Print using __str__
print(repr(dog_a))  # Print using __repr__
print(f"dog_a is named {dog_a.name}")  # Get the name using the property
print(dog_a.bark())  # Test the bark() method. Note that we don't pass "self". It is implicit.

print(f"dog_b is named {dog_b.name}")
dog_a.bark()
print(dog_a.bark())
```

The output looks like this:

```text
Dog Fido
Dog(name=Fido)
dog_a is named Fido
Woof!
dog_b is named Henry
Woof!
```

## Comparing Objects

- For objects to be comparable using `==`, we need to implement the `__eq__()` method.
- For objects to be checked in a _Collection_, - e.g. using `if thing in things` - then we also need to implement the `__hash__()` method.  This should always return a different `int` value for any unequal instances of immutable objects. (Mutable objects are unhashable).  Common ways to achieve such as hash include:
  - Returning a `hash` of a `tuple` (since tuples are immutable) of some instance attributes.
  - Returning a `hash` of the `__repr__()`, assuming that `__repr__()` returns a unique value for different objects.

E.g. here I'll create a `Point` class, which represents a point in two-dimensional space.  A `Point` is created from an `(x,y)` coordinate pair:

```python
from __future__ import annotations

class Point():
    """ Point class, which stores x and y """
        
    def __init__(self, x:int, y:int) -> None:
        self._x = x
        self._y = y
        
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, o: Point) -> bool:
        return self.x == o.x and self.y == o.y
        
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return f"({self._x}, {self._y})"
    
# Now let's test our Point class...
point_a = (5, 10)
print(point_a)
point_b = (6, 5)
print(point_b)
point_c = (5, 10)
print(point_c)

print(f"point_a == point_b? {point_a == point_b}")
print(f"point_a == point_c? {point_a == point_c}")

points = set()
points.add(point_a)

if point_b in points:
    print("point_b already in points")
    
if point_c in points:
    print("point_c already in points")
```

Output:

```text
point_a == point_b? False
point_a == point_c? True
point_c already in points
```

Note the `import` of `annotations` from `__future__`. This allows us to reference a type that has not yet been defined. E.g. where we reference a `Point` argument in method definitions in the `Point` class.  Without this import, trying to run the code above results in this:

```text
Traceback (most recent call last):
  File "f:\Users\Darren\localdev\Python\Advent-of-Code\src\snippets\scratch.py", line 3, in <module>
    class Point():
  File "f:\Users\Darren\localdev\Python\Advent-of-Code\src\snippets\scratch.py", line 21, in Point
    def __eq__(self, o: Point) -> bool:
NameError: name 'Point' is not defined
```

## Dataclass

This is a very cool _decorator_ which helps us save some time and effort, by circumventing the need to write lots of repetetive [boilerplate code](https://en.wikipedia.org/wiki/Boilerplate_code){:target="_blank"}, when we want to create a _class_ that mostly serves the purpose of storing and exposing some data.

Cool things about a `dataclass`:

- The `__init__()` method is created implicitly for us. All we need to do is define the variables that we want to be initialised when the object is created.
- Defaults can be easily specified for our instance variables.
- They can be _mutable_ or _immmutable_. We define a `dataclass` as _immutable_ by simply adding `frozen=True`. If we then try to change an instance variable, a `TypeError` will be thrown.
- If we make `eq=True` (which is the _default_), then an implicit `__eq__()` method is created for us, which compares objects by generating a `tuple` from all its fields.  But we can even specify which fields to include in the comparison, and which to ignore!
- If we make both `eq=True` and `frozen=True`, then an implicit `__hash__()` method is created for us.

To make something a `dataclass`, simply add `@dataclass` before the class definition. You will also need to import `dataclass`.

Now I'll recreate the above `Point` class, and call it in _exactly the same way_, but this time implement as a `dataclass`.  Look how much shorter it is!!

```python
from dataclasses import dataclass

@dataclass
class Point():
    """ Point class, which stores x and y """
    x: int
    y: int

# Now let's test our Point class...
point_a = (5, 10)
print(point_a)
point_b = (6, 5)
print(point_b)
point_c = (5, 10)
print(point_c)

print(f"point_a == point_b? {point_a == point_b}")
print(f"point_a == point_c? {point_a == point_c}")

points = set()
points.add(point_a)

if point_b in points:
    print("point_b already in points")
    
if point_c in points:
    print("point_c already in points")
```