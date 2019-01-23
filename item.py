import pygame

# This is the item class. Each item should have it's own class that will inherit this base class.
class Item:
    def __init__(self, image, rarity, value, name):
        self.image = image
        self.rarity = rarity
        self.value = value
        self.Hud_Display = False
        self.name = name

    def use(self, quantity=1):
        print('Item is not being used properly')

# This is the weapon class. It is a subclass of Item. All weapons will be of this class.
class Weapon(Item):
    def __init__(self, image, rarity, value, name, damage=0, accuracy=0):
        Item.__init__(self, image, rarity, value, name)
        self.options = []
        self.damage = damage
        self.accuracy = accuracy

    def add_option(self, option):
        self.options.append(option)


# Torch class
class Torch(Item):
    def __init__(self):
        Item.__init__(self, image=pygame.image.load("Image_Assets\\torch.png"), rarity=1, value=5, name='torch')
        self.Hud_Display = True

    def use(self, hud, quantity=1):
        hud.torch_count = 0
        hud.torch_diminish = 0
        return
