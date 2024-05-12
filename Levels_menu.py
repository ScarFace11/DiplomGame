from maze_settings import *
from AllMazes import *
import pygame_menu


def Maze_Generator():
    from MazeRandomGenerateEdit import MazeGeneratorEdit
    GeneartorObj = MazeGeneratorEdit()
    return GeneartorObj.Show_Generator()

def Back():
    from MainMenu import StartMenu
    return StartMenu()

class Levels:
    def __init__(self):
        self.MazeName = None
        self.frame = None
        self.menu = pygame_menu.Menu("Выбор уровня", maze_settings.Width, maze_settings.Height,
                                     theme=maze_settings.Settings_Theme)
        self.screen = maze_settings.screen
        self.Maze_Mode = "Collect points"
        self.Difficulty = "Нормальный"

    def Show_levels(self):
        Level_type = [("Стандартный лабиринт", "Standard_maze_list"),
                      ("Поиск флага", "Search_Flag_Maze_List"),
                      ("Головоломки", "Puzzle_maze_List")]

        Difficulty = [("Нормальный", "Difficulty_Normal"),
                      ("Сложный", "Difficulty_Hard")]
        self.menu.add.selector(title="Тип уровня", items=Level_type,
                               default=0, selector_id="Level_type",
                               onchange=self.Switch_type_Maze)

        self.menu.add.selector(title="Уровень сложности", items=Difficulty,
                               default=maze_settings.Levels_Difficulty_Index_Settings, selector_id="Level_difficulty",
                               onchange=self.Difficulty_change)

        self.frame = self.menu.add.frame_h(maze_settings.Width, maze_settings.Height - 550,
                                           background_color=(50, 50, 50),
                                           padding=0,
                                           max_width=maze_settings.Width,
                                           max_height=maze_settings.Height - 550)
        self.create_frame_selector_levels(Mazes_List.get("Standard_maze_list"))

        self.menu.add.button("Создать случайный лабиринт", Maze_Generator)

        self.menu.add.button("Назад", Back)

        self.menu.mainloop(self.screen)

    def create_frame_selector_levels(self, maze_type):

        for i in range(len(maze_type)):
            self.frame.pack(
                self.menu.add.button(i + 1,
                                     padding=(40, 40),
                                     button_id=f'b{i}',
                                     action=lambda x=i + 1: self.Pick_Maze(x, maze_type),
                                     font_size=60,
                                     border_color=(70, 120, 70),
                                     border_width=10,
                                     align=pygame_menu.locals.ALIGN_CENTER)
            )
        self.MazeName = len(maze_type)

    def Switch_type_Maze(self, _, size):
        if self.menu.get_widget("b0"):
            for i in range(self.MazeName):
                self.menu.remove_widget(f"b{i}")

        self.create_frame_selector_levels(Mazes_List.get(size))
        self.Maze_Mode = Mazes_mode_List.get(size)

    def Pick_Maze(self, key, maze_type):
        from OpenGame import Main
        from copy import deepcopy

        time = None

        OpG = Main(maze_settings.screen)
        if self.Difficulty == "Сложный" and self.Maze_Mode == "Collect points":
            time = Standard_maze_Timer.get(key)

        MazeMask = deepcopy(maze_type.get(key))
        OpG.main(MazeMask, self.Maze_Mode, time)


    def Difficulty_change(self, value, _):
        self.Difficulty = value[0][0]
        maze_settings.Levels_Difficulty_Index_Settings = value[1]


if __name__ == "__main__":
    LevelsObj = Levels()
    LevelsObj.Show_levels()
