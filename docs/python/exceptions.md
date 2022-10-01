---
title: Exceptions
tags: 
  - name: Exceptions - Python Docs
    link: https://docs.python.org/3/tutorial/errors.html
  - name: Python Exceptions @RealPython
    link: https://realpython.com/python-exceptions/
  - name: Assertions
    link: /python/assertion
---
## Exceptions

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
except some_exception:
  # code to execute only if "some_exception" is caught
except some_other_exception:
  # code to execute only if "some_other_exception" is caught
finally:
  # an optional block that we execute whether an exception is caught or not
```

So, we:
- Wrap the code that _could_ throw an exception in the `try:` block.
- Create an `except` block for each exception type that we may want to explicitly handle
- An optional `finally` block is for any code that we may want to exception after any exception handling has taken place, or even if there was no exception.

### Example: Input Validation for Bad Input

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

### What Exceptions to Catch?

### Raising Exceptions Programmatically

### The Exception Hierarchy

### Exception Payloads

### Defining Your Own Exceptions

### Exception Chaining

### Tracebacks

### Pattern: Exception to Break or Continue an Outer Loop


