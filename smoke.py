import pygame
from pygame.sprite import Sprite

smoke1_a = pygame.image.load("images/smoke1_a.png")
smoke1_b = pygame.image.load("images/smoke1_b.png")
smoke1_c = pygame.image.load("images/smoke1_c.png")
smoke1_d = pygame.image.load("images/smoke1_d.png")
smoke2_a = pygame.image.load("images/smoke2_a.png")
smoke2_b = pygame.image.load("images/smoke2_b.png")
smoke2_c = pygame.image.load("images/smoke2_c.png")
smoke2_d = pygame.image.load("images/smoke2_d.png")
smoke3_a = pygame.image.load("images/smoke3_a.png")
smoke3_b = pygame.image.load("images/smoke3_b.png")
smoke3_c = pygame.image.load("images/smoke3_c.png")
smoke3_d = pygame.image.load("images/smoke3_d.png")
smoke_a = pygame.image.load("images/smoke_a.png")
smoke_b = pygame.image.load("images/smoke_b.png")
smoke_c = pygame.image.load("images/smoke_c.png")
smoke_d = pygame.image.load("images/smoke_d.png")

smoke_a = [smoke1_a, smoke2_a, smoke3_a, smoke_a]
smoke_b = [smoke1_b, smoke2_b, smoke3_b, smoke_b]
smoke_c = [smoke1_c, smoke2_c, smoke3_c, smoke_c]
smoke_d = [smoke1_d, smoke2_d, smoke3_d, smoke_d]


class Smoke(Sprite):
    def __init__(self, ai_settings, screen, smoke_type, rect):
        super(Smoke, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.type = smoke_type
        self.image = smoke_a[self.type]
        self.rect = rect

    def rotate(self):
        if self.image is smoke_a[self.type]:
            self.image = smoke_b[self.type]
        elif self.image is smoke_b[self.type]:
            self.image = smoke_c[self.type]
        elif self.image is smoke_c[self.type]:
            self.image = smoke_d[self.type]
        else:
            self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)