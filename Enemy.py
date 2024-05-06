import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.rect = None
        self.image = None
        self.pos = pos
        self.size = size
        self.speed = 3.0

    def draw(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=self.pos)


class Wanderer(Enemy):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        img_path = 'Sprite/Enemy/Wanderer/1.png'
        self.draw(img_path)

    def Walk(self):
        self.rect.x += self.speed

    def update(self):
        self.Walk()
