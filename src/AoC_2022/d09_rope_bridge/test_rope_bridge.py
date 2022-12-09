""" Test our Rope_Bridge Solution """
from pathlib import Path
import unittest
import rope_bridge

SAMPLE_INPUT_FILE = Path(Path(__file__).parent, "input/sample_input.txt")

class TestRopeBridge(unittest.TestCase):
    """ Set up data using the sample input.
    Then run two tests, asserting the correct length of the returned lists. """
    
    def setUp(self):
        # load the data
        with open(SAMPLE_INPUT_FILE, mode="rt") as f:        
            self.data = [(d, int(v)) for d, v in [instruction.split() for instruction in f.read().splitlines()]]
        
    def test_part_1(self):
        expected = 88
        self.assertEqual(len(rope_bridge.pull_rope(self.data, 2)), expected)
        
    def test_part_2(self):
        expected = 36
        self.assertEqual(len(rope_bridge.pull_rope(self.data, 10)), expected)

if __name__ == "__main__":
    unittest.main()
