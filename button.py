import pygame.font


class Button:

    def __init__(self, ai_game, image, index_x, index_y):
        """Initialiseren van button attribute."""
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Dimensies en eigenschappen van de button.
        self.width, self.height = 100, 50

        # Bouwen van button rect object en het centeren.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = index_x * self.width * 1.2

        # Max aantal knoppen in x as.
        self.max_width = self.settings.screen_width
        self.max_index_x = self.max_width // self.width

        self.rect.y = index_y * self.height
        self.max_height = self.settings.screen_height
        self.max_index_y = self.max_height // self.height

        # Button text hoeft maar 1 keer.
        self._prep_msg(image)

    def _prep_msg(self, image):
        """img en center text op de button."""
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 75))
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.image_rect)
