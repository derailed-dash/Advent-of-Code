---
title: Defaultdict
tags: 
  - name: Dict
    link: https://realpython.com/python-dicts/
  - name: Defaultdict
    link: https://realpython.com/python-defaultdict/
---
## Defaultdict

### Page Contents

- [Overview](#overview)
- [Default Factory](#default-factory)
  - [int](#int)
  - [set](#set)
  - [dict](#dict)
  - [A Custom Factory](#a-custom-factory)

### Overview

I'll assume you already know what a Python dictionary is.  If not, [review this first](https://realpython.com/python-dicts/){:target="_blank"}.

If you try to reference a key that doesn't exist in a Python dictionary, you'll be met with a `KeyError`. E.g.

```python
my_dict = {}
my_dict["some_key"] = 200

print(my_dict["some_key"])
print(my_dict["some_other_key"])
```

Output:

```text
200
Traceback (most recent call last):
  File "c:\Users\djl\localdev\Python\Advent-of-Code\src\snippets\snippet.py", line 5, in <module>
    print(my_dict["some_other_key"])
          ~~~~~~~^^^^^^^^^^^^^^^^^^
KeyError: 'some_other_key'
```

The `defaultdict` is cool because it never raises a `KeyError`; instead, it assigns a default value to any key that is referenced, but which has not been explicitly initialised.

_"Initialised to what?"_, I hear you say!

Well, that depends on the _default factory_ that we have assigned to our `defaultdict` when we create it.

### Default Factory

We can assign many types of _default factory_ to a `defaultdict`, such as:

- int
- set
- dict
- a custom function

#### int

It's really useful to have a _default factory_ of `int`, when we want to increment dictionary values, but we also want to initialise a key (e.g. to 0) if we reference the key for the first time.

For example:

```python
from collections import defaultdict

d = defaultdict(int) 
   
L = [1, 2, 3, 4, 2, 4, 1, 2] 
   
# Iterate through the list for keeping the count 
for i in L: 
    # The default value is 0 
    # so there is no need to initialise the key first 
    d[i] += 1
       
print(d) 
```

Output:

```text
defaultdict(<class 'int'>, {1: 2, 2: 3, 3: 1, 4: 2})
```

This code:

- Begins by creating a `defaultdict` with a _default factory_ of `int`. This means that every time we reference a key in the dict for the first time, it will be implicitly assigned a value of 0.
- We iterate through our list.
- Every time we see a number, we increment the count for how many times we've seen that number.
- Finally, we print the counts for each number.

If we were not using a `defaultdict`, but rather a normal `dict`, then we would have to start each loop iteration by checking whether there is already a key for this value.  And if there isn't a key, we would explicitly add it.  Then we can increment it.

This is very cumbersome.  You can see why the `defaultdict(int)` is so awesome!

#### set

We can supply a _default factory_ of `set`, when we want a new set to be created implicit for each key. That way, we can simply call `add()` to add items to the set with each iteration.  We don't need to check whether the set already exists, and we don't need to explicitly create the empty sets.

A good example is when we build an [adjacency dictionary for an undirected, unweighted graph](/python/graph).

```python
from collections import defaultdict

edges = set() # store edge edge as a tuple of (node_a, node_b)

# Imagine we're only provided with the edges.
edges.add((1, 2))
edges.add((1, 5))
edges.add((2, 1))
edges.add((2, 3))
edges.add((3, 2))
edges.add((3, 4))
edges.add((4, 3))
edges.add((4, 5))
edges.add((4, 6))
edges.add((5, 1))
edges.add((5, 2))
edges.add((5, 4))
edges.add((6, 4))

# Now we build the adjacency map
node_map = defaultdict(set) # Use a set in order to filter out duplicate connections
for x, y in edges:
    node_map[x].add(y)  # a list of vertices that link to x
    node_map[y].add(x)  # a list of vertices that link to y

for vertex, connections in node_map.items():
    print(f"{vertex}: {connections}")
```

Output:

```text
1: {2, 5}
2: {1, 3, 5}
3: {2, 4}
4: {3, 5, 6}
5: {1, 2, 4}
6: {4}
```

#### dict

This is useful if we want to create a dictionary of dictionaries.  Each outer `dict` value is itself a `dict` created implicitly and initially empty.

A handy use case is where we want to build an adjacency dictionary for nodes edges that are weighted.  E.g.

```python
from collections import defaultdict

edges = dict() # store edge edge as a tuple of (node_a, node_b)

# Imagine we're only provided with edges and their weights
edges[('a', 'b')] = 10   # a is connected to b, with weight of 10
edges[('a', 'c')] = 20   # a is connected to c, with weight of 20. And so on
edges[('a', 'd')] = 30
edges[('b', 'c')] = 40
edges[('b', 'a')] = 50
edges[('c', 'a')] = 60

# Now we build the adjacency map
node_map = defaultdict(dict) 
for (x, y), weight in edges.items():
    node_map[x][y] = weight  # a list of vertices that link to x

for k, v in node_map.items():
    vals = "; ".join("to " + k + " with weight " + str(v) for k, v in v.items()) 
    print(f"From node {k}: {vals}")
```

The output looks like this:

```text
From node a: to b with weight 10; to c with weight 20; to d with weight 30
From node b: to c with weight 40; to a with weight 50
From node c: to a with weight 60
```

This is great!

But what if we had just used a regular dict. I.e. instead of this:

```python
# Now we build the adjacency map
node_map = defaultdict(dict) 
```

We could have instead written this:

```python
# Now we build the adjacency map
node_map = {} 
```

Well, if we do that, then the output of our program is this:

```text
    node_map[x][y] = weight
    ~~~~~~~~^^^
KeyError: 'a'
```

Why? Because the first time we reference `node_map[a]` is when we're trying to do this:

```python
node_map['a']['b'] = 10
```

But this throws a `KeyError`, because we've never assigned a value to `node_map['a']`. Python does not know that we `node_map['a']` needs to be initialised to an empty dictionary, so that we can add a K:V pair to it. 

When we use a `defaultdict(dict)`, this is all taken care of!

#### A Custom Factory

We can actually initialise our `defaultdict` to any type and any initial value we like.  For example:

```python
from collections import defaultdict

def def_value():
    return "Not defined"

dd = defaultdict(def_value)
dd["some_key"] = "Some value"

print(dd["some_key"])
print(dd["some_other_key"]) # Not explicitly set; so default is used
```

The output:

```text
Output:
Some value
Not defined
```