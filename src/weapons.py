from src.equipment import Equipment


class Weapon(Equipment):

    def __init__(self, damage=0, fire_rate=0, spread=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage
        self.fire_rate = fire_rate
        self.spread = spread
