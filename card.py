import pygame
from environment import Environment
from item import Item

class CardObject:
    def __init__(self, card, width, height):
        self.card = card
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.x_position = 0
        self.x_position = 0
        self.surface.blit(pygame.transform.scale(card.surface, (self.width, self.height)), (0, 0))


class CardItem(Item):
    def __init__(self, image, rarity, value, name, cardlist):
        Item.__init__(self, image, rarity, value, name)
        self.card_list = cardlist
        self.card_list_length = len(cardlist)


# Card class. For the list of existing cards
class Card:
    def __init__(self, name, type, text, image, font):
        self.image = image
        self.name = name
        self.text = text
        self.type = type
        self.width = int(Environment.ScreenWidth/4)
        self.height = int(self.width*1.4)
        self.surface = pygame.Surface((self.width, self.height))
        self.textbox_color = (239, 228, 176)
        self.name_buffer = self.name
        self.font = font
        #Adjusts the color of the card based on card type
        if type == 'Action':
            self.color = (255, 100, 100)
            self.surface.fill(self.color)
            pygame.draw.rect(self.surface, (100, 100, 100), (0, 0, self.width, self.height), 10)
        elif type == 'Reaction':
            self.color = (127, 255, 127)
            self.surface.fill(self.color)
            pygame.draw.rect(self.surface, (100, 100, 100), (0, 0, self.width, self.height), 10)
        elif type == 'Passive':
            self.color = (63, 127, 255)
            self.surface.fill(self.color)
            pygame.draw.rect(self.surface, (100, 100, 100), (0, 0, self.width, self.height), 10)
        else:
            self.color = (185, 122, 87)
            self.surface.fill(self.color)
            pygame.draw.rect(self.surface, (100, 100, 100), (0, 0, self.width, self.height), 10)
        self.text_lines = text.split("_")
        self.line_length = 0
        #If a single line is too short, this appends spaces to the end to keep the scaling function from stretching it
        for j in range(len(self.text_lines)):
            if len(self.text_lines[j]) < 12:
                self.diff = 12 - len(self.text_lines[j])
                for i in range(self.diff):
                    self.text_lines[j] += " "

        if len(self.name_buffer) < 12:
            self.diff = 12 - len(self.name)
            for i in range(self.diff):
                self.name_buffer += " "
        #This finds the longest line and attributes it to the width of the text box
        for i in self.text_lines:
            j = self.font.render(i, 1, (255, 255, 255), (255, 0, 255, 0))
            if j.get_width() > self.line_length:
                self.line_length = j.get_width()
        #If the text box is shorter than 3 lines, this sets the height to 3 lines to keep it from being stretched
        if len(self.text_lines) >= 3:
            self.line_height = len(self.text_lines)*self.font.get_height()
        else:
            self.line_height = 3*self.font.get_height()
        self.namebox_text = self.font.render(self.name_buffer, 1, (0, 0, 0), self.textbox_color)
        self.textbox_surface_0 = pygame.Surface((self.line_length, self.line_height))
        self.textbox_surface_0.fill(self.textbox_color)
        self.text_buffer = pygame.Surface((self.line_length, self.line_height))
        self.text_buffer.fill(self.textbox_color)
        for i in range(len(self.text_lines)):
            self.text_buffer = self.font.render(self.text_lines[i], 1, (0, 0, 0), (self.textbox_color))
            self.textbox_surface_0.blit(self.text_buffer, (1, i*self.font.get_height() +1))
        self.textbox_surface = pygame.transform.scale(self.textbox_surface_0, (int(self.width*.8), int(self.height*.3)))
        self.namebox_surface = pygame.Surface((int(self.width * .8), int(self.height * .1)))
        self.namebox_surface.fill(self.textbox_color)
        self.namebox_surface_0 = pygame.Surface((int(self.namebox_text.get_width()), int(self.namebox_surface.get_height())))
        self.namebox_surface_0.fill(self.textbox_color)
        self.namebox_surface_0.blit(self.namebox_text, (1, 1))
        self.namebox_surface_0 = pygame.transform.scale(self.namebox_surface_0, (self.namebox_surface.get_width(),
                                                                                 self.namebox_surface.get_height()))
        self.namebox_surface.blit(self.namebox_surface_0, (0, 0))
        self.image_surface = pygame.transform.scale(self.image, (int(self.width * .8), int(self.height * .4) - 10))
        self.surface.blit(self.image_surface, (int(self.width * .1), int(self.height * .2) + 5))
        self.surface.blit(self.textbox_surface, (int(self.width * .1), int(self.height * .6)))
        self.surface.blit(self.namebox_surface, (int(self.width * .1), int(self.height * .1)))
