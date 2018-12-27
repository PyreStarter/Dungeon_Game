import pygame

class Menu:

    def __init__(self):
        self.lista = []
        self.pola = []
        self.size_font = 32
        self.font_path = 'Fonts/coders_crux.ttf'
        self.font = pygame.font.Font
        self.dest_surface = pygame.Surface
        self.quantity_pol = 0
        self.color_tla = (51, 51, 51)
        self.color_text = (255, 255, 153)
        self.color_selection = (153, 102, 255)
        self.position_selection = 0
        self.position_set = (0, 0)
        self.menu_width = 0
        self.menu_height = 0

    class Pole:
        text = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        selection_rect = pygame.Rect

    # Implement
    def move_menu(self, top, left):
        self.position_set = (top, left)

    def set_colors(self, text, selection, background):
        self.color_tla = background
        self.color_text = text
        self.color_selection = selection

    def width(self):
        return self.menu_width

    def set_font_size(self, font_size):
        self.size_font = font_size

    def set_font(self, path):
        self.font_path = path

    def get_position(self):
        return self.position_selection

    # Implement
    def init(self, lista, dest_surface):
        self.dest_surface = dest_surface
        self.create_structure()

    def draw(self, move=0):
        if move:
            self.position_selection += move
            if self.position_selection == -1:
                self.position_selection = self.quantity_pol - 1
            self.position_selection %= self.quantity_pol
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.color_tla)
        selection_rect = self.pola[self.position_selection].selection_rect
        pygame.draw.rect(menu, self.color_selection, selection_rect)

        for i in range(self.quantity_pol):
            menu.blit(self.pola[i].pole, self.pola[i].pole_rect)
        self.dest_surface.blit(menu, self.position_set)
        return self.position_selection

    def create_structure(self):
