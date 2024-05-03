from MazeGenerator import *
from maze_settings import *

from maze import world



def main(screen):
    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    YELLOW = (255, 255, 0)
    

    pygame.display.set_caption("Maze Generator")



    # Переменные для ввода
    width = 11
    height = 11
    remove_walls_count = 0

    # Функция отображения текста
    def draw_text(text, x, y, color=BLACK):
        text_surface = font.render(text, True, YELLOW)
        screen.blit(text_surface, (x, y))

    # Функция отображения стрелок
    def draw_arrows():
        # Стрелки вправо для ширины (желтые)
        pygame.draw.polygon(screen, YELLOW, [(170, 20), (180, 30), (170, 40)])

        # Стрелки влево для ширины (желтые)
        pygame.draw.polygon(screen, YELLOW, [(20, 20), (10, 30), (20, 40)])


        # Стрелки вправо для высоты (желтые)
        pygame.draw.polygon(screen, YELLOW, [(370, 20), (360, 30), (370, 40)])

        # Стрелки влево для высоты (желтые)
        pygame.draw.polygon(screen, YELLOW, [(520, 20), (530, 30), (520, 40)])

    
    # Основной цикл программы
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    # Генерация лабиринта по нажатию Enter
                    remove_walls_count = max(0, min(remove_walls_count, (width - 1) * (height - 1) // 2 - 1))
                    maze, start = generate_maze(width, height, remove_walls_count)
                    print_maze(maze, "my_maze")
                    from OpenGame import Main
                    Opg = Main(screen)
                    Opg.main(maze)
                    #maze_world = world(maze,screen)
                    #maze_world._setup_world()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Обработка нажатия на стрелки
                x, y = event.pos
                if 30 < x < 70 and 20 < y < 80:
                    width = max(5, width - 1)
                elif 160 < x < 200 and 20 < y < 80:
                    width = min(25, width + 1)
                elif 520 < x < 560 and 20 < y < 80:
                    height = max(5, height - 1)
                elif 450 < x < 490 and 20 < y < 80:
                    height = min(25, height + 1)
        
        # Отображение текущих параметров
        draw_text(f"Ширина: {width}", 20, 20)
        draw_text(f"Высота: {height}", 370, 20)
        draw_text("Press Enter to generate maze", 20, 100, GRAY)

        # Отображение стрелок
        draw_arrows()

        pygame.display.flip()

    # Завершение программы
    pygame.quit()
