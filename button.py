class Button:

    def __init__(self, screen, img, x, y):
        self.screen = screen
        self.image = img
        self.rect = img.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def draw_button(self):
        self.screen.blit(self.image, self.rect)

    def press(self, mouse_x, mouse_y):
        return self.rect.collidepoint(mouse_x, mouse_y)
