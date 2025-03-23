import pygame as pg

class MapManager:
    def __init__(self, screen):
        self.screen = screen
        self.floor = pg.image.load("assets/floor.png").convert_alpha()
        self.wall = pg.image.load("assets/wall.png").convert_alpha()
        self.wall_left = pg.image.load("assets/wall_left.png").convert_alpha()
        self.wall_right = pg.image.load("assets/wall_right.png").convert_alpha()
        self.wall_corner = pg.image.load("assets/wall_corner.png").convert_alpha()
        self.grid = set()

    def draw_floor(self):
        floor_width, floor_height = self.floor.get_size()
        for y in range(0, self.screen.get_height(), floor_height):
            for x in range(0, self.screen.get_width(), floor_width):
                self.screen.blit(self.floor, (x, y))

    def draw_walls(self):
        wall_width, _ = self.wall.get_size()
        for x in range(0, self.screen.get_width(), wall_width):
            self.screen.blit(self.wall, (x, 0))

        screen_center_y = (self.screen.get_height() // 2)
        gap_size = 30
        wall_width, wall_height = self.wall_left.get_size()

        for y in range(2, self.screen.get_height(), wall_height):
            self.screen.blit(self.wall_left, (0, y))
            
          # Rysowanie prawej ściany z przerwą
        for y in range(2, self.screen.get_height(), wall_height):
            if not(screen_center_y - gap_size < y < screen_center_y + gap_size):
                self.screen.blit(self.wall_right, (self.screen.get_width() - wall_width, y))

        self.screen.blit(self.wall_corner, (self.screen.get_width() - wall_width, screen_center_y-2*gap_size))

    def is_valid_build(self, position, building_size):
        return position not in self.grid