from Items import ItemCreator


class ItemManager:
    def __init__(self):
        print(f'Item Manager loaded.')
        self.itemCreator = ItemCreator()
