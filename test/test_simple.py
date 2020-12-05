import pytest

class TestSimple(object):
    def test_equal_test(self):
        assert ( 1 == 1)

    def test_not_equal_test(self):
        assert ( 1 != 2)