import pygame
from enum import IntEnum

class MenuOptionState(IntEnum):
    SELECTED = 0
    UNSELECTED = 1
    DISABLED = 2

class MenuOption:
    def __init__(self, text):
        self.text = text
        self.state = MenuOptionState.UNSELECTED
        self.surface = pygame.Surface

class Menu:
    def __init__(self, options, surface, width=0, height=0):
        self.options = []
        for item in options:
            self.options.append(MenuOption(item))
        self.surface = surface
        self.font = pygame.font.Font('Fonts/coders_crux.ttf', 32)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.index = 0
        self.menu_widget = pygame.Surface
        self.active = False
        self.fill_menu_widget()

    def open(self):
        self.active = True
        self.index = 0
        self.surface.fill((255, 0, 255))
        self.update_menu_options()

    def close(self):
        self.active = False
        self.surface.fill((255, 0, 255))

    def fill_menu_widget(self):
        self.update_menu_options()

        for option in self.options:
            self.height = self.height + option.surface.get_height()
            self.width = max(self.width, option.surface.get_width())

        self.x = (self.surface.get_width() - self.width) / 2
        self.y = (self.surface.get_height() - self.height) / 2

        menu_widget = pygame.Surface((self.width, self.height))
        menu_item_height = self.height / len(self.options)
        for i in range(len(self.options)):
            menu_widget.blit(self.options[i].surface, pygame.Rect(0, menu_item_height * i, self.width, menu_item_height))
        self.menu_widget = menu_widget

    def draw(self):
        self.surface.blit(self.menu_widget, pygame.Rect(self.x, self.y, self.width, self.height))

    def get_index(self):
        return self.index

    def next(self):
        self.index = self.index + 1 if self.index < len(self.options) - 1 else 0
        self.update_menu_options()

    def previous(self):
        self.index = self.index - 1 if self.index > 0 else len(self.options) - 1
        self.update_menu_options()

    def update_menu_options(self):
        menu_widget = pygame.Surface((self.width, self.height))
        menu_item_height = self.height / len(self.options)
        for i in range(len(self.options)):
            if i == self.index:
                self.options[i].surface = self.font.render(self.options[i].text, 1, pygame.Color(0, 255, 0))
            else:
                self.options[i].surface = self.font.render(self.options[i].text, 1, pygame.Color(255, 255, 0))
            menu_widget.blit(self.options[i].surface, pygame.Rect(0, menu_item_height * i, self.width, menu_item_height))

        self.menu_widget = menu_widget
        self.draw()
