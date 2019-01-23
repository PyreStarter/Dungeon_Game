from menu import Menu
from environment import Environment
import pygame

# Every encounter (i.e. combat scenario, puzzle, riddle, trap, etc.) will be of this class.
class Encounter:
    def __init__(self, image):
        #self.menu.menu_width = Environment.ScreenWidth
        self.image = image
        self.options = []

    def add_option(self, option):
        self.options.append(option)

class CombatEncounter(Encounter):
    def __init__(self, image, font, menu_buffer, health):
        Encounter.__init__(self, pygame.transform.scale(image, (Environment.ScreenWidth, Environment.ScreenHeight)))
        self.buffer = menu_buffer
        self.running = False
        self.health = health
        self.font = font
        self.health_image = pygame.Surface((32, 32))
        self.health_image.fill((255, 0, 255))

    def set_health(self, health):
        self.health = health
        self.buffer.blit(self.health_image, (18, 32))
        self.health_image = self.font.render("HP: " + str(self.health), 1, (255, 255, 255), (255, 0, 255, 0))
        self.buffer.blit(self.health_image, (18, 32))
        self.health_image.fill((255, 0, 255))


    def initialize_menu(self):
        if len(self.options) >= 4:
            self.menu = Menu([str(self.options[0].name) + ' - ' + str(self.options[0].text),
                            str(self.options[1].name) + ' - ' + str(self.options[1].text),
                            str(self.options[2].name) + ' - ' + str(self.options[2].text),
                            str(self.options[3].name) + ' - ' + str(self.options[3].text),
                            'Run Away'],
                           self.buffer, width=Environment.ScreenWidth
                           )
        elif len(self.options) == 3:
            self.menu = Menu([str(self.options[0].name) + ' - ' + str(self.options[0].text),
                            str(self.options[1].name) + ' - ' + str(self.options[1].text),
                            str(self.options[2].name) + ' - ' + str(self.options[2].text),
                            'Run Away'],
                           self.buffer, width=Environment.ScreenWidth
                           )
        elif len(self.options) == 2:
            self.menu = Menu([str(self.options[0].name) + ' - ' + str(self.options[0].text),
                            str(self.options[1].name) + ' - ' + str(self.options[1].text),
                            'Run Away'],
                           self.buffer, width=Environment.ScreenWidth
                           )
        elif len(self.options) == 1:
            self.menu = Menu([str(self.options[0].name) + ' - ' + str(self.options[0].text),
                            'Run Away'],
                           self.buffer, width=Environment.ScreenWidth
                           )
        else:
            return 0
        self.menu.x = 0
        self.menu.y = Environment.ScreenHeight - self.menu.height
