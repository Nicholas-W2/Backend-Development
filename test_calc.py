# Unit Tests for Calculator App

# Run with the following command:
# python3 -m unittest test_calculator.py
# or just press the Run button on the top right!

import unittest
import calc

# Unit tests
class TestCalculator(unittest.TestCase):
    def test_add(self):
        result = calc.add(10, 5)
        self.assertEqual(result, 15)
    
    # Similarly, test the other functions of the Calculator App.
    # Test for the subtract function
    def test_subtract(self):
        result = calc.subtract(10, 5)
        self.assertEqual(result, 5)

    # Test for the multiply function
    def test_multiply(self):
        result = calc.multiply(10, 5)
        self.assertEqual(result, 50)

    # Test for the divide function
    def test_divide(self):
        # Check normal division
        result = calc.divide(10, 5)
        self.assertEqual(result, 2)
        
        # Check division by zero
        with self.assertRaises(ZeroDivisionError):
            calc.divide(10, 0)

if __name__ == '__main__':
    unittest.main()

# Run the tests
if __name__ == "__main__":
    unittest.main()