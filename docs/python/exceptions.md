---
title: Exceptions
tags: 
  - name: Exceptions - Python Docs
    link: https://docs.python.org/3/tutorial/errors.html
  - name: Python Exceptions @RealPython
    link: https://realpython.com/python-exceptions/
  - name: Exception hierarchy
    link: https://docs.python.org/3/library/exceptions.html#exception-hierarchy
  - name: Assertions
    link: /python/assertion
---
## Exceptions

### Page Contents

- [Overview](#overview)
- [The Exception Handling Process](#the-exception-handling-process)
- [How to Handle](#how-to-handle)
- [Example: Input Validation](#example-input-validation)
- [The Exception Hierarchy](#the-exception-hierarchy)
- [What Exceptions to Catch?](#what-exceptions-to-catch)
- [Example: Catching Different Exception Types](#example-catching-different-exception-types)
- [Raising Exceptions Programmatically](#raising-exceptions-programmatically)
- [Exception Payloads](#exception-payloads)
- [Defining Your Own Exceptions](#defining-your-own-exceptions)
- [Exception Chaining](#exception-chaining)
- [Tracebacks](#tracebacks)
- [Pattern: Exception to Break or Continue an Outer Loop](#pattern-exception-to-break-or-continue-an-outer-loop)
- [Write Exceptions as JSON](#write-exceptions-as-json)
- [EAFP](#eafp)

### Overview

Exceptions are used to handle situations that are not the _normal_ flow of our code. Exceptions are errors which are detected and  _thrown_ at runtime.  This is different to syntactic errors; i.e. where the code itself is structurally or syntactically not valid.

When an exception is _thrown_, there are basically two things we can do.

1. We can write code to _catch_ and handle the exception. This might mean gracefully dealing with a situation, allowing the program to then continue.
1. We can not bother writing any such code; the exception will cause our program to terminate with an error.

### The Exception Handling Process

1. **An exception is _raised_ by a line of code.**
  - E.g. when we do something bad, like... \
    -> Trying to divide by 0. \
    -> Capturing user input, not validating its type, and then always assuming the user has entered, say, an integer value. \
    -> Trying to write to a read-only file. \
    -> Trying to obtain a dictionary value with a non-existent key.
  - We can also programmatically raise our own exceptions.  We'll get to that later.

1. **Optionally handle the exception.**
  - I.e. do something to gracefully deal with the exception, allowing the program to continue.
  - Or, leave the exception unhandled, resulting in the program terminating.

### How to Handle

We use the **try-except block**, which is a construct that appears in many programming languages. (E.g. in Java, it's called _try-catch_).

The general structure is:

```python
try:
  # normal execution flow
except some_exception as some_err:
  # code to execute only if "some_exception" is caught.
except some_other_exception as some_err:
  # code to execute only if "some_other_exception" is caught
finally:
  # an optional block that we execute whether an exception is caught or not
```

So, we:
- Wrap the code that _could_ throw an exception in the `try:` block.
- Create an `except` block for each exception type that we may want to explicitly handle. The code will fall through to each successive `except` clause, until a matching exception is found.  
- We can optionally name our caught exception with the `as some_name` construct.  This allows us to interrogate the exception in more detail, within the `except` block.
- An optional `finally` block is for any code that we may want to exception after any exception handling has taken place, or even if there was no exception.

### Example: Input Validation

```python
print("Welcome to the number sorter!")
ready_to_quit = False
numbers_list = []

while not ready_to_quit:
    print("Enter some numbers, one entry at a time. Press Q to sort and Quit.")
    userEntered = input("> ").upper()
    if (userEntered == "Q"):
        break
    else:
        try:
            num_entered = int(userEntered)
        except ValueError:
            print("Not a number! Try again.")
        else:
            print("You entered", userEntered)
            numbers_list.append(num_entered)
        finally:
            print("Done with this try-catch iteration.", userEntered)
              
print("Size of list: {0}".format(len(numbers_list)))
numbers_list.sort()
print(",".join(str(num) for num in numbers_list))
```

This code:

- Uses an infinite loop to capture input.  We break out of the loop if the user enters `q`.
- Whenever the user enters a value (other than `q`), the code attempts to convert the input to an integer number.  It does this in `try-except` block. If the value entered can be parsed as an integer, the code continues happily to the next iteration.
- If the user enters invalid data (i.e. not a number), then Python _throws_ a `ValueError`, which we handle in the code by displaying an appropriate message.

Let's try it out with valid input:

```text
Welcome to the number sorter!
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 15
You entered 15
Done with this try-catch iteration. 15
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 5
You entered 5
Done with this try-catch iteration. 5
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 4
You entered 4
Done with this try-catch iteration. 4
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 9
You entered 9
Done with this try-catch iteration. 9
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> q
Size of list: 4
4,5,9,15
```

Now let's give it bad input, to test our `except` block:

```text
Welcome to the number sorter!
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 15
You entered 15
Done with this try-catch iteration. 15
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 5
You entered 5
Done with this try-catch iteration. 5
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 4
You entered 4
Done with this try-catch iteration. 4
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> foo
Not a number! Try again.
Done with this try-catch iteration. FOO
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> 10
You entered 10
Done with this try-catch iteration. 10
Enter some numbers, one entry at a time. Press Q to sort and Quit.
> q
Size of list: 4
4,5,10,15
```

### The Exception Hierarchy

Before we describe which exception types you should be handling in your code, let's first look at the [exception hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy){:target="_blank"}. I.e. the class hierarchy for all built-in exception types defined in the standard Python library:

```text
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- EncodingWarning
           +-- ResourceWarning
```

What does this mean?  Well, it means that exceptions are hierarchical, and that all these built-in exception types are ultimately descendents of the parent class, `BaseException`.  

For example:
- `ZeroDivisionError` inherits from `ArithmeticError`, which inherits from `Exception`, which inherits from `BaseException`.
- `KeyError` inherits from `LookupError`, which inherits from `Exception`, which inherits from `BaseException`.

In fact, you can take any class in Python, and view it's inheritance hierarchy with the `mro()` method.  For example:

```text
>>> KeyError.mro()
[<class 'KeyError'>, <class 'LookupError'>, <class 'Exception'>, <class 'BaseException'>, <class 'object'>]
>>> ValueError.mro()
[<class 'ValueError'>, <class 'Exception'>, <class 'BaseException'>, <class 'object'>]
```

### What Exceptions to Catch?

Here's the most important rule: **always specify an exception type!**  Never have an empty `except`. Why?  Because then your `except` block will catch **all** types of exceptions that can be thrown.  And you'll see from the hierarchy above that this includes the likes of `KeyboardInterrupt`, which are inherited from `BaseException`.

Take a look at this example:

```python
from random import randrange

def main():
    number = randrange(100)
    while True:     # loop until user guesses
        try:
            guess = int(input("Guess the number? Quit with Ctrl-C if you get bored: "))
        except Exception:     # Better than catching empty, since this would even catch KeyboardInterrupt!
            continue
        
        if guess == number:
            print("You win!")
            break   # exit the loop

if __name__ == "__main__":
    main()
```

This program picks a random number between 0 and 99, prompts the user for input, and only exits if the user guesses correctly.

But what if the user gets bored and wants to quit?  Here I aborted after four attempts:

```text
Guess the number? Quit with Ctrl-C if you get bored: 50
Guess the number? Quit with Ctrl-C if you get bored: 30
Guess the number? Quit with Ctrl-C if you get bored: 25
Guess the number? Quit with Ctrl-C if you get bored: 10
Guess the number? Quit with Ctrl-C if you get bored: Traceback (most recent call last):
  File "f:\Users\Darren\localdev\Python\Basic-Scripts\src\Exceptions\empty_except.py", line 16, in <module>
    main()
  File "f:\Users\Darren\localdev\Python\Basic-Scripts\src\Exceptions\empty_except.py", line 7, in main
    guess = int(input("Guess the number? Quit with Ctrl-C if you get bored: "))
KeyboardInterrupt
```

If we press Ctrl-C, this causes a `KeyboardInterrupt` to be raised.  Our code catches `Exception`, but **does not catch** `KeybaordInterrupt`.  Note from the exception hierarchy that `KeyboardInterrupt` does not descend from `Exception`. Instead, `KeyboardException` inherits directly from `BaseException`. And we're not catching `BaseException`.

But what happens if we just catch **everything**?  We can do this by having an _empty_ `except` block, like this:

```python
from random import randrange

def main():
    number = randrange(100)
    while True:     # loop until user guesses
        try:
            guess = int(input("Guess the number? Quit with Ctrl-C if you get bored: "))
        except:     # THIS IS BAD!!  It even catches KeyboardInterrupt
            continue
        
        if guess == number:
            print("You win!")
            break   # exit the loop

if __name__ == "__main__":
    main()
```

The above program cannot be terminated.  Pressing Ctrl-C does nothing, because the resulting `KeyboardException` is caught by our empty `except` block, and then the code simply continues with the infinite `while` loop.

My advice:

- Always catch _something_.  Don't leave the `except` empty.
- Catching `Exception` is better than nothing.  It doesn't catch `SystemExit`, `KeyboardInterrupt` or `GeneratorExit`.  It will catch all other built-in Python exceptions.
- Ideally, be a bit more specific. If you know what exceptions are likely, then try to handle them with a bit more specificity.  Some of the most common exception types you'll want to explicitly handle are:
  - `ValueError` - for handling inappropriate input
  - `IndexError` - for when the code attempts to reference an object using an index that is out of range
  - `KeyError` - when we try to reference a key that doesn't exist (e.g. in a dict lookup)
  - `StopIteration` - for when there are no more values to iterate over
- You can always follow your _specific_ exceptions with a more generic `catch Exception`.

### Example: Catching Different Exception Types

```python
from sys import stderr

person = {
    "Firstname": "Bob",
    "Role": "Trader",
    "ID": 123
}
try:
    last_name = person["Lastname"]  # lookup a key that doesn't exist
    print("Lastname: ", last_name)
except KeyError as error:
    print("No last name!")
    print(f"Error of type: {type(error).__name__} with message: {error}")
except Exception as error:
    print("Unknown error!")
    print(f"{error!r}", file=stderr)

```

And when we run it:

```text
No last name!
Error of type: KeyError with message: 'Lastname'
```

### Raising Exceptions Programmatically

### Exception Payloads

### Defining Your Own Exceptions

### Exception Chaining

### Tracebacks

### Pattern: Exception to Break or Continue an Outer Loop

### Write Exceptions as JSON

### EAFP