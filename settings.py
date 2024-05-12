import pygame
import pygame_menu
from maze_settings import maze_settings

pygame.init()


def Back():
    from MainMenu import StartMenu
    return StartMenu()


def ResizeTile(value, size):
    maze_settings.Settings_TileSizeIndex = value[1]
    maze_settings.Tile_size = size


def MusicSwitch(value):
    if value:
        maze_settings.GameMusicOn = True
    else:
        maze_settings.GameMusicOn = False


def MusicVolume(value):
    maze_settings.Settings_MusicVolume = value


def SoundSwitch(value):
    if value:
        maze_settings.GameSoundOn = True
    else:
        maze_settings.GameSoundOn = False


def SoundVolume(value):
    maze_settings.Settings_SoundVolume = value


class SettingsMenu:
    def __init__(self):
        self.Frame_Graphics = None
        self.Frame_Music = None
        self.Frame_Control = None
        self.Frame_Navigate_Main = None
        self.frame_navigate_Graphics_menu = None
        self.frame_navigate_music_menu = None
        self.frame_navigate_control_menu = None
        self.Menu_Main = pygame_menu.Menu("Настройки", maze_settings.Width, maze_settings.Height,
                                          theme=maze_settings.Settings_Theme)

        self.Menu_Setting_Graphics = pygame_menu.Menu("Графика", maze_settings.Width, maze_settings.Height,
                                                      theme=maze_settings.Settings_Theme)
        self.Menu_Setting_Music = pygame_menu.Menu("Музыка", maze_settings.Width, maze_settings.Height,
                                                   theme=maze_settings.Settings_Theme)
        self.Menu_Setting_Control = pygame_menu.Menu("Управление", maze_settings.Width, maze_settings.Height,
                                                     theme=maze_settings.Settings_Theme)
        self.resolutions = [(1920, 1080), (1300, 900), (1024, 720), (2560, 1080)]
        self.Tile_size = [50, 60, 70, 80, 90, 100]

        Link = self.Menu_Main.add.menu_link(self.Menu_Setting_Graphics)
        Link.open()

    def show_settings(self):
        self.Menu_Main.add.label("Ты не должен был тут оказаться")
        self.Menu_Main.add.button("Назад", Back)

        self.frame_navigate_Graphics_menu = self.Menu_Setting_Graphics.add.frame_h(maze_settings.Width // 2, 50,
                                                                                   background_color=(120, 200, 50),
                                                                                   padding=0,
                                                                                   )
        self.frame_navigate_Graphics_menu.pack(
            self.Menu_Setting_Graphics.add.button("Графика", self.Open_Graphics_menu))
        self.frame_navigate_Graphics_menu.pack(self.Menu_Setting_Graphics.add.button("Музыка", self.Open_Music_menu))
        self.frame_navigate_Graphics_menu.pack(
            self.Menu_Setting_Graphics.add.button("Управление", self.Open_Control_menu))

        self.Frame_Graphics = self.Menu_Setting_Graphics.add.frame_v(maze_settings.Width // 2,
                                                                     maze_settings.Height // 2,
                                                                     background_color=(50, 50, 50),
                                                                     padding=0,
                                                                     )
        self.Frame_Graphics.pack(self.Menu_Setting_Graphics.add.dropselect('Разрешение',
                                                                           [(f"{w}x{h}", (w, h)) for w, h in
                                                                            self.resolutions],
                                                                           onchange=self.draw,
                                                                           default=maze_settings.Settings_DefaultResolutionNumber))
        self.Frame_Graphics.pack(self.Menu_Setting_Graphics.add.dropselect('Размер текстур',
                                                                           [(f"{size}x{size}", size) for size in
                                                                            self.Tile_size],
                                                                           onchange=ResizeTile,
                                                                           default=maze_settings.Settings_TileSizeIndex))

        self.Menu_Setting_Graphics.add.button("Сбросить настройки", self.ResetSettings)
        self.Menu_Setting_Graphics.add.button("Назад", Back)

        self.frame_navigate_music_menu = self.Menu_Setting_Music.add.frame_h(maze_settings.Width // 2, 50,
                                                                             background_color=(120, 200, 50),
                                                                             padding=0,
                                                                             align=pygame_menu.locals.ALIGN_CENTER)

        self.frame_navigate_music_menu.pack(
            self.Menu_Setting_Music.add.button("Графика", self.Open_Graphics_menu))
        self.frame_navigate_music_menu.pack(
            self.Menu_Setting_Music.add.button("Музыка", self.Open_Music_menu))
        self.frame_navigate_music_menu.pack(
            self.Menu_Setting_Music.add.button("Управление", self.Open_Control_menu))

        self.Frame_Music = self.Menu_Setting_Music.add.frame_v(maze_settings.Width // 2,
                                                               maze_settings.Height // 2,
                                                               background_color=(50, 50, 50),
                                                               padding=0,
                                                               aligin=pygame_menu.locals.ALIGN_CENTER)
        self.Frame_Music.pack(
            self.Menu_Setting_Music.add.toggle_switch(title="Музыка", default=maze_settings.GameMusicOn,
                                                      toggleswitch_id="Music", onchange=MusicSwitch,
                                                      )
        )
        self.Frame_Music.pack(
            self.Menu_Setting_Music.add.range_slider(title="Громкость", default=maze_settings.Settings_MusicVolume,
                                                     range_values=(0, 100), increment=1,
                                                     value_format=lambda x: str(int(x)), onchange=MusicVolume)
        )
        self.Frame_Music.pack(
            self.Menu_Setting_Music.add.toggle_switch(title="Эффекты", default=maze_settings.GameSoundOn,
                                                      toggleswitch_id="Sound", onchange=SoundSwitch)
        )
        self.Frame_Music.pack(
            self.Menu_Setting_Music.add.range_slider(title="Громкость", default=maze_settings.Settings_SoundVolume,
                                                     range_values=(0, 100), increment=1,
                                                     value_format=lambda x: str(int(x)), onchange=SoundVolume)
        )
        self.Menu_Setting_Music.add.button("Сбросить настройки", self.ResetSettings)
        self.Menu_Setting_Music.add.button("Назад", Back)

        self.frame_navigate_control_menu = self.Menu_Setting_Control.add.frame_h(maze_settings.Width // 2, 50,
                                                                                 background_color=(120, 200, 50),
                                                                                 padding=0,
                                                                                 align=pygame_menu.locals.ALIGN_CENTER)

        self.frame_navigate_control_menu.pack(
            self.Menu_Setting_Control.add.button("Графика", self.Open_Graphics_menu))
        self.frame_navigate_control_menu.pack(
            self.Menu_Setting_Control.add.button("Музыка", self.Open_Music_menu))
        self.frame_navigate_control_menu.pack(
            self.Menu_Setting_Control.add.button("Управление", self.Open_Control_menu))

        self.Frame_Control = self.Menu_Setting_Control.add.frame_v(maze_settings.Width // 2,
                                                                   maze_settings.Height // 2,
                                                                   background_color=(50, 50, 50),
                                                                   padding=0,
                                                                   aligin=pygame_menu.locals.ALIGN_CENTER)

        ControlInfo = 'WASD / стрелки - движение персонажем\n' \
                      'Лкм - от персонажа рисуется путь и движется по нему*\n' \
                      '*пути перезаписываются\n' \
                      'Пкм - стереть путь\n' \
                      'Пробел - остановиться'
        self.Frame_Control.pack(self.Menu_Setting_Control.add.label(ControlInfo, max_char=-1, font_size=20))

        self.Menu_Setting_Control.add.button("Сбросить настройки", self.ResetSettings)
        self.Menu_Setting_Control.add.button("Назад", Back)

        self.Menu_Main.mainloop(maze_settings.screen)

    def Open_Graphics_menu(self):
        Link = self.Menu_Main.add.menu_link(self.Menu_Setting_Graphics)
        Link.open()

    def Open_Music_menu(self):
        Link = self.Menu_Main.add.menu_link(self.Menu_Setting_Music)
        Link.open()

    def Open_Control_menu(self):
        Link = self.Menu_Main.add.menu_link(self.Menu_Setting_Control)
        Link.open()

    def ResetSettings(self):
        maze_settings.Reset_Settings()
        self.Menu_Setting_Graphics.reset_value()
        self.Menu_Main.reset_value()
        self.Menu_Setting_Music.reset_value()
        self.Menu_Setting_Control.reset_value()
        value = (('1300x900', (1300, 900)), 1)
        self.draw(value, (1300, 900))

    def draw(self, value, resolution):
        maze_settings.Settings_DefaultResolutionNumber = value[1]

        w = pygame.Surface([maze_settings.Width, maze_settings.Height])
        Width, Height = resolution[0], resolution[1]

        frame = pygame.transform.scale(w, (Width, Height))
        maze_settings.screen.blit(frame, frame.get_rect())

        maze_settings.Width = Width
        maze_settings.Height = Height
        maze_settings.screen = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.HWSURFACE)

        if (Width, Height) == (maze_settings.current_w, maze_settings.current_h):
            maze_settings.screen = pygame.display.set_mode((Width, Height),
                                                           pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            maze_settings.screen = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.HWSURFACE)

        self.Menu_Main.resize(maze_settings.Width, maze_settings.Height)

        self.Menu_Setting_Graphics.resize(maze_settings.Width, maze_settings.Height)
        self.Frame_Graphics.resize(maze_settings.Width // 2, maze_settings.Height // 2)
        self.frame_navigate_Graphics_menu.resize(maze_settings.Width // 2, 50)

        self.Menu_Setting_Music.resize(maze_settings.Width, maze_settings.Height)
        self.Frame_Music.resize(maze_settings.Width // 2, maze_settings.Height // 2)
        self.frame_navigate_music_menu.resize(maze_settings.Width // 2, 50)

        self.Menu_Setting_Control.resize(maze_settings.Width, maze_settings.Height)
        self.Frame_Control.resize(maze_settings.Width // 2, maze_settings.Height // 2)
        self.frame_navigate_control_menu.resize(maze_settings.Width // 2, 50)

        pygame.display.update()

    #def settings_control(self):


if __name__ == "__main__":
    SettingsObj = SettingsMenu()
    SettingsObj.show_settings()
