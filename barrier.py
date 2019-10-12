from pygame.sprite import *

barrier_tl = pygame.image.load("images/barrier_tl.png")
barrier_tc = pygame.image.load("images/barrier_tc.png")
barrier_tr = pygame.image.load("images/barrier_tr.png")
barrier_bl = pygame.image.load("images/barrier_bl.png")
barrier_bc = pygame.image.load("images/barrier_bc.png")
barrier_br = pygame.image.load("images/barrier_br.png")
damaged_barrier_tl = pygame.image.load("images/damaged_barrier_tl.png")
damaged_barrier_tc = pygame.image.load("images/damaged_barrier_tc.png")
damaged_barrier_tr = pygame.image.load("images/damaged_barrier_tr.png")
damaged_barrier_bl = pygame.image.load("images/damaged_barrier_bl.png")
damaged_barrier_bc = pygame.image.load("images/damaged_barrier_bc.png")
damaged_barrier_br = pygame.image.load("images/damaged_barrier_br.png")
images = [barrier_tl, barrier_tc, barrier_tr, barrier_bl, barrier_bc, barrier_br]
damaged_images = [damaged_barrier_tl, damaged_barrier_tc, damaged_barrier_tr,
                  damaged_barrier_bl, damaged_barrier_bc, damaged_barrier_br]


class Barrier(Sprite):
    def __init__(self, ai_settings, screen, barrier_type, x_pos, y_pos):
        super(Barrier, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        '''TYPE
        0   1   2
        3   4   5
        '''
        self.type = barrier_type
        self.image = images[self.type]
        self.rect = self.image.get_rect()
        self.health = 2
        self.rect.centerx = x_pos
        self.rect.top = y_pos

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def damage(self):
        self.health -= 1

        if self.health == 1:
            self.image = damaged_images[self.type]

        elif self.health <= 0:
            self.kill()
