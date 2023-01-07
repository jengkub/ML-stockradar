import unittest
from unittest.mock import patch
import datetime

def my_function():
    # This function subtracts the current year from 2022
    return 2022 - datetime.datetime.now().year

class TestMyFunction(unittest.TestCase):
    @patch('datetime.datetime')
    def test_my_function(self, mock_datetime):
        # Set the return value of datetime.now()
        mock_now = mock_datetime.now.return_value
        mock_now.year = 2020
        
        # Call the function under test
        result = my_function()
        
        # Assert that the function returned the expected value
        self.assertEqual(result, 2)
        
        # Verify that datetime.now() was called
        mock_datetime.now.assert_called_once()


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)