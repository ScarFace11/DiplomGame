"""
import pygame
from maze import world
from maze_settings import *
pygame.init()
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("My PAC-MAN Game")

font = pygame.font.Font(None, 50)


class Menu:

    def __init__(self,punkts = [0,0,"Punkt",(255,255,255),(255,255,255),0]): # x,y,name,color1,color2,id
        self.punkts =punkts
        self.screen = screen
        
    def render(self,poverhnost,font,num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                text = font.render(i[2], True, i[4])
                text_rect = text.get_rect(center = (i[0], i[1]))
                #poverhnost.blit(font.render(i[2], True, i[4]), text_rect)
                poverhnost.blit(text, text_rect)
            else:
                text = font.render(i[2], True, i[3])
                text_rect = text.get_rect(center = (i[0], i[1]))
                poverhnost.blit(text, text_rect)
    
    def menu(self, player_event):
       
        World = world(maze, self.screen)
        done = True
        pygame.key.set_repeat(0,0)
        pygame.mouse.set_visible(True)
        font_menu = font
        punkt = 0
        while done:

            screen.fill((0,0,0))
            Name_text = font.render("Pac Man", True, (255, 255, 255))
            Name_rect = Name_text.get_rect(center=(Width // 2, Height // 5))
            screen.blit(Name_text, Name_rect)

            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0]>i[0]-800 and mp[0]<i[0]+800 and mp[1]>i[1]-25 and mp[1]<i[1]+20:
                    punkt =  i[5]
            self.render(screen, font_menu,punkt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if event.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or  (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    if punkt == 0:    
                        done = False

                        World.update(player_event) 


                    elif punkt == 3:
                        sys.exit()
         
            pygame.display.flip()
    def Open_Game_Menu(self):
        Game = Menu(punkts)
        Game.menu()
    


punkts = [
        (Width // 2,Height // 2- 150,"Play",(250,250,30),(250,30,250),0),      #(550,300, u"Play",(250,250,30),(250,30,250),0)
        (Width // 2,Height // 2+ 90,'Exit',(250,250,30),(250,30,250),3),      #(550,510, u'Exit',(250,250,30),(250,30,250),2)
        ]


#op = Menu(punkts)
#op.menu(player_event=)
#Open_Game_Menu()
"""
import pygame
import sys
from maze_settings import *


pygame.display.set_caption("Дипломная игра (Главное меню)")

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []

        self.BLACK = (0, 0, 0)
        self.font = pygame.font.Font(None, 36)

        self.selected_button_index = 0  # Начинаем с выбора первой кнопки
        self.create_buttons()

        self.play_game = False  # Флаг для перехода в игровой процесс
        self.dim_color = (0, 0, 0, 150)  # RGBA: четвёртый компонент - прозрачность
    def create_buttons(self):
        self.buttons = []

        self.add_button('Играть')
        self.add_button('Настройки')
        self.add_button('Выход')

    def add_button(self, text):
        text_render = self.font.render(text, True, Color_Yellow)
        text_rect = text_render.get_rect()
        text_rect.center = (self.screen.get_width() // 2, len(self.buttons) * 100 + 175) 

        button = Button(text, (self.screen.get_width() - text_rect.width) // 2, len(self.buttons) * 50 + text_rect.y , text_rect.width, text_rect.height)
        self.buttons.append(button)

    def draw_text(self, text, color, x, y):
        text_obj = self.font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_obj, text_rect)
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                for i, button in enumerate(self.buttons):
                    if button.is_hovered(event.pos):
                        self.selected_button_index = i
                        break

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(pos):
                        self.perform_button_action(button)
                        break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    for button in self.buttons:
                        if button.is_hovered(pygame.mouse.get_pos()):
                            self.perform_button_action(button)
                            break

                if event.key == pygame.K_DOWN:
                    self.move_down()
                elif event.key == pygame.K_UP:
                    self.move_up()


    def perform_button_action(self, button):
        
        if button.text == 'Играть':
            self.play_game = True  # Устанавливаем флаг для перехода в игру
            from Levels import show_level_menu
            show_level_menu()
        elif button.text == 'Настройки':
            from MazeRandomGenerateEdit import main
            main(self.screen)
        elif button.text == 'Выход':
            pygame.quit()
            sys.exit()

    def move_down(self):
        for i in range(len(self.buttons)):
            if self.buttons[i].hovered:
                if i < len(self.buttons) - 1:
                    self.buttons[i].hovered = False
                    self.buttons[i + 1].hovered = True
                    break

    def move_up(self):
        for i in range(len(self.buttons)):
            if self.buttons[i].hovered:
                if i > 0:
                    self.buttons[i].hovered = False
                    self.buttons[i - 1].hovered = True
                    break

    def run_menu(self):
        while not self.play_game:
            self.handle_events()

            #self.screen.fill(self.BLACK)  # Очистка экрана
            
            self.screen.blit(maze_settings.background_image, (0, 0))  # Отображение фона
            # Отображение затемнённого фона
            dim_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            dim_surface.fill(self.dim_color)
            dim_surface.set_alpha(self.dim_color[3])
            self.screen.blit(dim_surface, (0, 0))
            
            # Отрисовка кнопок меню
            for i, button in enumerate(self.buttons):
                if i == self.selected_button_index:
                    button.draw(self.screen, self.font, Color_Purple, Color_Yellow, self.BLACK)
                else:
                    button.draw(self.screen, self.font, Color_Yellow, Color_Purple, self.BLACK)

            pygame.display.update()

class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hovered = False
        self.centerWidth = 0#Width // 2
        self.centerHeight = (maze_settings.Height - self.height) // 2 #Height // 2 - 300

    def draw(self, surface, font, color, hover_color, bg_color):
        current_color = hover_color if self.hovered else color
        pygame.draw.rect(surface, bg_color, (self.x, self.y, self.width, self.height))
        self.draw_text(self.text, font, current_color, surface, self.x, self.y)


    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    def is_hovered(self, pos):
        text_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return text_rect.collidepoint(pos)