import pygame as pg
import random

class Person:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pg.image.load("assets/character.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.is_moving = True  # Flaga określająca, czy ludzik się porusza
        self.target_position = None  # Punkt docelowy (losowy punkt na krawędzi budynku)
        self.target_building = None  # Budynek, do którego zmierza
        self.stay_duration = 0  # Czas pobytu w budynku (w sekundach)
        self.arrival_time = 0  # Czas przybycia do budynku
        self.time_spent = 0  # Czas spędzony w budynku
        self.elapsed_time = 0  # Czas, który upłynął od ostatniego ruchu

    def move_towards(self, target_x, target_y, speed=2, tolerance=5):
        dx = target_x - self.x
        dy = target_y - self.y

        distance = (dx**2 + dy**2) ** 0.5
        if distance <= tolerance:
            self.is_moving = False
            return

        # Normalizacja wektora kierunku
        if distance != 0:
            dx /= distance
            dy /= distance

        # Aktualizacja pozycji
        self.x += dx * speed
        self.y += dy * speed

    def move_to_building(self, building_manager):
        """Znajdź najbliższy budynek i idź w jego stronę."""
        if not self.target_building:
            # Pobierz listę budynków
            buildings = building_manager.buildings
            building_images = building_manager.building_images
            
            # Filtruj budynki z wolnymi miejscami
            available_buildings = [building for building in buildings if building.has_space()]
            
            # Jeśli brak budynków z wolnymi miejscami, zakończ
            if not available_buildings:
                self.target_position = None
                self.is_moving = False
                return
            
            # Znajdź najbliższy budynek spośród dostępnych
            closest_building = None
            closest_distance = float('inf')
            
            for building in available_buildings:
                building_x, building_y = building.get_position()
                
                building_image = building_images[building.type]
                building_width, building_height = building_image.get_size()
                
                distance = ((self.x - building_x) ** 2 + (self.y - building_y) ** 2) ** 0.5
                
                if distance < closest_distance:
                    closest_distance = distance
                    closest_building = building
            
            # Jeżeli znaleziono najbliższy budynek, oblicz losowy punkt na jego obwodzie
            if closest_building:
                if not self.target_position:
                    self.target_building = closest_building 
                    building_x, building_y = closest_building.get_position()
                    building_image = building_images[closest_building.type]
                    building_width, building_height = building_image.get_size()
                    
                    # Losujemy krawędź (0: górna, 1: dolna, 2: lewa, 3: prawa)
                    edge = random.randint(0, 3)
                    
                    if closest_building.add_visitor_to_building():
                        character_center_x = self.width // 2
                        character_center_y = self.height // 2

                        if edge == 0:  # Górna krawędź
                            target_x = random.randint(building_x, building_x + building_width) - character_center_x
                            target_y = building_y - character_center_y
                        elif edge == 1:  # Dolna krawędź
                            target_x = random.randint(building_x, building_x + building_width) - character_center_x
                            target_y = building_y + building_height - character_center_y
                        elif edge == 2:  # Lewa krawędź
                            target_x = building_x - character_center_x
                            target_y = random.randint(building_y, building_y + building_height) - character_center_y
                        else:  # Prawa krawędź
                            target_x = building_x + building_width - character_center_x
                            target_y = random.randint(building_y, building_y + building_height) - character_center_y

                        self.target_position = (target_x, target_y)  # Ustawiamy punkt docelowy na losowej krawędzi budynku

        # Poruszaj się w kierunku pozycji budynku
        if self.target_position:
            self.move_towards(self.target_position[0], self.target_position[1])

        # Sprawdź, czy ludzik dotarł do budynku
        if self.is_at_building(building_manager):
            self.is_moving = False
            self.target_position = None

    def is_at_building(self, building_manager):
        """Sprawdza, czy ludzik dotarł do budynku."""
        if self.target_building:
            building_x, building_y = self.target_building.position
            # Uzyskaj wymiary budynku za pomocą tablicy obrazów w BuildingManager
            building_image = building_manager.building_images[self.target_building.type]
            building_width, building_height = building_image.get_size()

            tolerance = max(building_width, building_height) // 4
            if (abs(self.x - building_x) < tolerance) and (abs(self.y - building_y - building_height) < tolerance):
                return True
        return False


    def draw(self, screen):
        """Rysowanie ludzika na ekranie."""
        screen.blit(self.image, (self.x, self.y))

    def move_to_next_available_spot(self, building_manager):
        """Znajdź kolejny dostępny budynek i idź w jego stronę."""
        if not self.is_moving:  # Jeśli nie porusza się, znajdź nowy budynek
            self.is_moving = True
            # Znajdź najbliższy dostępny budynek
            self.target_building = building_manager.find_closest_building(self.x, self.y)
            if self.target_building:
                # Ustaw cel na pozycję budynku (środek budynku)
                building_x, building_y = self.target_building.position
                self.target_position = (building_x, building_y)

        # Poruszaj się w kierunku pozycji budynku
        if self.target_position:
            self.move_towards(self.target_position[0], self.target_position[1])

    def leave_building(self):
        """Po upływie czasu ludzik opuszcza budynek."""
        if self.target_building:  # Sprawdź, czy ludzik jest przypisany do budynku
            self.target_building.remove_visitor_from_building()
        self.target_position = None
        self.target_building = None
        self.is_moving = True
        self.stay_duration = 0  # Resetuj czas pobytu
        self.time_spent = 0  # Resetuj czas spędzony w budynku
        self.target_position = (800, 300)

        self.move_towards(self.target_position[0], self.target_position[1])

    def update_elapsed_time(self):
        current_time = pg.time.get_ticks()
        self.elapsed_time = (current_time - self.arrival_time) // 1000  # W sekundach

    def reset_elapsed_time(self):
        self.arrival_time = 0
        self.elapsed_time = 0