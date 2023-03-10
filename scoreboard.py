# Maken van scoreboard.
import pygame.font


class Scoreboard:
    """Een class voor score informatie te delen."""

    def __init__(self, ai_game, game_stats):
        self.wave_rect = None
        self.wave_image = None
        self.score_rect = None
        self.score_image = None

        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats

        # Font instellingen voor score informatie.
        self.text_color = (255, 50, 50)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()

    def prep_score(self):
        """Score veranderen in een afbeelding."""

        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Tekenen van score"""
        self.screen.blit(self.score_image, self.score_rect)

    def prep_wave(self):
        wave_str = f"wave: {self.stats.wave}"
        self.wave_image = self.font.render(wave_str, True,
                                           self.text_color, None)

        self.wave_rect = self.wave_image.get_rect()
        self.wave_rect.center = self.screen_rect.center
        self.wave_rect.top = 20

    def show_wave(self):
        self.screen.blit(self.wave_image, self.wave_rect)
