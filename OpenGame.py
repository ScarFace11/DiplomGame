from sys import exit

import pygame

from maze_settings import *
from maze import world
from Music import *


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player_event = False
        self.pause_active = False  # Флаг для отслеживания активности режима паузы

        # self.maze = None

    def main(self, mazenum):
        World = world(mazenum, self.screen)  # ---------

        while True:
            self.screen.fill((35, 45, 60))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not World.pause_flag and (not World.score_all and World.player.sprites()[0].life > 0):  # Проверяем, нужно ли выходить из GamePause
                            World.set_Pause_Flag(True)
                            self.pause_active = True  # Устанавливаем флаг активности режима паузы
                        else:
                            World.set_Pause_Flag(False)
                            self.pause_active = False
                    elif self.pause_active:
                        pass
                    elif event.key == pygame.K_SPACE:
                        self.player_event = 'stop'
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player_event = 'left'
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player_event = 'right'
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player_event = 'down'
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player_event = 'up'
                    elif event.key == pygame.K_r:
                        self.player_event = 'restart'

                # elif event.type == pygame.KEYUP:
                # self.player_event = 'stop'
            if World.death:
                self.player_event = 'stop'
                World.death = False

            World.update(self.screen, self.player_event)  # --------

            if not World.pause_flag:
                self.pause_active = False
            pygame.display.update()
            self.clock.tick(fps)
