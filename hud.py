from environment import Environment
import pygame

# Hud class, handles everything related to the HUD
class Hud:

    def __init__(self, inventory, database, width, height, font):
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
        self.font = font

    def set_item_tracker(self):
        count = 1
        for i in self.inventory.items:
            j = self.database.get_item(i[0])
            if j.Hud_Display:
                clear_space = pygame.Surface((96, 32))
                clear_space.fill((255, 0, 255))
                combined_image = pygame.Surface((76, 32))
                quantity_image = self.font.render(str(i[1]), 1, (255, 255, 255), (255, 0, 255))
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
