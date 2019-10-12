import pygame
from pygame.sprite import Sprite

p_laser_a = pygame.image.load("images/p_laser_a.png")
p_laser_b = pygame.image.load("images/p_laser_b.png")
a_laser_a = pygame.image.load("images/a_laser_a.png")
a_laser_b = pygame.image.load("images/a_laser_b.png")
laser_a = [a_laser_a, p_laser_a]
laser_b = [a_laser_b, p_laser_b]


class Bullet(Sprite):
        def __init__(self, ai_settings, screen, source, is_ship):
            super(Bullet, self).__init__()
            self.screen = screen

            self.bullet_type = 0
            if is_ship:
                self.bullet_type = 1
            self.image = laser_a[self.bullet_type]
            self.frame = 0
            self.rect = self.image.get_rect()
            self.rect.centerx = source.rect.centerx

            if is_ship:
                self.rect.top = source.rect.top
            else:
                self.rect.top = source.rect.bottom

            self.y = float(self.rect.y)

            self.color = ai_settings.bullet_color
            if self.bullet_type == 1:
                self.speed_factor = ai_settings.bullet_speed_factor
            else:
                self.speed_factor = ai_settings.alien_bullet_speed_factor

        def update(self):
            if self.bullet_type == 1:
                self.y -= self.speed_factor
            else:
                self.y += self.speed_factor
            self.rect.y = self.y
            self.rotate()

        def rotate(self):
            if self.frame == 0 or self.frame >= 8:
                self.image = laser_a[self.bullet_type]
                self.frame = 0
            elif self.frame == 4:
                self.image = laser_b[self.bullet_type]
            self.frame += 1

        def blitme(self):
            self.screen.blit(self.image, self.rect)
