---
title: NetworkX
main_img:
  name: Graphs
  link: /assets/images/networkx_graph.png
tags: 
  - name: Graphs and Graph Theory
    link: /python/graph
  - name: NetworkX
    link: https://networkx.org/documentation/stable/index.html
  - name: Customising NetworkX Graphs
    link: https://towardsdatascience.com/customizing-networkx-graphs-f80b4e69bedf
  - name: Matplotlib
    link: /python/matplotlib
---

## Introduction

[NetworkX](https://networkx.org/documentation/stable/index.html){:target="_blank"} is a cool library that allows us to create, manipulate, interrogate, and render graphs. It can take a lot of the pain out of building graphs.  It also has cool methods that allow us to do things like: _find the shortest path from a to b_. And it can also render the graph as an image for us.

### Installing NetworkX

```
py -m pip install networks
```

### NetworkX Guides and Tutorials

Here are a few useful links:

- [NetworkX Tutorial](https://networkx.org/documentation/stable/tutorial.html){:target="_blank"}
- [NetworkX Reference](https://networkx.org/documentation/stable/reference/index.html){:target="_blank"}
- [Examples Gallery](https://networkx.org/documentation/stable/auto_examples/index.html){:target="_blank"}
- [Layouts](https://networkx.org/documentation/stable/reference/drawing.html#module-networkx.drawing.layout){:target="_blank"}
- [Algorithms](https://networkx.org/documentation/stable/reference/algorithms/index.html){:target="_blank"}
- [Customizing NetworkX Graphs](https://towardsdatascience.com/customizing-networkx-graphs-f80b4e69bedf){:target="_blank"}

### Getting Started With NetworkX

We need to import the relevant packages.  You'll probably want to import `matplotlib.pyplot` if you want to render any [graph visualisations](/python/matplotlib){:target="_blank"}.

```python
import networkx as nx
import matplotlib.pyplot as plt
```

### Supplying Graph Data

Typically, we'll want to build a graph by supplying edge information.  I.e. a connection between one node and another.

For example, let's say we have a list of input data, which each line of data contains two locations.  We might build an _unweighted graph_ like this:

```python
def build_graph(data) -> nx.Graph:
    """ Build graph from list of connected points.

    Args:
        data (list[str]): pairs of points, in the form "Name_X connected to Name_Y"

    Returns:
        dict: (start, end) = distance
    """
    graph = nx.Graph()
    points_match = re.compile(r"^(\w+) connected to (\w+)")
    
    # Add each edge, in the form of a location pair
    for edge in data:
        start, end = points_match.findall(edge)[0]
        graph.add_edge(start, end)

    return graph
```

Or, if we also have some sort of weight information (e.g. distance between points, cost of a route, etc), then we can build a _directed graph_ like this:

```python
def build_graph(data) -> nx.Graph:
    """ Build graph from list of connected points.

    Args:
        data (list[str]): pairs of points, in the form "Name_X to Name_Y = distance_n"

    Returns:
        dict: (start, end) = distance
    """
    graph = nx.Graph()
    distance_match = re.compile(r"^(\w+) to (\w+) = (\d+)")
    
    # Add each edge, in the form of a location pair
    for edge in data:
        start, end, distance = distance_match.findall(edge)[0]
        distance = int(distance)
        graph.add_edge(start, end, distance=distance)
    
    return graph
```