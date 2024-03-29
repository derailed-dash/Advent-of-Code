---
title: NumPy
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
  - [By Reading a Text File](#by-reading-a-text-file)
- [Changing Shape](#changing-shape)
  - [Changing Dimensions](#changing-dimensions)
  - [Flattening](#flattening)
  - [Transposing](#transposing)
- [Basic Mathematical Operations](#basic-mathematical-operations)
  - [On One Array](#on-one-array)
  - [Between Two Arrays](#between-two-arrays)
- [Unary Operations (Including Statistical)](#unary-operations-including-statistical)
- [Indexing and Slicing](#indexing-and-slicing)
  - [Indexing and Slicing with One Dimension](#indexing-and-slicing-with-one-dimension)
  - [Indexing and Slicing with Multiple Dimensions](#indexing-and-slicing-with-multiple-dimensions)
  - [Using Index Arrays](#using-index-arrays)
- [Iterating](#iterating)
- [Rolling](#rolling)
- [Views and Copies](#views-and-copies)
- [Examples](#examples)
  - [Finding the Difference Between Elements](#finding-the-difference-between-elements)
  - [How Many Times is Value n Greater than Value n-1?](#how-many-times-is-value-n-greater-than-value-n-1)
  - [Turning a List of Str into a 2D NumPy Char Array](#turning-a-list-of-str-into-a-2d-numpy-char-array)
  - [Carving Up a 2D Array into Smaller Regions](#carving-up-a-2d-array-into-smaller-regions)
  - [Creating 2D Arrays, and Selecting / Updating Values](#creating-2d-arrays-and-selecting--updating-values)
  - [Counting the Intersection of Lines on a 2D Map](#counting-the-intersection-of-lines-on-a-2d-map)
  - [Counting and Rolling Values](#counting-and-rolling-values)
  - [NumPy, NetworkX and Dijkstra to Navigate a Height Map](#numpy-networkx-and-dijkstra-to-navigate-a-height-map)
- [More Examples](#more-examples)

## NumPy is Awesome

Short for _Numerical Python_, NumPy is core data science library for working with _homogeneous arrays_ of data. The central datastructure of NumPy is the `ndarray`, which is short for _n-dimensional array_. The number of dimensions is called the _rank_.  To help visualise these...

- Think of a rank 1 ndarray as a single row of data.
- Think of a rank 2 ndarray like a table.
- Think of a rank 3 ndarray like a 3d dimensional grid.

Unlike a Python `list` where elements can be of different types, every element in an `ndarray` must be of the same type.  The fact that the elements are of fixed type and size means that data at any position can be accessed, retrieved and manipulated very efficiently. With large arrays (e.g. with millions of elements), this performance advantage is massive.

## When Should You Use Numpy?

NumPy might save you a lot of coding, and be faster, for the following scenarios: 

- When you need to work with multi-dimensional numeric data. Particularly **large arrays of data**.
- When you need to be able to **slice data in more than one dimension**. E.g. where you need to be able to work with 'rectangular' regions of 2D data.
- When you want to perform **mathematical or statistical operations against rows or columns** of data.
- When you want to **use one array to do something to another array**. A trivial example might be having an array of boolean values that we use as a mask for deciding which values we reveal in another array.
- When we want to **flatten or transpose** data.

## Installing and Importing

If you're using a data science distribution like Anaconda, you'll already have NumPy installed.  If not, installing is trivial:

```
py -m pip install numpy
```

When importing, it's standard convention to import as `np`:

```python
import numpy as np
```

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

For example, creating a keypad:

```python
keypad = np.arange(1, 10).reshape(3, 3)
print(keypad)
```

Output:

```text
[[1 2 3]
 [4 5 6]
 [7 8 9]]
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
print(f"original_array: {original_array}")
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
original_array: [0 1 0 3 4]
with_array: [0 1 2 3 4]
with_as_array: [0 1 0 3 4]
```

### By Reading a CSV

```python
data = np.loadtxt(input_file, delimiter=",", dtype=np.int16)
```

### By Reading a Text File

Imagine we want to read in this file:

```text
.#.#.#
...##.
#....#
..#...
#.#..#
####..
```

To read directly into a NumPy array, we can do this:

```python
data = np.genfromtxt(input_file, dtype='U1', comments=None, delimiter=1)
```

Here:
- We use `U1` as the dtype for single character strings, and a delimiter of `1` to read in the data character by character.
- We set `comments=None`, because by default, lines starting with `#` are treated as comments and ignored.
But here, we want to treat `#` as valid data.

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

## Indexing and Slicing

### Indexing and Slicing with One Dimension

Slicing retuns a new array.

```python
one = np.arange(10)
print(one)
a_slice = one[2:4]
print(f"slice [2:4]: {a_slice}, and its type is: {type(a_slice)}")
print(f"slice [-2:]: {one[-2:]}")
print(f"reversing with [::-1]: {one[::-1]}")
```

```text
[0 1 2 3 4 5 6 7 8 9]
slice [2:4]: [2 3], and its type is: <class 'numpy.ndarray'>
slice [-2:]: [8 9]
reversing with [::-1]: [9 8 7 6 5 4 3 2 1 0]
```

### Indexing and Slicing with Multiple Dimensions

```python
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

### Using Index Arrays

As we've seen, we can index an n-dimensional array like this: `my_array[x, y, z]`.

However, if we pass in an array of indeces we can retrieve arbitrary elements from each dimension.  For example, with a one dimensional array, we can pass in an index array [x, y, z], like this: `my_array[[x, y, z]]`:

```python
three = (np.arange(10)**2)+1  # square numbers plus 1
print(three)
index_array = [1, 3, 5]  # a list of indexes
print(f"three[{index_array}]: {three[index_array]}")
```

```text
[ 1  2  5 10 17 26 37 50 65 82]
three[[2, 4, 6]]: [ 5 17 37]
```

We can actually use an index array with a different shape to the array we're indexing. The resulting array will have the same shape as the index array. For example, here we use an index array to retrieve the first, last, second, and penultimate elements from an array, and return them in a 2x2 grid:

```python
index_array = np.array([[0, -1],
                        [1, -2]])
print(f"With 2D index array\n{index_array}:\n{three[index_array]}")
```

```text
With 2D index array
[[ 0 -1]
 [ 1 -2]]:
[[ 1 82]
 [ 2 65]]
```

Here we see how we can pass separate row and column indexes to an array. In this example, we're using this combination of index arrays to retrieve the four corners of a 2D array.

```python
# Obtaining the corners
my_array = np.asarray([['tl', 'tm', 'tr'],
                       ['ml', 'mm', 'mr'],
                       ['bl', 'bm', 'br']])
print(my_array)
row_index = np.array([[0,  0], [-1, -1]]) # top,  top,   bottom, bottom
col_index = np.array([[0, -1], [ 0, -1]]) # left, right, left,   right
print(f"Obtaining the corners with:\n{np.array([row_index, col_index])}...\n" +
      f"{my_array[row_index, col_index]}")
```

```text
[['tl' 'tm' 'tr']
 ['ml' 'mm' 'mr']
 ['bl' 'bm' 'br']]
Obtaining the corners with:
[[[ 0  0]
  [-1 -1]]

 [[ 0 -1]
  [ 0 -1]]]...
[['tl' 'tr']
 ['bl' 'br']]
```

We can even update the corners!!  Note that in this example, I've set the `dtype` to `object`. This allows us store variable length strings. If we don't do this, the strings all get truncated. Doing this does negate many of the performance benefits of using fixed-length contiguous data. But for small arrays, it's fine.

```python
my_array = np.asarray([['tl', 'tm', 'tr'],
                       ['ml', 'mm', 'mr'],
                       ['bl', 'bm', 'br']], dtype=object)
print(my_array)
print("Updating corner elements...")
my_array[row_index, col_index] = "corner"
print(my_array)
```

Output:

```text
[['tl' 'tm' 'tr']
 ['ml' 'mm' 'mr']
 ['bl' 'bm' 'br']]
Updating corner elements...
[['corner' 'tm' 'corner']
 ['ml' 'mm' 'mr']
 ['corner' 'bm' 'corner']]
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

## Rolling

The `roll()` method allows us to move elements off the end of the array, and insert them at the beginning.  We can roll an arbitrary number of items. 

```python
import numpy as np

my_array = np.asarray(([5, 10, 15, 20, 5],
                       [20, 25, 30, 30, 30]))

print(f"Starting array:\n{my_array}")

# If we roll without specifying an axis, then the array is flattened before shifting.
# The resulting array has the same shape as the original
print("\nRolling the whole array...")
rolled = np.roll(my_array, 1)
print(f"Rolled:\n{rolled}")

print("\nRolling by row...")
for row in my_array:
    print(f"Rolled row: {np.roll(row, 1)}")
    
# More efficient to roll by axis
rolled = np.roll(my_array, 1, axis=1)
print(f"\nRolling the whole array by row axis:\n{rolled}")

# Obviously, we can do it by column too
rolled = np.roll(my_array, 1, axis=0)
print(f"\nRolling the whole array by col axis:\n{rolled}")
```

```text
Starting array:
[[ 5 10 15 20  5]
 [20 25 30 30 30]]

Rolling the whole array...
Rolled:
[[30  5 10 15 20]
 [ 5 20 25 30 30]]

Rolling by row...
Rolled row: [ 5  5 10 15 20]
Rolled row: [30 20 25 30 30]

Rolling the whole array by row axis:
[[ 5  5 10 15 20]
 [30 20 25 30 30]]

Rolling the whole array by col axis:
[[20 25 30 30 30]
 [ 5 10 15 20  5]]
```

## Views and Copies

We create a view using the `view()` method.  Views provide a view on the underlying data.  A view is useful if we want to maninpulate metadata of the array, such as the shape.  For example, imagine we want to transpose the array for some analysis, but we don't want to actually modify the data.  Views are a great way to do this efficiently.  In fact, reshaping will typically return a view, not a copy.

Conversely, the `copy()` method creates a shallow copy of the original data.  If you want a deep copy, use `deepcopy.copy(array)`.

## Examples

### Finding the Difference Between Elements

This example creates a one dimensional array of integers. We then use slicing to create show two new arrays:

1. An array starting from the second item, to the end.
1. An array starting from the first item, to the penultimate.

Thus, each item in the first array is n+1, relative to n in the second array.

We can thus determine the differences between each n and n+1, by subtracing the second array from the first.

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

### How Many Times is Value n Greater than Value n-1?

This builds on the previous example.  This time, our elements don't always increase in value.

Again, we create two new views on this array, with the n items and the n-1 items, respectively. But this time, we use the `>` operator to compare the elements in their matching positions. The result is a new array of booleans.

We can count the booleans, to determine how many times the value n was greater than the value n-1.

```python
my_array = np.asarray([1,5,20,15,11,16])
print(my_array)
increases = my_array[1:] > my_array[:-1]
print(f"n > n-1? {increases}")
print(f"Count of (n > n-1): {increases.sum()}")
```

```text
[ 1  5 20 15 11 16]
n > n-1? [ True  True False False  True]
Count of (n > n-1): 3
```

See a more sophisticated example at [2021 Day 1](/2021/1).

### Turning a List of Str into a 2D NumPy Char Array

```python
import numpy as np

data = """abcd
1234
efgh"""

my_array = np.array([list(line) for line in data.splitlines()])
print(my_array)
```

Output:

```text
[['a' 'b' 'c' 'd']
 ['1' '2' '3' '4']
 ['e' 'f' 'g' 'h']]
```

### Carving Up a 2D Array into Smaller Regions

This is taken from [2022 Day 22](/2022/22).

```python
import numpy as np

# Start with data where rows are of different lengths
data = """        1111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666"""

data = data.splitlines()
max_width = max(len(line) for line in data)
        
# Make all rows the same length
data = [line + " " * (max_width - len(line)) if len(line) < max_width else line for line in data]

my_array = np.array([list(line) for line in data])
print(my_array)

face_coords = [(2,0), (0,1), (1,1), (2,1), (2,2), (3,2)] # Faces 0-5
num_horiz_faces = max(x for x,y in face_coords) + 1
face_width = max_width // num_horiz_faces

faces = [my_array[y*face_width:(y+1)*face_width,
                  x*face_width:(x+1)*face_width] for x,y in face_coords]

for face in faces:
    print(face)
```

Output:

```text
[[' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '1' '1' '1' '1' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '1' '1' '1' '1' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '1' '1' '1' '1' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '1' '1' '1' '1' ' ' ' ' ' ' ' ']
 ['2' '2' '2' '2' '3' '3' '3' '3' '4' '4' '4' '4' ' ' ' ' ' ' ' ']
 ['2' '2' '2' '2' '3' '3' '3' '3' '4' '4' '4' '4' ' ' ' ' ' ' ' ']
 ['2' '2' '2' '2' '3' '3' '3' '3' '4' '4' '4' '4' ' ' ' ' ' ' ' ']
 ['2' '2' '2' '2' '3' '3' '3' '3' '4' '4' '4' '4' ' ' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '5' '5' '5' '5' '6' '6' '6' '6']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '5' '5' '5' '5' '6' '6' '6' '6']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '5' '5' '5' '5' '6' '6' '6' '6']
 [' ' ' ' ' ' ' ' ' ' ' ' ' ' ' ' '5' '5' '5' '5' '6' '6' '6' '6']]

Faces:
[['1' '1' '1' '1']
 ['1' '1' '1' '1']
 ['1' '1' '1' '1']
 ['1' '1' '1' '1']]
[['2' '2' '2' '2']
 ['2' '2' '2' '2']
 ['2' '2' '2' '2']
 ['2' '2' '2' '2']]
[['3' '3' '3' '3']
 ['3' '3' '3' '3']
 ['3' '3' '3' '3']
 ['3' '3' '3' '3']]
[['4' '4' '4' '4']
 ['4' '4' '4' '4']
 ['4' '4' '4' '4']
 ['4' '4' '4' '4']]
[['5' '5' '5' '5']
 ['5' '5' '5' '5']
 ['5' '5' '5' '5']
 ['5' '5' '5' '5']]
[['6' '6' '6' '6']
 ['6' '6' '6' '6']
 ['6' '6' '6' '6']
 ['6' '6' '6' '6']]
```

### Creating 2D Arrays, and Selecting / Updating Values

Based on [2015 Day 6](/2015/6).

```python
""" 
Configure 900 lights in a 30x30 grid, by following a set of instructions.
Lights begin turned off.
Coords are 0-indexed

Part 1:
    Instructions require lights to be toggled, turned on, or off.
    Calculate total lights turned on.

Part 2:
    Lights have variable brightness.  Instructions have new meanings:
        Turn on = increase by 1
        Turn off = decrease by 1
        Toggle = increase by 2
    Calculate total brightness.
"""
import re
import numpy as np

DATA = """toggle 1,6 through 2,6
turn off 1,7 through 2,9
turn off 6,1 through 6,3
turn off 8,2 through 11,6
turn on 19,2 through 21,3
turn on 17,4 through 26,8
turn on 10,10 through 19,15
turn off 4,14 through 6,16
toggle 5,15 through 15,25
toggle 20,1 through 29,10"""

INSTR_PATTERN = re.compile(r"(\d+),(\d+) through (\d+),(\d+)")

def main():
    data = DATA.splitlines()
    width = height = 30

    # Part 1
    lights = np.full((width, height), False, dtype=np.bool_) # fill with False
    process_instructions(data, lights)
    print(f"Part 1, lights on: {lights.sum()}")

    # Part 2
    lights = np.zeros((width, height), dtype=np.int8)   # Initialise with 0
    process_variable_brightness_instructions(data, lights)
    print(f"Part 2, brightness: {lights.sum()}")
    
    print(lights)

def process_instructions(data, lights):
    for line in data:
        match = INSTR_PATTERN.search(line)
        assert match, "All instruction lines are expeted to match"
        tl_x, tl_y, br_x, br_y = map(int, match.groups())

        if "toggle" in line:
            # lights[tl_x:br_x+1, tl_y:br_y+1] ^= True
            lights[tl_x:br_x+1, tl_y:br_y+1] = np.logical_not(lights[tl_x:br_x+1, tl_y:br_y+1])
        elif "on" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] = True
        elif "off" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] = False
            
def process_variable_brightness_instructions(data, lights):
    for line in data:
        match = INSTR_PATTERN.search(line)
        assert match, "All instruction lines are expeted to match"
        tl_x, tl_y, br_x, br_y = map(int, match.groups())

        if "toggle" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] += 2
        elif "on" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] += 1
        elif "off" in line:
            lights[tl_x:br_x+1, tl_y:br_y+1] -= 1

        lights[lights < 0] = 0

main()
```

### Counting the Intersection of Lines on a 2D Map

See [2021 Day 5: Hydrothermal vents](/2021/5).

### Counting and Rolling Values

See [2021 day 6: Lantern Fish](/2021/6).

### NumPy, NetworkX and Dijkstra to Navigate a Height Map

See [2022 Day 12: Hill Climbing](/2022/12).

## More Examples

- [On/off grid - 2015 Day 6](/2015/6)
- [Game of life - 2015 Day 18](/2015/18)
- [Counting when values increase - 2021 Day 1](/2021/1)
- [Counting how many times something is true in the grid - 2021 Day 5](/2021/5)
- [Unique, counts, and rolling - 2021 Day 6](/2015/6)
- [Reading CSV - 2021 Day 7](/2021/7)