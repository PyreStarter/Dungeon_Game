from Environment import *
import menu
import pygame

#Every encounter (i.e. combat scenario, puzzle, riddle, trap, etc.) will be of this class.
class Encounter:
    def __init__(self):
        self.running = False

class Top_Birb(Encounter):
    def __init__(self):
        Encounter.__init__(self)

    def init(self, image, menu_buffer, sword_attack_option):
        self.image = image
        self.menu = menu.Menu([str(sword_attack_option.name) + ' - ' + str(sword_attack_option.text), 'Cry', 'Run Away'],
                        menu_buffer)

        #self.menu.move_menu(0, (Environment.ScreenWidth - self.menu.menu_height))
        #self.menu.menu_width = Environment.ScreenHeight
