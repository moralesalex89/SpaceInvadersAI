import pygame

ufo_a = pygame.image.load('images/ufo_a.png')
ufo_b = pygame.image.load('images/ufo_b.png')
ufo_c = pygame.image.load('images/ufo_c.png')
ufo_d = pygame.image.load('images/ufo_d.png')
ufo_e = pygame.image.load('images/ufo_e.png')
ufo_f = pygame.image.load('images/ufo_f.png')
ufo = [ufo_a, ufo_b, ufo_c, ufo_d, ufo_e, ufo_f]


class UFO:
    def __init__(self, ai_settings, screen, sounds):
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = ufo_a
        self.rect = self.image.get_rect()
        self.rect.right = 0
        self.rect.bottom = ai_settings.alien_start_pos_y - ai_settings.alien_space_factor
        self.state = 0
        self.hit = False
        self.sounds = sounds

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def get_score(self):
        multiplier = 1.0
        if self.state == 1:
            multiplier = abs((self.rect.centerx - self.ai_settings.screen_width) / self.ai_settings.screen_width)
        elif self.state == 2:
            multiplier = abs(self.rect.centerx / self.ai_settings.screen_width)

        if multiplier > 1:
            multiplier = 1
        elif multiplier < 0:
            multiplier = 0

        # using 4000 as an example of base score, UFO has minimum score value of 1/4 (1000) of its base score
        # value returned depends on how far the UFO traveled relative to its starting side and decreases
        # linearly with the multiplier of the other 3/4 of the score being between 0-1 depending on where it is hit
        base = self.ai_settings.alien_points_ufo / 10
        score = round(((3 / 4 * base) * multiplier) + (1 / 4 * base))
        # base score initially divided by 10 and the * 10 is given back down here
        # this is to make all returned scores divisible by 10 so it always returns a "Nice" value
        score *= 10
#        print("UFO gave you " + str(score) + " points.")
        return score

    def set_spawn(self, is_left):
        if self.sounds.ufo_loop is False:
            self.sounds.ufo_play()

        if is_left:
            self.rect.right = 0
            self.state = 1
        else:
            self.rect.left = self.ai_settings.screen_width
            self.state = 2

    def update(self, simplify=False):
        if not simplify:
            self.rotate()
        if self.state == 1 and self.rect.left < self.ai_settings.screen_width:
            self.rect.x += self.ai_settings.ufo_speed_factor
        elif self.state == 2 and self.rect.right > 0:
            self.rect.x -= self.ai_settings.ufo_speed_factor
        else:
            self.state = 0
            self.sounds.ufo_stop()

    def rotate(self):
        frame = ufo.index(self.image)
        frame += 1
        frame = frame % len(ufo)
        self.image = ufo[frame]

    def active(self):
        if self.state == 0:
            return False
        else:
            return True

    def destroy(self):
        self.state = 0
        self.hit = True
        self.rect.right = 0
        self.sounds.ufo_stop()
        self.sounds.d_ufo_play()

    def reset(self):
        self.state = 0
        self.rect.right = 0
        self.image = ufo_a
        self.hit = False
        self.sounds.ufo_stop()
