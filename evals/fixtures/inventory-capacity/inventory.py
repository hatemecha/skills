class Inventory:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items = []

    def add(self, item: str):
        self.items.append(item)
