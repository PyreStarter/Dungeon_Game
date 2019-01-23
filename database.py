# This class is a database for organizing items. This will be removed upon implementation of a better solution
class Database:

    def __init__(self):
        self.item = []

    def add_item(self, item):
        self.item.append(item)

    def get_item(self, name):
        for i in self.item:
            if i.name == name:
                return i
        print('error: could not find item')
        return 0
