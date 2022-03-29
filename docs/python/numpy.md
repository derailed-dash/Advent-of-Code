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

We can create arrays by providing sequences or nested sequences.  

I'll use this block of code to demonstrate various ways of constructing an ndarray, swapping out the input data each time.

```python
import numpy as np

# A 1x3 1D array
my_array = np.array([1, 2, 3])
print(f"Shape: {my_array.shape}")
print(f"Size: {my_array.size}")
print(f"Type: {my_array.dtype}")
print(f"Data:\n{my_array}")
```

#### From a list

```python
# A 1x3 1D array
my_array = np.array([1, 2, 3])
```

```text
Shape: (3,)
Size: 3
Type: int32
Data:
[1 2 3]
```

#### A 2D Array from a list of lists

```python
# A 2x3 2D array
my_array = np.array([[1, 2, 3], 
                     [4, 5, 6]])
```

```text
Shape: (2, 3)
Size: 6
Type: int32
Data:
[[1 2 3]
 [4 5 6]]
```

#### Initilising with Zeroes

```python
# Initialise 1x4 to 0 as floats
my_array = np.zeros(4)
```

```text
Shape: (4,)
Size: 4
Type: float64
Data:
[0. 0. 0. 0.]
```

#### Explicitly Setting Type

```python
# Initialise 2x3 to 0 as int
my_array = np.zeros((2,3), dtype=np.int32)
```

```text
Shape: (2, 3)
Size: 6
Type: int32
Data:
[[0 0 0]
 [0 0 0]]
```

#### Initialising with Specified Value

```python
# Initialise 2x3 to 9
my_array = np.full((2,3), fill_value=9, dtype=np.int16)
```

```text
Shape: (2, 3)
Size: 6
Type: int16
Data:
[[9 9 9]
 [9 9 9]]
```

#### Initialising a 3D nparray with Boolean Type

```python
# Initialise 2x3x4 3D array to False
my_array = np.full((2,3,4), fill_value=False, dtype=np.bool8)
```

```text
Shape: (2, 3, 4)
Size: 24
Type: bool
Data:
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
```

```text
Shape: (5,)
Size: 5
Type: int32
Data:
[25 30 35 40 45]
```

#### Creating Linearly Spaced Values

What if we know the min and max, and we know how many elements we want?

```python
my_array = np.linspace(50, 100, 5)
```

```text
Shape: (5,)
Size: 5
Type: float64
Data:
[ 50.   62.5  75.   87.5 100. ]
```

It's important to note that when using `linspace()`, the second parameter is _inclusive_.  This contrasts to typical Python slicing, where the second number is excluded.

#### With Random Numbers

```python
my_array = np.random.rand(2,4)
```

```text
Shape: (2, 4)
Size: 8
Type: float64
Data:
[[0.86117672 0.30350405 0.94164174 0.73389799]
 [0.27561621 0.46655983 0.93122415 0.82242813]]
```

### Changing Shape

We can change the dimensions of an array.

```python
my_array = np.arange(start=10, stop=20, dtype=np.int16)
print(f"Shape: {my_array.shape}")
print(f"Size: {my_array.size}")
print(f"Type: {my_array.dtype}")
print(f"Data:\n{my_array}")

print("\nAfter reshaping...")
reshaped = my_array.reshape(2,5)
print(f"Shape: {reshaped.shape}")
print(f"Size: {reshaped.size}")
print(f"Type: {reshaped.dtype}")
print(f"Data:\n{reshaped}")
```

```text
Shape: (10,)
Size: 10
Type: int16
Data:
[10 11 12 13 14 15 16 17 18 19]

After reshaping...
Shape: (2, 5)
Size: 10
Type: int16
Data:
[[10 11 12 13 14]
 [15 16 17 18 19]]
 ```

 We can also flatten an existing array:

```python
 my_array = np.asarray([[2,3,4],
                      [5,6,7]])
print(f"Shape: {my_array.shape}")
print(f"Data:\n{my_array}")

print("\nAfter flattening...")
flattened = my_array.flatten()
print(f"Shape: {flattened.shape}")
print(f"Data:\n{flattened}") 
```

```text
Shape: (2, 3)
Data:
[[2 3 4]
 [5 6 7]]

After flattening...
Shape: (6,)
Data:
[2 3 4 5 6 7]
```