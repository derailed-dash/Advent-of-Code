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
  - name: Inheritance
    link: https://www.geeksforgeeks.org/inheritance-in-python/
  - name: Enum
    link: /python/enumerate#enum
---
Here I'll go into the basics of working with classes and objects in Python. This is not an exhaustive treatment, but should be enough to give you the basics, and should be enough to make my AoC solutions easier to follow.

## Page Contents

- [What is a Class? What is an Object?](#what-is-a-class-what-is-an-object)
  - [Attributes](#attributes)
  - [Methods](#methods)
- [Object-Oriented Programming (OOP)](#object-oriented-programming-oop)
- [Defining a Class](#defining-a-class)
- [Instance vs Class](#instance-vs-class)
  - [Attributes](#attributes-1)
  - [Methods](#methods-1)
- [Comparing Objects and Hashing](#comparing-objects-and-hashing)
- [Dataclass](#dataclass)
- [Inheritance](#inheritance)
- [Factory Pattern](#factory-pattern)
- [Examples](#examples)

## What is a Class? What is an Object?

Think of a _class_ as a blueprint.  It is the blueprint of a _thing_, where that thing has:

- **State** - called _attributes_.
- **Behaviour** - called _methods_.

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

- **Inheritance** - I.e. where an object can inherit - and override - the properties and methods from some sort of ancester, called a _parent class_.  We'll look at this in a bit more detail [later](#inheritance).
- **Polymorphism** - the idea that different objects can have the same _method signatures_, and exhibit different behavours at runtime, depending on the specific type of class that was instantiated.
- **Encapsulation** - the idea that an object can hide its internal implementation, so that we only interact with the object using its publicly accessible interface.  In Python, _encapsulation_ is not enforced, but there are _conventions_ we should follow.  E.g. if an _attribute_ or _method_ should not be used by anything other than the object itself, then we prefix the _attribute_ or _method_ with an `_` (underscore) character.

## Defining a Class

Here we use the simple example of a `Dog` class:

```python
class Dog():
    """ A Dog class """
    
    def __init__(self, name: str) -> None:
        """ How we create an instance of Dog. """s
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
- We use the `__init__()` method to _initialise_ any new instances of a class. I.e. whenever we create a new `Dog`, this is the method that gets called. We can define which attributes are required (or are optional) to the initialiser.
- In our Dog's `__init__()`, we expect a single explicit parameter to be passed, which is the `name` of the `Dog`. We're using _type hinting_ to tell the Python compiler that the `name` argument should be a `str`.  If we try to run code that passes anything else, our _linter_ will warn us we've probably done something wrong.
- The `__init__()` method initialises a single instance variable when an instance (object) is created. This is the `_name` instance variable.  Note that it is intended to be a private variable.
- We provide a method called `name()` which returns the name of a Dog instance. However, to make it easier to get our Dog's name, we can use the `@property` decorator to expose the name as if it were a public attribute.
- We define a `__repr__()` method that can be used to unambiguously identify a given instance.  This can be useful in debugging. The example below shows how we can introspection to get the name of this class: \

```python
def __repr__(self) -> str:
    return f"{self.__class__.__name__}(name={self._name})"
```
- We define a `__str__()` method, which is used to generate a friendly, human-readable representation of our `Dog`. Note that if a `__str__()` method has not been defined, Python will fall back on the `__repr__()`, if it is defined.

To use our `Dog` class:

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

## Instance vs Class

### Attributes

_Instance attributes_ belong to a specific instance of a class, i.e. a specific object. Whereas _class attributes_ belong to the class; this value is common across all instances of the class.

**Instance attributes** are prefixed with `self`.  They should generally be initialised in the `__init__()` method. If instance attributes will be set in a different method, then consider first initialising them to `None` in the `__init__()` method.

**Class attributes** are defined outside of any method, and do not include a `self` prefix.

Here's a couple of scenarios where we might want to use a **class attribute**:

```python
class MyClass():
    id = 0
    brand = "Foo"
    
    def __init__(self) -> None:
        self.id = MyClass.id
        MyClass.id += 1
        
my_instance_1 = MyClass()
print(f"ID: {my_instance_1.id}, brand: {MyClass.brand}")
my_instance_2 = MyClass()
print(f"ID: {my_instance_2.id}, brand: {MyClass.brand}")
```

Here's the output:

```text
ID: 0, brand: Foo
ID: 1, brand: Foo
```

### Methods

Similarly, it is possible for methods to _instance_, _class_ methods, or even _static_ methods.

|Method Type|How to Define|How to Use|Example Use Case|
|-----------|-------------|----------|----------------|
|Instance|`def some_method(self, parms...)`|From within the class using `self.some_method(parms)`; from outside the class using `my_instance.some_method(parms)`|Methods that need access to **instance attributes**.|
|Class|`def some_method(cls, parms...)` and decorate with `@classmethod`|From within or outside the class using `MyClass.some_method(parms)`|Methods that need access only to **class attributes**. E.g. to implement a _factory method_.|
|Static|`def some_method(parms...)` and decorate with `@staticmethod`|From within or outside the class using `MyClass.some_method(parms)`|Methods that have **no need to access or modify either class _or_ instance attributes**, but are otherwise logically linked to the _class_. This means that we could actually implement this method outside of the class; but it makes sense to method definition within the class.|

## Decorating Methods

_Private_ (implementation) attributes can be named using the prefix `_`, to discourage direct modification.  However, this is convention only. We could then provide `get` and `set` methods to access this private attribute. However, this is not considered _Pythonic_. Remember: `Python ≠ Java`!!

The alternative is to use the `@property` decorator. This decorator makes a method accessible as if it were a property. This property helps ensure that only the _public_ implementation is used. For example, where we may want to apply some validation or business logic when assigning a value to a property.

In this example, we make the `_age` attribute accessible using a `@property` method called `age`.  We simply reference age as if it were an attribute, not a method.

```python
class MyClass:
    
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age
        
    def __repr__(self):
        return f"{self._name}: {self._age}"
        
    @property
    def age(self):
        return self._age
    
if __name__ == "__main__":
    bob = MyClass("Bob", 20)
    
    print(bob)
    bob.age = 21
    print(bob)
```

## Printing and Representing

### Short Version

- Always define `__repr__()` for a class.  The default implementation of `__repr__()` is not very useful.  
- The `__repr__()` method is for unambiguously representing the object.
  - Useful for developers and debugging.
  - Retrieve this using `repr(my_object)`. E.g. `print(repr(my_object))`.  
- The `__str__()` method is for friendly printing.
  - Retrieve this using `print(my_object)`.
  - If no `__str__()` has been implemented, Python will fallback on `__repr__()`.

### Example

```python
class Point2D:

    def __init__(self, x, y) -> None:
        self._x = x
        self._y = y
        
    def __repr__(self) -> str:
        return "Point2D(x={}, y={})".format(self._x, self._y)
```

Or we can do this:

```python
def __repr__(self) -> str:
    return f"{self.__class__.__name__}(x={self._x}, y={self._y})"
```

## Comparing Objects and Hashing

- For objects to be comparable using `==`, we need to implement the `__eq__()` method. 
  - If we don't do this then the `==` operator compares _identity_ rather than _equality_. Identity means: is one object the exact same instance (i.e. occupying the same space in memory) as another?
  - _Equality_ means: are these equivalent, based on rules we define.
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

## Inheritance

### Overview

Recall that inheritance is an OO concept that allows a class to inherit properties and behaviour from a parent class. Inheritance is used to create an _is-a_ relationship between classes.

Using our simple analogy again:

  - `Vehicle` is a very abstract thing. It can accelerate, decelerate, and turn.
  - `Car` is a **subclass** (i.e. inherits from or **extends**) Vehicle.  A `Car` adds some additional attributes and methods.  E.g. a `Car` has four wheels.  Whereas a `Bike` has two.
  - `Mustang` is a **subclass** (i.e. inherits from or **extends**) of `Car`.  It adds some additional attributes and methods.  For example, it has two doors.  It is made by _Ford_.

The class we inherit from is called a _parent_ class.  The class that inherits from this _parent_ class is known as any of: _child_ class, _subclass_ or _descendent_.

In Python, the syntax for inheriting is:

```python
class MyChildClass(MyParentClass):
    # code
```

Some general notes on inheritance:

- Inheritance is explicitly defined by placing the parent classes in parentheses, at the end of the class definition.  A given subclass can inherit from more than one parent class.
- Subclasses inherit all methods of any parent classes.
- The base classes for a subclass can be obtained in the form of a tuple, using `__bases__`.
- Initialisers:
  - If a subclass does not define an initialiser (an `__init__()` method), then the initialiser of the base class is called automatically.
  - However, consider being explicit; if you want to call a base class initialiser, then do so explicitly using `super()`. 
- When inheriting from multiple parent classes, _method resolution order (MRO)_ is used to resolve methods at run time.  We can return this for a class using __mro__, or using the `mro()` method. It is dependent on base class definition order. Subclasses come before base classes.

Here's a simple inheritance example:

```python
class Foo:
    def __init__(self) -> None:
        print("Initialising a Foo")
    
    def do_foo(self):
        print(f"{self.__class__.__name__}: I know how to foo")
    
    def __repr__(self):
        return f"I am a {self.__class__.__name__}"
    
class Bar(Foo):
    def __init__(self) -> None:
        super().__init__()
        print("Initialising a Bar")
        
    def do_bar(self):
        print(f"{self.__class__.__name__}: I know how to bar")
    
    def __repr__(self):
        return f"I am a {self.__class__.__name__}"

print("Let's create a Foo...")
foo = Foo()
print(foo)
foo.do_foo()
# foo.do_bar() - We can't do this!

print("\nLet's create a Bar...")
bar = Bar()
print(bar)
bar.do_bar()
bar.do_foo() # Inherited from parent class!
```

Here's the output:

```text
Let's create a Foo...
Initialising a Foo
I am a Foo
Foo: I know how to foo

Let's create a Bar...
Initialising a Foo
Initialising a Bar
I am a Bar
Bar: I know how to bar
Bar: I know how to foo
```

### Abstract Base Class (ABC)

We use `ABC` where we want to provide some methods and/or attributes in a parent class, but it should not be possible to instantiate the parent class. I.e. the parent class is an _abstract concept_. And we would use this where we want to enforce that certain methods are implemented in a concrete implementation.

For example:

```python

from abc import ABC, abstractmethod
import math

class Shape(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def calc_area(self):
        pass

    def __str__():
        return "Shape"

class Circle(Shape):
    def __init__(self, radius):
        self._radius = radius

    def calc_area(self):
        return math.pi * self._radius**2
    
    def __str__(self):
        return f"Circle of radius {self._radius}"
    
    def __repr__(self):
        return f"Cicle(radius={self._radius})"

class Square(Shape):
    def __init__(self, side):
        self._length = side
        self._height = side

    def calc_area(self):
        return self._length * self._height

try:
    shape = Shape()
except TypeError as e:
    print(e)

circle = Circle(10)
print(circle.calc_area())

square = Square(10)
print(square.calc_area())
```

Output:

```text
Can't instantiate abstract class Shape without an implementation for abstract method 'calc_area'
314.1592653589793
100
```

### Multiple Inheritance

Python supports inheriting from multiple base classes. But be careful if base classes have common methods or properties. The method that gets chained from the subclass depends on a thing called _Method Resolution Order (MRO)_.

Example:

```python
class Class_A():
    def __init__(self):
        self._prop_a = "prop a"
        self._common_prop = "from a"
    
    def __str__(self):
        return f"{self._prop_a=}, {self._common_prop=}"

class Class_B():
    def __init__(self):
        self._prop_b = "prop b"
        self._common_prop = "from b"

    def __str__(self):
        return f"{self._prop_b=}, {self._common_prop=}"

class Class_C(Class_A, Class_B):
    pass

class Class_D(Class_B, Class_A):
    pass

my_c = Class_C()
print(my_c)

my_d = Class_D()
print(my_d)

# View MRO
print(Class_D.__mro__)
```

Output:

```text
self._prop_a='prop a', self._common_prop='from a'
self._prop_b='prop b', self._common_prop='from b'
(<class '__main__.Class_D'>, <class '__main__.Class_B'>, <class '__main__.Class_A'>, <class 'object'>)
```

### Interfaces

Interfaces are a mechanism for defining a "contract" that should be implemented by a class. I.e. the methods that a class must implement. 

In most OO languages it is not possible to subclass more than one base class, but it is possible to implement more than one interface. Python is a little different. It offers two approaches to providing interface-like capability:

- ABC
- Duck typing

#### ABC

As described previously, we can extend ABC and define abstract methods that must be implemented in the subclass.

Best practice: Define one or more classes that extend ABC, providing one or more abstract methods that we want to treat as an interface.

#### Duck Typing

"If it looks like a duck and quacks like a duck, it's a duck."

If the subclass provides the required methods, it is treated as implementing the interface. However, this is not strict enforcement.

#### Protocols

Python also has the concept of _protocols_.  A protocol is a set of operations or methods that a type must support, in order to implement that protocol.  All that is required to support a protocol is for the class to implement the necessary operations. This uses duck typing against a documented set of methods.

For example, take a look at [Collection Protocols](https://docs.python.org/3/library/collections.abc.html){:target="_blank"}.

## The Object Class

Object is the ultimate base class for all classes in Python.  Any class defined without an explicit base class, will extend object.

## Magic Methods

These are a set of methods associated with any object, which can be overridden. The take the form `__method__()`. For example, we can see the magic methods for the `object` class by during `dir(object)`:

```python
['__class__',
 '__delattr__',
 '__dir__',
 '__doc__',
 '__eq__',			# ==
 '__format__',
 '__ge__',			# >=
 '__getattribute__',      # runs whenever a variable is retrieved
 '__gt__',			# >
 '__hash__',
 '__init__',
 '__init_subclass__',
 '__le__',			# <=
 '__lt__',			# <
 '__ne__',			# !=
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',			# unambiguous representation
 '__setattr__',           # Runs whenever an attribute is set
 '__sizeof__',
 '__str__',			# str representation
 '__subclasshook__']
```

For example, we can implement equality like this:

```python
def __eq__(self, other):
  if isinstance(other, ThisClass):
    return (self.prop == other.prop ... )
  
  return NotImplemented
```

## Factory Pattern

The factory pattern is a creation design pattern that provides an interface for creating objects in a way that abstracts the instantiation logic. It is particularly well-suited to scenarios where we want to implement objects with different initial properties, but otherwise have identical behaviour.

It is typically implemented using a _classmethod_ that allows us to pass in a type, i.e. a specific type of object implementation.

Here I show a useful way to instantiate a class using factory method. In the example below, one factory method instantiates a `Shape` given a `ShapeType` (which is itself a subclass of [Enum](/python/enum)). Another factory method allows us to instantiate a `Shape` given a set of points.

```python
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ShapeType(Enum):
    HLINE =       {(0, 0), (1, 0), (2, 0), (3, 0)}
    PLUS =        {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}
    BACKWARDS_L = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}
    I =           {(0, 0), (0, 1), (0, 2), (0, 3)}
    SQUARE =      {(0, 0), (1, 0), (0, 1), (1, 1)}    

@dataclass(frozen=True)
class Point():
    """ Point with x,y coordinates and knows how to add a vector to create a new Point. """
    x: int
    y: int
    
    def __add__(self, other):
        """ Add other point/vector to this point, returning new point """
        return Point(self.x + other.x, self.y + other.y)     
    
    def __repr__(self) -> str:
        return f"P({self.x},{self.y})"

class Shape():
    """ Stores points that make up this shape. 
    Has a factory method to create Shape instances based on shape type. """
    
    def __init__(self, points: set[Point], at_rest=False) -> None:
        self.points: set[Point] = points   # the points that make up the shape
        self.at_rest = at_rest
    
    @classmethod
    def create_shape_by_type(cls, shape_type: str, origin: Point):
        """ Factory method to create an instance of our shape.
        The shape points are offset by the supplied origin. """
        return cls({(Point(*coords) + origin) for coords in ShapeType[shape_type].value})

    @classmethod
    def create_shape_from_points(cls, points: set[Point], at_rest=False):
        """ Factory method to create an instance of our shape.
        The shape points are offset by the supplied origin. """
        return cls(points, at_rest)
    
    def __str__(self):
        return f"Shape:({self.points})"

start = Point(0,0)
my_shape = Shape.create_shape_by_type(ShapeType.PLUS.name, start)
print(my_shape)
```

Another example:

```python
class KeypadMapping():
    NUMERIC = "numeric"
    DIRECTION = "direction"
   
    POINTS_FOR_DIRECTIONS = { "^": Point(0, -1),
                              "v": Point(0, 1),
                              "<": Point(-1, 0),
                              ">": Point(1, 0) }
   
    DIRECTIONS_FOR_POINTS = {v: k for k, v in POINTS_FOR_DIRECTIONS.items()}


    NUMERIC_KEYPAD = [
         ["7", "8", "9"],
         ["4", "5", "6"],
         ["1", "2", "3"],
        [None, "0", "A"]]


    DIRECTION_KEYPAD = [
        [None, "^", "A"],
         ["<", "v", ">"]]
       
    def __init__(self, keypad: list[list[str]]):
        self._keypad = keypad
        self._width = len(keypad[0])
        self._height = len(keypad)


        self._point_to_button: dict[Point, str] = {} {P(0,0): '7', P(1,0): '8',... }
        self._button_to_point: dict[str, Point] = {} # {'7': P(0,0), '8': P(1,0), ..., }
        self._build_keypad_dict()
        self._paths_for_pair = self._compute_paths_for_pair()
        self._path_lengths_for_pair = {pair: len(paths[0]) for pair, paths in
                                         self._paths_for_pair.items()}
   
    @classmethod
    def from_type(cls, keypad_type: str):
        """ Factory method to create a KeypadMapping instance with predefined keypads. """
       
        match keypad_type:
            case KeypadMapping.NUMERIC: return cls(KeypadMapping.NUMERIC_KEYPAD)
            case KeypadMapping.DIRECTION: return cls(KeypadMapping.DIRECTION_KEYPAD)
            case _: raise ValueError(f"Unknown keypad type: {keypad_type}")
           
    def _build_keypad_dict(self):
        """ Build a dictionary of keypad points and their associated keys. """
               
        for r, row in enumerate(self._keypad):
            for c, key in enumerate(row):
                if key:
                    self._point_to_button[Point(c, r)] = key
                    self._button_to_point[key] = Point(c, r)
```

Alternatively we could have created subclasses for `Direction` and `Numeric` types.  However, the factory pattern allows simpler dynamic selection of the type at runtime.
Subclassing would be better if the subclasses have distinct behaviour.  In this case, the only difference is one property.

## Dataclass

### Overview

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

### Immutable (Frozen) Objects

Add frozen=True if you want the dataclass to be immutable. I.e.

```python
@dataclass(frozen=True)
class Point2D():
    """ Our immutable point data class """
```

Note that with a frozen dataclass, you can't modify any attributes after the `__init__()`.  However, there is a standard workaround to allow you to use `__post_init__()`:

```python
@dataclass(frozen=True)
class Rectangle:
    width: int
    height: int
    area: int = field(init=False)

    def __post_init__(self):
        # bypass immutability and set the derived field
        object.__setattr__(self, "area", self.width * self.height)
```

### Field Properties

Useful for not only setting defaults, but also for changing field behaviour. For example here, we want a field to be ignored in equality checks

```python
from dataclasses import dataclass, field


@dataclass(frozen=True, eq=True)
class Amphipod():
    type: str
    moving: int = field(default=0, compare=False, hash=False)
```

We can even supply a default_factory, rather than default.  Then pass a function that will set the initial value.

### Post_Init Processing

The `__post_init__()` method runs AFTER the `__init__()` method for an object. A common use case is to initialise variables that are not supplied during object instantiation.

In this example, `initial_posn` has `init=False`, meaning it is not initialised (or expected) by the `__init__()` method. Instead, it is set programmatically in the `__post_init__()` method.

Also, we have defined two class variables.

```python
@dataclass
class Robot:
    """ A robot that wanders the warehouse. It has a starting position and fixed velocity. """
   
    posn: Point # current position
    velocity: Point
   
    # Instance variable to store the initial position
    initial_posn: Point = field(init=False)
   
    # Class variables - for efficiency
    width: ClassVar[int] = 0
    height: ClassVar[int] = 0
   
    def __post_init__(self):
        """ Set initial_posn after initialization """
        self.initial_posn = self.posn
       
    def posn_at_t(self, t: int) -> Point:
        """ Return the position at time t """
        new_x = (self.initial_posn.x + t*self.velocity.x) % Robot.width
        new_y = (self.initial_posn.y + t*self.velocity.y) % Robot.height
        return Point(new_x, new_y)
   
    def move(self) -> Point:
        """ Increment the current position by the velocity vector """
        new_x = (self.posn.x + self.velocity.x) % Robot.width
        new_y = (self.posn.y + self.velocity.y) % Robot.height
        self.posn = Point(new_x, new_y)
        return self.posn
```

### Versus NamedTuple

Similar to using `dataclass`, Python also has something called a `NamedTuple`.  This allows us to define a an immutable class with only attributes.  Thus, a `NamedTuple` is very similar to a frozen (immutable) `dataclass`.  The `dataclass` is a lot more powerful and flexible than `NamedTuple`, but it incurs a performance hit. You should probably use `dataclass` in preference to `NamedTuple`, unless performance is paramount.

```python
Point = NamedTuple("Point", [("x", Number), ("y", Number)])

def manhattan_distance(a_point: Point):
    return abs(a_point.x) + abs(a_point.y)

def manhattan_distance_from(self, other):
    diff = self - other
    return manhattan_distance(diff)

Point.__add__ = lambda self, other: Point(self.x + other.x, self.y + other.y)
Point.__sub__ = lambda self, other: Point(self.x - other.x, self.y - other.y)
Point.__mul__ = lambda self, scalar: Point(self.x * scalar, self.y * scalar)
Point.__rmul__ = lambda self, scalar: self * scalar # for when int comes first
Point.manhattan_distance = staticmethod(manhattan_distance)
Point.manhattan_distance_from = manhattan_distance_from
Point.__repr__ = lambda self: f"P({self.x},{self.y})"
```

## Examples

- [Factory Pattern: 2015 Day 22 - Wizards and Spells](/2015/22)
- [Factory Pattern: 2022 Day 17 - Tetris!](/2022/17)
- [Inheritence and constructor chaining: 2015 Day 22 - Wizard class](/2015/22)
- [Cache decorator: 2015 Day 22 - Wizards and Spells](/2015/22)
- [Cache decorator: type_defs](/python/reusable_code)