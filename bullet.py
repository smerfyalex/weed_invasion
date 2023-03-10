# Kogel class.

# Importeren modules.
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Een class voor behandeling kogel van een schip"""

    def __init__(self, ai_game, pos_x, pos_y, direction):
        """Maken van een kogel op zelfde positie van schip."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.direction = direction
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)

        if self.direction == 'up':
            self.rect.midbottom = (pos_x, pos_y)
        elif self.direction == 'down':
            self.rect.midtop = (pos_x, pos_y)

        self.y = float(self.rect.y)

    def update(self):
        """Bewegen van kogel y possitie"""
        if self.direction == 'up':
            self.y -= self.settings.bullet_speed
        elif self.direction == 'down':
            self.y += self.settings.alien_bullet_speed

        self.rect.y = self.y

    def draw_bullet(self):
        """Tekenen van kogel op het scherm"""
        pygame.draw.rect(self.screen, self.color, self.rect)
