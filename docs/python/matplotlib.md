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
  - name: NumPy
    link: /python/numpy
---
## Page Contents

- [Overview](#overview)
- [Installing](#installing)
- [Basic Usage](#basic-usage)
  - [Getting Axes](#getting-axes)
  - [Showing the Visualisation](#showing-the-visualisation)
  - [Grid Lines and Axis Limits](#grid-lines-and-axis-limits)
  - [Saving the Visualisation to a File](#saving-the-visualisation-to-a-file)
- [Examples](#examples)
  - [Basic Line Plot](#basic-line-plot)
  - [Line Plots with Equations](#line-plots-with-equations)
  - [Argand Diagram](#argand-diagram)
  - [Scatter Plot: No Lines](#scatter-plot-no-lines)
  - [Inverted and With Hidden Axes: Rendering Characters!](#inverted-and-with-hidden-axes-rendering-characters)
  - [Rendering Cubes using Matplotlib and NumPy](#rendering-cubes-using-matplotlib-and-numpy)
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

### Saving the Visualisation to a File

Instead of rendering the visualisation interactively, we can instead save it. This is easy to do.  Instead of using `plt.show()`, we use `plt.savefig()` and pass in the file we want to save to.

```python
# Save visualisation to a file
plt.savefig("myfile.jpg")

# With a transparent background
plt.savefig("myfile.jpg", transparent=True)
```

Maybe we want to save to a particular folder, and create that folder if it doesn't already exit:

```python
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent            # working directory
OUTPUT_DIR = Path(SCRIPT_DIR, "output/")      # where we want to put our new file
OUTPUT_FILE = Path(OUTPUT_DIR, "my_vis.png")  # the name of our new file

if not Path.exists(OUTPUT_DIR):               # Create folder if it doesn't exist
    Path.mkdir(OUTPUT_DIR)
plt.savefig(OUTPUT_FILE)
```

## Examples

The next few examples will start with this:

```python
from matplotlib import pyplot as plt

fig, axes = plt.subplots()

# add grid lines
axes.grid(True)
axes.set_xlabel("x")
axes.set_ylabel("y")
```

### Basic Line Plot 

```python
# create list of points
points = [ (1, 4), (2, 3), (4, 4), (0, 5) ]

# Unpack our x, y vals
all_x, all_y = zip(*points)

# Create out axes
fig, axes = plt.subplots()

# add lines at x=0, y=0 and labels
plt.axhline(0, color='black')
plt.axvline(0, color='black')
axes.set_xlim(0, max(all_x)+1)
axes.set_ylim(0, max(all_y)+1)
axes.set_xlabel("x")
axes.set_ylabel("y")

# add grid lines
axes.grid(True)

plt.plot(all_x, all_y)
plt.show()
```

Output:

<img src="{{'/assets/images/matplotlib_basic_line.png' | relative_url }}" alt="Line Plot" style="width:480px;" />

### Line Plots with Equations

```python
x = np.linspace(0, 2, 100) # Generate a numpy array of data to plot

fig, ax = plt.subplots()  # Create a figure and an axes
ax.plot(x, x, label='linear')  # Plot some data on the axes
ax.plot(x, x**2, label='quadratic')  # Plot more data on the axes...
ax.plot(x, x**3, label='cubic')  # ... and some more.
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend()  # Add a legend.

plt.show()
```

Output:

<img src="{{'/assets/images/matplotlib_line.png' | relative_url }}" alt="Line Plot from Equations" style="width:480px;" />

### Argand Diagram

```python
def cw_rotate(z: complex, degrees: float) -> complex:
    """ Returns a new point, after rotating the supplied point about the origin, clockwise.

    Args:
        z (complex): Point to rotate
        degrees (float): Degrees to rotate, CW

    Returns:
        complex: A new points
    """
    # Note that complex number phase is expressed as a CCW angle to the real axis.
    # Thus, to rotate CW, we have to always take the supplied angle from 360.
    return z * 1j**((360-degrees)/90)

points: list[complex] = [] # store our points

POINT = 3+2j # starting point
print(POINT)
points.append(POINT)

for cw_angle in (90, 180, 270):
    rotated_point = cw_rotate(POINT, cw_angle)
    points.append(rotated_point)

fig, axes = plt.subplots()  # Create out axes
axes.set_aspect('equal') # set x and y to equal aspect
axes.grid(True) # add grid lines

# add lines at x=0, y=0
plt.axhline(0, color='black')
plt.axvline(0, color='black')

# set the limits and labels for each axis
all_x = [num.real for num in points]
all_y = [num.imag for num in points]
axes.set_xlim(min(all_x), max(all_x))
axes.set_ylim(min(all_y), max(all_y))
axes.set_xlabel("real")
axes.set_ylabel("imag")

colours = ['blue', 'orange', 'green', 'red']

# Iterate over each point and plot
for i, point in enumerate(points):
    # For this point, plot from origin to the point
    plt.plot([0, point.real], [0, point.imag], '-', marker='o', color=colours[i])
    
    # Add an annotation to the point.  We can do this one of two ways...
    # plt.text(point.real, point.imag, str(point))
    plt.annotate(str(point), (point.real, point.imag), color=colours[i])
    
plt.show()
```

Output:

<img src="{{'/assets/images/matplotlib_argand.png' | relative_url }}" alt="Argand Plot" style="width:480px;" />

### Scatter Plot: No Lines

We can amend one line above and use the format string parameter to remove the lines, as follows:

```python
plt.plot([0, point.real], [0, point.imag], 'o', color=colours[i])
```

<img src="{{'/assets/images/matplotlib_argand_scatter.png' | relative_url }}" alt="Argand Plot" style="width:480px;" />

### Inverted and With Hidden Axes: Rendering Characters!

Imagine we have a number of (x,y) coordinates defined in a set of `point` objects called `dots`.  We can render them in a cool way, like this:

```python
""" Render these coordinates as a scatter plot """
all_x = [point.x for point in dots]
all_y = [point.y for point in dots]

axes = plt.gca()
axes.set_aspect('equal')
plt.axis("off") # hide the border around the plot axes
axes.set_xlim(min(all_x)-1, max(all_x)+1)
axes.set_ylim(min(all_y)-1, max(all_y)+1)
axes.invert_yaxis()

axes.scatter(all_x, all_y, marker="o", s=50)
plt.show()
```

Output:

<img src="{{'/assets/images/matplotlib_render_dots.png' | relative_url }}" alt="Render Dots" style="width:480px;" />

### Rendering Cubes Using Matplotlib and NumPy

Here's an example that renders 3D cubes based on a `set` of 3D coordinates:

```python
    def vis(self):
        """ Render a visualisation of our droplet """

        axes = [self._max_x+1, self._max_y+1, self._max_z+1]  # set bounds
        grid = np.zeros(axes, dtype=np.int8)   # Initialise 3d grid to empty
        for point in self.filled_cubes:  # set our array to filled for all filled cubes
            grid[point.x, point.y, point.z] = 1
        
        facecolors = np.where(grid==1, 'red', 'black')
        
        # Plot figure
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(grid, facecolors=facecolors, edgecolors="grey", alpha=0.3)
        ax.set_aspect('equal')
        plt.axis("off")
        plt.show()
```

The code above is taken from my [2022 Day 18](/python/2022/18) solution.  The rendered image looks like this:

![Droplet](/assets/images/lava_droplet.png)

## Seaborn

// Coming Soon