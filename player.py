from maze_settings import *
from support import import_sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations["walk"][self.frame_index]
        self.image = pygame.Surface((maze_settings.Tile_size, maze_settings.Tile_size))

        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2(0, 0)
        self.money = 0

        self.speed = maze_settings.Tile_size / 10.0
        # ��������� �������

        self.life = 3

        self.status = "walk"

        self.facing = {
            'up': False,
            'down': False,
            'right': False,
            'left': False
        }

        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.game_over = False
        self.win = False

    def _import_character_assets(self):
        character_path = "Sprite/pacman/"
        self.animations = {"walk": [], "win": [], "lose": []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)

    def set_facing(self, key):
        for direction in self.facing:
            self.facing[direction] = False
        self.facing[key] = True

    # animates the player actions
    def _animate(self):

        animation = self.animations[self.status]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (maze_settings.Tile_size, maze_settings.Tile_size))
        if self.facing['right']:
            self.image = image

        elif self.facing['left']:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        elif self.facing['up']:
            flipped_image = pygame.transform.rotate(image, 90)
            self.image = flipped_image

        elif self.facing['down']:
            flipped_image = pygame.transform.rotate(image, 270)
            self.image = flipped_image

        # set the rect
        if self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def _get_input(self, player_event):
        if player_event:
            if player_event == "right":
                self.direction.x = 1
                # self.direction.y = 0

            elif player_event == "left":
                self.direction.x = -1
                # self.direction.y = 0

            elif player_event == "up":
                self.direction.y = -1
                # self.direction.x = 0

            elif player_event == "down":
                self.direction.y = 1
                # self.direction.x = 0

            elif player_event == "stop":
                self.direction.x = 0
                self.direction.y = 0

            elif player_event == "restart":
                self.rect.x = 580
                self.rect.y = 485

        # else:
        # self.direction.x = 0
        # self.direction.y = 0

    # identifies player action
    def _get_status(self):
        if self.direction.x != 0 and self.direction.x != 0:
            self.status = "walk"

    # update the player's state
    def update(self, player_event, face):
        self._get_status()

        if self.life > 0 and not self.game_over:
            self._get_input(player_event)
        elif self.game_over and self.win:
            self.direction.x = 0
            self.direction.y = 0
            self.status = "win"
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.status = "lose"

        self.set_facing(face)

        self._animate()
