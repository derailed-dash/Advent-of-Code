---
title: Sets
tags: 
  - name: Python Sets
    link: https://www.tutorialspoint.com/python_data_structure/python_sets.htm
  - name: classes
    link: classes
---
**Sets** are really useful when we want to store a number of unique items, but we don't care about the order of those items.

Python sets have these attributes:

- They cannot contain duplicate items.  Adding a duplicate item simply does nothing.
- The items in the set must be _immutable_. I.e. objects that can't be modified and which are _hashable_. For this reason, it can be extremely convenient to use the [dataclass](classes#dataclass) when defining your own objects for use in sets, with the `frozen=True` attribute set.
- Items in the set are _unordered_. Thus, items are not _indexable_.  (Though, if you want an ordered set, you can create your own implementation.)

You should consider using sets whenever you need to:

- Count how many items in a collection are unique.
- Perform set algebra, such as:
  - Determine if an object already exists in another set (membership).
  - Determine which items overlap, across two different sets.

## Set Algebra

Mathematical _set algebra_ is easily achieved using Python sets. For example, we can use set algebra to determine when one `set` _contains_ another `set`, any _intersection_ of sets, any _difference_ between sets, and any _union_ that is created by combining sets.

<table class="dazbo-table" style="background: white; width: 440px">
    <tr>
      <th>Set Relationship</th>
      <th>Looks like</th>
    </tr>
    <tr><td>Union (&)</td><td><img src="{{'/assets/images/set_union.png' | relative_url }}" alt="Set union" style="width:100px;"/></td></tr>
    <tr><td>Intersection(&)</td><td><img src="{{'/assets/images/set_intersection.png' | relative_url }}" alt="Set intersection" style="width:100px;"/></td></tr>
    <tr><td>Difference (-)</td><td><img src="{{'/assets/images/set_difference.png' | relative_url }}" alt="Set difference" style="width:100px;"/></td></tr>
    <tr><td>Symmmetric Difference</td><td><img src="{{'/assets/images/symmetric_diff.png' | relative_url }}" alt="Set difference" style="width:100px;"/></td></tr>
    <tr><td>Superset/Contains (>)</td><td><img src="{{'/assets/images/set_superset.png' | relative_url }}" alt="Set difference" style="width:100px;"/></td></tr> 
    <tr><td>Subset (<)</td><td></td></tr>    
</table>
