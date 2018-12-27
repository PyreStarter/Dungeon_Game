from Encounters import *
from Environment import *
import pygame
import random
import menu

pygame.font.init()
font = pygame.font.Font('Fonts\\coders_crux.ttf', 64)

# Every encounter (i.e. combat scenario, puzzle, riddle, trap, etc.) will be of this class.
class Encounter:
    def __init__(self, image):
        self.menu = menu.Menu()
        self.image = image
        self.options = []

    def add_option(self, option):
        self.options.append(option)


class Combat_Encounter(Encounter):
    def __init__(self, image, menu_buffer, health):
        Encounter.__init__(self, image)
        self.buffer = menu_buffer
        self.running = False
        self.health = health
        self.health_image = pygame.Surface((32, 32))
        self.health_image.fill((255, 0, 255))

    def set_health(self, health):
        self.health = health
        self.buffer.blit(self.health_image, (18, 32))
        self.health_image = font.render("HP: " + str(self.health), 1, (255, 255, 255), (255, 0, 255))
        self.buffer.blit(self.health_image, (18, 32))
        self.health_image.fill((255, 0, 255))

    def initialize_menu(self):
        if len(self.options) >= 4:
            self.menu.init([str(self.options[0].name) + ' - ' + str(self.options[0].text),
                            str(self.options[1].name) + ' - ' + str(self.options[1].text),
                            str(self.options[2].name) + ' - ' + str(self.options[2].text),
                            str(self.options[3].name) + ' - ' + str(self.options[3].text),
                            'Run Away'],
                           self.buffer
                           )
        elif len(self.options) == 3:
            self.menu.init([str(self.options[0].name) + ' - ' + str(self.options[0].text),
                            str(self.options[1].name) + ' - ' + str(self.options[1].text),
                            str(self.options[2].name) + ' - ' + str(self.options[2].text),
                            'Run Away'],
                           self.buffer
                           )
        elif len(self.options) == 2:
            self.menu.init([str(self.options[0].name) + ' - ' + str(self.options[0].text),
                            str(self.options[1].name) + ' - ' + str(self.options[1].text),
                            'Run Away'],
                           self.buffer
                           )
        elif len(self.options) == 1:
            self.menu.init([str(self.options[0].name) + ' - ' + str(self.options[0].text),
                            'Run Away'],
                           self.buffer
                           )
        else:
            return 0
        self.menu.x = 0
        self.menu.y = Environment.ScreenHeight - self.menu.height
        self.menu.menu_width = Environment.ScreenWidth


# This class is for defining the unique options that will be provided by certain scenarios, items, and skills.
class Option:
    def __init__(self, name, text, damage=0, chance=0):
        self.name = name
        self.text = text
        self.chosen = False
        self.damage = damage
        self.chance = chance

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
    def __init__(self, image, rarity, value, name):
        Item.__init__(self, image, rarity, value, name)
        self.options = []
        self.damage = 0
        self.accuracy = 0

    def add_option(self, option):
        self.options.append(option)

# Torch class
class Torch(Item):
    def __init__(self):
        Item.__init__(self, pygame.image.load("Image_Assets\\torch.png"), 1, 5, 'torch')
        self.Hud_Display = True

    def use(self, hud, quantity=1):
        hud.torch_count = 0
        hud.torch_diminish = 0
        return


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


# Background class. This will be used for the scrolling backdrops in the dungeon.
class Background:

    def __init__(self):
        self.image = pygame.image.load("Image_Assets\\dungeon_background.png")
        self.surface = pygame.Surface((640, 480))
        self.speed_counter = 0

    def move(self, speed=1):
        self.surface.fill((255, 0, 255))
        self.surface.blit(self.image, (0, 0), ((0 + speed*self.speed_counter), 0, (640 - speed*self.speed_counter), 480))
        if self.speed_counter:
            self.surface.blit(self.image, ((640 - speed*self.speed_counter), 0), (0, 0, speed*self.speed_counter, 480))
        self.speed_counter += 1
        if self.speed_counter >= int(640/speed):
            self.speed_counter = 0


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


