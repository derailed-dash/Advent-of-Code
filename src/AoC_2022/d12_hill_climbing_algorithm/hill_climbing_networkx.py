from pathlib import Path
import time
import networkx as nx
import numpy as np

SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = Path(SCRIPT_DIR, "input/input.txt")

def main():
    with open(INPUT_FILE, mode="rt") as f:
        height_map = np.array([[ord(x) for x in line.strip()] 
                               for line in f.readlines()]).astype(np.byte)

    start = tuple(np.argwhere(height_map == ord('S'))[0])
    end = tuple(np.argwhere(height_map == ord('E'))[0])
    
    # replace start and end
    height_map[start] = ord('a')
    height_map[end] = ord('z')
    
    all_points = {(tuple(x)) for x in np.transpose(height_map.nonzero())}
    all_vectors =[(dx, dy) for dx in range(-1, 2)
                           for dy in range(-1, 2) if abs(dy) != abs(dx)]

    # Build the graph
    graph = nx.DiGraph()
    for loc in all_points:
        current_height = height_map[loc]
        for vector in all_vectors:
            neighbour = (vector[0] + loc[0], vector[1] + loc[1])
            if neighbour in all_points and height_map[neighbour] - current_height <= 1:
                graph.add_edge(loc, neighbour)

    p1 = nx.shortest_path_length(graph, start, end)
    print(p1)

    # part2
    all_low_elements = [tuple(loc) for loc in np.argwhere(height_map == ord('a'))]
    p2, _ = nx.multi_source_dijkstra(graph, all_low_elements, end)
    print(p2)
            
if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
