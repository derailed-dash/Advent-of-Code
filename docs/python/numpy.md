---
title: Numpy
main_img:
  name: NumPy
  link: /assets/images/numpy_logo.png
tags: 
  - name: NumPy Quick Start
    link: https://numpy.org/devdocs/user/quickstart.html
  - name: NumPy Basics for Beginners
    link: https://numpy.org/devdocs/user/absolute_beginners.html
  - name: NumPy Reference
    link: https://numpy.org/doc/stable/reference/index.html#reference
  - name: pip
    link: /python/packages
---
## Page Contents

- [NumPy is Awesome](#numpy-is-awesome)
- [When Should You Use Numpy?](#when-should-you-use-numpy)
- [Installing and Importing](#installing-and-importing)
- [Getting Started](#getting-started)

## NumPy is Awesome

Short for _Numerical Python_, NumPy is core data science library for working with _homogeneous arrays_ of data. The central datastructure of NumPy is the `ndarray`, which is short for _n-dimensional array_. The number of dimensions is called the _rank_.  To help visualise these...

- Think of a rank 1 ndarray as a single row of data.
- Think of a rank 2 ndarray like a table.
- Think of a rank 3 ndarray like a 3d dimensional grid.

Unlike a Python `list` where elements can be of different types, every element in an `ndarray` must be of the same type.  The fact that the elements are of fixed type and size means that data at any position can be accessed, retrieved and manipulated very efficiently. With large arrays (e.g. with millions of elements), this performance advantage is massive.

## When Should You Use Numpy?

NumPy might save you a lot of coding, and be faster, for the following scenarios: 

- When you need to work with multi-dimensional numeric data. Particularly large arrays of data.
- When you need to be able to slice data in more than one dimension. E.g. where you need to be able to work with 'rectangular' regions of 2D data.
- When you want to perform mathematical or statistical operations against rows or columns of data.
- When you want to use one array to do something to another array. A trivial example might be having an array of boolean values, that we use a mask for deciding which values we reveal in another array.
- When we want to flatten or transpose data.

## Installing and Importing

If you're using a data science distribution like Anaconda, you'll already have NumPy installed.  If not, installing is trivial:

```
py -m pip install numpy
```

When importing, it's standard convention to import as `np`:

```python
import numpy as np
```

## Getting Started

Check out some of the links above to get familiar with NumPy.

### Creating Arrays

#### From a list

```python
import numpy as np

# A 1x3 1D array
my_array = np.array([1, 2, 3])
print(my_array)
```

```text
[1 2 3]
```

#### A 2D Array from a list of lists

```python
# A 2x3 2D array
my_array = np.array([[1, 2, 3], 
                     [4, 5, 6]])
print(my_array)
```

```text
[[1 2 3]
 [4 5 6]]
```

#### Initilising with Zeroes

```python
# Initialise 1x4 to 0 as floats
my_array = np.zeros(4)
print(my_array)
```

```text
[0. 0. 0. 0.]
```

#### Explicitly Setting Type

```python
# Initialise 2x3 to 0 as int
my_array = np.zeros((2,3), dtype=np.int32)
print(my_array)
```

```text
[[0 0 0]
 [0 0 0]]
```

#### Initialising with Specified Value

```python
# Initialise 2x3 to 9
my_array = np.full((2,3), fill_value=9, dtype=np.int32)
print(my_array)
```

```text
[[9 9 9]
 [9 9 9]]
```

#### Initialising a 3D nparray with Boolean Type

```python
# Initialise 2x3x4 3D array to False
my_array = np.full((2,3,4), fill_value=False, dtype=np.bool8)
print(my_array)
```

```text
[[[False False False False]
  [False False False False]
  [False False False False]]

 [[False False False False]
  [False False False False]
  [False False False False]]]
```

#### Initialising With a Range

```python
# Initialise with a range
my_array = np.arange(25, 50, 5)
print(my_array)
```

```text
[25 30 35 40 45]
```