# Hud class, handles everything related to the HUD
class Hud:

    def __init__(self, inventory, database, width, height):
        self.inventory = inventory
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill((255, 0, 255))
        self.surface.set_colorkey((255, 0, 255))
        self.database = database
        self.set_item_tracker()
        self.torch_meter_image = pygame.image.load("Image_Assets\\meter_1.png")
        self.torch_diminish = 0
        self.torch_count = 0

    def set_item_tracker(self):
        count = 1
        for i in self.inventory.items:
            j = self.database.get_item(i[0])
            if j.Hud_Display:
                clear_space = pygame.Surface((96, 32))
                clear_space.fill((255, 0, 255))
                combined_image = pygame.Surface((76, 32))
                quantity_image = font.render(str(i[1]), 1, (255, 255, 255), (255, 0, 255))
                combined_image.blit(j.image, (0, 0))
                combined_image.blit(quantity_image, (32, 0))
                if i[1] <= 9:
                    combined_image.blit(clear_space, (56, 0))
                self.surface.blit(clear_space, ((self.width - (96*count)), 0))
                self.surface.blit(combined_image, ((self.width - (96*count)), 0))
                count += 1

    def set_torch_meter(self):
        torch = self.database.get_item('torch')
        clear_space = pygame.Surface((128, 32))
        clear_space.fill((255, 0, 255))
        meter_surface = pygame.Surface((128, 32))
        meter_surface.fill((255, 0, 255))
        meter_surface.set_colorkey((255, 0, 255))
        if self.torch_diminish < 128:
            meter_surface.blit(self.torch_meter_image, (0, 0), (0, 0, (128 - self.torch_diminish), 32))
        self.surface.blit(torch.image, (int(Environment.ScreenWidth/64), int(Environment.ScreenHeight/4)))
        self.surface.blit(clear_space, (int(Environment.ScreenWidth/64)+32, int(Environment.ScreenHeight/4)))
        self.surface.blit(meter_surface, (int(Environment.ScreenWidth/64)+32, int(Environment.ScreenHeight/4)))

    def update_torch_meter(self, speed=1):
        if self.torch_count >= speed:
            self.torch_diminish += 1
            self.torch_count = 0
        self.torch_count += 1

    def update(self, inventory):
        self.inventory = inventory
        self.set_item_tracker()
        self.set_torch_meter()


# This is a function that will take in a probability of success and return successful(True) or unsuccessful(False)
#  - The equation will probably be altered for game feel in the future
def chance_outcome(chance):
    number = random.randint(1, 100)
    if number <= chance:
        return True
    if number > chance:
        return False


