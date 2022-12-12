---
title: Shortest Path Algorithms
main_img:
  name: Graphs
  link: /assets/images/shortest_path.png
tags: 
  - name: Graphs and Graph Theory
    link: /python/graph
  - name: NetworkX
    link: /python/networkx
  - name: A* Algorithm
    link: https://www.redblobgames.com/pathfinding/a-star/introduction.html
---

## Page Contents

- [Overview](#overview)
- [Algorithm Summary](#algorithm-summary)
- [The Final Frontier!](#the-final-frontier)
- [Breadth First Search (BFS)](#breadth-first-search-bfs)
  - [How It Works](#how-it-works)
  - [The Queue](#the-queue)
  - [Implementing the BFS](#implementing-the-bfs)
  - [Breadcrumb Trail](#breadcrumb-trail)
- [Dijkstra's Algorithm](#dijkstras-algorithm)
- [A* Algorithm](#a-algorithm)

## Overview

These algorithms help you find optimum paths through a graph.

Honestly, you won't get far in Advent-of-Code if you don't know them. Eric loves challenges like...

- _Find the shortest path from a to b_ 
- _Find the optimum way to arrange this thing_

Here are my three top reasons why you should learn this:

1. You'll get the right answer!
1. It'll save you LOADS of time and effort.
1. **These algorithms are cool!!**

## Algorithm Summary

First, let me provide a quick summary and comparison.  Then we'll get into the details after.

|Algorithm|Summary|When To Use It|
|---------|-------|--------------|
|_Breadth First Search (BFS)_|Aka "flood fill". Explores equally in all directions. Uses a FIFO queue. A `list` will do fine.|For finding the shortest path where the _cost_ is constant for any move. Or, for finding ALL paths from a to b.|
|_Dijkstra’s Algorithm_|BFS + a cost-based optimisation. I.e. prioritises paths to explore, favouring lower cost paths. Uses a _priority queue_, i.e. `heapq`.|When movement costs may vary.|
|_A*_|Optimised for a single destination. I.e. prioritises paths that _seem_ to be approaching the goal. Still uses a `heapq`, but uses some sort of cost heuristic. Depending on the value of the distance heuristic, it may not add much value over Dijkstra, and may actually be slower.|When we have an idea of the direction we need to follow|

## The Final Frontier!

All these algorithms utilise the concept of an expanding **frontier**.  This expanding frontier is sometimes called a _flood fill_. **It gives us a way to visit every allowed location on a map.**

How the frontier works:

1. Pick and remove a location from the frontier. Let's call it _current_.
1. Expand the frontier by finding all of the valid next moves from _current_. Let's call them _neighbours_.  Add the _neighbours_ to the frontier.

Here's some code that will perform a flood fill to explore every valid location in the graph:

```python
frontier = Queue() # For BFS, we just use a FIFO queue.
frontier.put(start)
explored = set()  # To stop us exploring the same location more than once.
explored.add(start)

# keep going until the frontier is empty; i.e. when we've explored all the valid nodes
while frontier:   
   current = frontier.popleft()  # pop the first item off the FIFO queue
   for next in graph.neighbors(current):  # get all the valid neighbours
      if next not in explored:
         frontier.put(next) # add it to the frontier
         explored.add(next)  # mark it as explored
```

## Breadth First Search (BFS)

BFS can be used to find a path from a to b. It can also be used to find paths from a to all locations in the graph.

It is **guaranteed to find a solution if one exists.**  The frontier expands at an equal rate in all directions, and uses a FIFO (first-in, first-out) queue to implement the frontier.

### How It Works

- We want to explore a graph, with a _start_. If our graph was a tree, then we start with the root node. So we add the root to the frontier.
- It then explores all adjacent nodes. I.e. we add those to the frontier.
- Then we explore all the nodes that are adjacent to _those_ nodes.
- The BFS algorithm ensures that the same vertex is not followed twice.

So the sequence of exploration looks like this:

![Tree](/assets/images/bfs_tree.png){:style="width: 320px"}

The numbers represent the sequence of traversal. But note that it is possible for the same node to appear in the tree more than once.

When we find a node that matches our goal, we stop. Thus, a **BFS is just a flood fill, with a goal.**

### The Queue

We can implement the queue in many ways:

- Using a vanilla `list`.
- Better: using a `deque` to implement a FIFO queue; it is much more efficient for appending and popping at each end.
- If we use a `heapq`, then we end up popping based on a priority rather than FIFO. This is how we implement _Dijkstra's Algorithm_ or _A*_.
- If we use a `stack`, then we end up with last-in, first-out (LIFO), which actually turns a BFS into a **depth first search (DFS)**!

### Implementing the BFS

Here's some pseudocode that shows how to implement the BFS:

```python
function BFS(graph, root):
  queue = new Queue()
  label root as explored  # we know about this node, but not its children
  queue.enqueue(root)
  while queue not empty:
    current = queue.pop()
    if current is goal:
      return current

    for neighbour in graph.adjacent_nodes(current):
      if neighbour is not explored:
        label neighbour as explored
        queue.enqueue(neighbour)
```

There are a couple of convenient ways to label a node as explored:

1. We can store them in a `set`.
1. We can add them to a `dictionary`

If we use a `set`:

```python
frontier = deque() # For BFS, we just use a FIFO queue. A deque is perfect.
frontier.append(start)
explored = set()  # To stop us exploring the same location more than once.
explored.append(start)

# keep going until the frontier is empty; i.e. when we've explored all the valid nodes
while frontier:   
    current = frontier.popleft()  # pop the first item off the FIFO queue

    if current == goal:
        break

    for next in graph.neighbors(current):  # get all the valid neighbours
        if next not in explored:
            frontier.put(next) # add it to the frontier
            explored.add(next)  # mark it as explored

if current != goal:
    # there was no solution!
```

### Breadcrumb Trail

If we use a `dictionary` instead of a `set`, we can create a _breadcrumb trail_ to each point we've explored.

Let's explore every valid point in the graph:

```python
frontier = deque() # For BFS, we just use a FIFO queue. A deque is perfect.
frontier.append(start)
came_from = {}  #  To stop us exploring the same location more than once; and for breadcrumbs
came_from[start] = None  # This marks the last breadcrumb

# keep going until the frontier is empty; i.e. when we've explored all the valid nodes
while frontier:   
    current = frontier.popleft()  # pop the first item off the FIFO queue

    for next in graph.neighbors(current):  # get all the valid neighbours
        if next not in came_from:
            frontier.put(next) # add it to the frontier
            came_from[next] = current
```

We can then create the breadcrumb path, like this:

```python
current = goal  # start at the end
path = []       # to store every point in a specific path
while current != start: 
   path.append(current)
   current = came_from[current]  # get the next node in the trail
path.append(start) # optional - depends if we want the first node to be included or not
path.reverse() # optional - depends whether we want start->end or end->start
```

## Dijkstra's Algorithm

// Coming soon

## A* Algorithm

// Coming soon