# Space-invaders.
import random
import sys
import pygame
import pygame.time
from pygame import mixer
from time import sleep

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from hp_meter import HealthBar


class AlianInvasion:
    """Algemene class voor behandelen game assets en gedrag"""

    def __init__(self):
        """Instaleren van het spel, maken van spel resource"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.stats = GameStats(self)  # Statistics van het spel.
        self.sb = Scoreboard(self, self.stats)  # Score display rechts van boven.

        self.ship = Ship(self)  # Tekenen van schip.
        self.hp_meter = HealthBar(self, self.stats)

        self.aliens = pygame.sprite.Group()  # Tekenen van alien.
        self.bullets = pygame.sprite.Group()  # Tekenen van kogels.
        self.last_alien_bullet_time = 0
        self.alien_bullets = pygame.sprite.Group()  # Tekenen van alien kogels.

        self._create_fleet()  # Maken van alien vloot.

        # Maken van verschillende knoppen.
        self._button_creator()

    def run_game(self):
        """Starten van main loop voor het spel"""
        while True:
            self._check_events()  # Kijken voor inputs users keyboard of muis.

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()  # Updaten van kogels.
                self._update_bullet()  # Verwijderen van kogel na verlaten scherm.
                self._update_aliens()  # Aliens bewegen naar rechts.
                self.alien_bullets.update()  # Updaten van alien kogels.
                self._fire_alien_bullet()
                self._update_alien_bullet()

            self.clock.tick(self.fps)
            self._update_screen()  # Opnieuw tekenen telkens deze door de loop gaat.

    def _check_events(self):
        """Reageren op keypresses en muis events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # Als een key wordt in gedrukt.
                self._check_key_down_events(event)
            elif event.type == pygame.KEYUP:  # Als een key wordt losgelaten.
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_key_down_events(self, event):
        """Reageren op key press"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.stats.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Reageren op key release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _button_creator(self):
        self.play_button = Button(self, "image/Start.png", index_x=0.5, index_y=12)
        self.score_button = Button(self, "image/Score.png", index_x=0.5, index_y=13)
        self.settings_button = Button(self, "image/Opties.png", index_x=0.5, index_y=14)
        self.stop_button = Button(self, "image/Stop.png", index_x=0.5, index_y=15)

    def _check_play_button(self, mouse_pos):
        start_clicked = self.play_button.rect.collidepoint(mouse_pos)
        quit_clicked = self.stop_button.rect.collidepoint(mouse_pos)
        if start_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)
            self.stats.reset_stats()
            self.hp_meter.reset_hp_bar()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_wave()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

        elif quit_clicked and not self.stats.game_active:
            sys.exit()

    def _fire_bullet(self):
        """Maken van een nieuwe kogel en deze toevoegen aan group"""
        if len(self.bullets) < self.settings.bullet_max:
            new_bullet = Bullet(self, self.ship.rect.centerx, self.ship.rect.top, 'up')
            self.bullets.add(new_bullet)
        # geluid van schot.
        bullet_sound = pygame.mixer.Sound("sounds/laser_shot.wav")
        bullet_sound.set_volume(0.1)
        bullet_sound.play()

    def _update_bullet(self):
        # Kogels verwijderen die zijn verdwenen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _fire_alien_bullet(self):
        fire = pygame.time.get_ticks()
        if fire - self.last_alien_bullet_time > 1000:
            if len(self.alien_bullets) < self.settings.alien_bullet_max:
                alien = random.choice(self.aliens.sprites())
                new_bullet = Bullet(self, alien.rect.centerx, alien.rect.bottom, 'down')
                self.alien_bullets.add(new_bullet)
                self.last_alien_bullet_time = fire

    def _update_alien_bullet(self):
        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(alien_bullet)
        self._check_alien_bullet_collisions()

    def _check_bullet_alien_collisions(self):
        """Reageert op kogel-alien collisions."""
        collision = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, False)

        if collision:
            for aliens in collision.values():
                for alien in aliens:
                    alien.hitpoints -= 1
                    self.stats.score += alien.points
                    if alien.hitpoints <= 0:
                        self.aliens.remove(alien)
                    self.sb.prep_score()

                # Geluid van ontploffing npc.
            explosion_sound = mixer.Sound("sounds/explosion.wav")
            explosion_sound.set_volume(0.1)
            explosion_sound.play()

        if not self.aliens:
            self.stats.wave += 1
            self.bullets.empty()
            self._create_fleet()
            self.sb.prep_wave()

    def _check_alien_bullet_collisions(self):
        for bullet in self.alien_bullets:
            if bullet.rect.colliderect(self.ship.rect):
                self.alien_bullets.remove(bullet)

                if self.stats.ship_left >= 0:
                    self.stats.current_ship_hp -= 1
                    self.hp_meter.update()

                    if self.stats.current_ship_hp == 0:
                        self._reset_game()


                else:
                    self.stats.game_active = False
                    pygame.mouse.set_visible(True)

    def _reset_game(self):
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        self.stats.ship_left -= 1

        self.ship.center_ship()
        self.hp_meter.reset_hp_bar()
        self.stats.current_ship_hp = self.settings.max_ship_hp

        self._create_fleet()

        sleep(0.5)

        print(self.stats.ship_left)

    def _create_alien(self, alien_number, row_number):
        if self.stats.game_active:
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien_height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)
            if self.stats.wave >= 2:
                alien.switch_image()

    def _create_fleet(self):
        """Maken van aliens"""
        # Maak een alien.
        if self.stats.game_active:
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            # X as maken van aliens.
            available_space_x = self.settings.screen_width - alien_width
            number_aliens_x = available_space_x // (2 * alien_width)
            # Y as maken van aliens.
            ship_height = self.ship.rect.height
            available_space_y = (self.settings.screen_height -
                                 (3 * alien_height) - ship_height)
            number_rows = available_space_y // (3 * alien_height) + 1

            for row_number in range(number_rows):
                for alien_number in range(number_aliens_x):
                    self._create_alien(alien_number, row_number)

    def _update_aliens(self):
        """Updaten van alle aliens van de vloot."""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _ship_hit(self):
        if self.stats.ship_left > 0:
            self._reset_game()

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Kijken of aliens bottom van scherm zijn."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Gedraagd zich als een geraakt schip.
                self._ship_hit()

                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _show_fps(self):
        self.font = pygame.font.Font(None, 30)
        self.fps_text = self.font.render(str(int(self.clock.get_fps())), True, (255, 0, 0))
        self.screen.blit(self.fps_text, (10, 10))

    def _update_screen(self):
        """Maken van nieuw scherm & update naar nieuw scherm"""

        if not self.stats.game_active:
            self.play_button.screen.blit(self.settings.menu_background, (0, 0))
            pygame.display.set_caption("Menu")
            self.play_button.draw_button()
            self.stop_button.draw_button()
            self.settings_button.draw_button()
            self.score_button.draw_button()
        else:
            self.screen.blit(self.settings.bg_color, (0, 0))
            pygame.display.set_caption("Weed Invasion")
            self.ship.blitme()
            self.hp_meter.draw()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            for alien_bullet in self.alien_bullets.sprites():
                alien_bullet.draw_bullet()

            self.aliens.draw(self.screen)

            self.sb.show_score()
            self._show_fps()
            self.sb.show_wave()

        # Meeste recente scherm zichtbaar maken.
        pygame.display.flip()


if __name__ == '__main__':
    ai = AlianInvasion()
    ai.run_game()
