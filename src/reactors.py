from src.equipment import Equipment
from src.utils import clamp


class Reactor(Equipment):

    def __init__(self, recharge_rate=3, power_capacity=100,
                 cooling_rate=4, heat_capacity=50,
                 heat_inefficiency=1, overheat_threshold=0.75, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recharge_rate = recharge_rate
        self.power_capacity = power_capacity
        self.current_power = power_capacity
        self.cooling_rate = cooling_rate
        self.heat_capacity = heat_capacity
        self.heat_inefficiency = heat_inefficiency
        self.overheat_threshold = overheat_threshold
        self.overheating = False
        self.current_heat = 0

    def equip_to_parent(self, parent):
        super().equip_to_parent(parent)

    def update(self, delta_time, *args, **kwargs) -> None:
        if self.current_heat < self.heat_capacity and self.current_power < self.power_capacity:
            power_generated = clamp(self.current_power + (self.recharge_rate * delta_time / 1000),
                                    0, self.power_capacity) - self.current_power
            self.current_heat += power_generated * self.heat_inefficiency
            self.current_power += power_generated

        if self.current_heat >= self.heat_capacity:
            self.overheating = True

        if self.current_heat > 0:
            self.current_heat -= (self.cooling_rate * self.parent.cooling_modifier) * delta_time / 1000
            if self.current_heat < self.heat_capacity * self.overheat_threshold:
                self.overheating = False

        print(f"Current Power {self.current_power}/Power Capacity {self.power_capacity}")
        print(f"Current Heat {self.current_heat}/Heat Capacity {self.heat_capacity}")
        print(f"Overheating: {self.overheating}")
