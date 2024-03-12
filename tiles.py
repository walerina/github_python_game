import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('orange')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift

class Barrier(Tile):      
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.Surface((size, size))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft = pos)

class Barrier_fragile(Barrier):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.pos = pos
        self.image = pygame.Surface((size, size))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)
        self.broken = False

    def broke(self):
        self.broken = True
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=self.pos)

class Barrier_enemy(Barrier):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.damage = 5
        self.image = pygame.Surface((size, size))
        self.image.fill('yellow')
        self.rect = self.image.get_rect(topleft = pos)