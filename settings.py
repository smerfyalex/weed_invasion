# Settings alien_invasion
import pygame.image


class Settings:
    """Een class die alle settings bevat voor alien_invasion"""

    def __init__(self):
        """initialiseren game's settings"""
        # Screen class.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = pygame.image.load("image/backround.png")
        self.bg_color = pygame.transform.scale(self.bg_color, (self.screen_width, self.screen_height))
        self.speedup_scale = 1.15

        # Schip class.
        self.ship_limit = 2
        self.max_ship_hp = 9

        # Kogel class.
        self.bullet_max = 15
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (50, 250, 0)

        # Alien class.
        self.alien_bullet = 0.5
        self.fleet_drop_speed = 40
        self.alien_bullet = (0, 250, 0)
        self.alien_bullet_speed = 3.75
        self.alien_bullet_max = 30
        self.alien_bullet_probability = 0.05

        # Button class.
        self.button_color = (0, 250, 0)
        self.button_text_color = (50, 235, 10)

        # background class..
        self.menu_background = pygame.image.load("image/Menu scherm AI.png")
        self.menu_background = pygame.transform.scale(self.menu_background, (self.screen_width, self.screen_height))

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Settings die veranderen tijdens het spel."""
        self.ship_speed = 5.25
        self.bullet_speed = 5.75
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale




