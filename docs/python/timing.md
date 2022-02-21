---
layout: default
title: Timing
---
# {{ page.title }}

The [time](https://docs.python.org/3/library/time.html){:target="_blank"} module is a convenient and easy way to measure how long something takes to run. 

Simply call `time.perf_counter()` before and after executing something. The difference between the two responses is the number of seconds taken. E.g.

```python
import time

t1 = time.perf_counter()
my_func()
t2 = time.perf_counter()
print(f"Execution time: {t2 - t1:0.4f} seconds", t2 - t1)
```
