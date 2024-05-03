import pygame

pygame.init()
"""
Нумерация в лабиринте:
    1 - Стенки лабиринта (через них нельзя пройти)
    2 - Пакмен - под управлением игрока
    41 - Ловушка шипы, когда они полностию показались, то игрок при соприкосновении теряет 1 хп и возвращается к стартовой точке
    42 - Ловушка лазер, игрок при соприкосновении теряет 1 хп и возвращается к стартовой точке
    5 - Монетка - в будущем нужна для покупки в магазине
    6 - бонус - находится на всех дорожках, нужно для набора счёта, в дальнейшем для рекордной таблицы
    9 - пустота 
"""

#Tile_size = 50 # 50 
color_way = (155, 205, 255)
#color_way = (255, 205, 255)
#color_wall = (60, 60, 60)
#color_bonus = (0, 255, 0)
Color_Purple = (255, 30, 255)
Color_Yellow = (255, 255, 30)
Color_Black = (0, 0, 0)


class MazeSettings:
    def __init__(self, screen):
        self.Width = default_Width
        self.Height = default_Height
        self.screen = screen

        self.background_image = pygame.image.load('Sprite/bg.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.Width, self.Height))

        self.GameMusicOn = True
        self.GameSoundOn = True

        self.Settings_DefaultResolutionNumber = 1
        self.Settings_MusicVolume = 20
        self.Settings_SoundVolume = 50

        self.Settings_TileSizeIndex = 0
        self.Tile_size = 50

    def Reset_Settings(self):
        self.background_image = pygame.image.load('Sprite/bg.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.Width, self.Height))

        self.GameMusicOn = True
        self.GameSoundOn = True

        self.Settings_DefaultResolutionNumber = 1
        self.Settings_MusicVolume = 20
        self.Settings_SoundVolume = 50

        self.Settings_TileSize = 0
        self.Tile_size = 50


default_Width, default_Height = 1300, 900
maze_settings: MazeSettings = MazeSettings(
    screen=pygame.display.set_mode((default_Width, default_Height), pygame.DOUBLEBUF | pygame.HWSURFACE))

fps = 60
font = pygame.font.Font(None, 36)
