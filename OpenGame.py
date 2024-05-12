from sys import exit

from maze_settings import *
from maze import CreateWorld
from Music import *


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player_event = False
        self.World_event = None
        self.pause_active = False  # Флаг для отслеживания активности режима паузы

        # self.maze = None

    def main(self, mazenum, Maze_mode, time):
        World = CreateWorld(mazenum, self.screen, Maze_mode, time)  # ---------
        while True:
            self.screen.fill((35, 45, 60))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.World_event = "LeftMouseDown"
                        self.player_event = "Automation"
                    elif event.button == 3:
                        self.World_event = "RightMouseDown"
                    World.Player_Press_Button = True
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.World_event = "ESCDown"
                        if World.player:
                            if not World.pause_flag and (not World.score_all and World.player.sprites()[0].life > 0):  # Проверяем, нужно ли выходить из GamePause
                                World.set_Pause_Flag(True)
                                self.pause_active = True  # Устанавливаем флаг активности режима паузы
                            else:
                                World.set_Pause_Flag(False)
                                self.pause_active = False
                        else:
                            if self.pause_active:
                                World.set_Pause_Flag(False)
                                self.pause_active = False
                            else:
                                World.set_Pause_Flag(True)
                                self.pause_active = True
                    elif event.key == pygame.K_SPACE:
                        self.player_event = "stop"
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player_event = 'left'
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player_event = 'right'
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player_event = 'down'
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player_event = 'up'
                    elif event.key == pygame.K_r:
                        if not maze_settings.Visibility_Enemy_Path:
                            maze_settings.Visibility_Enemy_Path = True
                        else:
                            maze_settings.Visibility_Enemy_Path = False

                    World.Player_Press_Button = True

                # elif event.type == pygame.KEYUP:
                # self.player_event = 'stop'
            if World.death:
                World.Player_death_and_not_Press_button = True
                World.Player_Press_Button = False
                self.player_event = "stop"

                World.death = False

                if World.WandererEnemy:
                    World.pathWanderer.empty_path()
            if World.pause_flag or World.finished or World.score_all:
                World.Player_Press_Button = False

            World.update(self.screen, self.player_event, self.World_event)  # --------
            self.World_event = None

            if not World.pause_flag:
                self.pause_active = False
            pygame.display.update()
            self.clock.tick(fps)


if __name__ == "__main__":
    OpenGameObj = Main(maze_settings.screen)
    OpenGameObj.main(maze_settings.FastMazeStart, "Collect points", None)
