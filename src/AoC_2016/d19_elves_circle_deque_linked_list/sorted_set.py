""" Creating a SortedSet, as an example of how to implement various Collections protocols. 
E.g. Container, Sized, Iterable, Sequence, Set and MutableSet. """
from typing import Iterable
from collections.abc import Sequence, MutableSet
from bisect import bisect_left, insort_left
from itertools import chain

#pylint: disable=arguments-differ

class SortedSet(Sequence, MutableSet):
    """ Implementation of a SortedSet.
    
    Implements the following protocols: 
    Containers, Sized, Iterable, Sequence, Set, MutableSet
    
    Subclasses the Abstract Base Classes: Sequence, MutableSet
    https://docs.python.org/3/library/collections.abc.html
    
    Collections.abc.Sequence provides mixin methods, e.g. index and count, 
    which leverage implementations we override here. 
    
    Collections.abc.MutableSet provides mixin methods: 
    __le__, __lt__, __eq__, __ne__, __gt__, __ge__, __and__, __or__,
    __sub__, __xor__ , isdisjoint(), clear(), pop().
    Though we've overridden some of these to be more efficient. """
    
    def __init__(self, items=None) -> None:
        
        # If we pass in a single item that isn't iterable, turn it into a list first
        if items is not None and not isinstance(items, Iterable):
            items = [items]
        
        # Creating a set throws out all duplicates
        # The sorted() method is useful, since it always returns a list
        self._items = sorted(set(items)) if items is not None else []    # allow items or empty
        self._index = 0
    
    # Implement the Container protocol, which requires __contains__
    def __contains__(self, item) -> bool:
        # We could just return "item in self._items", 
        # but not very efficient to do this with a sorted list
    
        # More efficient to do a binary search algorithm.
        # Here we look for the insertion point for item in a sorted list,
        # or return the index of the item, if it already exists.
        index = bisect_left(self._items, item) 
        
        # If the list already contains the item, 
        # then the returned index will be the index of the item.
        # But before we do that test, we first need to check that 
        # we're not testing an index out of bounds.
        # E.g. if index returned from bisect_left 
        # places the insertion point at the end of the existing list 
        return (index != len(self._items)) and (self._items[index] == item)
    
    # Implement Sized protocol, which requires __len__
    def __len__(self):
        return len(self._items)
    
    # Implement the Iterator protocol, which requires __next__ and __iter__
    def __iter__(self):
        return iter(self._items)
    
    def __next__(self):
        # we could also do: for item in self._items: yield item
        
        if self._index >= len(self._items):
            raise StopIteration
        
        result = self._items[self._index]
        self._index += 1
        return result

    # Implement the Sequence protocol.
    # Needs indexing by position (getitem), indexing by item (index),
    # slicing, reversing, counting, concatenation and repetition
    # If we've implemented __getitem__() and __len__(), 
    # then the mixin method __reversed__() will create a reverse iterator 
    # by walking back from the end.
    
    # We don't need to implement index or count methods, 
    # since we'll get these from collections.abc.Sequence
    # However, since this is a SORTED set, 
    # it's much more efficient to implement our own index method
    # I.e. one that performs a binary bisect algorithm, 
    # rather than a linear search through the whole set.
    def index(self, item) -> int:
        """ Override abc.Sequence.index(). Get index that contains this value 
        Use binary search algorithm, since our data is always sorted. """
        
        # bisect_left finds the insertion point (index) to add item, to maintain a sorted list
        index = bisect_left(self._items, item)
        
        # If the list already contains the item, 
        # then the returned index will be the index of the item.
        # But before we do that test, we first need to check that 
        # we're not testing an index out of bounds.
        # E.g. if index returned from bisect_left 
        # places the insertion point at the end of the existing list 
        if (index != len(self._items)) and (self._items[index] == item):
            return index
        raise ValueError("{} not found".format(repr(item)))
    
    def __getitem__(self, index):
        """Provides implementation for []. 
        If we get using an int value, we want to return a single value.
        If we slice, we want to return a new SortedSet() object.

        Args:
            index ([slice]): Slice object, with start and stop """
        
        result = self._items[index]     # returns item or list
        return SortedSet(result) if isinstance(index, slice) else result
    
    # Concatenation
    def __add__(self, other):
        # chain (flatten) all iterables from both this SortedList, and the other SortedList
        if isinstance(other, SortedSet):
            return SortedSet(chain(self._items, other._items))
        else:
            return NotImplemented
       
    # Repetition using a rhs multiplicand 
    # Since we can't have duplicate values in a set, multiplying by >=1 
    # will always produce the same set
    def __mul__(self, right_multiplicand):
        return SortedSet(self._items) if right_multiplicand >= 1 else SortedSet()
    
    # Repetition using a lhs multiplicand
    def __rmul__(self, left_multiplicand):
        # delegate to __mul__
        return self * left_multiplicand
    
    # Implement the Set protocol.
    # We've already implemented __contains__, __iter__ and __len__.
    # Collections.abc.Set provides a load of mixin methods already, 
    # which implement all the infix operators (e.g. &, |, <, >, ^)
    # But we need to implement the named methods ourselves, i.e.
    # issubset, issuperset, union, intersection, difference, symmetric_difference.
    def issubset(self, iterable):
        return self <= SortedSet(iterable)
    
    def issuperset(self, iterable):
        return self >= SortedSet(iterable)

    def union(self, iterable):
        return self | SortedSet(iterable)

    def intersection(self, iterable):
        return self & SortedSet(iterable)

    def difference(self, iterable):
        return self - SortedSet(iterable)

    def symmetric_difference(self, iterable):
        return self ^ SortedSet(iterable)
    
    # Implement MutableSet protocol methods add and discard
    def add(self, item) -> None:
        """ Add item to the set """
        if item not in self._items:
            insort_left(self._items, item)
    
    def __delitem__(self, index):
        """ To call del on an item by index position """
        self._items.pop(index)
    
    def discard(self, item) -> None:
        """ Discards the specified item.  Faster than remove().
        Does not raise an error if the item does not exist. """
        if item in self._items:
            # faster to find the index by binary search and remove the item at the index,
            # vs simply calling self._items.remove(item)
            index = bisect_left(self._items, item)
            if index <= self._index:
                self._index -= 1    # update the index used for our iterator, i.e. for next()
            self._items.pop(index)

    def __eq__(self, o: object) -> bool:
        """ Test equality (equivalence) """
        if isinstance(o, SortedSet):
            return self._items == o._items
        else:
            # returns obj, not raising an error!  Causing Python to try comparison in reverse
            return NotImplemented   
        
    # Inequality is implemented by default, by negating equality
    # Regardless, best practice to explicitly define __ne__
    def __ne__(self, o: object) -> bool:
        if isinstance(o, SortedSet):
            return self._items != o._items
        else:
            return NotImplemented   
    
    def __repr__(self) -> str:
        """ E.g. empty: SortedSet()
                 not empty: SortedSet([3, 6, 9]) 
        """
        return f"{self.__class__.__name__}({repr(self._items) if self._items else ''})"
