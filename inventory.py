from item import Weapon
import pygame

# Inventory class. For keeping track of who has what.
class Inventory:

    def __init__(self):
        self.items = []
        self.main_hand = Weapon(pygame.image.load("Image_Assets\\meter_1.png"), 0, 0, 0)
        self.off_hand = Weapon(pygame.image.load("Image_Assets\\meter_1.png"), 0, 0, 0)

    def add_item(self, item, quantity=1):
        for i in self.items:
            if i[0] == item.name:
                i[1] += quantity
                return
        self.items.append([item.name, quantity])

    def use_item(self, hud, item, quantity=1):
        for i in self.items:
            if i[0] == item.name:
                if i[1] >= quantity:
                    i[1] -= quantity
                    item.use(hud, quantity)
                else:
                    print('Error: Not enough items to use')
                return

    def set_main_hand(self, item):
        self.main_hand = item
        return

    def set_off_hand(self, item):
        self.off_hand = item
