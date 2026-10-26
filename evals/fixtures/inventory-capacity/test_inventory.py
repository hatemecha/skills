import unittest
from inventory import Inventory


class InventoryTests(unittest.TestCase):
    def test_capacity_and_remaining_slots(self):
        inventory = Inventory(capacity=2)
        self.assertEqual(inventory.remaining, 2)
        self.assertTrue(inventory.add("A"))
        self.assertEqual(inventory.remaining, 1)
        self.assertTrue(inventory.add("B"))
        self.assertEqual(inventory.remaining, 0)
        self.assertFalse(inventory.add("C"))
        self.assertEqual(inventory.items, ["A", "B"])


if __name__ == "__main__":
    unittest.main()
