import pygame
import pygame_menu

from maze_settings import maze_settings

pygame.init()


def StartMenu():
    pygame.display.set_caption("Меню")

    def Levels():
        from Levels import show_level_menu
        return show_level_menu()

    def Levels_menu():
        from Levels_menu import Levels
        Levels_obj = Levels()
        return Levels_obj.Show_levels()

    def Shop_Menu():
        from Shop import Shop
        Shopmenuobj = Shop()
        return Shopmenuobj.Show_Shop()

    def Settings():
        from settings import SettingsMenu
        settingsmenuobj = SettingsMenu()
        return settingsmenuobj.show_settings()

    mytheme = pygame_menu.themes.THEME_ORANGE.copy()

    myimage = pygame_menu.baseimage.BaseImage(
        image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    mytheme.background_color = myimage

    menu = pygame_menu.Menu("Игра", maze_settings.Width, maze_settings.Height, theme=mytheme)

    engine = pygame_menu.sound.Sound()
    engine.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, 'Sound/Widgets/target-menu.mp3')
    menu.set_sound(engine, recursive=True)

    menu.add.button("Выбор уровня", Levels_menu)
    menu.add.button("Магазин", Shop_Menu)
    menu.add.button("Настройки", Settings)
    menu.add.button("Выход", action=pygame_menu.events.EXIT)


    menu.mainloop(maze_settings.screen)


if __name__ == "__main__":
    StartMenu()
