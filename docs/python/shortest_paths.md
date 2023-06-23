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
  - [BFS Examples](#bfs-examples)
- [Dijkstra's Algorithm](#dijkstras-algorithm)
  - [Dijkstra's Algorithm Examples](#dijkstras-algorithm-examples)
- [A* Algorithm](#a-algorithm)
  - [A* Examples](#a-examples)
- [Credit Where It's Due](#credit-where-its-due)

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

<table class="dazbo-table" style="width: 800px">
    <tr>
      <th style="width:100px">Algorithm</th>
      <th style="width:350px">Summary</th>
      <th style="width:350px">When To Use It</th>
    </tr>
    <tr>
      <td style="font-weight: bold">Breadth First Search (BFS)</td>
      <td>Aka "flood fill". Explores equally in all directions. Uses a FIFO queue. 
      A <code class="language-plaintext highlighter-rouge">list</code> will work, 
      but a <code class="language-plaintext highlighter-rouge">deque</code> is best.</td>
      <td>For finding the shortest path where the _cost_ is constant for any move. 
      Or, for finding every point in a graph.  Or for finding ALL paths from a to b.</td>
    </tr>
    <tr>
      <td style="font-weight: bold">Dijkstra’s Algorithm</td>
      <td>Flood fill + a cost-based optimisation. I.e. prioritises paths to explore, favouring lower cost paths. Uses a _priority queue_, i.e. <code class="language-plaintext highlighter-rouge">heapq</code>.</td>
      <td>When movement costs may vary.</td>
    </tr>
    <tr>
      <td style="font-weight: bold">A*</td>
      <td>Optimised for a single destination. I.e. prioritises paths that _seem_ to be approaching the goal. Still uses a <code class="language-plaintext highlighter-rouge">heapq</code>, but uses some sort of cost heuristic. Depending on the value of the distance heuristic, it may not add much value over Dijkstra, and may actually be slower.</td>
      <td>When we have an idea of the direction we need to follow.</td>
    </tr>
</table>

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

- We want to explore a graph, made up of edges connected by vertices. E.g. if we're solving the path through a map, then each map location is a vertex. The graph has a _start_ location, which is the root node of our tree. So we add the root to the frontier.
- It then explores all adjacent nodes. These will be `distance=1` from the root. We add those to the frontier.
- Then we explore all the nodes that are adjacent to _those_ nodes. I.e. the nodes that are `distance=2` from the root.
- The BFS algorithm ensures that the same vertex is not followed twice; i.e. we never revisit a node we've visited before. This is crucial because it means that once we've a path to a note, we must have found the _shortest_ route to that node.

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
frontier = deque() # For BFS, we need a FIFO queue. A deque is perfect.
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

### Keeping Track of Distance

If we're only interested in the shortest distance to a point, but we don't need to create the actual path, a cool trick is to keep track of the distance in our queue.  E.g.

```python
frontier = deque() # For BFS, we need a FIFO queue. A deque is perfect.
frontier.append(start, 0) # Queue always includes (point, steps)
explored = set()  # To stop us exploring the same location more than once.
explored.append(start)

# keep going until the frontier is empty; i.e. when we've explored all the valid nodes
while frontier:   
    current, steps = frontier.popleft()  # pop the first item off the FIFO queue

    if current == goal:
        break

    for next in graph.neighbors(current):  # get all the valid neighbours
        if next not in explored:
            frontier.put(next, steps+1) # add it to the frontier
            explored.add(next)  # mark it as explored

if current != goal:
    # there was no solution!

# distance from start to goal = steps 
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

### BFS Examples

- [Lava basins flood fill with BFS - 2021 Day 9](/2021/9)
- [Cave navigating with BFS and allowing repeats - 2021 Day 12](/2021/12)
- [Cave navigating with BFS and NetworkX - 2021 Day 12](/2021/12)
- [Path through a map with elevation, plus breadcrumb trail - 2022 Day 12](/2022/12)
- [BFS path to outside - 2022 Day 18](/2022/18)
- [BFS with class generating next states - 2022 Day 24](/2022/24)

## Dijkstra's Algorithm

### Dijkstra's Algorithm Examples

- [Risk maze - with heapq and breadcrumbs - 2021 day 15](/2021/15)
- [Lowest cost rearranging amphipods - with next state, heapq and breadcrumbs - 2021 day 23](/2021/23)
- [Hill climbing with NetworkX - 2022 Day 12](/2022/12)

## A* Algorithm

### A* Examples

## Credit Where It's Due

When I first learned these algorithms, the best guide I came across was [this one](https://www.redblobgames.com/pathfinding/a-star/introduction.html){:target="_blank"}. I wrote a lot of notes when I first read it, and in writing this page today, I've been referring to my previous notes.  So, the content I've written here will likely have a lot in common with the amazing content from [https://www.redblobgames.com](https://www.redblobgames.com/){:target="_blank"}.
