import unittest
from logic import cart_total


class CartTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(cart_total([15, 40, 5]), 60)


if __name__ == "__main__":
    unittest.main()
