---
title: Assertion
tags: 
  - name: Assertions in Python
    link: https://www.tutorialspoint.com/python/assertions_in_python.htm
---
## Assertions and Invariants

### Overview

Assertions are a great way to check that your code is doing what you _think_ it should be doing. We use assertions to **test for invariants**.  This means checking a condition that we always believe should be true. Or to put it another way:

Use assertions to **test for something that you believe should *never* happen**.

(Contrast _exceptions_, which should be used for conditions that might happen.)

In plain English, an assertion might go something like this:

> "I assert that the variable called _okay_ is always `True`"

The general Python syntax is:

```python
assert condition [, message]
```

So, for the example above:

```python
assert okay, "We're not okay!"
```

If the assertion is `True`, then the program continues without displaying any message.  If the assertion fails (i.e. the condition is `False`), then an `AssertionError` will be thrown.  Unless the exception is caught, this will cause your program to terminate.

Let's try it out:

```python
okay = True
assert okay, "We're not okay!"
print("Finished")
```

Output:

```text
Finished
```

```python
okay = False
assert okay, "We're not okay!"
print("Finished")
```

Output:

```text
Traceback (most recent call last):
  File "f:\Users\Darren\localdev\Python\Basic-Scripts\src\Exceptions\assertion_demo.py", line 2, in <module>
    assert okay, "We're not okay!"
AssertionError: We're not okay!
```

### Handing AssertionError

Like any exception in Python, we can handle it programmatically:

```python
okay = False

try:
    print("About to assert...")
    assert okay, "We're not okay!"
    print("If our assertion fails, this message won't print.")
except AssertionError as e:
    print(e)
    
print("Finished")
```

Output:

```text
About to assert...
We're not okay!
Finished
```

### Assertions as a Way to Comment Code

**Assertions are helpful in checking our code is behaving as we expect.**  At the same time, **they are a useful way to document our code**. So think about where an assertion might be preferable over a normal comment.

### Asserting Unreachable Conditions

Consider using `assert False` for any condition that you believe should never happen.

I'll set up a trivial example:

```python
validated_input = "c"
if validated_input == "y":
    print("Yes")
elif validated_input == "n":
    print("No")
else:
    assert False, "Looks like we did a poor job validating the input."
```

Pretend that the variable called `validated_input` was set by some sort of user input process.  We believe this user input has validation in place, such that at this point in the code, the variable can only be set to `"y"` or to `"n"`. But somehow our validation has failed, and the variable has been set to `"c"`.  This shouldn't be possible! The `assert` statement helps us identify that this scenario has happened.

Output:

```text
Traceback (most recent call last):
  File "f:\Users\Darren\localdev\Python\Basic-Scripts\src\Exceptions\assertion_demo.py", line 7, in <module>
    assert False, "Looks like we did a poor job validating the input."   
AssertionError: Looks like we did a poor job validating the input.  
```

This can save you a lot of time in debugging problems in your code!

### Performance Considerations

Used judiciously, assertions should have no significant impact on your application's performance. But there are some considerations:

- It may not be wise to place an assert within a loop that runs many times. (But sometimes it may be worth it!)
- It is unwise to provide an assert condition that is computationally intensive.
- You can always tell your program to run without assertions, by passing the `-O` command line paramater at run time.