""" Testing the type_defs module """
import unittest
from shutil import rmtree
from os import path
from common.aoc_commons import (
    Point, 
    Grid, 
    Vectors, 
    VectorDicts, 
    write_puzzle_input_file,
    binary_search, 
    merge_intervals,
    get_factors,
    get_locations,
    to_base_n
)

class TestTypes(unittest.TestCase):
    """ Unit tests of various classes in type_defs """
    
    def setUp(self):
        self.locations = get_locations(__file__)
        self.clear_input_file()
        
        self.points = set()
        self.a_point = Point(5, 5)
        self.b_point = Point(1, 2)
        self.c_point = Point(6, 7)
        self.d_point = Point(4, 3)
        self.e_point = Point(3, 6)
        self.y_invert_point = Point(0, -1)
        
        self.points.add(self.a_point)
        self.points.add(self.b_point)  
        self.points.add(self.c_point)  
        self.points.add(self.d_point)  
        self.points.add(self.e_point)
        
        self.a_point_neighbours = self.a_point.neighbours()

    def clear_input_file(self):
        """ Clear the input file """
        if self.locations.input_dir.exists():
            print(f"Deleting {self.locations.input_dir}")
            rmtree(self.locations.input_dir)
    
    def test_locations(self):
        """ That folder and file names are as expected """   
        # use normcase to un-escape and ignore case differences in the paths
        script_directory = path.normcase(path.dirname(path.realpath(__file__)))
        self.assertEqual(path.normcase(self.locations.script_dir), script_directory)
        
        this_script = path.splitext(path.basename(__file__))[0]
        self.assertEqual(self.locations.script_name, this_script)        

    def test_write_puzzle_input_file(self):
        """ We can create an input folder and input file """
        
        # Try to retrieve input that does not exist
        self.assertTrue(write_puzzle_input_file(2010, 1, self.locations))
        with open(self.locations.input_file, "r") as file:
            data = file.read()
        self.assertIn("Failed", data)
        
        # Clear the folder and then retrieve legitimate input
        self.clear_input_file()
        self.assertTrue(write_puzzle_input_file(2015, 1, self.locations))
        with open(self.locations.input_file, "r") as file:
            data = file.read()
        self.assertIn("(((())))", data)
        
        # Does not retrieve file if it already exists
        self.assertFalse(write_puzzle_input_file(2015, 1, self.locations))

    def test_vectors(self):
        self.assertEqual(Vectors.N.value, (0, 1))
        self.assertEqual(Vectors.NW.value, (-1, 1))
        self.assertEqual(Vectors.S.value, (0, -1))
        self.assertEqual(Vectors.E.value, (1, 0))
        self.assertEqual(Vectors.N.y_inverted, (0, -1))
        self.assertEqual(Vectors.SW.value, (-1, -1))
        
    def test_vector_dicts(self):
        self.assertEqual(VectorDicts.ARROWS[">"], (1, 0))
        self.assertEqual(VectorDicts.ARROWS["v"], (0, -1))
        self.assertEqual(VectorDicts.DIRS["L"], (-1, 0))
        self.assertEqual(VectorDicts.DIRS["U"], (0, 1))
        self.assertEqual(VectorDicts.NINE_BOX["tr"], (1, 1))
        self.assertEqual(VectorDicts.NINE_BOX["bl"], (-1, -1))
        
    def test_point_arithmetic(self):
        self.assertEqual(self.a_point + self.b_point, self.c_point, "Asserting Point addition")
        self.assertEqual(self.a_point - self.b_point, self.d_point, "Asserting Point subtraction")
        self.assertEqual(self.b_point * Point(3, 3), self.e_point, "Asserting multiplication")
    
    def test_manhattan_distance(self):
        self.assertEqual(Point.manhattan_distance(self.e_point), 3+6)
        self.assertEqual(self.c_point.manhattan_distance_from(self.b_point), abs(self.a_point.x)+abs(self.a_point.y))
        
    def test_point_containers(self):
        all_neighbours_count = 8 # point has 8 neighbours
        diag_neighbours_count = 4 # point has 4 orthogonal neighbours

        self.assertEqual(len(self.a_point_neighbours), all_neighbours_count, 
                         f"Expect {all_neighbours_count} from all neighbours")
        
        a_point_diag_neighbours = self.a_point.neighbours(include_diagonals=False)
        self.assertEqual(len(a_point_diag_neighbours), diag_neighbours_count, 
                         f"Expect {diag_neighbours_count} orthogonal neighbours")
        self.assertNotIn(self.a_point, self.a_point.neighbours(), 
                         "Check neighbours does not include self")
        self.assertIn(self.a_point, self.a_point.neighbours(include_self=True), 
                         "Check neighbours includes self")
        self.assertEqual(len(self.a_point.neighbours(include_self=True)), all_neighbours_count+1, 
                         f"All neighbours with self should be {all_neighbours_count+1}")
        
    def test_point_neighbour_generator(self):
        gen = self.a_point.yield_neighbours()
        
        for _ in range(len(self.a_point_neighbours)):
            self.assertIn(next(gen), self.a_point_neighbours, "Generated item is a valid neighbour")
            
        with self.assertRaises(StopIteration): # no more items to generate
            next(gen)
            
    def test_grid(self):
        input_grid = ["5483143223",
                      "2745854711",
                      "5264556173",
                      "6141336146",
                      "6357385478",
                      "4167524645",
                      "2176841721"]
    
        input_array_data = [[int(posn) for posn in row] for row in input_grid]      
        grid = Grid(input_array_data)
        self.assertEqual(grid.height, len(input_grid))
        self.assertEqual(grid.width, len(input_grid[0]))
        self.assertTrue(grid.valid_location(Point(1, 1)))
        self.assertFalse(grid.valid_location(Point(11,8)))
        self.assertEqual(grid.value_at_point(Point(1, 1)), 7)
        self.assertEqual(grid.rows_as_str()[0], "5483143223")
        self.assertEqual(grid.cols_as_str()[0], "5256642")
      
    def test_binary_search(self):
        self.assertEqual(binary_search(225, 0, 20, lambda x: x**2, reverse_search=True), None)
        self.assertEqual(binary_search(225, 0, 20, lambda x: x**2), 15)
    
    def test_merge_intervals(self):
        pairs = [
            [1, 5],    # Non-overlapping pair
            [3, 7],    # Overlapping pair
            [8, 12],   # Non-overlapping pair
            [10, 15],  # Overlapping pair
            [18, 20]   # Non-overlapping pair
        ]
        
        expected = [[1, 7], [8, 15], [18, 20]]
        
        self.assertEqual(merge_intervals(pairs), expected)
        
    def test_get_factors(self):
        expected = {1, 2, 4, 8}
        self.assertEqual(get_factors(8), expected)
        
    def test_to_base_n(self):
        self.assertEqual(to_base_n(10, 2), "1010")
        self.assertEqual(to_base_n(38, 5), "123")
        self.assertEqual(to_base_n(24, 12), "20")
        self.assertEqual(to_base_n(0, 12), "0")
        self.assertEqual(to_base_n(57, 10), "57")
          
if __name__ == "__main__":
    unittest.main(verbosity=2)
