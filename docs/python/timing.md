---
title: Timing and Progress
main_img:
  name: Argand Plot
  link: /assets/images/progress.jpg
tags: 
  - name: Time
    link: https://docs.python.org/3/library/time.html
  - name: String format()
    link: https://www.w3schools.com/python/ref_string_format.asp
  - name: f-strings
    link: https://www.freecodecamp.org/news/python-f-strings-tutorial-how-to-use-f-strings-for-string-formatting
  - name: tqdm (progress bar)
    link: https://pypi.org/project/tqdm
---
## Time Module

The [time](https://docs.python.org/3/library/time.html){:target="_blank"} module is a convenient and easy way to measure how long something takes to run. 

Simply call `time.perf_counter()` before and after executing something. The difference between the two responses is the number of seconds taken.

In the example below, I'm using the `sleep()` method to simulate a long running process. Here, I'm telling Python to sleep for 2 seconds.

```python
import time

t1 = time.perf_counter()
time.sleep(2) # sleep for 2 seconds
t2 = time.perf_counter()
print(f"Execution time: {t2 - t1:0.4f} seconds")
```

Output:

```text
Execution time: 2.0037 seconds
```

Note how I'm displaying the elapsed time with 4 decimal places of precision, using the `:0.4f` [format](https://www.w3schools.com/python/ref_string_format.asp){:target="_blank"} within an [f-string](https://www.freecodecamp.org/news/python-f-strings-tutorial-how-to-use-f-strings-for-string-formatting/){:target="_blank"}.

Here I'll change the program to simulate waiting for 10 milliseconds:

```python
import time

t1 = time.perf_counter()
time.sleep(0.01) # sleep for 0.1s (i.e. 10ms)
t2 = time.perf_counter()
print(f"Execution time: {t2 - t1:0.4f} seconds")
```

The output:

```text
Execution time: 0.0109 seconds
```

## Progress Bar with tqdm

The [tqdm](https://pypi.org/project/tqdm/){:target="_blank"} class is an awesome tool for creating a **dynamic progress bar**. This is really useful if you have a long-running process, and you want to see a real-time indicator on how much of the process is completed, and an estimate of how long is left.

It's incredibly easy to use.  In its simplest form, you simply wrap tqdm around any _iterable_ in a loop.

First, if you haven't yet installed tqdm into your environment, you'll need to install it with **pip**.

```text
py -m pip install tqdm
```

First, let's simulate a long running process:

```python
from time import sleep

steps = 10

for step in range(steps):
    sleep(0.5)
```

This program iterates through 10 steps, and pauses for 0.5s on each step. So obviously, it will take about 5 seconds to run.  During that time, there is no visual indication of progress.

To use tqdm, all you have to do is wrap `tqdm` around the _iterable_, like this:

```python
from time import sleep
from tqdm import tqdm

steps = 10

for step in tqdm(range(steps)):
    sleep(0.5)
```

![Progress Bar]({{ '../assets/images/progress_bar.gif' | relative_url }})