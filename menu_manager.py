from enum import Enum
from environment import Environment, HUDElements
from menu import Menu
from player import CardPlayer
import pygame

class GameMenu(Enum):
    NONE = 0
    STARTUP = 1
    SELECT_ATTRIBUTES = 2
    CONFIRM_ATTRIBUTES = 3
    TAVERN = 4
    DUNGEON = 5
    INVENTORY = 6

    # TODO: Test-only menus. These will need to be deleted or hidden.
    CARD_TEST = 100
    INVENTORY_TEST = 101

class MenuManager:
    def __init__(self, buffer, player):
        self.buffer = buffer
        self.menu_list = {}

        self.menu_list[GameMenu.STARTUP] = StartupMenu(options=['New Game', 'Card Test', 'Inventory Test', 'Quit'], surface=self.buffer)
        self.menu_list[GameMenu.SELECT_ATTRIBUTES] = SelectAttributesMenu(options=['+1 Power', '+1 Skill', '+1 Wit'], surface=self.buffer, player=player)
        self.menu_list[GameMenu.CONFIRM_ATTRIBUTES] = ConfirmAttributesMenu(options=['No', 'Yes'], surface=self.buffer, player=player)
        self.menu_list[GameMenu.TAVERN] = TavernMenu(options=['Enter Dungeon', 'Inventory', 'Save & Quit'], surface=self.buffer)
        self.menu_list[GameMenu.DUNGEON] = DungeonMenu(options=['Inventory', 'Decklist', 'Stop', 'Turn Around', 'Save & Quit'], surface=self.buffer)

        self.menu_list[GameMenu.INVENTORY] = Menu(['test', 'test', 'test'], self.buffer)

        decklistmenu = False
        inventory = False
        running = True
        dungeon = False
        card_test = False
        inventorymenu = False

        #self.menu_list[GameMenu.CARD_TEST] = Menu([], self.buffer)
        self.active_menu = GameMenu.NONE
        self.open(GameMenu.STARTUP)

    def handle_key(self, key):
        if self.active_menu != GameMenu.NONE:
            menu = self.menu_list[self.active_menu]
            if key == pygame.K_ESCAPE:
                menu.close()
            elif key == pygame.K_UP or key == pygame.K_LEFT:
                menu.previous()
            elif key == pygame.K_DOWN or key == pygame.K_RIGHT:
                menu.next()
            elif key == pygame.K_RETURN:
                next_menu = menu.select()
                if next_menu != self.active_menu:
                    menu.close()
                    self.open(next_menu)
        else:
            if key == pygame.K_ESCAPE:
                self.open(GameMenu.DUNGEON)

    def draw(self):
        if self.active_menu != GameMenu.NONE:
            self.menu_list[self.active_menu].draw()

    def open(self, menu):
        self.active_menu = menu
        if menu != GameMenu.NONE:
            self.menu_list[menu].open()

class StartupMenu(Menu):
    def select(self):
        selected = self.options[self.index].text
        next_menu = GameMenu.STARTUP
        if selected == "New Game":
            next_menu = GameMenu.SELECT_ATTRIBUTES
        elif selected == "Card Test":
            next_menu = GameMenu.CARD_TEST
        elif selected == "Inventory Test":
            next_menu = GameMenu.INVENTORY_TEST
        elif selected == "Quit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            raise OptionError
        return next_menu

