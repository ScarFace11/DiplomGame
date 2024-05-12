from MazeGenerator import *
from maze_settings import *

import pygame_menu


def Back():
    from Levels_menu import Levels
    LevelsObj = Levels()
    return LevelsObj.Show_levels()


class MazeGeneratorEdit:
    def __init__(self):
        self.frame = None
        self.menu = pygame_menu.Menu("Случайный лабиринт", maze_settings.Width, maze_settings.Height,
                                     theme=maze_settings.Settings_Theme)

        self.screen = maze_settings.screen

        self.remove_walls_count = 0
        self.width = 11
        self.height = 11
        self.FlagBool = False

        self.Maze_type = "Collect points"

    def Show_Generator(self):
        self.frame = self.menu.add.frame_v(maze_settings.Width // 2, maze_settings.Height // 2,
                                           background_color=(120, 120, 120),
                                           padding=0,
                                           align=pygame_menu.locals.ALIGN_CENTER)

        self.frame.pack(self.menu.add.text_input('Ширина: ', default=self.width, maxchar=2, input_underline='_',
                                                 input_underline_len=3, input_type=pygame_menu.locals.INPUT_INT,
                                                 onreturn=self.get_width))
        self.frame.pack(self.menu.add.text_input('Высота: ', default=self.height, maxchar=2, input_underline='_',
                                                 input_underline_len=3, input_type=pygame_menu.locals.INPUT_INT,
                                                 onreturn=self.get_height))

        self.frame.pack(self.menu.add.toggle_switch("Добавить флаг", self.FlagBool, self.Get_Flag))

        Text = "Это альфа версия, поэтому вводите значения в пределах нормы\n" \
               "Не ниже 11, не больше 60\n" \
               "при вводе ширины и высоты, нажимайте Enter для подтверждения\n" \
               "Лучше выглядеть будет, если ввести нечетные значения"
        self.frame.pack(self.menu.add.label(Text, font_size=14))

        self.menu.add.button("Создать", self.CreateMaze)

        self.menu.add.button("Назад", Back)

        self.menu.mainloop(self.screen)

    def Get_Flag(self, value):
        self.FlagBool = value
        if value:
            self.Maze_type = "Getting to the point"
        else:
            self.Maze_type = "Collect points"

    def get_width(self, value):
        self.width = value

    def get_height(self, value):
        self.height = value

    def CreateMaze(self):
        if self.width >= 11 and self.height >= 11:
            self.remove_walls_count = max(0, min(self.remove_walls_count, (self.width - 1) * (self.height - 1) // 2 - 1))
            maze, start = generate_maze(self.width, self.height, self.remove_walls_count, self.FlagBool)
            print_maze(maze, "my_maze")
            from OpenGame import Main
            Opg = Main(self.screen)
            Opg.main(maze, self.Maze_type, None)




if __name__ == "__main__":
    GeneratorObj = MazeGeneratorEdit()
    GeneratorObj.Show_Generator()
