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
- [Some Common Exception Types](#some-common-exception-types)
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

### Some Common Exception Types

Here are some of the more common exception types, and what they mean:

|Exception|Description|
|---------|-----------|
|ValueError|Often thrown when the input value is of the wrong type or bad|
|IndexError|When we attempt an out-of-range lookup; e.g. using at index beyond the end of a list|
|KeyError|When a key lookup fails; e.g. attempting to retrieve a value from a dict using a key that doesn't exist|
|StopIteration|When we have no more values to iterate over|

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

It is possible to raise an exception ourselves, programmatically. Here's an example of when we might want to do this:

```python
""" Find the median of any iterable.
Explicitly handle empty iterable use case by raising a ValueError,
otherwise we'll see an IndexError raised by the implementation. """
def median(iterable):
    items = sorted(iterable)
    
    # Odd e.g. 1, 4, 5, 6, 9: median index = 4 // 2 = 2
    # Even e.g. 1, 4, 5, 6, 9, 10: median index = 5 // 2 = 2
    median_index = (len(items) - 1) // 2    # integer division
    if len(items) % 2 != 0:
        return items[median_index]
    
    return (items[median_index] + items[median_index+1]) / 2.0
 
def test(iterable):
    print(f"Using {iterable}...")
    print(median(iterable))

numbers = [1, 4, 5, 6, 9]
test(numbers)

numbers = []
test(numbers)
```

Here we've created a function that determines the median from any supplied iterable (e.g. list) of numbers. It calculates the median as follows:

- Sort the supplied values in numerical order.
- Determines the number of values in the list. Subtract one from this number, and then divide by 2, ignoring any remainder. Store this as our index.
  - E.g. if we have 6 numbers, then we divide 5 by 2, to get 2.
  - E.g. if we have 5 numbers, then we divide 4 by 2, to get 2.
- If the total number of values was odd, then we return the value at the index calculated. This is the median.
- If the total number of values was even, then we need to return the value in between the value at our index, and the subsequent value.

We test the function using two lists: the first has some numbers, but the second list is empty.  This is the result:

```text
Using [1, 4, 5, 6, 9]...
5
Using []...
Traceback (most recent call last):
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 23, in <module>   
    test(numbers)
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 17, in test       
    print(median(iterable))
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 13, in median     
    return (items[median_index] + items[median_index+1]) / 2.0
IndexError: list index out of range
```

We can see that when we supply the first list, our code has no trouble calculating the median.  But when we supply an empty list, an uncaught `IndexError` is thrown. This happens because when we try to reference `items[median_index]` in our `median()` function, the `items` list is empty, so the index tries to reference a value that doesn't exist.  Doh!  Furthermore, this error isn't very useful to anyone else running our code. It would be much more helpful if our code through a more useful exception in this scenario.

As an improvement, we can choose to throw an exception, if our function is given an empty list:

```python
""" Find the median of any iterable.
Explicitly handle empty iterable use case by raising a ValueError,
otherwise we'll see an IndexError raised by the implementation. """
def median(iterable):
    items = sorted(iterable)
    if len(items) == 0:
        raise ValueError("median() arg was empty sequence")
    
    # Odd e.g. 1, 4, 5, 6, 9: median index = 4 // 2 = 2
    # Even e.g. 1, 4, 5, 6, 9, 10: median index = 5 // 2 = 2
    median_index = (len(items) - 1) // 2    # integer division
    if len(items) % 2 != 0:
        return items[median_index]
    
    return (items[median_index] + items[median_index+1]) / 2.0
 
def test(iterable):
    print(f"Using {iterable}...")
    print(median(iterable))

numbers = [1, 4, 5, 6, 9]
test(numbers)

numbers = []
test(numbers)
```

The only difference was the addition of a test to see if the list was empty, and the explicit code to throw a more appropriate `ValueError`, if the list is indeed empty.

Now when we run it:

```text
Using [1, 4, 5, 6, 9]...
5
Using []...
Traceback (most recent call last):
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 25, in <module>   
    test(numbers)
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 19, in test       
    print(median(iterable))
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 7, in median      
    raise ValueError("median() arg was empty sequence")
ValueError: median() arg was empty sequence
```

This is a bit better. When we pass an empty list, the code now shows a more appropriate `ValueError`, and also has a message payload in the `Exception`, which is printed when the exception is thrown.

Unfortunately, we still get a messy stack trace.  So one more improvement we can make it is to actually handle the `ValueError`, when it is thrown. I.e.

```python
""" Find the median of any iterable.
Explicitly handle empty iterable use case by raising a ValueError,
otherwise we'll see an IndexError raised by the implementation. """
def median(iterable):
    items = sorted(iterable)
    if len(items) == 0:
        raise ValueError("median() arg was empty sequence")
    
    # Odd e.g. 1, 4, 5, 6, 9: median index = 4 // 2 = 2
    # Even e.g. 1, 4, 5, 6, 9, 10: median index = 5 // 2 = 2
    median_index = (len(items) - 1) // 2    # integer division
    if len(items) % 2 != 0:
        return items[median_index]
    
    return (items[median_index] + items[median_index+1]) / 2.0
 
def test(iterable):
    try:
        print(f"Using {iterable}...")
        print(median(iterable))
    except ValueError as err:
        print(f"Error of type: {type(err).__name__} with message: {err}")

numbers = [1, 4, 5, 6, 9]
test(numbers)

numbers = []
test(numbers)
```

The only change here was that the lines in our `test()` function have now been wrapped with a `try-except` block.

When we run our code:

```text
Using [1, 4, 5, 6, 9]...
5
Using []...
Error of type: ValueError with message: median() arg was empty sequence
```

You can see that the output is much less messy.  
- The first list works fine, as expected.
- The second list results in a `ValueError`, which is caught.  The code then prints the error message in a friendly way.

### Exception Payloads

### Defining Your Own Exceptions

### Exception Chaining

### Tracebacks

### Pattern: Exception to Break or Continue an Outer Loop

### Write Exceptions as JSON

### EAFP