import pygame


class HealthBar:

    def __init__(self, ai_game, game_stats):
        self.settings = ai_game.settings
        self.stats = game_stats
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.x = 550
        self.y = 60
        self.width = 100
        self.height = 10
        self.max_hp = self.settings.max_ship_hp
        self.current_hp = self.stats.current_ship_hp
        self.red = (255, 0, 0)  # Rood
        self.green = (0, 255, 0)  # Groen
        self.white = (255, 255, 255)  # Wit

    def update(self):
        print("current hp", self.current_hp)
        self.current_hp = self.stats.current_ship_hp

    def draw(self):
        # Draw the outline of the health bar
        outline_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.white, outline_rect, 2)

        # Calculate the fill percentage of the health bar
        fill_percentage = self.current_hp / self.max_hp
        fill_width = int(self.width * fill_percentage)

        # Draw the fill of the health bar
        fill_rect_1 = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.red, fill_rect_1)
        fill_rect_2 = pygame.Rect(self.x, self.y, fill_width, self.height)
        pygame.draw.rect(self.screen, self.green, fill_rect_2)

    def reset_hp_bar(self):
        self.current_hp = self.settings.max_ship_hp
