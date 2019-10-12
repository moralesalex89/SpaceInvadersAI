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


def run_game():
    pygame.init()
    clock = pygame.time.Clock()

    highscores = HighScore()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    sounds = Sound()

    play_button = Button(screen, pygame.image.load('images/play_btn.png'), 850, 400)
    high_score_button = Button(screen, pygame.image.load('images/high_score_btn.png'), 850, 600)
    menu_bg = Button(screen,
                     pygame.image.load('images/menu.png'), ai_settings.screen_width / 2, ai_settings.screen_height / 2)
    stats = GameStats(ai_settings, highscores)
    sb = Scoreboard(ai_settings, screen, sounds, stats)

    ship = Ship(ai_settings, screen, sounds)
    bullets = Group()
    alien_bullets = Group()
    aliens = Group()
    ufo = UFO(ai_settings, screen, sounds)
    barriers = Group()
    smokes = Group()

    gf.create_fleet(ai_settings, screen, sounds, aliens)
    gf.create_barriers(ai_settings, screen, barriers)

    # timers used for animation and event checking
    alien_timer = Timer(ai_settings.alien_frame_factor)
    smoke_timer = Timer(8)
    ship_timer = Timer(4)
    ufo_timer = Timer(ai_settings.alien_frame_factor * 5)

    while True:
        clock.tick(60)
        gf.check_events(ai_settings, screen, sounds, stats, sb, highscores, play_button, high_score_button,
                        ship, aliens, bullets, barriers, alien_bullets, smokes)

        if stats.game_active:
            gf.update_timers(alien_timer, ufo_timer, ship_timer, smoke_timer)
            gf.update_ship(stats, sb, highscores, ship, aliens, ufo, bullets, alien_bullets, ship_timer, alien_timer)
            if not ship.hit:
                gf.update_bullets(ai_settings, screen, sounds, stats, sb,  ship, aliens, ufo,
                                  bullets, barriers, alien_bullets, smokes, alien_timer, ufo_timer, smoke_timer)
                gf.update_aliens(ai_settings, screen, sounds, ship, aliens, barriers, alien_bullets, alien_timer)
                gf.update_ufo(ufo, ufo_timer)
                gf.update_smokes(smokes, smoke_timer)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, ufo, bullets, menu_bg,
                         play_button, high_score_button, barriers, alien_bullets, smokes)


run_game()
