---
title: Regular Expressions
tags: 
  - name: Regular Expression HOWTO
    link: https://docs.python.org/3/howto/regex.html
  - name: Python RE module
    link: https://docs.python.org/3/library/re.html#module-re
  - name: Python Regex module
    link: https://pypi.org/project/regex/
  - name: Regexr
    link: https://regexr.com/
---
**Regular expressions** (often shortened to **regex**) are a way to look for matching patterns in any text. We can use the pattern to determine where the pattern appears in the text, or to do more sophisticated things like replacing patterns in text.

## Page Contents

- [Patterns](#patterns)
- [Matching Patterns in Python](#matching-patterns-in-python)
- [Naming Groups](#naming-groups)
- [Replacing](#replacing)
- [More Examples](#more-examples)
  - [Asserting the Match, and Mapping](#asserting-the-match-and-mapping)
  - [Using findall()](#using-findall)

## Patterns

A _pattern_ is something we want to match within a string. Patterns can be simple, or complex. Patterns include the text we want to look for, along with _metacharacters_ which have special meanings.

Check out this [tutorial](https://docs.python.org/3/howto/regex.html){:target="_blank"} for a guide on how to build patterns.

Then, make a note of this [the awesome regexr.com](https://regexr.com/){:target="_blank"}, which is a great place to test and build your regular expressions.  It also includes some really useful cheat sheets and references.

## Matching Patterns in Python

Python provides a built-in library for working with regular expressions, called `re`. This will generally be good enough for most of our regular expression needs in Python.  However, there are some niche cases where you want to do stuff that `re` doesn't offer. In this case, try out the third party Python [regex module](https://pypi.org/project/regex/){:target="_blank"}, which is basically `re` on steroids. E.g. finding overlapping pattern matches.

In general, the approach to regex in Python is to compile the pattern, and then use one of handful of methods to apply the pattern to a string or strings.

For example:

```python
import re

# Assume we've loaded in some multiline text data into the variable `data`

# We want to match rows of data that looks like: 5-7 z: qhcgzzz
# We want to obtain 5, 7, z, and qhcgzzz as four separate variables
matcher = re.compile(r"(\d+)-(\d+) ([a-z]): ([a-z]+)")
for row in data:
    match = matcher.match(row)
    min_val, max_val, policy_char, token_str = match.groups()
```

Here:

- We wrap the pattern with `r"regex"`, to avoid any need for convoluted escape characters.  The `r` prefix turns the `str` into Python's _raw_ string format.  In short, it's just a good idea to always pass patterns in this raw format.
- The `match(row)` method looks for the pattern within the text called `row`. In particular, the `match()` method will look for the match from the _beginning_ of the line of data.
- If we want to look for the pattern at any position in the data, we should use `search()` instead of `match()`.
- If `match()` or `search()` are successful, they return a `match` object. If not, they return `None`.
- The regex pattern itself is split into several groups, by wrapping each group within parentheses, i.e. `(group)`. When we call the `groups()` method against any successful `match` object, this returns a _tuple_ of the four groups in our regex pattern.

It can be useful to perform assignment at the same time as checking if match object was returned.  For example, here we will only enter the `if` block if a match was found. If a match was found, then the match object will have been assigned to the variable called `match`:

```python
    if match := matcher.match(row):
        # do stuff with match object
```

We don't have to compile the pattern in advance.  For example, we can do this:

```python
# We're looking for data like... "25,50 -> 30,600"
for line in data:
    x1, y1, x2, y2 = map(int, re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line).groups())
    lines.append(Line(x1, y1, x2, y2))
```

Here, we're:

- Calling `match()` against `re`, rather than against a precompiled pattern.
- We're returning the four groups in the pattern.
- We're mapping all four groups from `str` type to `int` type, since we expect the data to always be numeric.
- We use the four numbers - which are two pairs of x,y coordinates - to create a Line object. 

## Naming Groups

We can actually name groups in the regex pattern itself. Then, instead of calling `groups()` on a match object, we can instead call `groupdict()`. This returns a dictionary, where the keys are the names of the groups, and the values are the string values from the match.

Compare these two approaches:

```python
import re

test = "John Smith"

# First, just using groups() and then unpacking the tuple
name_pattern = r"(\w+) (\w+)"
if (match := re.match(name_pattern, test)):
    first_name, last_name = match.groups()
    print(f"Unpacking groups(): {first_name}, {last_name}")

# Now, using named groups and returning a dict
name_pattern = r"(?P<first>\w+) (?P<last>\w+)"
if (match := re.match(name_pattern, test)):
    name_dict = match.groupdict()
    print(f"Using groupdict(): {name_dict['first']}, {name_dict['last']}")
```

Output:

```text
Unpacking groups(): John, Smith
Using groupdict(): John, Smith
```

Even more usefully, we can actually embed Python variables within the pattern string.  You can see how this can be useful if using `groupdict()`:

```python
test = "John Smith"

first_name_grp = "first"
last_name_grp = "last"
name_pattern = rf"(?P<{first_name_grp}>\w+) (?P<{last_name_grp}>\w+)"
if (match := re.match(name_pattern, test)):
    name_dict = match.groupdict()
    print("Using groupdict() with variables in the pattern: "
         f"{name_dict[first_name_grp]}, {name_dict[last_name_grp]}")
```

Note how we're prefixing the pattern string with both `r` to make it _raw_, and `f` in order to use f-string interpoloation, i.e. so that we can reference variables like `{first_name_grp}` within the string.

## Replacing

Use the `sub()` method to replace occurrences of a match with a replacement string.

For example:

```python
line = re.sub(r"(\d+)", r"RULE_\1", line)
```

Here, any number that we find is replaced by "RULE_" + number. E.g.
`15` becomes `RULE_15`.

The trick to this is to use `\n` to reference the `nth` group in the preceeding pattern.

This example turns any number `n` into X(n). E.g. `456` becomes `X(456)`:

```python
re.sub(r"(\d+)", r"X(\1)", input)
```

Here's a more sophisticated example. It takes a string like: \
`= x yz | ab c` \
and replaces it with: \
`= ((x yz) / (ab c))`

```python
line = re.sub(r"= (.*) \| (.*)$", r"= ((\1) / (\2))", line)
```

## More Examples

### Asserting the Match, and Mapping

```python
INSTR_PATTERN = re.compile(r"(\d+),(\d+) through (\d+),(\d+)")

for line in data:
    match = INSTR_PATTERN.search(line)
    assert match, "All instruction lines are expeted to match"
    tl_x, tl_y, br_x, br_y = map(int, match.groups())
```

Here we're processing multiple lines of data. We're looking for lines that contain something like:

```text
4,14 through 6,16
```

- The four `(\d+)` groups are used to capture each of the four numbers in the line.
- We're using an [assert](/python/assertion) to validate that we found a match to our pattern in the current line. By including this assertion, we're explicitly stating that we believe the input data is good. If any line fails to match the pattern, then the program will terminate with an `AssertionError`.
- We're using the `groups()` method to return the four groups as a `tuple`. We're then using _tuple unpacking_ to unpack the tuple into four separate variables.
- Finally, because we know the four variables are all numbers, we're using the `map()` function, to convert each variable from a `str` to an `int`.  Here, the `map()` function is applying the `int()` function each member of the tuple that was passed in.

### Using findall()

Here is another way to retrieve matches and their groups.  Note how each line expects to return a single match, which is we always index the return value of `findall()` with `[0]`.  This match contains our four groups, as a tuple.

```python
pattern = re.compile(r"(\d+),(\d+) through (\d+),(\d+)")
print("\nUsing findall with existing pattern:")
for line in data:
    tl_x, tl_y, br_x, br_y = map(int, pattern.findall(line)[0])
    print(f"tl_x: {tl_x}, tl_y: {tl_y}, br_x: {br_x}, br_y: {br_y}")
    
print("\nUsing findall, pattern on the fly:")
for line in data:
    tl_x, tl_y, br_x, br_y = map(int, re.findall(r"(\d+),(\d+) through (\d+),(\d+)", line)[0])
    print(f"tl_x: {tl_x}, tl_y: {tl_y}, br_x: {br_x}, br_y: {br_y}")
```