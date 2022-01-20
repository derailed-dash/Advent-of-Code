r"""
Author: Darren
Date: 12/12/2021

Solving https://adventofcode.com/2021/day/12

We need to find all the paths through a network of caves,
and then determine the best path.
The cave map is provided in the form of connected pairs (edges). E.g.
start-A
start-b                     start
A-c                         /   \
A-b                     c--A-----b--d
b-d                         \   /
A-end                        end
b-end

Caves can be connected to 0, 1 or more other caves.
Lowercase is for small caves. Uppercase is for large caves.

Solution 2:
    Still using a BFS, but using NetworkX to build the graph.
    This saves on having to manually create the nodes or the adjacency dictionaries.
    Also allows easy visualisation.

Part 1:
    We want to find the number of distinct paths from start to end,
    where we can visit small caves once, but other caves any number of times.
    
    We wanted an undirected unweighted graph, 
    and then to find number of distinct paths from start to end,
    only visiting small caves (lowercase) 0 or 1 times.
    
    Create an adjacency dictionary, so we can get all neighbours of any cave.
    Determine which are small and which are large.
    
    To find all the unique paths, do a BFS.
    Store (start, path) in the queue.
    While items in the queue:
    - Pop (cave, path)
    - If the cave is the end, we've determined a valid route, so store it and continue.
    - Otherwise, get all the neighbours.
    - If the neighbour is new or big cave, update the path and append to the queue.
    - If not new, then if start/end/small, then skip.

Part 2:
    Now we want to be able to visit a single small cave twice.
    
    Update the BFS so that the queue tuple also contains an attribute
    for whether we've "visited_twice" for any cave.
    Now, if the neighbour is in the path, and the neighbour is a small cave,
    and we haven't yet visited twice, then we can enqueue with visited twice option.
"""
import logging
from pathlib import Path
import time
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = "input/input.txt"
# INPUT_FILE = "input/sample_input.txt"

RENDER = True
OUTPUT_DIR = Path(SCRIPT_DIR / "output/")
OUTPUT_FILE = Path(OUTPUT_DIR / "cave_graph.png")  # where we'll save the animation to

class CaveGraph():
    """ Stores pairs of connected caves, i.e. edges. 
    Determines all caves from supplied edges. 
    Determines which caves are small, and which are large. 
    Creates a lookup to obtain all caves linked to a given cave. 
    Finally, knows how to determine all unique paths from start to end, 
    according to the rules given. """
    
    START = "start"
    END = "end"
    
    def __init__(self, edges:set[tuple[str, str]]) -> None:
        """ Takes a set of edges, where each edge is in the form (a, b) """
        self.start = CaveGraph.START
        self.end = CaveGraph.END
        
        self._graph = nx.Graph()    # Internal implementation of the graph
        self._graph.add_edges_from(edges)   # Build the graph
        
        self._small_caves: set[str] = set()
        self._large_caves: set[str] = set()
        self._categorise_caves()  # populate the empty fields
            
        assert self.start in self._graph, "Start needs to be mapped"
        assert self.end in self._graph, "Finish needs to be mapped"

    def _categorise_caves(self):
        """ Build a set of all caves from the edges.
        This will also initialise small_caves and large_caves """
        
        for edge in self.edges:
            for cave in edge:
                if cave not in (self.start, self.end):
                    if cave.islower():
                        self._small_caves.add(cave)
                    else: 
                        self._large_caves.add(cave)
    
    def render(self, file):
        _ = plt.subplot(121)
        pos = nx.spring_layout(self._graph)
        
        # set colours for each node in the array, in the same order as the nodes
        colours = []
        for node in self.nodes:
            if node in (CaveGraph.START, CaveGraph.END):
                colours.append("green")
            elif node in self.large_caves:
                colours.append("blue")
            else:
                colours.append("red")
        
        nx.draw(self._graph, pos=pos, node_color=colours, with_labels=True)
        
        dir_path = Path(file).parent
        if not Path.exists(dir_path):
            Path.mkdir(dir_path)
        plt.savefig(file)
                 
    @property
    def edges(self) -> tuple[str,str]:
        """ All the edges.  An edge is one cave linked to another. """
        return self._graph.edges
    
    @property
    def nodes(self):
        return self._graph.nodes

    @property
    def small_caves(self):
        """ Caves labelled lowercase. Subset of self.caves. """
        return self._small_caves    

    @property
    def large_caves(self):
        """ Caves labelled uppercase. Subset of self.caves. """        
        return self._large_caves
                    
    def get_paths_through(self, small_cave_twice=False) -> set[tuple]:
        """ Get all unique paths through from start to end, using a BFS.

        Args:
            small_cave_twice (bool, optional): Whether we can 
                    visit a small cave more than once. Defaults to False.
        """
        start = (self.start, [self.start], False)  # (starting cave, [path with only start], used twice)
        queue = deque()
        queue.append(start)  

        unique_paths: set[tuple] = set()    # To store each path that goes from start to end
        
        while queue:
            # If we popleft(), we do a BFS.  If we simply pop(), we're doing a DFS.
            # Since we need to discover all paths, it makes no difference to performance.
            cave, path, used_twice = queue.popleft()    # current cave, paths visited, twice?
            
            if cave == self.end:    # we've reached the end of a desired path
                unique_paths.add(tuple(path))
                continue
            
            for neighbour in self._graph[cave]:
                new_path = path + [neighbour]   # Need a new path object
                if neighbour in path:
                    # big caves fall through and can be re-added to the path
                    
                    if neighbour in (self.start, self.end):
                        continue # we can't revisit start and finish
                    
                    if neighbour in self.small_caves:
                        if small_cave_twice and not used_twice:
                            # If we've visited this small cave once before
                            # Then add it again, but "use up" our used_twice
                            queue.append((neighbour, new_path, True))
                        continue
                
                    assert neighbour in self.large_caves
                    
                # If we're here, it's either big caves or neighbours not in the path
                queue.append((neighbour, new_path, used_twice))
                logger.debug(new_path)
                
        return unique_paths

def main():
    input_file = Path(SCRIPT_DIR, INPUT_FILE)
    with open(input_file, mode="rt") as f:
        edges = set(tuple(line.split("-")) for line in f.read().splitlines())
        
    graph = CaveGraph(edges)    # Create graph from edges supplied in input

    logger.debug("Nodes=%s", graph.nodes)
    logger.debug("Edges=%s", graph.edges)
    
    if RENDER:
        graph.render(OUTPUT_FILE)
    
    # Part 1
    unique_paths = graph.get_paths_through()
    logger.info("Part 1: unique paths count=%d", len(unique_paths))
    
    # Part 2
    unique_paths = graph.get_paths_through(small_cave_twice=True)
    logger.info("Part 2: unique paths count=%d", len(unique_paths))
       
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    logger.info("Execution time: %0.4f seconds", t2 - t1)
