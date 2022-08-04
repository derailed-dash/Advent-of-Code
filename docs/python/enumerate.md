---
title: Enumerate
tags: 
  - name: Enumerate
    link: https://realpython.com/python-enumerate/
---
**The enumerate function is useful for obtaining a counter for any loop.**

For example, consider this iteration of a tuple:

```python
names = ("Darren", "Josh", "Julie")
for name in names:
    print(name)
```

Output:

```text
Darren
Josh
Julie
```

We can wrap the iterable inside `enumerate()`, and then add a variable to store the current iteration count:

```python
names = ("Darren", "Josh", "Julie")
for i, name in enumerate(names):
    print(f"{i}: {name}")
```

Output:

```text
0: Darren
1: Josh
2: Julie
```

Thus, using `enumerate` has given us a counter, which starts at 0 by default. We can change the start value by adding a second parameter to `enumerate()`, i.e. `start=some_value`. For example:

```python
names = ("Darren", "Josh", "Julie")
for i, name in enumerate(names, start=1):
    print(f"{i}: {name}")
```

Output:

```text
1: Darren
2: Josh
3: Julie
```