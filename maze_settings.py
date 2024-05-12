import pygame
import pygame_menu

from AllMazes import maze1

pygame.init()
"""
Нумерация в лабиринте:
    1 - Стенки лабиринта (через них нельзя пройти)
    2 - Пакмен - под управлением игрока
    31 - Враг Скиталец, просто блуждает
    41 - Ловушка шипы, когда они полностью показались, то игрок при соприкосновении теряет 1 хп и возвращается к стартовой точке
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

DisplayInfo = pygame.display.Info()


class MazeSettings:

    def __init__(self, screen):
        self.Width = default_Width
        self.Height = default_Height

        self.current_w = DisplayInfo.current_w
        self.current_h = DisplayInfo.current_h

        self.screen = screen

        self.background_image = pygame.image.load('Sprite/bg.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.Width, self.Height))

        self.GameMusicOn = True
        self.GameSoundOn = True

        self.Settings_DefaultResolutionNumber = 1
        self.Settings_MusicVolume = 20
        self.Settings_SoundVolume = 50

        #self.Levels_Difficulty_Settings = "Difficulty_Normal"
        self.Levels_Difficulty_Index_Settings = 0

        self.Settings_Theme = pygame_menu.themes.THEME_ORANGE.copy()
        #theme=pygame_menu.themes.THEME_BLUE
        self.myimage = pygame_menu.baseimage.BaseImage(
            image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
        )
        self.Settings_Theme.background_color = self.myimage

        self.Settings_TileSizeIndex = 0
        self.Tile_size = 50

        self.MazeStructure = {0, 2, 31, 32, 33, 41, 42, 5, 6, 10}
        self.Camera_Offset = [0, 0]

        self.Path = None
        self.Visibility_Enemy_Path = False

        self.Shop_Money = 0

        self.Player_hp = 3

        self.FastMazeStart = maze1

    def Reset_Settings(self):
        self.background_image = pygame.image.load('Sprite/bg.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.Width, self.Height))

        self.GameMusicOn = True
        self.GameSoundOn = True

        self.Settings_DefaultResolutionNumber = 1
        self.Settings_MusicVolume = 20
        self.Settings_SoundVolume = 50



        self.Settings_TileSizeIndex = 0
        self.Tile_size = 50


default_Width, default_Height = 1300, 900
maze_settings: MazeSettings = MazeSettings(
    screen=pygame.display.set_mode((default_Width, default_Height), pygame.DOUBLEBUF | pygame.HWSURFACE))

fps = 60
font = pygame.font.Font(None, 36)