class SelectAttributesMenu(Menu):
    def __init__(self, options, surface, player):
        self.player = player
        Menu.__init__(self, options, surface)

    def select(self):
        selected = self.options[self.index].text
        next_menu = GameMenu.SELECT_ATTRIBUTES
        if selected == "+1 Power":
            self.player.power += 1
            self.player.points_left -= 1
        elif selected == "+1 Skill":
            self.player.skill += 1
            self.player.points_left -= 1
        elif selected == "+1 Wit":
            self.player.wit += 1
            self.player.points_left -= 1
        else:
            raise OptionError

        if self.player.points_left <= 0:
            next_menu = GameMenu.CONFIRM_ATTRIBUTES
        return next_menu

    def draw(self):
        stat_block = pygame.Surface((HUDElements.StatBlockWidth, HUDElements.StatBlockHeight))
        stat_block.blit(self.font.render("Power: " + str(self.player.power), 1, (255, 255, 255)), (0, 0))
        stat_block.blit(self.font.render("Skill: " + str(self.player.skill), 1, (255, 255, 255)), (0, self.font.get_height()))
        stat_block.blit(self.font.render("Wit: " + str(self.player.wit), 1, (255, 255, 255)), (0, 2 * self.font.get_height()))
        stat_block.blit(self.font.render("Points left: " + str(self.player.points_left), 1, (255, 255, 255)), (0, 3 * self.font.get_height()))
        self.surface.blit(stat_block, pygame.Rect(HUDElements.StatBlockX, HUDElements.StatBlockY, HUDElements.StatBlockWidth, HUDElements.StatBlockHeight))
        Menu.draw(self)

class ConfirmAttributesMenu(Menu):
    def __init__(self, options, surface, player):
        self.player = player
        Menu.__init__(self, options, surface)

    def select(self):
        selected = self.options[self.index].text
        next_menu = GameMenu.CONFIRM_ATTRIBUTES
        if selected == "No":
            next_menu = GameMenu.SELECT_ATTRIBUTES
            self.player.skill = 0
            self.player.power = 0
            self.player.wit = 0
            self.player.points_left = 5
        elif selected == "Yes":
            next_menu = GameMenu.TAVERN
        else:
            raise OptionError
        return next_menu

    def draw(self):
        # TODO(tabitha): de-duplicate code (shared with select attributes menu)
        stat_block = pygame.Surface((HUDElements.StatBlockWidth, HUDElements.StatBlockHeight))
        stat_block.blit(self.font.render("Power: " + str(self.player.power), 1, (255, 255, 255)), (0, 0))
        stat_block.blit(self.font.render("Skill: " + str(self.player.skill), 1, (255, 255, 255)), (0, self.font.get_height()))
        stat_block.blit(self.font.render("Wit: " + str(self.player.wit), 1, (255, 255, 255)), (0, 2 * self.font.get_height()))
        stat_block.blit(self.font.render("Points left: " + str(self.player.points_left), 1, (255, 255, 255)), (0, 3 * self.font.get_height()))
        stat_block.blit(self.font.render("Confirm stat allocation?", 1, (255, 255, 255)), (0, 4 * self.font.get_height()))
        self.surface.blit(stat_block, pygame.Rect(HUDElements.StatBlockX, HUDElements.StatBlockY, HUDElements.StatBlockWidth, HUDElements.StatBlockHeight))
        Menu.draw(self)


class TavernMenu(Menu):
    def select(self):
        selected = self.options[self.index].text
        next_menu = GameMenu.TAVERN
        if selected == "Enter Dungeon":
            next_menu = GameMenu.NONE
        elif selected == "Inventory":
            # TODO: Open an inventory menu
            next_menu = GameMenu.TAVERN
        elif selected == "Save & Quit":
            # TODO: save before quitting
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            raise OptionError
        return next_menu


class DungeonMenu(Menu):
    def select(self):
        selected = self.options[self.index].text
        next_menu = GameMenu.DUNGEON
        if selected == "Inventory":
            next_menu = GameMenu.INVENTORY
        elif selected == "Decklist":
            next_menu = GameMenu.DECKLIST
        elif selected == "Stop":
            # TODO: What should stop do???
            next_menu = GameMenu.DUNGEON
        elif selected == "Turn Around":
            # TODO: Turn around.
            next_menu = GameMenu.DUNGEON
        elif selected == "Save & Quit":
            # TODO: save before quitting
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        else:
            raise OptionError
        return next_menu
