import pygame


class Ship:
    """Een class voor handelingen van een schip"""

    def __init__(self, ai_game):
        """Initialiseren van een schip en zijn start positie"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Laden van afb schip en verkijgen van hoeken.
        self.image = pygame.image.load('image/ship.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x)

    def update(self):
        """Update van schip positie gebasseerd op beweging vlag"""
        # Update schip value en niet van rect.
        if self.moving_right:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed
        if self.moving_left:
            if self.moving_left and self.rect.left > 0:
                self.x -= self.settings.ship_speed

        # Update rect object van self.x.
        self.rect.x = self.x

    def center_ship(self):
        """Center het ship op scherm."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Tekenen van een schip en zijn huidige locatie"""

        self.screen.blit(self.image, self.rect)
