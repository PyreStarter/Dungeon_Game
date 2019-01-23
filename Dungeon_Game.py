from encounters import CombatEncounter
from card import Card, CardObject, CardItem
from database import Database
from deck import Deck
from environment import Environment
from hud import Hud
from inventory import Inventory
from item import Weapon, Torch
from player import Player
import pygame
import random
import menu
import json

pygame.font.init()
font = pygame.font.Font('Fonts\\coders_crux.ttf', 64)

# This class is for defining the unique options that will be provided by certain scenarios, items, and skills.
class Option:
    def __init__(self, name, text, damage=0, chance=0):
        self.name = name
        self.text = text
        self.chosen = False
        self.damage = damage
        self.chance = chance


class Card_Player:

    def __init__(self):
        self.deck = Deck()
        self.skill = 0
        self.power = 0
        self.wit = 0
        self.points_left = 0
        self.starting_hand_size = 0
        self.inventory = []

    def add_item(self, item):
        self.inventory.append(item)



# Background class. This will be used for the scrolling backdrops in the dungeon.
class Background:

    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("Image_Assets\\dungeon_background.png"), (Environment.ScreenWidth, Environment.ScreenHeight))
        self.surface = pygame.Surface((Environment.ScreenWidth, Environment.ScreenHeight))
        self.speed_counter = 0

    def move(self, speed_multiplier=1):
        self.speed = (Environment.ScreenWidth/640)*speed_multiplier
        self.surface.fill((255, 0, 255))
        self.surface.blit(self.image, (0, 0), ((0 + self.speed*self.speed_counter), 0, (Environment.ScreenWidth - self.speed*self.speed_counter), Environment.ScreenHeight))
        if self.speed_counter:
            self.surface.blit(self.image, ((Environment.ScreenWidth - self.speed*self.speed_counter), 0), (0, 0, self.speed*self.speed_counter, Environment.ScreenHeight))
        self.speed_counter += self.speed
        if self.speed_counter >= int(Environment.ScreenWidth/self.speed):
            self.speed_counter = 0


# This is a function that will take in a probability of success and return successful(True) or unsuccessful(False)
#  - The equation will probably be altered for game feel in the future
def chance_outcome(chance):
    number = random.randint(1, 100)
    if number <= chance:
        return True
    if number > chance:
        return False


def new_player_deck(player, card_index):
    player.deck = Deck()
    for i in card_index:
        if i.name == "Fumble":
            if player.skill < 2:
                player.deck.add_card(i)
                if player.skill < 1:
                    player.deck.add_card(i)
                    player.deck.add_card(i)
    for i in card_index:
        if i.name == "Quick":
            if player.skill > 2:
                player.deck.add_card(i)
                if player.skill > 3:
                    player.deck.add_card(i)
                    if player.skill > 4:
                        player.deck.add_card(i)
    for i in card_index:
        if i.name == "Dodge":
            if player.skill > 1:
                player.deck.add_card(i)
                if player.skill > 3:
                    player.deck.add_card(i)
                    if player.skill > 3:
                        player.deck.add_card(i)
    for i in card_index:
        if i.name == "Untouchable":
            if player.skill > 4:
                player.deck.add_card(i)
    for i in card_index:
        if i.name == "Strike":
            if player.power > 0:
                player.deck.add_card(i)
                if player.power > 1:
                    player.deck.add_card(i)
                    player.deck.add_card(i)
    for i in card_index:
        if i.name == "Great Strength":
            if player.power > 2:
                player.deck.add_card(i)
                if player.power > 3:
                    player.deck.add_card(i)
                    player.deck.add_card(i)
    for i in card_index:
        if i.name == "Monstrous Strength":
            if player.power > 4:
                player.deck.add_card(i)
    for i in card_index:
        if i.name == "Initiative":
            if player.wit > 3:
                player.deck.add_card(i)
    for i in card_index:
        if i.name == "Caution":
            if player.wit > 3:
                player.deck.add_card(i)
    for i in card_index:
        if i.name == "Quick Thinking":
            if player.wit > 4:
                player.deck.add_card(i)
    if player.wit == 0:
        player.starting_hand_size = 3
    elif player.wit == 1:
        player.starting_hand_size = 4
    elif player.wit == 2:
        player.starting_hand_size = 5
    elif player.wit > 2:
        player.starting_hand_size = 6
    return 0


def new_player_inventory(player, items):
    for i in items:
        if i.name == "Dagger":
            player.add_item(i)
    for i in items:
        if i.name == "Backpack":
            player.add_item(i)
    for i in items:
        if i.name == "Leather Armor":
            player.add_item(i)

def add_inventory_cards(player):
    for i in player.inventory:
        for j in i.card_list:
            player.deck.add_card(j)


def confirmation(buffer, screen):
    buffer.set_colorkey((255, 0, 255))
    screen.set_colorkey((255, 0, 255))
    confirmation_menu = menu.Menu()
    confirmation_menu.init(['No', 'Yes'], buffer)
    confirmation = True
    confirmation_menu.draw()
    while confirmation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                if event.key == pygame.K_UP:
                    confirmation_menu.select_previous()
                    confirmation_menu.draw()
                if event.key == pygame.K_DOWN:
                    confirmation_menu.select_next()
                    confirmation_menu.draw()
                if event.key == pygame.K_RETURN:
                    return confirmation_menu.get_index()
        screen.blit(buffer, (0, 0))
        pygame.display.flip()
    return 0



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
    decklist_buffer = menu_buffer

    dungeon_background = Background()
    player = Player()
    item_database = Database()
    card_player = Card_Player()

    player_inventory = Inventory()
    player_hud = Hud(player_inventory, item_database, Environment.ScreenWidth, Environment.ScreenHeight, font)

    torch = Torch()
    item_database.add_item(torch)

    player_inventory.add_item(torch)

# Card Stuff Card Stuff Card Stuff Card Stuff Card Stuff

    card_list = json.load(open("Image_Assets\\card_list.json"))
    card_index = []

    for i in card_list['card']:
        card_index.append(Card(i['name'], i['type'], i['text'], pygame.image.load(i['image']), font))

    card_item_list = json.load(open("Image_Assets\\card_item_list.json"))
    card_item_index = []

    for i in card_item_list['item']:
        temp_card_list = []
        for j in i['card']:
            for k in card_index:
                if str(j) == str(k.name):
                    temp_card_list.append(k)
        card_item_index.append(CardItem(pygame.image.load(i['image']), i['rarity'], i['value'], i['name'], temp_card_list))
        del temp_card_list


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

    top_birb = CombatEncounter(pygame.image.load("Image_Assets\\Tokoyami.png"), font, menu_buffer, 10)
    if len(player_inventory.main_hand.options):
        top_birb.add_option(player_inventory.main_hand.options[0])
    if len(player_inventory.off_hand.options):
        top_birb.add_option(player_inventory.off_hand.options[0])
    top_birb.initialize_menu()

