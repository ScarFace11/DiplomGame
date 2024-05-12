from Music import *

pygame.font.init()


def ReturnToLevelSelect(world_event):
    if world_event == "ESCDown":
        from Levels_menu import Levels
        Levels_obj = Levels()
        return Levels_obj.Show_levels()


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 70)
        self.fontTime = pygame.font.SysFont("impact", 60)
        self.fontExit = pygame.font.SysFont("impact", 40)
        self.message_color = pygame.Color("darkorange")
        self.game_music = False
        self.GameSound = GameSound()
        self.Timer_Get = False
        self.timer = pygame.time.get_ticks()
        self.Get_Money = False

    def show_life(self, player_group):

        life_size = 40
        img_path = "Sprite/life/heart.png"
        life_image = pygame.image.load(img_path)
        life_image = pygame.transform.scale(life_image, (life_size, life_size))
        for player in player_group.sprites():
            for index in range(player.life):
                indent = index * life_size
                self.screen.blit(life_image, (indent, life_size))

    # когда хп = 0
    def _game_lose(self, player, time, world_event):
        if not self.Timer_Get:
            self.timer = time
            self.Timer_Get = True

        if not self.game_music:
            self.GameSound.Finish()
            self.game_music = True
        player.game_over = True
        message = self.font.render('You Lose...', True, self.message_color)
        messageTime = self.fontTime.render(f'Время игры: {self.timer[0]}:{self.timer[1]}', True, self.message_color)
        messageExit = self.fontExit.render('Press Esc to exit', True, self.message_color)
        self.screen.blit(message, (maze_settings.Width // 2 - message.get_width() // 2, maze_settings.Height // 3 + 70))
        self.screen.blit(messageTime,
                         (maze_settings.Width // 2 - messageTime.get_width() // 2, maze_settings.Height // 3 + 140))
        self.screen.blit(messageExit,
                         (maze_settings.Width // 2 - messageExit.get_width() // 2, maze_settings.Height // 3 + 210))
        ReturnToLevelSelect(world_event)

    # когда игрок взял все бонусы
    def _game_win(self, player, time, take_money, world_event):
        if not self.Timer_Get:
            self.timer = time
            self.Timer_Get = True
        if not self.game_music:
            self.GameSound.Finish()
            self.game_music = True
        if not self.Get_Money:
            maze_settings.Shop_Money += take_money
            self.Get_Money = True

        player.game_over = True
        player.win = True
        message = self.font.render('You Win!!', True, self.message_color)
        messageTime = self.fontTime.render(f'Время игры: {self.timer[0]}:{self.timer[1]}', True, self.message_color)
        messageExit = self.fontExit.render('Press Esc to exit', True, self.message_color)

        self.screen.blit(message, (maze_settings.Width // 2 - message.get_width() // 2, maze_settings.Height // 3 + 70))
        self.screen.blit(messageTime,
                         (maze_settings.Width // 2 - messageTime.get_width() // 2, maze_settings.Height // 3 + 140))
        self.screen.blit(messageExit,
                         (maze_settings.Width // 2 - messageExit.get_width() // 2, maze_settings.Height // 3 + 210))
        ReturnToLevelSelect(world_event)

    # проверка победил ли игрок или проиграл
    def game_state(self, player, goal, finished, time, time_left, take_money, world_event):
        if player.life <= 0 or time_left == 0:
            self._game_lose(player, time, world_event)

        elif goal or finished:
            self._game_win(player, time, take_money, world_event)
