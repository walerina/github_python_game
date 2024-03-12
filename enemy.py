import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.w = 32
        self.h = 704
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill('black')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.direction.x = 1
        self.speed = 3

    def update(self):
        self.rect.x += self.direction.x * self.speed

    def return_h(self):
        return self.h

    def return_w(self):
        return self.w

    def return_x(self):
        return self.rect.x