# creating the menus

    opening_menu = menu.Menu()
    opening_menu.init(['New Game', 'Card Test', 'Inventory Test', 'Quit'], menu_buffer)
    opening = True

    opening_menu.draw()

    tavern_menu = menu.Menu()
    tavern_menu.init(['Enter Dungeon', 'Inventory', 'Quit'], menu_buffer)
    tavern = False

    dungeon_menu = menu.Menu()
    dungeon_menu.init(['Inventory', 'Decklist', 'Stop', 'Turn Around', 'Save & Quit'], menu_buffer)
    dungeonmenu = False

    decklistmenu = False
    inventory = False
    running = True
    dungeon = False
    card_test = False
    inventorymenu = False

    new_attributes_menu = menu.Menu()
    new_attributes_menu.init(['+1 Power', '+1 Skill', '+1 Wit'], menu_buffer)
    new_attributes = False


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
                        opening_menu.select_previous()
                        opening_menu.draw()
                    if event.key == pygame.K_DOWN:
                        opening_menu.select_next()
                        opening_menu.draw()
                    if event.key == pygame.K_RETURN:
                        if opening_menu.get_index() == 3:
                            running = False
                            opening = False
                        if opening_menu.get_index() == 2:
                            opening = False
                            inventory = True
                            temp_items = []
                            for i in card_item_index:
                                temp_items.append(i.name)
                            inventory_menu = menu.Menu()
                            inventory_menu.init(temp_items, menu_buffer)
                            menu_buffer.fill((0, 0, 0))
                            inventory_menu.x = 0
                            inventory_menu.y = 0
                            inventory_menu.draw()
                            for i in card_item_index:
                                if i.name == inventory_menu.options[inventory_menu.index].text:
                                    for j in range(i.card_list_length):
                                        menu_buffer.blit(i.card_list[j].surface, (
                                            int(Environment.ScreenWidth * .15) + j * i.card_list[j].width + 10, 20))
                        if opening_menu.get_index() == 1:
                            card_test = True
                            opening = False
                            menu_buffer.fill((255, 0, 255))
                            t = 0
                            menu_buffer.blit(card_index[t].surface, (int(Environment.ScreenWidth * .5), 20))
                            test_deck = Deck()
                        if opening_menu.get_index() == 0:
                            new_attributes = True
                            opening = False
                            card_player.power = 0
                            card_player.skill = 0
                            card_player.wit = 0
                            card_player.points_left = 5
                            menu_buffer.fill((255, 0, 255))
                            decklist_buffer.fill((255, 0, 255))
                            decklist_buffer.blit(font.render("Power: " + str(card_player.power), 1, (255, 255, 255),
                                                             (255, 0, 255)), (0, 0 * font.get_height()))
                            decklist_buffer.blit(font.render("Skill: " + str(card_player.skill), 1, (255, 255, 255),
                                                             (255, 0, 255)), (0, 1 * font.get_height()))
                            decklist_buffer.blit(font.render("Wit: " + str(card_player.wit), 1, (255, 255, 255),
                                                             (255, 0, 255)), (0, 2 * font.get_height()))
                            decklist_buffer.blit(font.render("Points left: " + str(card_player.points_left), 1,
                                                             (255, 255, 255),(255, 0, 255)), (0, 3 * font.get_height()))
                            menu_buffer.blit(decklist_buffer, (0, 0))
                            new_attributes_menu.draw()

        if new_attributes:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    new_attributes = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        new_attributes = False
                        opening = True
                    if event.key == pygame.K_UP:
                        new_attributes_menu.select_previous()
                        new_attributes_menu.draw()
                    if event.key == pygame.K_DOWN:
                        new_attributes_menu.select_next()
                        new_attributes_menu.draw()
                    if event.key == pygame.K_RETURN:
                        if new_attributes_menu.get_index() == 2:
                            card_player.wit += 1
                            card_player.points_left -= 1
                        if new_attributes_menu.get_index() == 1:
                            card_player.skill += 1
                            card_player.points_left -= 1
                        if new_attributes_menu.get_index() == 0:
                            card_player.power += 1
                            card_player.points_left -= 1
                        decklist_buffer.fill((255, 0, 255))
                        decklist_buffer.blit(font.render("Power: " + str(card_player.power), 1, (255, 255, 255),
                                                             (255, 0, 255)), (0, 0 * font.get_height()))
                        decklist_buffer.blit(font.render("Skill: " + str(card_player.skill), 1, (255, 255, 255),
                                                         (255, 0, 255)), (0, 1 * font.get_height()))
                        decklist_buffer.blit(font.render("Wit: " + str(card_player.wit), 1, (255, 255, 255),
                                                         (255, 0, 255)), (0, 2 * font.get_height()))
                        decklist_buffer.blit(font.render("Points left: " + str(card_player.points_left), 1, (255, 255, 255),
                                                         (255, 0, 255)), (0, 3 * font.get_height()))
                        menu_buffer.blit(decklist_buffer, (0, 0))
                        new_attributes_menu.draw()
                        if card_player.points_left == 0:
                            menu_buffer.fill((0, 0, 0))
                            decklist_buffer.blit(font.render("Power: " + str(card_player.power), 1, (255, 255, 255),
                                                             (0, 0, 0)), (0, 0 * font.get_height()))
                            decklist_buffer.blit(font.render("Skill: " + str(card_player.skill), 1, (255, 255, 255),
                                                             (0, 0, 0)), (0, 1 * font.get_height()))
                            decklist_buffer.blit(font.render("Wit: " + str(card_player.wit), 1, (255, 255, 255),
                                                             (0, 0, 0)), (0, 2 * font.get_height()))
                            decklist_buffer.blit(
                                font.render("Points left: " + str(card_player.points_left), 1, (255, 255, 255),
                                            (0, 0, 0)), (0, 3 * font.get_height()))
                            decklist_buffer.blit(
                                font.render("Confirm stat allocation?", 1, (255, 255, 255),
                                            (0, 0, 0)), (0, 4 * font.get_height()))
                            menu_buffer.blit(decklist_buffer, (0, 0))
                            c = confirmation(menu_buffer, screen)
                            if c:
                                new_attributes = False
                                tavern = True
                                menu_buffer.fill((255, 0, 255))
                                tavern_menu.draw()
                                new_player_deck(card_player, card_index)
                                new_player_inventory(card_player, card_item_index)
                                add_inventory_cards(card_player)
                            else:
                                card_player.power = 0
                                card_player.skill = 0
                                card_player.wit = 0
                                card_player.points_left = 5
                                menu_buffer.fill((255, 0, 255))
                                decklist_buffer.fill((255, 0, 255))
                                decklist_buffer.blit(font.render("Power: " + str(card_player.power), 1, (255, 255, 255),
                                                                 (255, 0, 255)), (0, 0 * font.get_height()))
                                decklist_buffer.blit(font.render("Skill: " + str(card_player.skill), 1, (255, 255, 255),
                                                                 (255, 0, 255)), (0, 1 * font.get_height()))
                                decklist_buffer.blit(font.render("Wit: " + str(card_player.wit), 1, (255, 255, 255),
                                                                 (255, 0, 255)), (0, 2 * font.get_height()))
                                decklist_buffer.blit(font.render("Points left: " + str(card_player.points_left), 1,
                                                                 (255, 255, 255), (255, 0, 255)),
                                                     (0, 3 * font.get_height()))
                                menu_buffer.blit(decklist_buffer, (0, 0))
                                new_attributes_menu.draw()

        if card_test:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    card_test = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        card_test = False
                        opening = True
                        menu_buffer.fill((255, 0, 255))
                        opening_menu.draw()
                    if event.key == pygame.K_UP:
                        if t < len(card_index) - 1:
                            t += 1
                        else:
                            t = 1 - len(card_index)
                        menu_buffer.blit(decklist_buffer, (0, 0))
                        menu_buffer.blit(card_index[t].surface,
                                         (int(Environment.ScreenWidth * .5), 20))
                    if event.key == pygame.K_DOWN:
                        if t > (len(card_index)*-1):
                            t -= 1
                        else:
                            t = len(card_index) - 1
                        menu_buffer.blit(decklist_buffer, (0, 0))
                        menu_buffer.blit(card_index[t].surface,
                                         (int(Environment.ScreenWidth*.5), 20))
                    if event.key == pygame.K_RETURN:
                        test_deck.add_card(card_index[t])
                        decklist_buffer.fill((255, 0, 255))
                        for i in range(len(test_deck.get_decklist())):
                            decklist_buffer.blit(font.render(str(test_deck.get_decklist()[i][1]) + "x " +
                                                         test_deck.get_decklist()[i][0], 1, (255, 255, 255),
                                                                     (255, 0, 255)), (0, i * font.get_height()))
                        menu_buffer.blit(decklist_buffer, (0, 0))
                        menu_buffer.blit(card_index[t].surface,
                                         (int(Environment.ScreenWidth * .5), 20))
                    if event.key == pygame.K_h:
                        active_cards = []
                        hand = random.sample(test_deck.list, 5)
                        for i in range(len(hand)):
                            active_cards.append(CardObject(hand[i], int(Environment.ScreenWidth/len(hand)), int(Environment.ScreenWidth/len(hand)*1.4)))
                            menu_buffer.blit(active_cards[i].surface, (active_cards[i].width * i, Environment.ScreenHeight - active_cards[i].height))


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
                        tavern_menu.select_previous()
                        tavern_menu.draw()
                    if event.key == pygame.K_DOWN:
                        tavern_menu.select_next()
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
                        dungeon_menu.select_previous()
                        dungeon_menu.draw()
                    if event.key == pygame.K_DOWN:
                        dungeon_menu.select_next()
                        dungeon_menu.draw()
                    if event.key == pygame.K_RETURN:
                        if dungeon_menu.get_index() == 4:
                            dungeon = False
                            dungeonmenu = False
                            running = False
                        if dungeon_menu.get_index() == 1:
                            dungeon = False
                            dungeonmenu = False
                            decklistmenu = True
                            temp_list = []
                            for i in card_player.deck.get_decklist():
                                temp_list.append(str(i[1]) + "x " + i[0])
                            decklist_menu = menu.Menu()
                            decklist_menu.init(temp_list, menu_buffer)
                            menu_buffer.fill((0, 0, 0))
                            decklist_menu.x = 0
                            decklist_menu.y = 0
                            decklist_menu.draw()
                            for i in card_index:
                                if i.name == decklist_menu.options[decklist_menu.index].text.split("x ", 1)[1]:
                                    menu_buffer.blit(i.surface, (int(Environment.ScreenWidth * .5), 20))
                        if dungeon_menu.get_index() == 0:
                            dungeonmenu = False
                            dungeon = False
                            inventorymenu = True
                            temp_items = []
                            for i in card_player.inventory:
                                temp_items.append(i.name)
                            inventory_menu = menu.Menu()
                            inventory_menu.init(temp_items, menu_buffer)
                            menu_buffer.fill((0, 0, 0))
                            inventory_menu.x = 0
                            inventory_menu.y = 0
                            inventory_menu.draw()
                            for i in card_item_index:
                                if i.name == inventory_menu.options[inventory_menu.index].text:
                                    for j in range(i.card_list_length):
                                        menu_buffer.blit(i.card_list[j].surface, (
                                            int(Environment.ScreenWidth * .15) + j * i.card_list[j].width + 10, 20))

        if decklistmenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    dungeon = False
                    decklistmenu = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        decklistmenu = False
                        dungeonmenu = True
                        dungeon = True
                        menu_buffer.fill((255, 0, 255))
                        dungeon_menu.draw()
                    if event.key == pygame.K_UP:
                        menu_buffer.fill((0, 0, 0))
                        decklist_menu.select_previous()
                        decklist_menu.draw()
                        for i in card_index:
                            if i.name == decklist_menu.options[decklist_menu.index].text.split("x ", 1)[1]:
                                menu_buffer.blit(i.surface, (int(Environment.ScreenWidth * .5), 20))
                    if event.key == pygame.K_DOWN:
                        menu_buffer.fill((0, 0, 0))
                        decklist_menu.select_next()
                        decklist_menu.draw()
                        for i in card_index:
                            if i.name == decklist_menu.options[decklist_menu.index].text.split("x ", 1)[1]:
                                menu_buffer.blit(i.surface, (int(Environment.ScreenWidth * .5), 20))
                    if event.key == pygame.K_h:
                        active_cards = []
                        hand = random.sample(card_player.deck.list, 5)
                        for i in range(len(hand)):
                            active_cards.append(CardObject(hand[i], int(Environment.ScreenWidth/len(hand)), int(Environment.ScreenWidth/len(hand)*1.4)))
                            menu_buffer.blit(active_cards[i].surface, (active_cards[i].width * i, Environment.ScreenHeight - active_cards[i].height))


        if inventory:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    dungeon = False
                    inventory = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        inventory = False
                        opening = True
                        menu_buffer.fill((255, 0, 255))
                        opening_menu.draw()
                    if event.key == pygame.K_UP:
                        menu_buffer.fill((0, 0, 0))
                        inventory_menu.select_previous()
                        inventory_menu.draw()
                        for i in card_item_index:
                            if i.name == inventory_menu.options[inventory_menu.index].text:
                                for j in range(i.card_list_length):
                                    menu_buffer.blit(i.card_list[j].surface, (int(Environment.ScreenWidth * .15) + j*i.card_list[j].width + 10, 20))
                    if event.key == pygame.K_DOWN:
                        menu_buffer.fill((0, 0, 0))
                        inventory_menu.select_next()
                        inventory_menu.draw()
                        for i in card_item_index:
                            if i.name == inventory_menu.options[inventory_menu.index].text:
                                for j in range(i.card_list_length):
                                    menu_buffer.blit(i.card_list[j].surface, (int(Environment.ScreenWidth * .15) + j*i.card_list[j].width + 10, 20))

        if inventorymenu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    dungeon = False
                    inventory = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        inventory = False
                        dungeon = True
                        dungeonmenu = True
                        menu_buffer.fill((255, 0, 255))
                        dungeon_menu.draw()
                    if event.key == pygame.K_UP:
                        menu_buffer.fill((0, 0, 0))
                        inventory_menu.select_previous()
                        inventory_menu.draw()
                        for i in card_item_index:
                            if i.name == inventory_menu.options[inventory_menu.index].text:
                                for j in range(i.card_list_length):
                                    menu_buffer.blit(i.card_list[j].surface, (int(Environment.ScreenWidth * .15) + j*i.card_list[j].width + 10, 20))
                    if event.key == pygame.K_DOWN:
                        menu_buffer.fill((0, 0, 0))
                        inventory_menu.select_next()
                        inventory_menu.draw()
                        for i in card_item_index:
                            if i.name == inventory_menu.options[inventory_menu.index].text:
                                for j in range(i.card_list_length):
                                    menu_buffer.blit(i.card_list[j].surface, (int(Environment.ScreenWidth * .15) + j*i.card_list[j].width + 10, 20))


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
                        top_birb.menu.select_previous()
                        top_birb.menu.draw()
                    if event.key == pygame.K_DOWN:
                        top_birb.menu.select_next()
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

        if dungeonmenu or tavern or opening or top_birb.running or card_test or inventory or new_attributes or decklistmenu or inventorymenu:
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
