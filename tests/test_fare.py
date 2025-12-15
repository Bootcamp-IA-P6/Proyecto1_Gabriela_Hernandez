import unittest
import main

class TestCalculateFare(unittest.TestCase):

    def test_calculate_fare_basic(self):        
        main.STOPPED_RATE = 0.02
        main.MOVING_RATE = 0.05

        stopped = 10   
        moving = 20  
        
        total = main.calculate_fare(stopped, moving)
        
        self.assertAlmostEqual(total, 10 * 0.02 + 20 * 0.05, places=2)

if __name__ == "__main__":
    unittest.main()
