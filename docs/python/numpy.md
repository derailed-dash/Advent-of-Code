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
- [Creating Arrays](#creating-arrays)
  - [From a List](#from-a-list)
  - [A 2D Array from a list of lists](#a-2d-array-from-a-list-of-lists)
  - [Initilising with Zeroes](#initilising-with-zeroes)
  - [Explicitly Setting Type](#explicitly-setting-type)
  - [Initialising with Specified Value](#initialising-with-specified-value)
  - [Initialising a 3D Array with Boolean Type](#initialising-a-3d-array-with-boolean-type)
  - [Initialising With a Range](#initialising-with-a-range)
  - [Creating Linearly Spaced Values](#creating-linearly-spaced-values)
  - [With Random Numbers](#with-random-numbers)
  - [Creating an Array Based on Another Array](#creating-an-array-based-on-another-array)
  - [By Reading a CSV](#by-reading-a-csv)
- [Changing Shape](#changing-shape)
  - [Changing Dimensions](#changing-dimensions)
  - [Flattening](#flattening)
  - [Transposing](#transposing)
- [Basic Mathematical Operations](#basic-mathematical-operations)
  - [On One Array](#on-one-array)
  - [Between Two Arrays](#between-two-arrays)
- [Unary Operations (Including Statistical)](#unary-operations-including-statistical)
- [Examples](#examples)
  - [Finding the Difference Between Elements](#finding-the-difference-between-elements)
- [Indexing and Slicing](#indexing-and-slicing)
- [Iterating](#iterating)

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

## Creating Arrays

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

### From a list

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

### A 2D Array from a list of lists

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

### Initilising with Zeroes

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

### Explicitly Setting Type

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

### Initialising with Specified Value

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

### Initialising a 3D Array with Boolean Type

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

### Initialising With a Range

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

### Creating Linearly Spaced Values

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

### With Random Numbers

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

### Creating an Array Based on Another Array

```python
my_array = np.asarray([[2,3,4],
                      [5,6,7]])
print(my_array)
new_array = np.zeros_like(my_array)
print(new_array)
```

```text
[[2 3 4]
 [5 6 7]]
[[0 0 0]
 [0 0 0]]
```

Note that `np.array()` makes a copy of the original data when creating the `ndarray`.  Changes to the `ndarray` will not be reflected in the original array. Whereas `np.asarray()` does not create a copy. So changes to the array are reflected in the original array.

```python
import numpy as np

original_array = np.array(list(range(5)))

print("Creating with np.array()...")
with_array = np.array(original_array)
print(with_array)

print("Creating with np.asarray()...")
with_as_array = np.asarray(original_array)
print(with_as_array)

print("Updating the original array...")
original_array[2] = 0
print(f"my_list: {original_array}")
print(f"with_array: {with_array}")
print(f"with_as_array: {with_as_array}")
```

Output:

```text
Creating with np.array()...
[0 1 2 3 4]
Creating with np.asarray()...
[0 1 2 3 4]
Updating the original array...
my_list: [0 1 0 3 4]
with_array: [0 1 2 3 4]
with_as_array: [0 1 0 3 4]
```

### By Reading a CSV

```python
data = np.loadtxt(input_file, delimiter=",", dtype=np.int16)
```

## Changing Shape

### Changing Dimensions

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

### Flattening

We can also flatten an existing array.  The `flatten()` method takes an existing array, and returns a new, flattened array.

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

### Transposing

```python
my_array = np.asarray([[2,3,4],
                      [5,6,7]])
print(my_array)
print(f"Transposed:\n{my_array.T}")
```

```text
[[2 3 4]
 [5 6 7]]
Transposed:
[[2 5]
 [3 6]
 [4 7]]
 ```

## Basic Mathematical Operations

### On One Array

You can perform basic mathematical operations on an array.  The operation applies to every element in the array, and returns a new array with the same shape.

```python
my_array = np.asarray([[5, 10, 15, 20, 5],
                       [20, 25, 30, 30, 30]])

plus_one = my_array + 1
times_two = my_array * 2

print(f"my_array:\n{my_array}")
print(f"plus_one:\n{plus_one}")
print(f"times_two:\n{times_two}")
```

```text
my_array:
[[ 5 10 15 20  5]
 [20 25 30 30 30]]
plus_one:
[[ 6 11 16 21  6]
 [21 26 31 31 31]]
times_two:
[[10 20 30 40 10]
 [40 50 60 60 60]]
```

### Between Two Arrays

We can perform basic arithmetic between two arrays of the same shape. The mathematical operations are performed between elements in the identical positions of the two arrays.

```python
one = np.asarray([[1, 2],
                  [3, 4]])

two = np.asarray(([5, 10],
                  [15, 20]))

print(f"one:\n{one}")
print(f"two:\n{two}")

print(f"one+two:\n{one+two}")
print(f"one*two:\n{one*two}")
print(f"two/one:\n{two/one}")
```

```text
one:
[[1 2]
 [3 4]]
two:
[[ 5 10]
 [15 20]]
one+two:
[[ 6 12]
 [18 24]]
one*two:
[[ 5 20]
 [45 80]]
two/one:
[[5. 5.]
 [5. 5.]]
```

## Unary Operations (Including Statistical)

```python
my_array = np.asarray([[5, 10, 15, 20, 5],
                       [20, 25, 30, 30, 30]])
print(f"my_array:\n{my_array}")

print("\nWorking with sums...")
print(f"sum: {my_array.sum()}")
print(f"sum axis 0 (cols): {my_array.sum(axis=0)}")
print(f"sum axis 1 (rows): {my_array.sum(axis=1)}")
print(f"Cumulative sum: {my_array.cumsum()}")

print("\nBasic numerical analysis...")
print(f"max: {my_array.max()}")
print(f"min axis 0 (cols): {my_array.min(axis=0)}")
print(f"mean axis 0 (cols): {my_array.mean(axis=0)}")
print(f"median axis 1 (rows): {np.median(my_array, axis=1)}")

print("\nGet sorted unique items, and their counts...")
uniques, counts = np.unique(my_array, return_counts=True)
print(f"Uniques: {uniques}")
print(f"Counts: {counts}")
```

```text
my_array:
[[ 5 10 15 20  5]
 [20 25 30 30 30]]

Working with sums...
sum: 190
sum axis 0 (cols): [25 35 45 50 35]
sum axis 1 (rows): [ 55 135]
Cumulative sum: [  5  15  30  50  55  75 100 130 160 190]

Basic numerical analysis...
max: 30
min axis 0 (cols): [ 5 10 15 20  5]
mean axis 0 (cols): [12.5 17.5 22.5 25.  17.5]
median axis 1 (rows): [10. 30.]

Get sorted unique items, and their counts...
Uniques: [ 5 10 15 20 25 30]
Counts: [2 1 1 2 1 3]
```

## Examples

### Finding the Difference Between Elements

```python
my_array = np.asarray([1,2,4,7,11,16])
print(my_array)

print(f"From 2nd to the end: {my_array[1:]}")
print(f"From 1st to penultimate: {my_array[:-1]}")
print(f"Diffs: {my_array[1:]-my_array[:-1]}")
```

```text
[ 1  2  4  7 11 16]
From 2nd to the end: [ 2  4  7 11 16]
From 1st to penultimate: [ 1  2  4  7 11]
Diffs: [1 2 3 4 5]
```

## Indexing and Slicing

```python
one = np.arange(10)
print(one)
print(f"slice [2:4]: {one[2:4]}")
print(f"slice [-2:]: {one[-2:]}")
print(f"reversing with [::-1]: {one[::-1]}")

print()
two = np.asarray([[5, 10, 15, 20, 5],
                  [20, 25, 30, 30, 30],
                  [15, 12, 9, 6, 3]])
print(two)
print(f"two.shape: {two.shape}")
print(f"Accessing the first row with [0]: {two[0]}")
print(f"The same result with [0,:]:  {two[0,:]}")
print(f"The same result with [0,...]:  {two[0,...]}")
print(f"Accessing first row, 3rd element with [0,2]: {two[0,2]}")
print(f"Accessing all rows, third column with [:,2]: {two[:,2]}")
print(f"The same result with [...,2]: {two[...,2]}")
print(f"Accessing a 2D grid with [1:, 2:4]:\n{two[1:, 2:4]}")
```

```text
[0 1 2 3 4 5 6 7 8 9]
slice [2:4]: [2 3]
slice [-2:]: [8 9]
reversing with [::-1]: [9 8 7 6 5 4 3 2 1 0]

[[ 5 10 15 20  5]
 [20 25 30 30 30]
 [15 12  9  6  3]]
two.shape: (3, 5)
Accessing the first row with [0]: [ 5 10 15 20  5]
The same result with [0,:]:  [ 5 10 15 20  5]
The same result with [0,...]:  [ 5 10 15 20  5]
Accessing first row, 3rd element with [0,2]: 15
Accessing all rows, third column with [:,2]: [15 30  9]
The same result with [...,2]: [15 30  9]
Accessing a 2D grid with [1:, 2:4]:
[[30 30]
 [ 9  6]]
```

## Iterating

Iterating follows the same rules as indexing and slicing.

Note the use of `np.nditer()` to return an iterator that allows the original array to be updated in place.

```python
one = np.arange(10)  # create 1D array
print(one)

print("\nIterating over items...")
for item in one:
    print(item)
    item *= 2   # This will achieve nothing in the original array!

print("Did the array update? No...")
for item in one:
    print(item)

# But we can create a read/write iterator:
print("\nUpdate using nditer...:")
for item in np.nditer(one, op_flags=['readwrite']):
    item *= 2

print("Did the array update? Yes...")   
for item in one:
    print(item)
```

```text
[0 1 2 3 4 5 6 7 8 9]

Iterating over items...
0
1
2
3
4
5
6
7
8
9
Did the array update? No...
0
1
2
3
4
5
6
7
8
9

Update using nditer...:
Did the array update? Yes...
0
2
4
6
8
10
12
14
16
18
```

Iterating with more than one dimension:

```python
print(two)
print(f"two.shape: {two.shape}")
print("\nIterating over rows")
for row in two:
    print(row)

print("\nIterating over a row with [0]")
for item in two[0]:
    print(item)

print("The same result with [0, ...]")
for item in two[0, ...]:
    print(item)
    
# Array index shorthand
print("The same result with [0, ...]")
for item in two[0, ...]:
    print(item[...])

print("\nIterating over all rows, third column with [: ,2]:")
for item in two[: ,2]:
    print(item)
    
print("\nFlattening row-wise and iterating over all:")
for item in two.flatten():
    print(item)
    
print("Or iterating over all, without creating a flatted array first:")
for item in np.nditer(two):
    print(item)

print("\nFlattening column-wise and iterating over all:")
for item in two.flatten(order="F"):
    print(item)
    
print("Or iterating over all, without creating a flatted array first:")
for item in np.nditer(two, order="F"):
    print(item)
```

```text
[[ 5 10 15 20  5]
 [20 25 30 30 30]
 [15 12  9  6  3]]
two.shape: (3, 5)

Iterating over rows
[ 5 10 15 20  5]
[20 25 30 30 30]
[15 12  9  6  3]

Iterating over a row with [0]
5
10
15
20
5
The same result with [0, ...]
5
10
15
20
5
The same result with [0, ...]
5
10
15
20
5

Iterating over all rows, third column with [: ,2]:
15
30
9

Flattening row-wise and iterating over all:
5
10
15
20
5
20
25
30
30
30
15
12
9
6
3
Or iterating over all, without creating a flatted array first:
5
10
15
20
5
20
25
30
30
30
15
12
9
6
3

Flattening column-wise and iterating over all:
5
20
15
10
25
12
15
30
9
20
30
6
5
30
3
Or iterating over all, without creating a flatted array first:
5
20
15
10
25
12
15
30
9
20
30
6
5
30
3
```