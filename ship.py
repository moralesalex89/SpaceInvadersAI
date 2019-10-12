import pygame
from pygame.sprite import Sprite

ship = pygame.image.load('images/ship.png')
s_death_a = pygame.image.load('images/ship_death_a.png')
s_death_b = pygame.image.load('images/ship_death_b.png')
s_death_c = pygame.image.load('images/ship_death_c.png')
s_death_d = pygame.image.load('images/ship_death_d.png')
s_death_e = pygame.image.load('images/ship_death_e.png')
s_death_f = pygame.image.load('images/ship_death_f.png')
s_death_g = pygame.image.load('images/ship_death_g.png')
s_death_h = pygame.image.load('images/ship_death_h.png')
s_death_i = pygame.image.load('images/ship_death_i.png')
s_death_j = pygame.image.load('images/ship_death_j.png')
s_death_k = pygame.image.load('images/ship_death_k.png')
s_death_l = pygame.image.load('images/ship_death_l.png')
s_death = [s_death_a, s_death_b, s_death_c, s_death_d, s_death_e, s_death_f,
           s_death_g, s_death_h, s_death_i, s_death_j, s_death_k, s_death_l]


class Ship(Sprite):
    def __init__(self, ai_settings, screen, sounds):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.sounds = sounds

        self.image = ship
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False
        self.hit = False
        self.state = 0

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.image = ship
        self.hit = False
        self.state = 0
        self.center = self.screen_rect.centerx

    def play_death(self):
        if self.state >= len(s_death):
            return True
        else:
            self.rect.centery = self.rect.centery
            self.image = s_death[self.state]
            self.state += 1
            return False

    def destroy(self):
        self.sounds.explosion_play()
        self.hit = True
