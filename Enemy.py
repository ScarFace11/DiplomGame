import pygame
from maze_settings import maze_settings


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.rect = None
        self.image = None
        self.pos = pos
        self.size = size
        self.speed = 2.5  #maze_settings.Tile_size / 10 #- 3
        self.direction = pygame.math.Vector2(0, 0)
        self.camera_offset = None
        self.name = None
        self.color_path = None

        self.path = []
        self.destroy_path = False
        self.collision_rects = []

    def draw(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(topleft=self.pos)

    def get_coord(self):
        col = self.rect.centerx // maze_settings.Tile_size
        row = self.rect.centery // maze_settings.Tile_size
        return col, row

    def set_path(self, path, camera_offset):
        self.path = path
        self.camera_offset = camera_offset
        self.create_collision_rects()
        self.get_direction()

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = point.x * maze_settings.Tile_size - int(self.camera_offset[0]) + (
                        maze_settings.Tile_size // 2)
                y = point.y * maze_settings.Tile_size - int(self.camera_offset[1]) + (
                        maze_settings.Tile_size // 2)
                rect = pygame.Rect(
                    (x + int(self.camera_offset[0]), y + int(self.camera_offset[1])),
                    (3, 3))
                self.collision_rects.append(rect)

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.rect.center)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            if (start - end) == [0, 0]:
                self.direction = pygame.math.Vector2(0, 0)
            else:
                self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.path = []

    def check_collision(self):
        if self.collision_rects:
            self.destroy_path = False
            for rect in self.collision_rects:
                if rect.collidepoint(self.rect.center):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.destroy_path = True


class Wanderer_Red(Enemy):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        img_path = 'Sprite/Enemy/Wanderer/1.png'
        self.draw(img_path)
        self.pos = self.rect.center
        self.name = "Red_Wanderer"
        self.color_path = '#FF0000'

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        self.check_collision()


class Wanderer_Blue(Enemy):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        img_path = 'Sprite/Enemy/Wanderer/2.png'
        self.draw(img_path)
        self.pos = self.rect.center
        self.name = "Blue_Wanderer"
        self.color_path = '#3691CF'

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        self.check_collision()


class Wanderer_Pink(Enemy):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        img_path = 'Sprite/Enemy/Wanderer/3.png'
        self.draw(img_path)
        self.pos = self.rect.center
        self.name = "Pink_Wanderer"
        self.color_path = '#FF80FF'
        self.speed = maze_settings.Tile_size / 10

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        self.check_collision()
