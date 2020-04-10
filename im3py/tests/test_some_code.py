"""Tests for the fake code functionality.

:author:   <developer names>
:email:    <developer emails>

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

import unittest

import im3py.some_code as fake


class TestSomeCode(unittest.TestCase):
    """Tests for functions in `some_code.py`."""

    LIST_OF_GOOD_VALS = [1, 2.0, 3]
    LIST_OF_BAD_VALS = ['1', '2.0', '3']

    def test_get_sum(self):
        """Test that ensure the correct value and error messages from `get_sum()`"""

        # valid result if data good
        self.assertEqual(fake.get_sum(TestSomeCode.LIST_OF_GOOD_VALS), sum(TestSomeCode.LIST_OF_GOOD_VALS))

        # expect type error
        with self.assertRaises(TypeError):
            fake.get_sum(TestSomeCode.LIST_OF_BAD_VALS)

    def test_get_mean(self):
        """Test that ensure the correct value and error messages from `get_mean()`"""

        # valid result if data good
        true_mean = sum(TestSomeCode.LIST_OF_GOOD_VALS) / len(TestSomeCode.LIST_OF_GOOD_VALS)
        self.assertEqual(fake.get_mean(TestSomeCode.LIST_OF_GOOD_VALS), true_mean)

        # expect type error
        with self.assertRaises(TypeError):
            fake.get_mean(TestSomeCode.LIST_OF_BAD_VALS)


if __name__ == '__main__':
    unittest.main()
