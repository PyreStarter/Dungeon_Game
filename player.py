from deck import Deck
import pygame

# Player class
class Player:

    def __init__(self):
        self.strength = 1
        self.dexterity = 1
        self.awareness = 1
        self.stealth = 1
        self.health = 3
        self.width = 32
        self.height = 32
        self.image = pygame.image.load("Image_Assets\\player.png")
        self.surface = pygame.Surface((self.width, self.height))
        self.frame = 0
        self.speed_counter = 0

    def move(self, speed=1):
        self.surface.blit(self.image, (0, 0), (self.frame * 32, 0, 32, 32))
        self.speed_counter += 1
        if self.speed_counter == speed:
            self.frame += 1
            self.speed_counter = 0
        if self.frame == 4:
            self.frame = 0


class CardPlayer:

    def __init__(self):
        self.deck = Deck()
        self.skill = 0
        self.power = 0
        self.wit = 0
        self.points_left = 5
        self.starting_hand_size = 0
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)
