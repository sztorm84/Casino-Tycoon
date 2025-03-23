import random

class Building:
    def __init__(self, building_type, position, cost, income, capacity, attractiveness):
        self.type = building_type               # Typ budynku
        self.position = position                # Pozycja na mapie
        self.cost = cost                        # Koszt budowy
        self.income = income                    # zysk generowany przez budynek
        self.capacity = capacity                # Liczba miejsc dla graczy
        self.attractiveness = attractiveness    # Atrakcyjność budynku
        self.visitors = 0                       # Liczba odwiedzających
        self.WIN_REWARD = 50                    # Stała wartość nagrody
        self.WIN_CHANCE = 0.02                  # Szansa 2% na wygraną dla każdego klienta

    def earn_income(self):
        """Generuj dochód, jeśli jest przynajmniej jeden odwiedzający."""
        if self.visitors > 0:
            if random.random() < self.WIN_CHANCE:
                return -self.WIN_REWARD
            else:
                return self.income * self.visitors
        return 0

    def draw(self, screen, image):
        """Rysowanie budynku na ekranie."""
        screen.blit(image, self.position)

    def get_cost(self):
        return self.cost

    def get_position(self):
        return self.position

    def get_capacity(self):
        return self.capacity
    
    def add_visitor_to_building(self):
        """Dodaje odwiedzającego do budynku, jeśli jest miejsce."""
        if self.visitors < self.capacity:
            self.visitors += 1
            return True
        return False
    
    def remove_visitor_from_building(self):
        """Usuwa odwiedzającego z budynku."""
        if self.visitors > 0:
            self.visitors -= 1
            return True
        return False
    
    def has_space(self):
        """Sprawdza, czy budynek ma wolne miejsce."""
        return self.visitors < self.capacity