class Player:
    def __init__(self, money, reputation, visitors, day):
        self.money = money
        self.reputation = reputation
        self.visitors = visitors
        self.day = day

    def add_visitor(self):
        """Zwiększa licznik odwiedzających."""
        self.visitors += 1

    def spend_money(self, amount):
        """Odejmuje pieniądze od gracza."""
        self.money -= amount