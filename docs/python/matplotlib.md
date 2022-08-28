---
title: Visualisations and Plots with Matplotlib
main_img:
  name: matplotlib
  link: /assets/images/numpy_logo.png
tags: 
  - name: Matplotlib
    link: https://matplotlib.org/
  - name: Official Matplotlib Tutorials
    link: https://matplotlib.org/stable/tutorials/index.html
  - name: Geeks-for-Geeks Matplotlib Tutorial
    link: https://www.geeksforgeeks.org/matplotlib-tutorial/?ref=lbp
  - name: Graph Plotting with Matplotlib
    link: https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
  - name: Python Guides Matplotlib Tutorials
    link: https://pythonguides.com/category/python-tutorials/matplotlib/
  - name: Seaborn
    link: https://seaborn.pydata.org/
---
## Page Contents

- [Overview](#overview)
- [Installing](#installing)
- [Seaborn](#seaborn)

## Overview

**Matplotlib is an amazing library for creating static, animated and interactive visualisations in Python, including graphs and 3D plots.**

## Installing

```text
py -m pip install matplotlib
```

## Basic Usage

- Many of the basic capabilities you'll need are exposed through the `pyplot`. So the first thing you'll want to do is import `pyplot`.
- Visualisations are created on `figures`, which in turn contain one more more `axes`; i.e. an individual plot area.

### Getting Axes

Here are a few ways to obtain axes for plotting on:

```python
from matplotlib import pyplot as plt

fig, axes = plt.subplots()

# or with 'get current axes'
axes = plt.gca()

# to set all axes to use equal aspects, rather than auto...
axes.set_aspect('equal', adjustable='box')
```

### Showing the Visualisation

```python
# To show interactively, i.e. pausing code execution until the window is closed
plt.show()
```

### Grid Lines and Axis Limits

```python
# add grid lines
axes.grid(True)

# set the limits for each axis
axes.set_xlim(-4, 4)
axes.set_ylim(-4, 4)
axes.set_xlabel("real")
axes.set_ylabel("imag")

plt.show()
```

The output looks like this:

<img src="{{'/assets/images/matplotlib_axes.png' | relative_url }}" alt="Axes" style="width:480px;" />

Of course, there's no data yet.

### Plotting Simple Graphs

The next few examples will start with this:

```python
from matplotlib import pyplot as plt

fig, axes = plt.subplots()

# add grid lines
axes.grid(True)
axes.set_xlabel("x")
axes.set_ylabel("y")
```



## Seaborn

