import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from maze_settings import maze_settings


class Pathfinder:
    def __init__(self, matrix, player):
        self.camera_offset = None
        self.screen = None
        self.matrix = matrix
        self.inverted_matrix = [[1 if val in maze_settings.MazeStructure else 0 for val in row] for row in
                                matrix]  # 0 становится путём, а 1 препятствием
        self.grid = Grid(matrix=self.inverted_matrix)
        self.select_surf = pygame.image.load('Sprite/Select_cursor/Select.png').convert_alpha()
        self.select_surf = pygame.transform.scale(self.select_surf,
                                                  (maze_settings.Tile_size, maze_settings.Tile_size))
        self.path = []

        self.player = player


    def draw_active_cell(self, screen, camera_offset):
        self.camera_offset = camera_offset
        self.screen = screen
        mouse_pos = pygame.mouse.get_pos()
        real_mouse_pos_x = mouse_pos[0] + int(self.camera_offset[0])
        real_mouse_pos_y = mouse_pos[1] + int(self.camera_offset[1])
        col = real_mouse_pos_x // maze_settings.Tile_size
        row = real_mouse_pos_y // maze_settings.Tile_size

        # Проверяем, что индексы находятся в пределах размеров матрицы
        if 0 <= row < len(self.matrix) and 0 <= col < len(self.matrix[0]):
            current_cell_value = self.matrix[row][col]
            if current_cell_value != 1:
                rect = pygame.Rect((col * maze_settings.Tile_size - int(self.camera_offset[0]),
                                    row * maze_settings.Tile_size - int(self.camera_offset[1])),
                                   (maze_settings.Tile_size, maze_settings.Tile_size))
                screen.blit(self.select_surf, rect)

    def create_path(self):

        start_x, start_y = self.player.sprites()[0].get_coord()
        start = self.grid.node(start_x, start_y)

        mouse_pos = pygame.mouse.get_pos()
        real_mouse_pos_x = mouse_pos[0] + int(self.camera_offset[0])
        real_mouse_pos_y = mouse_pos[1] + int(self.camera_offset[1])
        end_x = real_mouse_pos_x // maze_settings.Tile_size
        end_y = real_mouse_pos_y // maze_settings.Tile_size
        end = self.grid.node(end_x, end_y)

        finder = AStarFinder()
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        # print("Координаты точек пути:", [(node.x, node.y) for node in self.path])
        self.player.sprites()[0].set_path(self.path)

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = point.x * maze_settings.Tile_size - int(self.camera_offset[0]) + (maze_settings.Tile_size // 2)
                y = point.y * maze_settings.Tile_size - int(self.camera_offset[1]) + (maze_settings.Tile_size // 2)
                points.append((x, y))
                if len(points) >= 2:
                    pygame.draw.circle(self.screen, "#4a4a4a", (x, y), 2)

            if len(points) >= 2:
                pygame.draw.lines(self.screen, '#4a4a4a', False, points, 5)

    def empty_path(self):
        self.path = []

    def update(self, screen, camera_offset):
        self.draw_active_cell(screen, camera_offset)
        self.draw_path()


""""
matrix = [
    [1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,1,0,1],
    [1,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1],
]
inverted_matrix = [[1 if val == 0 else 0 for val in row] for row in matrix]

grid = Grid(matrix=inverted_matrix)

start = grid.node(1,1)
end = grid.node(7,1)
finder = AStarFinder()

path,runs = finder.find_path(start,end,grid)
#print(path)
print(*map(lambda GridNode: (GridNode.x, GridNode.y), path))
print("Координаты точек пути:", [(node.x, node.y) for node in path])
"""
