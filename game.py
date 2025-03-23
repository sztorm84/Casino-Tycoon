import pygame as pg
from Player import Player
from MapManager import MapManager
from BuildingManager import BuildingManager
from UIManager import UIManager
from Person import Person

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((800, 600), pg.RESIZABLE | pg.SCALED)
        pg.display.set_caption("Casino Tycoon")
        self.clock = pg.time.Clock()
        self.running = True
        self.time = 8 * 60 # Czas w grze (8:00)
        self.last_time_update = pg.time.get_ticks()
        
        # Inicjalizacja komponentów gry
        self.player = Player(money=800, reputation=50, visitors=0, day=1)
        self.map_manager = MapManager(self.screen)
        self.building_manager = BuildingManager(self.screen, self.map_manager)
        self.ui_manager = UIManager(self.screen, self.building_manager)
        self.ui_manager.set_game(self)

        # Pozycja drzwi wejściowych
        self.entry_point = (self.map_manager.screen.get_width(), self.map_manager.screen.get_height() / 2)

        # Inicjalizacja listy odwiedzających
        self.visitors = []  # Lista klientów w grze
        self.last_visitor_spawn = pg.time.get_ticks()  # Ostatni czas pojawienia się klienta

    def start(self):
        while self.running:
            self.update()
            self.render()
            self.clock.tick(60)
            self.update_time()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            self.ui_manager.handle_input(event, self.player, self.map_manager)
            self.ui_manager.handle_event(event)
        # Tworzenie nowych klientów
        self.spawn_visitors()
        
        # Aktualizacja ruchu klientów
        self.update_visitors()

    def render(self):
        self.map_manager.draw_floor()
        self.map_manager.draw_walls()
        self.building_manager.draw_buildings()
        game_time = self.format_time()  # Sformatowany czas
        self.ui_manager.draw_interface(self.player, game_time)  # Przekaż czas do UI
        # Rysowanie podglądu wybranej budowli
        self.building_manager.draw_preview()

        # Rysowanie odwiedzających (ludzików)
        for visitor in self.visitors:
            visitor.draw(self.screen)

        pg.display.flip()

    def update_time(self):
        """Aktualizuje czas w grze co 1 sekundę rzeczywistego czasu."""
        current_ticks = pg.time.get_ticks()
        elapsed_time = current_ticks - self.last_time_update
        
        if elapsed_time >= 1000:
            self.time += 10
            self.last_time_update = current_ticks
            # Oblicz dochód gracza z budynków na podstawie liczby odwiedzających
            total_income = 0
            for building in self.building_manager.buildings:
                total_income += building.earn_income()
            
            self.player.money += total_income
            
            if self.time >= 24 * 60:
                self.time = 0
                self.player.day += 1

    def format_time(self):
        hours = self.time // 60
        minutes = self.time % 60
        return f"{hours:02}:{minutes:02}"
    
    def spawn_visitors(self):
        """Tworzy nowych klientów przy drzwiach wejściowych co pewien czas."""
        current_time = pg.time.get_ticks()
        base_interval = 10000  # Czas dla 50% atrakcyjności
        min_interval = 5000    # Minimalny czas dla 100% atrakcyjności
        max_attractiveness = 100
        attractiveness_factor = max(0, min(self.player.reputation, max_attractiveness)) / max_attractiveness
        spawn_interval = base_interval - (base_interval - min_interval) * attractiveness_factor

        # Sprawdź, czy są wolne miejsca w budynkach
        available_buildings = [building for building in self.building_manager.buildings if building.has_space()]

        if current_time - self.last_visitor_spawn >= spawn_interval and available_buildings:
            self.add_visitor(self.entry_point)  # Dodaj klienta przy drzwiach
            self.last_visitor_spawn = current_time
    
    def add_visitor(self, position):
        """Dodaje nowego odwiedzającego do gry."""
        visitor = Person(position[0], position[1], 30, 30)
        self.visitors.append(visitor)
        self.player.add_visitor()

    def update_visitors(self):
        """Aktualizuje stan wszystkich odwiedzających."""
        for visitor in self.visitors:
            # Jeśli odwiedzający jest w budynku, sprawdź, czy powinien go opuścić
            if not visitor.is_moving and visitor.target_building:
                if visitor.stay_duration == 0:
                    visitor.stay_duration = (pg.time.get_ticks()//1000)+10
                
                # Aktualizuj czas spędzony w budynku
                visitor.update_elapsed_time()
                
                if visitor.elapsed_time >= visitor.stay_duration:
                    # Usunięcie odwiedzającego z budynku i zmiana jego stanu
                    visitor.target_building.remove_visitor_from_building()
                    visitor.reset_elapsed_time() 
                    visitor.leave_building()
            else:
                # Jeśli odwiedzający nie dotarł do budynku, poruszaj się w jego stronę
                visitor.move_to_building(self.building_manager)