# MAIN FUNCTION LES GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
def main():

    pygame.init()
    pygame.mixer.init()

    logo = pygame.image.load("Image_Assets\\logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("game")

    screen = pygame.display.set_mode((Environment.ScreenWidth, Environment.ScreenHeight))
    screen_buffer_1 = pygame.Surface((Environment.ScreenWidth, Environment.ScreenHeight))
    screen_buffer_2 = pygame.Surface((Environment.ScreenWidth, Environment.ScreenHeight))
    menu_buffer = pygame.Surface((Environment.ScreenWidth, Environment.ScreenHeight))
    screen_buffer_1.fill((0, 0, 0))
    screen_buffer_2.fill((255, 0, 255))
    menu_buffer.fill((255, 0, 255))
    screen_buffer_1.set_colorkey((255, 0, 255))
    screen_buffer_2.set_colorkey((255, 0, 255))
    menu_buffer.set_colorkey((255, 0, 255))

    dungeon_background = Background()
    player = Player()
    item_database = Database()

    player_inventory = Inventory()
    player_hud = Hud(player_inventory, item_database, Environment.ScreenWidth, Environment.ScreenHeight)

    torch = Torch()
    item_database.add_item(torch)

    player_inventory.add_item(torch)



# This is creating a weapon, changing its attributes, giving it a combat option, and equiping it to the character.

    steel_short_sword = Weapon(logo, 10, 2, "Steel Short Sword")
    steel_short_sword.damage = 3
    steel_short_sword.accuracy = 65
    sword_attack_option = Option("Sword Attack",
                                 str(str(steel_short_sword.accuracy + player.dexterity*5) +"% chance to deal " + str(steel_short_sword.damage + player.strength) + " damage (attack)"),
                                 steel_short_sword.damage + player.strength,
                                 steel_short_sword.accuracy + player.dexterity*5
                                 )
    steel_short_sword.add_option(sword_attack_option)

    player_inventory.set_main_hand(steel_short_sword)

# This is creating a shield for the player to use

    round_wooden_shield = Weapon(logo, 4, 1, "Round Wooden Shield")
    round_wooden_shield.damage = 0
    round_wooden_shield.accuracy = 20
    shield_bash_option = Option("Shield Bash",
                                str(str(round_wooden_shield.accuracy + player.dexterity*5) +"% chance to deal " + str(round_wooden_shield.damage + player.strength) + " damage (guard)"),
                                round_wooden_shield.damage + player.strength,
                                round_wooden_shield.accuracy + player.dexterity*5
                                )
    round_wooden_shield.add_option(shield_bash_option)

    player_inventory.set_off_hand(round_wooden_shield)

# This is creating the Top Birb encounter

    top_birb = Combat_Encounter(pygame.image.load("Image_Assets\\Tokoyami.png"), menu_buffer, 10)
    if len(player_inventory.main_hand.options):
        top_birb.add_option(player_inventory.main_hand.options[0])
    if len(player_inventory.off_hand.options):
        top_birb.add_option(player_inventory.off_hand.options[0])
    top_birb.initialize_menu()

# creating the menus

    opening_menu = menu.Menu()
    opening_menu.init(['New Game', 'Options', 'Quit'], menu_buffer)
    opening = True

    opening_menu.draw()

    tavern_menu = menu.Menu()
    tavern_menu.init(['Enter Dungeon', 'Inventory', 'Quit'], menu_buffer)
    tavern = False

    dungeon_menu = menu.Menu()
    dungeon_menu.init(['Inventory', 'Character', 'Stop', 'Turn Around', 'Save & Quit'], menu_buffer)
    dungeonmenu = False

    running = True
    dungeon = False


# \\\\\\\\This is the beginning of the while loop that is the entire game. This is where the magic happens./////////

    while running:

        if opening:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    opening = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        opening = False
                    if event.key == pygame.K_UP:
                        opening_menu.draw()
                    if event.key == pygame.K_DOWN:
                        opening_menu.draw()
                    if event.key == pygame.K_RETURN:
                        if opening_menu.get_index() == 2:
                            running = False
                            opening = False
                        if opening_menu.get_index() == 0:
                            tavern = True
                            opening = False
                            menu_buffer.fill((255, 0, 255))
                            tavern_menu.draw()

        if tavern:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    tavern = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        tavern = False
                        opening = True
                        menu_buffer.fill((255, 0, 255))
                        opening_menu.draw()
                    if event.key == pygame.K_UP:
                        tavern_menu.draw()
                    if event.key == pygame.K_DOWN:
                        tavern_menu.draw()
                    if event.key == pygame.K_RETURN:
                        if tavern_menu.get_index() == 2:
                            tavern = False
                            opening = True
                            menu_buffer.fill((255, 0, 255))
                            opening_menu.draw()
                        if tavern_menu.get_index() == 0:
                            tavern = False
                            dungeon = True
                            menu_buffer.fill((255, 0, 255))

        if dungeonmenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    dungeon = False
                    dungeonmenu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        player_inventory.add_item(torch)
                    if event.key == pygame.K_y:
                        player_inventory.use_item(player_hud, torch)
                    if event.key == pygame.K_ESCAPE:
                        dungeonmenu = False
                        menu_buffer.fill((255, 0, 255))
                    if event.key == pygame.K_UP:
                        dungeon_menu.draw()
                    if event.key == pygame.K_DOWN:
                        dungeon_menu.draw()
                    if event.key == pygame.K_RETURN:
                        if dungeon_menu.get_index() == 4:
                            dungeon = False
                            dungeonmenu = False
                            running = False

        if dungeon:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    dungeon = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        dungeonmenu = True
                        dungeon_menu.draw()
                    if event.key == pygame.K_p:
                        top_birb.running = True
                        dungeon = False
                        top_birb.menu.draw()
            if not dungeonmenu:
                player_hud.update_torch_meter(25)
                dungeon_background.move(1)
                player.move(100)
                screen_buffer_2.blit(player.surface, ((Environment.ScreenWidth/2 - player.width/2), (Environment.ScreenHeight/2 - player.height/2)))
            player_hud.update(player_inventory)
            screen_buffer_1.blit(dungeon_background.surface, (0, 0))

        if top_birb.running:
            screen_buffer_2.blit(top_birb.image, (0, 0))
            top_birb.set_health(top_birb.health)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    top_birb.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        top_birb.menu.draw()
                    if event.key == pygame.K_DOWN:
                        top_birb.menu.draw()
                    if event.key == pygame.K_RETURN:
                        if top_birb.menu.get_index() == len(top_birb.options):
                            top_birb.running = False
                            dungeon = True
                            menu_buffer.fill((255, 0, 255))
                            screen_buffer_2.fill((255, 0, 255))
                        if top_birb.menu.get_index() == 0:
                            if chance_outcome(top_birb.options[0].chance):
                                top_birb.set_health(top_birb.health - top_birb.options[0].damage)
                                if top_birb.health <= 0:
                                    top_birb.running = False
                                    dungeon = True
                                    menu_buffer.fill((255, 0, 255))
                                    screen_buffer_2.fill((255, 0, 255))
                        if top_birb.menu.get_index() == 1:
                            if chance_outcome(top_birb.options[1].chance):
                                top_birb.set_health(top_birb.health - top_birb.options[1].damage)
                                if top_birb.health <= 0:
                                    top_birb.running = False
                                    dungeon = True
                                    menu_buffer.fill((255, 0, 255))
                                    screen_buffer_2.fill((255, 0, 255))
                        if top_birb.menu.get_index() == 2:
                            if chance_outcome(top_birb.options[2].chance):
                                top_birb.set_health(top_birb.health - top_birb.options[2].damage)
                                if top_birb.health <= 0:
                                    top_birb.running = False
                                    dungeon = True
                                    menu_buffer.fill((255, 0, 255))
                                    screen_buffer_2.fill((255, 0, 255))
                        if top_birb.menu.get_index() == 3:
                            if chance_outcome(top_birb.options[3].chance):
                                top_birb.set_health(top_birb.health - top_birb.options[3].damage)
                                if top_birb.health <= 0:
                                    top_birb.running = False
                                    dungeon = True
                                    menu_buffer.fill((255, 0, 255))
                                    screen_buffer_2.fill((255, 0, 255))

        if dungeonmenu or tavern or opening or top_birb.running:
            menu_boolean = True
        else:
            menu_boolean = False

        screen.blit(screen_buffer_1, (0, 0))
        screen.blit(screen_buffer_2, (0, 0))
        if dungeon:
            screen.blit(player_hud.surface, (0, 0))
        if menu_boolean:
            screen.blit(menu_buffer, (0, 0))

        pygame.display.flip()
        screen.fill((255, 0, 255))


if __name__=="__main__":
    # call the main function
    main()
