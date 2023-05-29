""" Testing the type_defs module """
from common.type_defs import Point

my_point = Point(5, 5)
print(my_point)

all_neighbours = my_point.neighbours()
print(all_neighbours)

diag_neighbours = my_point.neighbours(include_diagonals=False)
print(diag_neighbours)
