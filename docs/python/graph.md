---
title: Graphs and Graph Theory
main_img:
  name: Graphs
  link: /assets/images/graph_theory.png
tags: 
  - name: Graph Theory (Wikipedia)
    link: https://en.wikipedia.org/wiki/Graph_(abstract_data_type)
  - name: Graph Theory 101 (Harvard Uni)
    link: https://sitn.hms.harvard.edu/flash/2021/graph-theory-101/
---

## Graph Theory Overview

Here we're talking about very specific definitions of a _graph_.  Not the kind of graph where you plot points on x and y axes, but rather: **an abstract model that represents a set of _vertices_ (also called _nodes_ or _points_), linked together by _edges_ (also called links or lines).**

Graphs can be categorised as:

- **Undirected**: edges have no direction; or **directed**: edges have direction.
- **Unweighted**: edges have no magnitude; or **weighted**: edges have magnitude.

We can summarise like this:

|Graph Type|Description|E.g.|
|----------|-----------|----|
|_Undirected_|An associated set of unordered nodes.|![Undirected unweighted](/assets/images/undirected_unweighted.png)|
|_Directed_|An associated set of ordered nodes. It is the direction of the edges (arrows) that dictates order.|![Directed unweighted](/assets/images/directed_unweighted.png)|
|_Unweighted_|The edges have no magnitude. I.e. edges simply join nodes, but edge weight is unimportant.|(Both of the above.)
|_Weighted_|The edges have magnitude, and this magnitude is important.  E.g. the weight could represent distance, or cost.|![Undirected weighted](/assets/images/undirected_weighted.png)|

It's worth noting that undirected graphs can be either unweighted and weighted; and directed graphs can be either unweighted or weightd.

A **tree** is an **_acyclic graph_ - i.e. one in which no loops are created - where vertices are connected by exactly one path.**

![Tree](/assets/images/graph_tree.png)

However, as the image shows, a given node can appear more than once in a tree.

## Adjacency Lists

It's generally a good idea to store graphs using _adjacency lists_.  I.e. a map that links a given vertex to all the vertices it is directly connected to.

Consider the undirected graph above, where:

- 1 is connected to 2 and 5. (2 edges.)
- 2 is connected to 1 and 3. (2 edges.)
- 3 is connected to 2 and 4. (2 edges.)
- 4 is connected to 3 and 6. (2 edges.)
- 5 is connected to 1 and 4. (2 edges.)
- 6 is connected to 4. (1 edge.)

We could build this graph using an adjacency list as follows:

```python

```
