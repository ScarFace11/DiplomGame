import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.rect = None
        self.image = None
        self.pos = pos
        self.size = size

    def draw(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=self.pos)


class Wall(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        img_path = 'Sprite/wall/stone.png'
        self.draw(img_path)


class Way(Tile):
    def __init__(self, pos, size):
        """

        :rtype: object
        """
        super().__init__(pos, size)
        img_path = 'Sprite/way/Default1Way.png'
        self.draw(img_path)


class Score(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        img_path = 'Sprite/score/score.png'
        self.draw(img_path)


class Goal(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        img_path = 'Sprite/money/money.png'
        self.draw(img_path)


class Icons(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        img_path = 'Sprite/icons/finish-flag.png'
        self.draw(img_path)
