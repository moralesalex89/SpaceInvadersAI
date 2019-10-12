import pygame

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()


class Sound:
    def __init__(self):
        self.ufo = pygame.mixer.Sound('sounds/ufo_highpitch.wav')
        self.ufo_loop = False
        self.ufo.set_volume(0.05)
        self.d_ufo = pygame.mixer.Sound('sounds/ufo_lowpitch.wav')
        self.d_ufo.set_volume(0.05)
        self.laser = pygame.mixer.Sound('sounds/invaderkilled.wav')
        self.laser.set_volume(0.1)
        self.shoot = pygame.mixer.Sound('sounds/shoot.wav')
        self.shoot.set_volume(0.1)
        self.explosion = pygame.mixer.Sound('sounds/explosion.wav')
        self.explosion.set_volume(0.1)
        self.move = pygame.mixer.Sound('sounds/fastinvader2.wav')
        self.move.set_volume(0.5)

    def ufo_play(self):
        self.ufo.play(-1)
        self.ufo_loop = True

    def ufo_stop(self):
        self.ufo.stop()
        self.ufo_loop = False

    def d_ufo_play(self):
        self.d_ufo.play()

    def laser_play(self):
        self.laser.play()

    def shoot_play(self):
        self.shoot.play()

    def explosion_play(self):
        self.explosion.play()

    def move_play(self):
        self.move.play()
