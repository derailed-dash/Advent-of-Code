---
title: Unit Testing
tags: 
  - name: Unit Testing in Python
    link: https://realpython.com/python-testing/
  - name: Assertion
    link: /python/assertion
---
## Unit Tests

Unit tests are small, coded, repeatable tests that execute a component of our code, and [assert](/python/assertion) that the code does what we expected.

The idea is that unit tests are quick to repeat.  So we can use them to:

- Validate that components of our code do what is expected.
- Check that we haven't broken anything, whenever we change our code.

## unittest

### Overview

Python includes a built-in `unittest` package. To use it:

- `import unittest`
- Create _test cases_. These are related sets of tests. For each test case, we need a `class` that extends `unittest.TestCase`.
  - If required, implement a `setUp()` method in our class.  If this method is present, it will be automatically executed when we run our test case.  The job of the `setUp()` method is initialise any data and attributes that the tests will require in this test case. For example, if you have some test data, this is where you would read it and store it. Note that you will store this data as attributes in your class.
  - Implement one or more `test_xxx()` methods, where `xxx` is some arbitrary name for your test. Any such method will be executed automatically, when we run our test case.
  - Inside our `test_xxx()` method, we include assertions, but using `unittest` specific methods. I'll show you these a bit later.

- Finally, run our test case(s):

```python
if __name__ == "__main__":
    unittest.main()
```

### Asserting

|Method|What it does|Example|
|------|------------|-------|
|assertTrue|Checks that the expression is True|`self.assertTrue(6 in self.s)`|
|assertFalse|Checks that the expression is False|`self.assertFalse(6 in self.s)`|
|assertEqual|Checks that the first parameter equals the second|`self.assertEqual(len(s), 0)`|
|assertNotEqual|You can guess this one!|`self.assertNotEqual(len(s), 0)`|
|assertRaises|Checks that statement raises an exception|`self.assertRaises(StopIteration, lambda: next(i))`|

### Demo

Here I'm testing the answers to two Advent of Code parts, using the supplied test data:

```python
""" Test our Rope_Bridge Solution """
from pathlib import Path
import unittest
import rope_bridge  # We need to import the code we will be testing

SAMPLE_INPUT_FILE = Path(Path(__file__).parent, "input/sample_input.txt")

class TestRopeBridge(unittest.TestCase):
    """ Set up data using the sample input.
    Then run two tests, asserting the correct length of the returned lists. """
    
    def setUp(self):
        # load the data
        with open(SAMPLE_INPUT_FILE, mode="rt") as f:        
            self.data = [(d, int(v)) for d, v in [instruction.split() for instruction in f.read().splitlines()]]
        
    def test_part_1(self):
        expected = 88
        self.assertEqual(len(rope_bridge.pull_rope(self.data, 2)), expected)
        
    def test_part_2(self):
        expected = 36
        self.assertEqual(len(rope_bridge.pull_rope(self.data, 10)), expected)

if __name__ == "__main__":
    unittest.main()
```

When we run it with the expected data, and it works, the output looks like this:

```text
..
----------------------------------------------------------------------
Ran 2 tests in 0.007s

OK
```

We can see that it ran two tests, and they both passed.  Hurrah!

But what if our code has bugs?  I've just changed my solution code so that it returns empty lists, instead of lists of the required lengths. Now, the output of our unit testing looks like this:

```text
FF
======================================================================
FAIL: test_part_1 (__main__.TestRopeBridge)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "f:\Users\Darren\localdev\Python\Advent-of-Code\src\AoC_2022\d09_rope_bridge\test_rope_bridge.py", line 19, in test_part_1  
    self.assertEqual(len(rope_bridge.pull_rope(self.data, 2)), expected)
AssertionError: 0 != 88

======================================================================
FAIL: test_part_2 (__main__.TestRopeBridge)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "f:\Users\Darren\localdev\Python\Advent-of-Code\src\AoC_2022\d09_rope_bridge\test_rope_bridge.py", line 23, in test_part_2  
    self.assertEqual(len(rope_bridge.pull_rope(self.data, 10)), expected)
AssertionError: 0 != 36

----------------------------------------------------------------------
Ran 2 tests in 0.007s

FAILED (failures=2)
```

Now we can see that both tests failed.  The test tells us what was expected, and what was actually received. So this is **really useful**!!