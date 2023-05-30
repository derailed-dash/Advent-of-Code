""" Testing the type_defs module """
import unittest
from common.type_defs import Point

class TestTypes(unittest.TestCase):
    
    def setUp(self):
        self.points = set()
        self.a_point = Point(5, 5)
        self.b_point = Point(1, 2)
        self.c_point = Point(6, 7)
        self.d_point = Point(4, 3)
        self.e_point = Point(3, 6)
        
        self.points.add(self.a_point)
        self.points.add(self.b_point)  
        self.points.add(self.c_point)  
        self.points.add(self.d_point)  
        self.points.add(self.e_point)
        
        self.a_point_neighbours = self.a_point.neighbours() 
        
    def test_point_arithmetic(self):
        self.assertEqual(self.a_point + self.b_point, self.c_point, "Asserting Point addition")
        self.assertEqual(self.a_point - self.b_point, self.d_point, "Asserting Point subtraction")
        self.assertEqual(self.b_point * 3, self.e_point, "Asserting multiplication")
    
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

if __name__ == "__main__":
    unittest.main(verbosity=2)
