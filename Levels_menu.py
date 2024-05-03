from maze_settings import *
import pygame_menu


class Levels:
    def __init__(self):
        self.menu = pygame_menu.Menu("Выбор уровня", maze_settings.Width, maze_settings.Height,
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.screen = maze_settings.screen
    def Show_levels(self):
        self.menu.add.label("Стандартный лабиринт", margin=(0, 50))
        self.create_frame_selector_levels()

        self.menu.add.button("Назад", self.Back)

        self.menu.mainloop(self.screen)

    def create_frame_selector_levels(self):
        frame = self.menu.add.frame_h(maze_settings.Width , maze_settings.Height - 550,
                                      background_color=(50, 50, 50), padding=0,
                                      max_width=maze_settings.Width ,
                                      max_height=maze_settings.Height - 550)
        for i in range(9):
            frame.pack(
                self.menu.add.button(i + 1,
                                     padding=(40, 40),
                                     button_id=f'{i}',
                                     action=lambda x=i+1: self.Pick_Maze(x),
                                     font_size=60,
                                     border_color=(70, 120, 70),
                                     border_width=10,
                                     align=pygame_menu.locals.ALIGN_CENTER)
            )

    def Switch_type(self):
        pass

    def Selector_Maze(self):
        pass

    def Pick_Maze(self, key):
        from AllMazes import Standart_maze_list
        from OpenGame import Main
        from copy import deepcopy

        OpG = Main(maze_settings.screen)
        MazeMask = deepcopy(Standart_maze_list.get(key))
        OpG.main(MazeMask)

        #print(Standart_maze_list.get(key))

    def Back(self):
        from MainMenu import StartMenu
        return StartMenu()


if __name__ == "__main__":
    LevelsObj = Levels()
    LevelsObj.Show_levels()
