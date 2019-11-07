import pygame
from pygame.sprite import Group

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
    
        gf.create_fleet(self.ai_settings, self.screen, self.sounds, self.aliens)
        gf.create_barriers(self.ai_settings, self.screen, self.barriers)
    
        # timers used for animation and event checking
        self.alien_timer = Timer(self.ai_settings.alien_frame_factor)
        self.smoke_timer = Timer(8)
        self.ship_timer = Timer(4)
        self.ufo_timer = Timer(self.ai_settings.alien_frame_factor * 5)

        self.stats.game_active = True

    def frame_step(self, simplify=False, inputs=None):
        gf.check_events(self.ai_settings, self.screen, self.sounds, self.stats, self.sb, self.scores, self.play_button, self.high_score_button, 
                        self.ship, self.aliens, self.bullets, self.barriers, self.alien_bullets, self.smokes, inputs)

        if self.stats.game_active:
            gf.update_timers(self.alien_timer, self.ufo_timer, self.ship_timer, self.smoke_timer)
            gf.update_ship(self.stats, self.sb, self.scores, self.ship, self.aliens, self.ufo, self.bullets, self.alien_bullets, self.ship_timer, self.alien_timer)
            if not self.ship.hit:
                gf.update_bullets(self.ai_settings, self.screen, self.sounds, self.stats, self.sb, self.ship, self.aliens, self.ufo,
                                  self.bullets, self.barriers, self.alien_bullets, self.smokes, self.alien_timer, self.ufo_timer, self.smoke_timer, simplify)
                gf.update_aliens(self.ai_settings, self.screen, self.sounds, self.ship, self.aliens, self.barriers, self.alien_bullets, self.alien_timer, simplify)
                gf.update_ufo(self.ufo, self.ufo_timer, simplify)
                gf.update_smokes(self.smokes, self.smoke_timer)

        gf.update_screen(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.ufo, self.bullets, self.menu_bg, 
                         self.play_button, self.high_score_button, self.barriers, self.alien_bullets, self.smokes, simplify)

        reward = self.stats.score
        game_state = self.stats.game_active

        if self.stats.game_active is False:
            self.__init__()
            reward = -1

        if inputs is not None:
            image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        else:
            image_data = None
        pygame.display.update()

        clock.tick(60)
        return reward, image_data, game_state


if __name__ == '__main__':
    game = SpaceInvadersGame()
    status = True
    while status:
        status = game.frame_step()[2]
