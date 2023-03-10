import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Een class voor één alien"""

    def __init__(self, ai_game):
        """Initialiseren van alien en een start positie geven."""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.aliens = {'alien1': {'image': pygame.image.load("image/alien_1.png").convert_alpha(),
                                  'points': 5, 'speed': 2.00, 'hp': 1},
                       'alien2': {'image': pygame.image.load("image/alien_2.png").convert_alpha(),
                                  'points': 5, 'speed': 3.25, 'hp': 2}}

        self.name = 'alien1'

        self.dynamic_alien()
        self.rect = self.image.get_rect()

        # Alien starten linkse boven hoek.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Opslaan van alien positie horizontaal.
        self.x = float(self.rect.x)

        # Settings punten en speed van alien.

    def dynamic_alien(self):
        self.image = self.aliens[self.name]['image']
        self.points = self.aliens[self.name]['points']
        self.speed = self.aliens[self.name]['speed']
        self.hitpoints = self.aliens[self.name]['hp']

    def switch_image(self):
        """Verwisselen van alien soort."""
        if self.name == 'alien1':
            self.name = 'alien2'
            self.image = self.aliens[self.name]['image']
            self.points = self.aliens[self.name]['points']
            self.speed = self.aliens[self.name]['speed']
            self.hitpoints = self.aliens[self.name]['hp']
        else:
            self.name = 'alien1'
            self.image = self.aliens[self.name]['image']
            self.points = self.aliens[self.name]['points']
            self.speed = self.aliens[self.name]['speed']
            self.hitpoints = self.aliens[self.name]['hp']

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Alien updaten."""
        self.x += (self.speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
