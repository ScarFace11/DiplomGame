import pygame
import pygame_menu
from maze_settings import maze_settings

pygame.init()


class SettingsMenu:
    def __init__(self):
        pass

    def show_settings(self):

        def Back():
            from MainMenu import StartMenu
            return StartMenu()

        def ResetSettings():
            maze_settings.Reset_Settings()
            Menu_Setting.reset_value()
            self.show_settings()

        def draw(value, resolution):
            maze_settings.Settings_DefaultResolutionNumber = value[1]

            w = pygame.Surface([maze_settings.Width, maze_settings.Height])
            Width, Height = resolution[0], resolution[1]

            frame = pygame.transform.scale(w, (Width, Height))
            maze_settings.screen.blit(frame, frame.get_rect())

            maze_settings.Width = Width
            maze_settings.Height = Height
            maze_settings.screen = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.HWSURFACE)

            if (Width, Height) == (1920, 1080):
                maze_settings.screen = pygame.display.set_mode((Width, Height),
                                                               pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
            if (Width, Height) == (2560, 1080):
                maze_settings.screen = pygame.display.set_mode((Width, Height),
                                                               pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
            else:
                maze_settings.screen = pygame.display.set_mode((Width, Height), pygame.DOUBLEBUF | pygame.HWSURFACE)

            Menu_Setting.resize(maze_settings.Width, maze_settings.Height)

            pygame.display.update()

        def ResizeTile(value, size):
            maze_settings.Settings_TileSizeIndex = value[1]
            maze_settings.Tile_size = size

        def MusicSwitch(value):
            if value:
                maze_settings.GameMusicOn = True
            else:
                maze_settings.GameMusicOn = False

        def SoundSwitch(value):
            if value:
                maze_settings.GameSoundOn = True
            else:
                maze_settings.GameSoundOn = False

        def MusicVolume(value):
            maze_settings.Settings_MusicVolume = value

        def SoundVolume(value):
            maze_settings.Settings_SoundVolume = value

        Menu_Setting = pygame_menu.Menu("Настройки", maze_settings.Width, maze_settings.Height,
                                        theme=pygame_menu.themes.THEME_BLUE)

        resolutions = [(1920, 1080), (1300, 900), (1024, 720), (2560, 1080)]

        Tile_size = [50, 60, 70, 80, 90, 100]

        Menu_Setting.add.dropselect('Разрешение', [(f"{w}x{h}", (w, h)) for w, h in resolutions],
                                    onchange=draw,
                                    default=maze_settings.Settings_DefaultResolutionNumber)
        Menu_Setting.add.dropselect('Размер текстур', [(f"{size}x{size}", size) for size in Tile_size],
                                    onchange=ResizeTile,
                                    default=maze_settings.Settings_TileSizeIndex)
        Menu_Setting.add.toggle_switch(title="Музыка", default=maze_settings.GameMusicOn,
                                       toggleswitch_id="Music",
                                       onchange=MusicSwitch)
        Menu_Setting.add.range_slider(title="Громкость", default=maze_settings.Settings_MusicVolume,
                                      range_values=(0, 100),
                                      increment=1,
                                      value_format=lambda x: str(int(x)),
                                      onchange=MusicVolume)
        Menu_Setting.add.toggle_switch(title="Эффекты", default=maze_settings.GameSoundOn,
                                       toggleswitch_id="Sound",
                                       onchange=SoundSwitch)
        Menu_Setting.add.range_slider(title="Громкость", default=maze_settings.Settings_SoundVolume,
                                      range_values=(0, 100),
                                      increment=1,
                                      value_format=lambda x: str(int(x)),
                                      onchange=SoundVolume)
        Menu_Setting.add.button("Сбросить настройки", ResetSettings)
        Menu_Setting.add.button("Назад", Back)

        Menu_Setting.mainloop(maze_settings.screen)


if __name__ == "__main__":
    SettingsObj = SettingsMenu()
    SettingsObj.show_settings()
