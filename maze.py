from random import randint

import pygame.time

from maze_settings import *
from player import Player
from Tile import *
from Enemy import *
from trap import Spike, Laser
from game import Game
from Music import *
from pygame.sprite import spritecollideany
from Pathfinder import Pathfinder, PathfinderEnemy

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)


class CreateWorld:
    def __init__(self, world_data, screen, Maze_mode, time):

        self.timer_font = pygame.font.SysFont("Calibri", 38)
        self.start_time = pygame.time.get_ticks()
        self.start_left_time = pygame.time.get_ticks()
        self.time_ms = 0, 0
        self.timer_surf = self.timer_font.render(f'{self.time_ms[0]}:{self.time_ms[1]:02d}', True, (255, 255, 255))

        self.timer_left = None
        self.Enemy_current_time_spawn = None
        if time:
            self.timer_left = time
            self.timer_left_minutes = self.timer_left // 60
            self.timer_left_seconds = self.timer_left % 60
            self.timer_left_font = pygame.font.SysFont("Calibri", 38, True, True)
            self.timer_left_surf = self.timer_left_font.render(
                f'{self.timer_left_minutes}:{self.timer_left_seconds:02d}', True,
                (248, 0, 0))

        self.screen = screen
        self.Maze_mode = Maze_mode
        self.world_data = world_data
        self._setup_world()

        self.current_time = 0
        if self.player:
            self.pathPlayer = Pathfinder(self.world_data, self.player)
            if self.WandererEnemy:
                self.pathWanderer = PathfinderEnemy(self.world_data, self.WandererEnemy, self.player)

        self.game = Game(self.screen)

        self.death = False
        self.score_all = False
        self.finished = False
        self.pause_flag = False
        self.Player_Invincibility = False
        self.Timer_Respawn_Start = False
        self.Player_Press_Button = False
        self.Player_death_and_not_Press_button = False

        self.player_face = 'right'

        self.Timer_Respawn = 0
        self.Timer_Menu_Pause = 0
        self.Timer_Press_Button = 0

        self.take_money = 0

        self.Music = GameMusic()
        self.Music.Background()

        # GameMusic.Background()
        # pygame.mouse.set_visible(False)

    # Генерация уровня
    def _setup_world(self):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.way = pygame.sprite.Group()
        self.WandererEnemy = pygame.sprite.Group()

        self.finish_flag = pygame.sprite.Group()
        self.SpikeTraps = pygame.sprite.Group()
        self.LaserTraps = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()
        self.score = pygame.sprite.Group()

        self.all_sprite = CameraGroup()

        self.Wanderer_Red_coord = []
        self.Wanderer_Blue_coord = []
        self.Wanderer_Pink_coord = []
        self.Player_coord = []

        self.Enemy_current_time_spawn = 0

        # Генерация монеток
        money_flag = True
        total_money = 5
        if total_money != 0 and money_flag:

            coins = [(randint(1, len(self.world_data[0]) - 1), randint(1, len(self.world_data) - 1))
                     for _ in range(total_money)]
            for coin in coins:

                random_x, random_y = coin
                while self.world_data[random_y][random_x] != 0:
                    random_x, random_y = (randint(1, len(self.world_data[0]) - 1),
                                          randint(1, len(self.world_data) - 1))
                self.world_data[random_y][random_x] = 5

        # Распределение очков
        score_flag = True
        if score_flag:
            score_positions = [(i, j) for i in range(len(self.world_data) - 1)
                               for j in range(len(self.world_data[i]) - 1)
                               if self.world_data[i][j] == 0]

            for pos in score_positions:
                self.world_data[pos[0]][pos[1]] = 6
            self.Score_spawn = len(score_positions)

        for i, row in enumerate(self.world_data):
            for j, value in enumerate(row):
                x, y = j * maze_settings.Tile_size, i * maze_settings.Tile_size

                way_sprite = Way((x, y), maze_settings.Tile_size)
                self.way.add(way_sprite)
                self.all_sprite.add(way_sprite)

                if value == 2:
                    self.player_start_cord_x, self.player_start_cord_y = x, y
                    self.Player_coord += [[x, y]]
                elif value == 1:
                    tile = Wall((x, y), maze_settings.Tile_size)
                    self.tiles.add(tile)
                    self.all_sprite.add(tile)
                elif value == 31:
                    self.Wanderer_Red_coord += [[x, y]]
                elif value == 32:
                    self.Wanderer_Blue_coord += [[x, y]]
                elif value == 33:
                    self.Wanderer_Pink_coord += [[x, y]]
                elif value == 41:
                    self.SpikeTrap = Spike((x, y), maze_settings.Tile_size)
                    self.SpikeTraps.add(self.SpikeTrap)
                    self.all_sprite.add(self.SpikeTrap)
                elif value == 42:
                    self.LaserTrap = Laser((x, y), maze_settings.Tile_size)
                    self.LaserTraps.add(self.LaserTrap)
                    self.all_sprite.add(self.LaserTrap)
                elif value == 5:
                    goal = Goal((x, y), maze_settings.Tile_size)
                    self.goal.add(goal)
                    self.all_sprite.add(goal)
                elif value == 6:
                    score_sprite = Score((x, y), maze_settings.Tile_size)
                    self.score.add(score_sprite)
                    self.all_sprite.add(score_sprite)

                elif value == 10:
                    finish_sprite = Icons((x, y), maze_settings.Tile_size)
                    self.finish_flag.add(finish_sprite)
                    self.all_sprite.add(finish_sprite)

        if self.Wanderer_Red_coord:
            for x, y in self.Wanderer_Red_coord:
                WandersSprite = Wanderer_Red((x, y), maze_settings.Tile_size)
                self.WandererEnemy.add(WandersSprite)
                self.all_sprite.add(WandersSprite)
                self.Enemy_current_time_spawn = pygame.time.get_ticks()
        if self.Wanderer_Blue_coord:
            for x, y in self.Wanderer_Blue_coord:
                WandersSprite = Wanderer_Blue((x, y), maze_settings.Tile_size)
                self.WandererEnemy.add(WandersSprite)
                self.all_sprite.add(WandersSprite)
                self.Enemy_current_time_spawn = pygame.time.get_ticks()
        if self.Wanderer_Pink_coord:
            for x, y in self.Wanderer_Pink_coord:
                WandersSprite = Wanderer_Pink((x, y), maze_settings.Tile_size)
                self.WandererEnemy.add(WandersSprite)
                self.all_sprite.add(WandersSprite)
                self.Enemy_current_time_spawn = pygame.time.get_ticks()
        if self.Player_coord:
            for x, y in self.Player_coord:
                player_sprite = Player((x, y))
                self.player.add(player_sprite)
                self.all_sprite.add(player_sprite)

    # Обработка столкновений
    def _handle_collision(self):
        # Получаем список всех спрайтов в группе self.player
        player_sprites = self.player.sprites()

        # Проверяем коллизии для каждого спрайта игрока
        for player in player_sprites:
            collided_goal = spritecollideany(player, self.goal)
            if collided_goal is not None:
                collided_goal.kill()
                self.take_money += 1


                # Инициализируем collided_score заранее
            collided_score = None
            if self.score:
                collided_score = spritecollideany(player, self.score)

            if collided_score is not None:
                collided_score.kill()
                self.Score_spawn -= 1
                if self.Maze_mode == "Collect points" and self.Score_spawn == 0:
                    self.score_all = True

            collide_finish_flag = None
            if self.Maze_mode == "Getting to the point" and self.finish_flag:
                collide_finish_flag = spritecollideany(player, self.finish_flag)
            if collide_finish_flag is not None:
                self.finished = True
            if not self.Player_Invincibility:
                for Spike_Trap in self.SpikeTraps.sprites():
                    if spritecollideany(player,
                                        self.SpikeTraps) and Spike_Trap.status == 'activated':
                        player.rect.x = self.player_start_cord_x
                        player.rect.y = self.player_start_cord_y
                        player.life -= 1
                        self.death = True

                for LaserTrap in self.LaserTraps.sprites():
                    if spritecollideany(player,
                                        self.LaserTraps) and LaserTrap.status == 'activated':
                        player.rect.x = self.player_start_cord_x
                        player.rect.y = self.player_start_cord_y
                        player.life -= 1
                        self.death = True
                for _ in self.WandererEnemy.sprites():
                    if spritecollideany(player, self.WandererEnemy):
                        player.rect.x = self.player_start_cord_x
                        player.rect.y = self.player_start_cord_y
                        player.life -= 1
                        self.death = True

    def Invincibility_After_Respawn(self):
        if self.Player_Press_Button:
            if self.Player_death_and_not_Press_button:
                self.Timer_Respawn_Start = True
                self.Timer_Respawn = pygame.time.get_ticks()
                self.Player_death_and_not_Press_button = False

            if self.Timer_Respawn_Start and self.current_time - self.Timer_Respawn <= 5000:
                self.Player_Invincibility = True

            elif self.Timer_Respawn_Start and self.current_time - self.Timer_Menu_Pause == 0:
                self.Player_Invincibility = True

            else:
                self.Player_Invincibility = False
                self.Timer_Respawn_Start = False
        else:
            self.Player_Invincibility = True

    # придумать уровни с головоломками
    # возможно сделать слои на карте
    # сделать магазин со скинами за монеты
    # мб сделать бесконечный режим, где надо просто очки лутать (игра будет на рекорд)
    # сделать просто больше уровней

    # Горизонтальное и вертикальное передвижение персонажа
    def _horizontal_movement_collision(self):
        # Итерируем по всем спрайтам игрока в группе
        for player in self.player.sprites():
            player.rect.x += player.direction.x * player.speed
            collided = False

            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    collided = True

                    if player.direction.x < 0:  # Движение влево
                        player.rect.left = sprite.rect.right
                        player.direction.x = 0
                        self.current_x = player.rect.left
                    elif player.direction.x > 0:  # Движение вправо
                        player.rect.right = sprite.rect.left
                        player.direction.x = 0
                        self.current_x = player.rect.right

            # Если нет столкновений, определяем направление игрока
            if not collided:
                for sprite in self.tiles.sprites():
                    if player.rect.left != sprite.rect.right and player.direction.x < 0:
                        self.player_face = 'left'
                        break  # Прерываем цикл, если направление найдено
                    elif player.rect.right != sprite.rect.left and player.direction.x > 0:
                        self.player_face = 'right'
                        break  # Прерываем цикл, если направление найдено

    # prevents player to pass through objects vertically
    def _vertical_movement_collision(self):
        for player in self.player.sprites():
            player.rect.y += player.direction.y * player.speed

            collided = False

            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    collided = True

                    if player.direction.y > 0:  # Движение вниз
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                    elif player.direction.y < 0:  # Движение вверх
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0
                        player.on_ceiling = True

            # Если нет столкновений, определяем направление игрока
            if not collided:
                for sprite in self.tiles.sprites():
                    if player.rect.bottom <= sprite.rect.top and player.direction.y > 0:
                        self.player_face = 'down'
                        break  # Прерываем цикл, если направление найдено
                    elif player.rect.top >= sprite.rect.bottom and player.direction.y < 0:
                        self.player_face = 'up'
                        break  # Прерываем цикл, если направление найдено

    # Обработка события паузы
    def set_Pause_Flag(self, value):
        self.pause_flag = value
        if value:
            # Если группа не пуста, то получаем первый спрайт из группы
            player = self.player.sprites()[0] if self.player else None
            if player:
                player.speed = 0

        else:
            # Если группа не пуста, то получаем первый спрайт из группы
            player = self.player.sprites()[0] if self.player else None
            if player:
                player.speed = maze_settings.Tile_size / 10.0

    # Отрисовка меню паузы
    def GamePause(self, screen):

        Continue_color = Color_Yellow
        Back_color = Color_Yellow

        s = pygame.Surface((maze_settings.Width // 2 - 140, maze_settings.Height // 2 - 120), pygame.SRCALPHA)
        pygame.draw.rect(s, (128, 128, 128, 128), (0, 0, 300, 200), 0, 34)
        screen.blit(s, (maze_settings.Width // 2 - 140, maze_settings.Height // 2 - 120))

        pygame.draw.rect(screen, (255, 255, 30),
                         (maze_settings.Width // 2 - 140, maze_settings.Height // 2 - 120, 300, 200), 5, 34)

        Continue_text = font.render("Продолжить", True, Continue_color)
        Continue_rect = Continue_text.get_rect(center=(maze_settings.Width // 2, maze_settings.Height // 2 - 80))
        screen.blit(Continue_text, Continue_rect)

        Back_text = font.render("Выйти", True, Back_color)
        Back_rect = Back_text.get_rect(center=(maze_settings.Width // 2, maze_settings.Height // 2))
        screen.blit(Back_text, Back_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if mouse_click[0]:  # Проверка левой кнопки мыши (нажата ли она)
            if Continue_rect.collidepoint(mouse_pos):
                self.set_Pause_Flag(False)

            elif Back_rect.collidepoint(mouse_pos):
                GameMusicAndSounds.MusicOff()
                from Levels_menu import Levels
                Levels_obj = Levels()
                return Levels_obj.Show_levels()

        Continue_collide = Continue_rect.collidepoint(mouse_pos)
        Back_collide = Back_rect.collidepoint(mouse_pos)

        Continue_color = Color_Purple if Continue_collide else Color_Yellow
        Back_color = Color_Purple if Back_collide else Color_Yellow

        # Redraw with updated colors
        pygame.draw.rect(screen, (255, 255, 30),
                         (maze_settings.Width // 2 - 140, maze_settings.Height // 2 - 120, 300, 200), 5, 34)

        Continue_text = font.render("Продолжить", True, Continue_color)
        screen.blit(Continue_text, Continue_rect)

        Back_text = font.render("Выйти", True, Back_color)
        screen.blit(Back_text, Back_rect)

    # Создать путь для игрока
    def Player_Create_path(self, screen, world_event):
        player = self.player.sprites()[0]
        camera_offset = pygame.math.Vector2(player.rect.centerx - maze_settings.Width / 2,
                                            player.rect.centery - maze_settings.Height / 2)
        self.pathPlayer.update(screen, camera_offset, world_event)

    # Создать путь для противника
    def Enemy_Create_Path(self, screen):
        player = self.player.sprites()[0]
        camera_offset = pygame.math.Vector2(player.rect.centerx - maze_settings.Width / 2,
                                            player.rect.centery - maze_settings.Height / 2)

        self.pathWanderer.Enemy_update(screen, camera_offset)

    def Print_Timer(self):
        if self.Player_Press_Button:
            self.time_ms = self.current_time - self.start_time
            new_hms = (self.time_ms // (1000 * 60)) % 60, (self.time_ms // 1000) % 60
            if new_hms != self.time_ms:
                self.time_ms = new_hms
                self.timer_surf = self.timer_font.render(f'{self.time_ms[0]}:{self.time_ms[1]:02d}', True,
                                                         (255, 255, 255))
        self.screen.blit(self.timer_surf, (maze_settings.Width // 2 - 50, maze_settings.Height - 50))

        if self.timer_left:
            if self.Player_Press_Button:
                while self.timer_left > 0 and self.current_time - self.start_left_time > 1000 and not self.pause_flag:
                    self.timer_left -= 1
                    self.timer_left_minutes = self.timer_left // 60
                    self.timer_left_seconds = self.timer_left % 60
                    self.timer_left_surf = self.timer_left_font.render(
                        f'{self.timer_left_minutes}:{self.timer_left_seconds:02d}',
                        True, (248, 0, 0))
                    self.start_left_time = self.current_time
            self.screen.blit(self.timer_left_surf, (maze_settings.Width // 2 - self.timer_left_surf.get_width() // 2,
                                                    self.timer_left_surf.get_width() - self.timer_left_surf.get_width() // 2))

    # Обновление игры со всеми изменениями
    def update(self, screen, player_event, world_event):
        self.SpikeTraps.update()
        self.LaserTraps.update()
        self.all_sprite.custom_draw(self.player, self.world_data)
        if self.player:
            self.current_time = pygame.time.get_ticks()

            # for draw tile
            # self.draw_tile()

            # for trap
            # if (self.trap_visible):
            # self.traps.remove(self.trap)
            # self.traps.draw(screen)

            # for collision
            self._handle_collision()

            self.Invincibility_After_Respawn()
            self.Player_Create_path(screen, world_event)
            self.player.update(player_event, self.player_face)

            # Enemy
            if self.WandererEnemy:
                if self.Player_Press_Button:
                    self.Enemy_Create_Path(screen)
                    self.WandererEnemy.update()
                    if self.current_time - self.Enemy_current_time_spawn > 800:
                        self.pathWanderer.create_Enemy_path()
                        self.Enemy_current_time_spawn = self.current_time

                    for sprite in self.WandererEnemy.sprites():
                        if sprite.name == 'Pink_Wanderer' and not sprite.path:
                            self.pathWanderer.create_Pink_Wanderer_path(self.world_data)
            self._horizontal_movement_collision()
            self._vertical_movement_collision()

            # отображение хп и проверка конца игры
            self.game.show_life(self.player)
            self.game.game_state(self.player.sprites()[0], self.score_all, self.finished, self.time_ms, self.timer_left, self.take_money, world_event)
            if not self.score_all and not self.finished and self.player.sprites()[0].life != 0 and self.timer_left != 0:
                self.Print_Timer()

        if world_event == "RightMouseDown":
            if self.player.sprites()[0].empty_path:
                self.player.sprites()[0].empty_path()

        if self.pause_flag:
            self.Timer_Menu_Pause = pygame.time.get_ticks()
            self.GamePause(screen)

        clock.tick(fps)

        text_fps = font.render(str(int(clock.get_fps())), True, (255, 255, 255))
        screen.blit(text_fps, (10, 100))


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.offset_rect = None

    def custom_draw(self, player_group, world_data):
        if player_group:
            player = player_group.sprites()[0]
            self.offset.x = player.rect.centerx - maze_settings.Width / 2
            self.offset.y = player.rect.centery - maze_settings.Height / 2
            MazeSettings.Camera_Offset = self.offset
        else:
            self.offset.x = maze_settings.Width / 2 - ((len(world_data[0]) - 1) * maze_settings.Tile_size)
            self.offset.y = maze_settings.Height / 2 - ((len(world_data) - 1) * maze_settings.Tile_size)

        for sprite in self:
            self.offset_rect = sprite.rect.copy()
            self.offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, self.offset_rect)
