""" 
Testing the aoc_commons module 
Make sure your session cookie value is current
"""
import logging
import unittest
from shutil import rmtree
from os import path

# py -m pip uninstall dazbo-aoc-commons
import aoc_common.aoc_commons as ac  # for local testing

# py -m pip install dazbo-aoc-commons
# import aoc_commons as ac           # for testing using installed pip package

# Set logging level of aoc_commons
logger = logging.getLogger("aoc_common.aoc_commons")
logger.setLevel(logging.INFO)

class TestTypes(unittest.TestCase):
    """ Unit tests of various classes in type_defs """
    
    def setUp(self):
        """ Read locations, clear the input folder, and set up some test data """
        self.locations = ac.get_locations(__file__)
        self.clear_input_folder()
        
        self.points = set()
        self.a_point = ac.Point(5, 5)
        self.b_point = ac.Point(1, 2)
        self.c_point = ac.Point(6, 7)
        self.d_point = ac.Point(4, 3)
        self.e_point = ac.Point(3, 6)
        self.y_invert_point = ac.Point(0, -1)
        
        self.points.add(self.a_point)
        self.points.add(self.b_point)  
        self.points.add(self.c_point)  
        self.points.add(self.d_point)  
        self.points.add(self.e_point)
        
        self.a_point_neighbours = self.a_point.neighbours()

    def tearDown(self) -> None:
        self.clear_input_folder()  
        return super().tearDown()
    
    def clear_input_folder(self):
        if self.locations.input_dir.exists():
            print(f"Deleting {self.locations.input_dir}")
            rmtree(self.locations.input_dir)
    
    def test_locations(self): 
        """ Test that the locations and script name are set properly """
        # use normcase to un-escape and ignore case differences in the paths
        script_directory = path.normcase(path.dirname(path.realpath(__file__)))
        self.assertEqual(path.normcase(self.locations.script_dir), script_directory)
        
        this_script = path.splitext(path.basename(__file__))[0]
        self.assertEqual(self.locations.script_name, this_script)        

    def test_write_puzzle_input_file(self):
        """ Test that we can retrieve AoC input data.
        This depends on having a valid session cookie. 
        The ac attempts to read the session cookie from a .env file. """
        
        # Try to retrieve input that does not exist
        with self.assertRaises(ValueError):
            ac.write_puzzle_input_file(2010, 1, self.locations)
        
        # Retrieve legitimate input
        self.assertIn("(((())))", ac.write_puzzle_input_file(2015, 1, self.locations))
        
        # Does not retrieve file if it already exists - returns existing input file path instead
        self.assertEqual(path.basename(self.locations.input_file), 
                         ac.write_puzzle_input_file(2015, 1, self.locations))

    def test_vectors(self):
        """ Test our Vector Enums """
        self.assertEqual(ac.Vectors.N.value, (0, 1))
        self.assertEqual(ac.Vectors.NW.value, (-1, 1))
        self.assertEqual(ac.Vectors.S.value, (0, -1))
        self.assertEqual(ac.Vectors.E.value, (1, 0))
        self.assertEqual(ac.Vectors.N.y_inverted, (0, -1))
        self.assertEqual(ac.Vectors.SW.value, (-1, -1))
        
    def test_vector_dicts(self):
        """ Test our vector dicts using arrow keys """
        self.assertEqual(ac.VectorDicts.ARROWS[">"], (1, 0))
        self.assertEqual(ac.VectorDicts.ARROWS["v"], (0, -1))
        self.assertEqual(ac.VectorDicts.DIRS["L"], (-1, 0))
        self.assertEqual(ac.VectorDicts.DIRS["U"], (0, 1))
        self.assertEqual(ac.VectorDicts.NINE_BOX["tr"], (1, 1))
        self.assertEqual(ac.VectorDicts.NINE_BOX["bl"], (-1, -1))
        
    def test_point_arithmetic(self):
        """ Test we can add, subtract and multiply points """
        self.assertEqual(self.a_point + self.b_point, self.c_point, "Asserting Point addition")
        self.assertEqual(self.a_point - self.b_point, self.d_point, "Asserting Point subtraction")
        self.assertEqual(self.b_point * ac.Point(3, 3), self.e_point, "Asserting multiplication")
    
    def test_manhattan_distance(self):
        """ Test Manhattan distance between points, i.e. the sum of the two vectors """
        self.assertEqual(ac.Point.manhattan_distance(self.e_point), 3+6)
        self.assertEqual(self.c_point.manhattan_distance_from(self.b_point), abs(self.a_point.x)+abs(self.a_point.y))
        
    def test_point_containers(self):
        """ Test a points neighbours and orthogonal neighbours """
        
        all_neighbours_count = 8 # point has 8 neighbours
        orthog_neighbours_count = 4 # point has 4 orthogonal neighbours

        self.assertEqual(len(self.a_point_neighbours), all_neighbours_count, 
                         f"Expect {all_neighbours_count} from all neighbours")
        
        a_point_orthog_neighbours = self.a_point.neighbours(include_diagonals=False)
        self.assertEqual(len(a_point_orthog_neighbours), orthog_neighbours_count, 
                         f"Expect {orthog_neighbours_count} orthogonal neighbours")
        self.assertNotIn(self.a_point, self.a_point.neighbours(), 
                         "Check neighbours does not include self")
        self.assertIn(self.a_point, self.a_point.neighbours(include_self=True), 
                         "Check neighbours includes self")
        self.assertEqual(len(self.a_point.neighbours(include_self=True)), all_neighbours_count+1, 
                         f"All neighbours with self should be {all_neighbours_count+1}")
        
    def test_point_neighbour_generator(self):
        """ Test we can use a generator to return neighbours """
        gen = self.a_point.yield_neighbours()
        
        for _ in range(len(self.a_point_neighbours)):
            self.assertIn(next(gen), self.a_point_neighbours, "Generated item is a valid neighbour")
            
        with self.assertRaises(StopIteration): # no more items to generate
            next(gen)
            
    def test_grid(self):
        """ Test our Grid class.
        Test height and width, valid locations within the grid, values at a location.
        Test we can retrieve a row and a column, as str.
        """
        input_grid = ["5483143223",
                      "2745854711",
                      "5264556173",
                      "6141336146",
                      "6357385478",
                      "4167524645",
                      "2176841721"]
    
        input_array_data = [[int(posn) for posn in row] for row in input_grid]      
        grid = ac.Grid(input_array_data)
        self.assertEqual(grid.height, len(input_grid))
        self.assertEqual(grid.width, len(input_grid[0]))
        self.assertTrue(grid.valid_location(ac.Point(1, 1)))
        self.assertFalse(grid.valid_location(ac.Point(11,8)))
        self.assertEqual(grid.value_at_point(ac.Point(1, 1)), 7)
        self.assertEqual(grid.rows_as_str()[0], "5483143223")
        self.assertEqual(grid.cols_as_str()[0], "5256642")
      
    def test_binary_search(self):
        """ Test a binary search, 
        i.e. where we start with a midpoint, evaluate the result of a function,
        and see if it gives us the result we want. """
        self.assertEqual(ac.binary_search(225, 0, 20, lambda x: x**2, reverse_search=True), None)
        self.assertEqual(ac.binary_search(225, 0, 20, lambda x: x**2), 15)
    
    def test_merge_intervals(self):
        """ Test our ability to take a set of intervals and merge them. """
        pairs = [
            [1, 5],    # Non-overlapping pair
            [3, 7],    # Overlapping pair
            [8, 12],   # Non-overlapping pair
            [10, 15],  # Overlapping pair
            [18, 20]   # Non-overlapping pair
        ]
        
        expected = [[1, 7], [8, 15], [18, 20]]
        
        self.assertEqual(ac.merge_intervals(pairs), expected)
        
    def test_get_factors(self):
        """ Test that we can retrieve all factors of a number """
        expected = {1, 2, 4, 8} # factors of 8
        self.assertEqual(ac.get_factors(8), expected)
        
    def test_to_base_n(self):
        """ Test our abiltiy to obtain the str representation of a number converted to any base """
        self.assertEqual(ac.to_base_n(10, 2), "1010")
        self.assertEqual(ac.to_base_n(38, 5), "123")
        self.assertEqual(ac.to_base_n(24, 12), "20")
        self.assertEqual(ac.to_base_n(0, 12), "0")
        self.assertEqual(ac.to_base_n(57, 10), "57")
          
if __name__ == "__main__":
    unittest.main(verbosity=2) # if we want to include function names and docstring headers
    # unittest.main()
