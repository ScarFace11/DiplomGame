# Генерация на сайте https://keesiemeijer.github.io/maze-generator/#generate
# Wall thickness: 2
# Maze entries: none
# Bias: none, но пожеланию можно сделать горизонтальный или вертикальный
# Remove maze walls: 300


"""
from PIL import Image
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
"""


def GetMazeFromParcing():
    #Нерабочая версия № 2
    """
    # Инициализация веб-драйвера
    driver = webdriver.Chrome()  # Укажите путь к драйверу вашего браузера

    # URL страницы с генератором лабиринтов
    url = "https://keesiemeijer.github.io/maze-generator/#generate"

    # Открытие страницы в браузере
    driver.get(url)

    # Нахождение и ввод значений в соответствующие элементы
    wall_thickness_input = driver.find_element_by_id('wall-size')
    wall_thickness_input.clear()
    wall_thickness_input.send_keys('2')

    columns_input = driver.find_element_by_id('width')
    columns_input.clear()
    columns_input.send_keys('8')

    rows_input = driver.find_element_by_id('height')
    rows_input.clear()
    rows_input.send_keys('8')

    # Выбор нужной опции в select
    entry_select = driver.find_element_by_id('entry')
    entry_select.find_elements_by_tag_name('option')[1].click()  # Выбор второй опции

    remove_walls_input = driver.find_element_by_id('remove_walls')
    remove_walls_input.clear()
    remove_walls_input.send_keys('300')

    # Нажатие кнопки генерации лабиринта
    generate_button = driver.find_element_by_id('generate')
    generate_button.click()

    # Пауза для завершения генерации (может потребоваться подождать, чтобы лабиринт полностью сгенерировался)
    time.sleep(5)

    # Закрытие браузера
    driver.quit()
    """
    # Нерабочая версия № 1
    """
    Value_Wall_thickness = 2
    Value_Columns = 8
    Value_Rows = 8
    Value_Remove_maze_walls = 300
    url = "https://keesiemeijer.github.io/maze-generator/#generate"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        form_data = {}


        input_Wall_thickness = soup.find('input', {'id': 'wall-size'})
        input_Wall_thickness['value'] = Value_Wall_thickness
        form_data['wall-size'] = input_Wall_thickness

        input_Columns = soup.find('input', {'id': 'width'})
        input_Columns['value'] = Value_Columns
        form_data['width'] = input_Columns

        input_Rows = soup.find('input', {'id': 'height'})
        input_Rows['value'] = Value_Rows
        form_data['height'] = Value_Rows

        input_Maze_entries = soup.find('select', {'id': 'entry'})
        # Находим все опции внутри select
        options = input_Maze_entries.find_all('option')
        
        # Проходим по опциям и выбираем нужную
        for option in options:
            option.attrs.pop('selected', None)
            if option.get('value') == "":
                option['selected'] = 'selected'

        input_Remove_maze_walls = soup.find('input', {'id': 'remove_walls'})
        input_Remove_maze_walls['value'] = Value_Remove_maze_walls
        form_data['remove_walls'] = Value_Remove_maze_walls
        response_post = requests.post(url, data=form_data)
        if response_post.status_code == 200:
            print("Данные успешно отправлены!")
        else:
            print("Ошибка при отправке данных:", response_post.status_code)
    else:
        print("Произошла ошибка:", response.status_code)
    """


#GetMazeFromParcing()


import random


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def is_valid_wall(maze, y, x):
    return maze[y][x] == 1 and maze[y - 1][x] == 1 and maze[y + 1][x] == 1


def remove_walls(maze, remove_walls_count):
    if not remove_walls_count or not maze:
        return maze

    min_val = 1
    max_val = len(maze) - 1
    max_tries = remove_walls_count
    walls_removed = 0
    tries = 0

    while tries < max_tries and walls_removed < remove_walls_count:
        tries += 1

        # Get random row from matrix
        y = random.randint(min_val, max_val - 1)

        walls = [i for i in range(1, len(maze[y]) - 1) if is_valid_wall(maze, y, i)]
        random.shuffle(walls)

        for wall in walls:
            if maze[y][wall] == 1:
                maze[y][wall] = 0
                walls_removed += 1
                break

    return maze


def generate_maze(width, height, remove_walls_count, StateFlag):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def recursive_backtracking(x, y):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                maze[ny][nx] = 0
                recursive_backtracking(nx, ny)

    start_x, start_y = random.randrange(1, width - 1, 2), random.randrange(1, height - 1, 2)
    maze[start_y][start_x] = 0
    recursive_backtracking(start_x, start_y)

    remove_walls(maze, remove_walls_count)

    # Place the digit 2 at a random location where the value is 0
    empty_cells = [(y, x) for y in range(height) for x in range(width) if maze[y][x] == 0]
    if empty_cells:
        y, x = random.choice(empty_cells)
        maze[y][x] = 2
    if empty_cells and StateFlag:
        y, x = random.choice(empty_cells)
        maze[y][x] = 10
    """
    for i in range(40):
        empty_cells = [(y, x) for y in range(height) for x in range(width) if maze[y][x] == 0]
        if empty_cells:
            y, x = random.choice(empty_cells)
            maze[y][x] = 41
    """
    return maze, (start_x, start_y)


def print_maze(maze, maze_name):
    print(f"{maze_name} = [")
    for row in maze:
        print(f"{row},")
    print(']')


def main():
    width, height = 11, 11  # задайте нужные размеры лабиринта
    maze_name = "my_maze"

    remove_walls_count = 0
    remove_walls_count = max(0, min(remove_walls_count, (width - 1) * (
            height - 1) // 2 - 1))  # Убеждаемся, что значение находится в диапазоне от 0 до максимального возможного числа

    maze, start = generate_maze(width, height, remove_walls_count)
    print_maze(maze, maze_name)

#main()
