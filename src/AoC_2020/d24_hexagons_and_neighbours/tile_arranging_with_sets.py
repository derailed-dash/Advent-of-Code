"""
Author: Darren
Date: 24/12/2020

Solving: https://adventofcode.com/2020/day/24

Floor of hexagonal tiles.  They have two sides: white and black.
Tiles start white side up.

Part 1
------
Coordinate system that describes tiles to be flipped.  Each row describes coords to a single tile.
Always start at reference tile (tile 0) and then follow coord instructions in an input row.
Coords are ne, e, se, sw, w, nw.  E.g.
sesenwnenenewseeswwswswwnenewsewsw

How many tiles end up black side up?

Part 2
------
Conway-like rules, that flip certain tiles (simultaneously) with each iteration.  Rules:
    - Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    - Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

Solution 2 of 2
---------------
Using sets rather than dicts is ~10x faster.

Let's use x,y coords to describe tile locations.
Hexagon class stores its colour, and knows how to get adjacent vectors, and how to get neighbours.
Store only black tiles in black_tiles set. Use set algebra to check if neighbours are black.
With each iteration:
    Create new padded set, to account for edge effects.
        Note: when padding, only add hexagons where x and y are both even, or x and y are both odd.
        This cuts the time by at least half.
    Loop through all tiles.  
    Find neighbours for each.  Create black_neighbours_set using intersection.
    Add / remove tiles from black_tiles, accordingly.
"""
import os
import time
import re
import imageio
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from AoC_2020.d24_hexagons_and_neighbours.hex import Hexagon

SCRIPT_DIR = os.path.dirname(__file__)
INPUT_FILE = "input/data.txt"
SAMPLE_INPUT_FILE = "input/sample_data.txt"

NUMBER_OF_ITERATIONS = 10

# enable if you want to create an animation
ANIM_ENABLED = True
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output/")
ANIM_FILE = os.path.join(OUTPUT_DIR, "tile_anim.gif")
anim_frame_files = []

def main():
    # input_file = os.path.join(SCRIPT_DIR, INPUT_FILE)
    input_file = os.path.join(SCRIPT_DIR, SAMPLE_INPUT_FILE)
    print("Input file is: " + input_file)
    data = read_input(input_file)

    black_tiles = process_tile_positions(data)
    print(f"Sum of black tiles: {len(black_tiles)}")

    living_art(black_tiles, NUMBER_OF_ITERATIONS)
    print(f"Sum of black tiles: {len(black_tiles)}")

    if is_vis_enabled():
        build_anim()
    else:
        print("Visualisation disabled.")


def is_vis_enabled():
    return ANIM_ENABLED and NUMBER_OF_ITERATIONS <= 15

def pad_all_tiles(black_tiles, all_tiles):
    min_x = min(black_tiles, key=lambda x: x[0])[0]
    max_x = max(black_tiles, key=lambda x: x[0])[0]
    min_y = min(black_tiles, key=lambda x: x[1])[1]
    max_y = max(black_tiles, key=lambda x: x[1])[1]

    # Note, we have to go 2 either side for x, since e and w coords are +/- 2 on x axis.
    for x in range(min_x - 2, max_x + 3):
        for y in range(min_y - 1 , max_y + 2):
            locn = tuple([x, y])

            if locn not in all_tiles:
                if (locn[0] %2 == 0 and locn[1] %2 == 0):
                    all_tiles.add(locn)
                elif (locn[0] %2 != 0 and locn[1] %2 != 0):
                    all_tiles.add(locn)
    return


def vis_state(black_tiles, all_tiles, iteration):
    white_tiles = all_tiles.difference(black_tiles)

    all_x, all_y = zip(*all_tiles)
    white_x, white_y = zip(*white_tiles)
    black_x, black_y = zip(*black_tiles)
    
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # hexagon!
    shape = 'h'

    fig, ax = plt.subplots(dpi=141)
    ax.set_facecolor('xkcd:orange')
    ax.set_xlim(min_x-1, max_x+1)
    ax.set_ylim(min_y-1, max_y+1)

    # we want x axis compressed, given our hex geometry.
    # I.e. given that e or w = 2 units.
    ax.set_aspect(1.75)

    # dynamically compute the marker size
    fig.canvas.draw()
    mkr_size = ((ax.get_window_extent().width / (max_x-min_x) * (134/fig.dpi)) ** 2)

    # make sure the ticks have integer values
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    ax.scatter(black_x, black_y, marker=shape, s=mkr_size, color='black', edgecolors='black')
    ax.scatter(white_x, white_y, marker=shape, s=mkr_size, color='white', edgecolors='black')
    ax.set_title(f"Tile Floor, Iteration: {iteration-1}")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # save the plot as a frame
    filename = OUTPUT_DIR + "tiles_anim_" + str(iteration) + ".png"
    plt.savefig(filename)
    # plt.show()
    anim_frame_files.append(filename)

def build_anim():
    with imageio.get_writer(ANIM_FILE, mode='I', fps=0.75) as writer:
        for filename in anim_frame_files:
            image = imageio.imread(filename)
            writer.append_data(image)

    for filename in set(anim_frame_files):
        os.remove(filename)


def living_art(black_tiles, iterations):
    iteration = 0
    all_tiles = set()

    while (iteration < iterations):
        tiles_to_remove = set()
        tiles_to_add = set()

        iteration += 1
        # print(f"Iteration: {iteration}")
        
        pad_all_tiles(black_tiles, all_tiles)
        if ANIM_ENABLED:
            if (NUMBER_OF_ITERATIONS > 15):
                print("You probably ought to reduce the number of iterations!")
            else:
                vis_state(black_tiles, all_tiles, iteration)

        for tile_location in all_tiles:
            neighbours = set(Hexagon.get_neighbours(tile_location))
            black_neighbours =  len(neighbours.intersection(black_tiles))

            if tile_location in black_tiles:
                # print(f"Black tile {tile_location} has {black_neighbours} black neighbours.")
                if black_neighbours == 0 or black_neighbours > 2:
                    tiles_to_remove.add(tile_location)
            else:
                # white tile
                if black_neighbours == 2:
                    tiles_to_add.add(tile_location)

        black_tiles.update(tiles_to_add)
        black_tiles.difference_update(tiles_to_remove)


def read_input(a_file):
    with open(a_file, mode="rt") as f:
        data = f.read().splitlines()

    return data


def process_tile_positions(data):
    ''' Return only black tiles at the referenced positions '''
    tokenizer = re.compile(r'(ne|e|se|sw|w|nw)')

    # store tiles as { [x,y]: Hexagon('b'), [x,y]: Hexagon('w'), etc}
    tiles = {}

    for tile in data:
        tokens = tokenizer.findall(tile)
        location_x = 0
        location_y = 0
        for token in tokens:
            vector = Hexagon.get_vector(token)
            location_x += vector[0]
            location_y += vector[1]
        
        target_location = tuple([location_x, location_y])
        if target_location not in tiles:
            tiles[target_location] = Hexagon('b')
        else:
            tiles[target_location].flip()
    
    return set(coord for coord, hex in tiles.items() if hex.is_black())


if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
