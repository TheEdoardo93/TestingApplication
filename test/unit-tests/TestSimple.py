import pytest
import unittest

class TestSimple(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(1, 1)

    def test_not_equal(self):
        self.assertFalse(1 == 2)

if __name__ == '__main__':
    unittest.main()
