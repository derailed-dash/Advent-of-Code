---
title: Map-Filter-Reduce
---
The `map()`, `filter()` and `reduce()` functions are convenient shorthands for applying functions to every member of an iterable. They circumvent the need to write a loop to process the iterable.

- [map](#map)
- [filter](#filter)
- [reduce](#reduce)

## map

The `map()` function **applies a function against every member in a sequence**. The function takes two arguments:

1. The function we need to apply to each member of the iterable, _without_ the parentheses.
1. The iterable itself.

### Converting from Str to Int

Here we apply the `int()` function to each member of a list.  The original list contains str values.

```python
def print_seq(seq):
    for item in seq:
        print(f"{item}, type: {type(item)}")

sequence = ['1', '2', '3', '4', '5'] # list of str values
print("Items in sequence...")
print_seq(sequence)

new_seq = map(int, sequence) # convert each str to an int
print("Items in new_seq...")
print_seq(new_seq)
```

Output:

```text
Items in sequence...
1, type: <class 'str'>
2, type: <class 'str'>
3, type: <class 'str'>
4, type: <class 'str'>
5, type: <class 'str'>
Items in new_seq...
1, type: <class 'int'>
2, type: <class 'int'>
3, type: <class 'int'>
4, type: <class 'int'>
5, type: <class 'int'>
```

### Getting Word Lengths

Here we split a phrase into its constituent words.  Then we apply the `len()` function to each word, to determine the length of each word.

```python
PHRASE = "The quick brown fox jumped over the lazy dog"
words = PHRASE.split()

word_lengths = map(len, words)
for word, word_len in zip(words, word_lengths):
    print(f"Word: {word}, length: {word_len}")
```

Output:

```text
Word: The, length: 3
Word: quick, length: 5
Word: brown, length: 5
Word: fox, length: 3
Word: jumped, length: 6
Word: over, length: 4
Word: the, length: 3
Word: lazy, length: 4
Word: dog, length: 3
```

## filter

The `filter()` function applies a function to each member of an iterable.  The function it applies must always return a `boolean`.  If the function returns `True`, then this member of the iterable is included in the iterable returned by the `filter()` function itself.  If the function returns `False`, then this member is not included.

TL;DR: We can use `filter` to **apply filtering criteria to a collection, and only return those items that meet the criteria.**

As with `map()`, the `filter()` function takes two parameters:

1. The function that is used to filter our collection, _without_ the parentheses.  It must return a boolean.
1. The iterable itself.

### Filtering Based on Word Length

If we continue our example from above, we could write a filter to only return words that have 5 characters or more:

```python
long_words = list(filter(lambda x: len(x) >= 5, words))
print(long_words)
```

Output:

```text
['quick', 'brown', 'jumped']
```

## reduce

