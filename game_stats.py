

class GameStats:
    """Track statistics voor weed invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.game_active = False
        self.settings = ai_game.settings
        self.max_ship_hp = self.settings.max_ship_hp
        self.current_left = self.settings.ship_limit
        self.reset_stats()


    def reset_stats(self):
        """Initialize statistics die kunnen veranderen tijdens spel."""
        self.ship_left = self.settings.ship_limit
        self.current_ship_hp = self.settings.max_ship_hp
        self.score = int(0)
        self.wave = int(1)

