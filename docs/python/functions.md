---
title: Functions
tags: 
  - name: Functions
    link: https://www.programiz.com/python-programming/function
  - name: Docstrings
    link: https://www.geeksforgeeks.org/python-docstrings/
  - name: Exceptions
    link: /python/exceptions
---
## Functions

### Page Contents

- [Overview](#overview)

### Overview

A **function** is a way of taking some code and making it callable. This allows us to implement chunks of code that we want to re-use. It also helps us break down our code into manageable and readable units of functionality.

The general syntax is:

```python
def my_function(some_arg, some_other_arg):
   """ Some docstring """
   some_result = do_some_stuff(some_arg)
   ret_value = do_some_other_stuff(some_other_arg, some_result)
   return ret_value
```

- The `def` keyword binds a function body (i.e. the code) to a name, such that a function is simply an object. Thus, a function is a _callable object_.
- After a function has been defined, we can call our function from another part of our code.
- Function arguments are passed in the brackets.  Functions do not always require arguments.
- It is _useful_ to include a _docstring_, i.e. brief documentation that explains what the function does, and how to use it.
- A function does not always need to return a value.  But often, a function does something, and then returns a value as output.  If no return value is explicitly specified, the function will always return `None`.
- Functions can return multiple values, as a `tuple`.  Whenever more than one value is returned by a function, it is automatically converted to a tuple. For example:

```python
def min_and_max(items):
    """ Takes a list of values, and returns the smallest and largest values from the list.
        Returns: a tuple, composed of the min and max values from the list """
    return min(items), max(items)

print(min_and_max([50,5,20,30]))
```

Output:

```text
(5, 50)
```

Note how the output is actually just a single tuple, containing our two values.

### Fibonacci Example

```python
def fib(n):
    """ Generate the Fibonacci Sequence for n iterations """
    ret_val = []
    if (n==0):
        return ret_val

    current_loop = 0

    a = 0
    b = 1

    while (current_loop <= n):
        ret_val.append(f"Iteration {current_loop}: value={str(b)}")
        a, b = b, a+b
        current_loop += 1

    return ret_val

# Test our code
try:
    iterations = int(input("How many Fibonacci numbers would you like? "))
    values = fib(iterations)
    for v in values:
        print(v)
except ValueError:
    print("You didn't enter a number, you muppet.")
```