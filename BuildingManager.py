import pygame as pg
from Building import Building
from MapManager import MapManager

class BuildingManager:
    def __init__(self, screen, map_manager):
        self.screen = screen
        self.map_manager = map_manager
        self.buildings = []
        self.building_images = [
            pg.image.load("assets/s11.png").convert_alpha(),
            pg.image.load("assets/s22.png").convert_alpha(),
            pg.image.load("assets/s3.png").convert_alpha(),
            pg.image.load("assets/s4.png").convert_alpha(),
            pg.image.load("assets/s5.png").convert_alpha()
        ]
        self.building_data = [
            {"cost": 200, "income": 1.5, "capacity": 5, "attractiveness": 5},
            {"cost": 500, "income": 2.5, "capacity": 10, "attractiveness": 10},
            {"cost": 100, "income": 1, "capacity": 2, "attractiveness": 5},
            {"cost": 300, "income": 1.5, "capacity": 6, "attractiveness": 8},
            {"cost": 700, "income": 2, "capacity": 15, "attractiveness": 12}
        ]
        self.selected_type = None  # Wybrany typ budowli
        self.selected_image = None  # Obraz wybranej budowli (do podglądu)
        self.buttons = []

    def is_position_occupied(self, position, size):
        """Sprawdza, czy podana pozycja koliduje z istniejącymi budowlami."""
        new_rect = pg.Rect(position[0], position[1], size[0], size[1])
        for building in self.buildings:
            building_size = self.building_images[building.type].get_size()
            building_rect = pg.Rect(building.position[0], building.position[1], building_size[0], building_size[1])
            if new_rect.colliderect(building_rect):  # Sprawdź kolizję prostokątów
                return True 
        # Sprawdzanie kolizji z ścianą
        wall_width, _ = self.map_manager.wall.get_size()
        for x in range(0, self.screen.get_width(), wall_width):
            wall_rect = pg.Rect(x, 0, wall_width, self.map_manager.wall.get_height())
            if new_rect.colliderect(wall_rect):
                return True
            
              # Sprawdzanie kolizji z interfejsem
            if position[1] + size[1] > self.screen.get_height() - 100:
                return True
            
            if position[0] + size[0] > self.screen.get_width() or position[0]< 0:
                return True
        return False

    def draw_menu(self):
        """Rysuje menu budowy."""
        for rect, i in self.buttons:
            self.screen.blit(self.building_images[i], rect.topleft)

    def draw_buildings(self):
        """Rysuje wszystkie budowle na ekranie."""
        for building in self.buildings:
            building.draw(self.screen, self.building_images[building.type])

    def draw_preview(self):
        if self.selected_image:
            mouse_pos = pg.mouse.get_pos()
            size = self.selected_image.get_size()
            build_position = (mouse_pos[0] - size[0] // 2, mouse_pos[1] - size[1] // 2)
            
            # Sprawdzenie kolizji
            color = (255, 0, 0) if self.is_position_occupied(build_position, size) else (255, 255, 255)
            
            # Zmiana koloru przy podglądzie
            preview_image = self.selected_image.copy()
            preview_image.fill(color, special_flags=pg.BLEND_RGB_MULT)
            
            self.screen.blit(preview_image, build_position)

    def handle_building_selection(self, event, player, map_manager):
        """Obsługuje wybór budowli i jej umieszczenie."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()

            for rect, building_type in self.buttons:
                if rect.collidepoint(mouse_pos):
                    self.selected_type = building_type
                    self.selected_image = self.building_images[building_type]
                    return

            if self.selected_type is not None:
                building_info = self.building_data[self.selected_type]
                cost = building_info["cost"]
                income = building_info["income"]
                capacity = building_info["capacity"]
                attractiveness = building_info["attractiveness"]
                size = self.building_images[self.selected_type].get_size()
                build_position = (mouse_pos[0] - size[0] // 2, mouse_pos[1] - size[1] // 2)
                if (player.money >= cost and 
                    map_manager.is_valid_build(build_position, size) and 
                    not self.is_position_occupied(build_position, size)):
                    player.spend_money(cost)
                    # Dodaj nowy budynek z wszystkimi atrybutami
                    self.buildings.append(Building(
                        building_type=self.selected_type,
                        position=build_position,
                        cost=cost,
                        income=income,
                        capacity=capacity,
                        attractiveness=attractiveness
                    ))
                    # Dodaj atrakcyjność za nowy budynek
                    player.reputation += attractiveness
                    
                    if player.reputation > 100:
                        player.reputation = 100
                    self.selected_type = None
                    self.selected_image = None

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            self.selected_type = None
            self.selected_image = None

    def calculate_income(self):
        """Oblicza całkowity dochód z wszystkich budynków."""
        total_income = 0
        for building in self.buildings:
            total_income += building.income
        return total_income
    
    def find_closest_building(self, x, y):
        """Znajdź najbliższy budynek do punktu (x, y)."""
        closest_building = None
        closest_building_type = None
        min_distance = float('inf')
        
        for building in self.buildings:
            building_x, building_y = building.position
            distance = ((building_x - x) ** 2 + (building_y - y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_building = building
                closest_building_type = building.type
        
        return closest_building, closest_building_type
    
    def get_building_dimensions(self):
        """Zwraca wymiary wszystkich postawionych budynków."""
        building_dimensions = []
        for building in self.buildings:
            building_image = self.building_images[building.type]
            width, height = building_image.get_size()
            building_dimensions.append({
                "type": building.type,
                "position": building.position,
                "width": width,
                "height": height
            })
        return building_dimensions