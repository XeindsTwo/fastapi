from models.pizza import Pizza

class PizzaManager:
    def __init__(self):
        self.pizzas = []

    def get_all(self):
        return self.pizzas