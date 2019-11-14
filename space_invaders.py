import pygame
from pygame.sprite import Group

from PIL import ImageGrab
from cv2 import *
import numpy
from scipy import misc

from highscore import HighScore
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from sound import Sound
from button import Button
from ship import Ship
from timer import Timer
from ufo import UFO
import game_functions as gf

pygame.init()
clock = pygame.time.Clock()


class SpaceInvadersGame:
    def __init__(self):
        self.scores = HighScore()
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode((self.ai_settings.screen_width, self.ai_settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.sounds = Sound()

        self.play_button = Button(self.screen, pygame.image.load('images/play_btn.png'), 850, 400)
        self.high_score_button = Button(self.screen, pygame.image.load('images/high_score_btn.png'), 850, 600)
        self.menu_bg = Button(self.screen, 
                         pygame.image.load('images/menu.png'), self.ai_settings.screen_width / 2, self.ai_settings.screen_height / 2)
        self.stats = GameStats(self.ai_settings, self.scores)
        self.sb = Scoreboard(self.ai_settings, self.screen, self.sounds, self.stats)

        self.ship = Ship(self.ai_settings, self.screen, self.sounds)
        self.bullets = Group()
        self.alien_bullets = Group()
        self.aliens = Group()
        self.ufo = UFO(self.ai_settings, self.screen, self.sounds)
        self.barriers = Group()
        self.smokes = Group()
        self.inactive = self.ai_settings.fps * 10

        gf.create_fleet(self.ai_settings, self.screen, self.sounds, self.aliens)
        gf.create_barriers(self.ai_settings, self.screen, self.barriers)
    
        # timers used for animation and event checking
        self.alien_timer = Timer(self.ai_settings.alien_frame_factor)
        self.smoke_timer = Timer(self.ai_settings.smoke_timer)
        self.ship_timer = Timer(self.ai_settings.ship_timer)
        self.ufo_timer = Timer(self.ai_settings.alien_frame_factor * 5)
        self.bullet_delay = 0

        self.stats.game_active = True

    def frame_step(self, simplify=False, inputs=None, name="Player"):
        init_bullet_count = len(self.bullets)
        gf.check_events(self.ai_settings, self.screen, self.sounds, self.stats, self.sb, self.scores, self.play_button, self.high_score_button,
                        self.ship, self.aliens, self.ufo, self.bullets, self.bullet_delay, self.barriers, self.alien_bullets, self.smokes, inputs)

        bullet_count = len(self.bullets)
        alien_count = len(self.aliens)
        ufo_state = self.ufo.hit
        ship_pos = self.ship.rect.left

        if init_bullet_count < bullet_count:
            self.bullet_delay = self.ai_settings.bullet_delay
        elif self.bullet_delay > 0:
            self.bullet_delay -= 1

        if self.stats.game_active:
            gf.update_timers(self.alien_timer, self.ufo_timer, self.ship_timer, self.smoke_timer)
            gf.update_ship(self.stats, self.sb, self.scores, self.ship, self.aliens, self.ufo, self.bullets, self.alien_bullets, self.ship_timer, self.alien_timer, simplify)
            if not self.ship.hit:
                gf.update_bullets(self.ai_settings, self.screen, self.sounds, self.stats, self.sb, self.ship, self.aliens, self.ufo,
                                  self.bullets, self.bullet_delay, self.barriers, self.alien_bullets, self.smokes, self.alien_timer, self.ufo_timer, self.smoke_timer, simplify)
                gf.update_aliens(self.ai_settings, self.screen, self.sounds, self.ship, self.aliens, self.barriers, self.alien_bullets, self.alien_timer, simplify)
                gf.update_ufo(self.ufo, self.ufo_timer, simplify)
                gf.update_smokes(self.smokes, self.smoke_timer)

        gf.update_screen(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.ufo, self.bullets, self.menu_bg,
                         self.play_button, self.high_score_button, self.barriers, self.alien_bullets, self.smokes, simplify)

        pygame.display.update()

        reward = 0
        if bullet_count > len(self.bullets):
            if len(self.aliens) < alien_count or self.ufo.hit != ufo_state:
                reward += 1
            else:
                reward -= 1
        if not gf.ship_in_invader_range(self.ai_settings, self.ship, self.aliens, self.ufo):
            reward -= 1
        if gf.ship_in_bullet_path(self.ship, self.alien_bullets):
            reward -= 1
        if reward < 0:
            reward = -1

        if alien_count < len(self.aliens):
            game_state = False
            reward = 1
            self.inactive = 240
            self.bullet_delay = 0

        else:
            game_state = self.stats.game_active

        if self.stats.game_active is False or self.inactive <= 0:
            self.stats.game_active = True
            reward = -1
            self.inactive = 240
            self.bullet_delay = 0
            self.scores.check_place(int(round(self.stats.score, -1)), name)
            gf.restart(self.ai_settings, self.screen, self.sounds, self.stats, self.sb,
                      self.ship, self.aliens, self.ufo, self.bullets, self.barriers, self.alien_bullets, self.smokes)

        image_data = None
        if inputs is not None:
            if len(inputs) == 3:
                img = self.screen
                image_data = pygame.surfarray.array3d(img)

        clock.tick(self.ai_settings.fps)
        self.inactive += reward
        print(reward, self.inactive)

        return reward, image_data, game_state


if __name__ == '__main__':
    game = SpaceInvadersGame()
    status = True
    while status:
        status = game.frame_step(simplify=True)[2]
