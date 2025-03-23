import pygame as pg

class UIManager:
    def __init__(self, screen, building_manager):
        self.screen = screen
        self.interface_height = 100
        self.building_manager = building_manager
        self.create_buttons()
        self.create_simulation_buttons()
        self.game = None

    def set_game(self, game):
        """Ustawia instancję gry."""
        self.game = game

    def draw_interface(self, player, game_time):
        # Rysowanie dolnego interfejsu
        pg.draw.rect(self.screen, (50, 50, 50), (0, self.screen.get_height() - self.interface_height, 
                                                self.screen.get_width(), self.interface_height))

        # Statystyki do wyświetlenia
        stats_font = pg.font.Font(None, 15)
        stats_texts = [
            f"Dochody: {player.money} $",
            f"Reputacja: {player.reputation}%",
            f"Odwiedzający: {player.visitors}",
            f"Dzień: {player.day}",
            f"Godzina: {game_time}"
        ]

        # Ustawienia pozycji ramki i jej wymiarów
        frame_width = 120
        frame_height = 100
        frame_x = 0
        frame_y = self.screen.get_height() - frame_height

        # Rysowanie złotej ramki
        pg.draw.rect(self.screen, (212, 175, 55), (frame_x, frame_y, frame_width, frame_height))

        # Rysowanie tła wewnątrz ramki
        pg.draw.rect(self.screen, (30, 30, 30), (frame_x + 3, frame_y + 3, frame_width - 6, frame_height - 6))

        # Renderowanie statystyk w ramce
        margin = 10
        for i, text in enumerate(stats_texts):
            rendered_text = stats_font.render(text, True, (255, 255, 255))
            self.screen.blit(rendered_text, (frame_x + margin, frame_y + margin + i * 18))

        # Rysowanie menu budowy
        self.building_manager.draw_menu()

        # Rysowanie przycisków symulacji
        # self.draw_simulation_buttons()


    def handle_input(self, event, player, map_manager):
        self.building_manager.handle_building_selection(event, player, map_manager)

    def create_buttons(self):
        """Tworzy przyciski budowy na podstawie obrazów."""
        button_spacing = 20
        stats_width = 120
        stats_margin = 10
        
        # Wyśrodkowanie przycisków na szerokości ekranu
        x_pos = stats_width + stats_margin + 10
        y_pos = self.screen.get_height() - self.interface_height + 10
        
        for i, image in enumerate(self.building_manager.building_images):
            button_rect = pg.Rect(
                x_pos,
                y_pos,
                image.get_width(),
                image.get_height()
            )
            self.building_manager.buttons.append((button_rect, i))  # Dodanie przycisku do listy w BuildingManager
            x_pos += image.get_width() + button_spacing

    def create_simulation_buttons(self):
        """Tworzy przyciski do startu i pauzy symulacji."""
        button_spacing = 20
        button_width = 100
        button_height = 50

        x_pos = self.screen.get_width() - button_width - button_spacing
        y_pos = self.screen.get_height() - self.interface_height+25

        # Przycisk startu
        self.start_button = pg.Rect(
            x_pos,
            y_pos,
            button_width,
            button_height
        )

        # Przycisk pauzy
        self.pause_button = pg.Rect(
            x_pos - button_width - button_spacing,
            y_pos,
            button_width,
            button_height
        )

    def handle_event(self, event):
        """Obsługuje zdarzenia interfejsu użytkownika."""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # Obsługa przycisków symulacji
            if self.start_button.collidepoint(mouse_pos):
                self.start_simulation()
            elif self.pause_button.collidepoint(mouse_pos):
                self.pause_simulation()

            # Obsługa przycisków budowy
            for button_rect, action in self.building_manager.buttons:
                if button_rect.collidepoint(mouse_pos):
                    self.building_manager.selected_type = action
                    self.building_manager.selected_image = self.building_manager.building_images[action]