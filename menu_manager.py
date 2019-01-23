from enum import Enum
from menu import Menu
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

        self.menu_list[GameMenu.STARTUP] = StartupMenu(['New Game', 'Card Test', 'Inventory Test', 'Quit'], self.buffer)
        self.menu_list[GameMenu.SELECT_ATTRIBUTES] = SelectAttributesMenu(options=['+1 Power', '+1 Skill', '+1 Wit'], surface=self.buffer, player=player)
        self.menu_list[GameMenu.CONFIRM_ATTRIBUTES] = ConfirmAttributesMenu(['No', 'Yes'], self.buffer)
        self.menu_list[GameMenu.TAVERN] = TavernMenu(['Enter Dungeon', 'Inventory', 'Save & Quit'], self.buffer)
        self.menu_list[GameMenu.DUNGEON] = DungeonMenu(['Inventory', 'Decklist', 'Stop', 'Turn Around', 'Save & Quit'], self.buffer)

        self.menu_list[GameMenu.INVENTORY] = Menu(['test', 'test', 'test'], self.buffer)

        decklistmenu = False
        inventory = False
        running = True
        dungeon = False
        card_test = False
        inventorymenu = False

        #self.menu_list[GameMenu.CARD_TEST] = Menu([], self.buffer)

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
                menu.close()
                self.open(menu.select())
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
        Menu.__init__(self, options, surface)
        self.player = player

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

class ConfirmAttributesMenu(Menu):
    def select(self):
        selected = self.options[self.index].text
        next_menu = GameMenu.CONFIRM_ATTRIBUTES
        if selected == "No":
            next_menu = GameMenu.SELECT_ATTRIBUTES
        elif selected == "Yes":
            next_menu = GameMenu.TAVERN
        else:
            raise OptionError
        return next_menu


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
