""" Testing the type_defs module """
import unittest
from common.type_defs import (
    Point, 
    Grid, 
    Vectors, 
    VectorDicts, 
    binary_search, 
    merge_intervals
)

class TestTypes(unittest.TestCase):
    """ Unit tests of various classes in type_defs """
    
    def setUp(self):
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
          
if __name__ == "__main__":
    unittest.main(verbosity=2)
