from src.equipment import Equipment
import pygame


class Shield(Equipment):

    def __init__(self, health=10, regen=1, broken_recharge_time=5, recharge_power_ratio=1, color=(0, 0, 255, 200), *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.health = health
        self.current_health = health
        self.regen = regen
        self.consumable_regen = 0
        self.broken_recharge_time = broken_recharge_time
        self.recharge_power_ratio = recharge_power_ratio
        self.color = color
        self.current_recharge = 0
        self.recharging = True
        self.mask = None
        self.angle = 0
        self.original_image = None

    def update(self, delta_time, surface):

        if self.current_health <= 0 and self.current_recharge < self.broken_recharge_time:
            self.recharging = False
            self.current_health = 0
            self.current_recharge += delta_time / 1000
            if self.current_recharge >= self.broken_recharge_time:
                self.recharging = True
                self.current_recharge = 0

        if self.current_health < self.health and self.recharging and self.parent.reactor.current_power > 0:
            health_regenerated = self.regen * delta_time / 1000
            if health_regenerated * self.recharge_power_ratio > self.parent.reactor.current_power / self.recharge_power_ratio:
                health_regenerated = self.parent.reactor.current_power / self.recharge_power_ratio
            self.current_health += health_regenerated
            self.current_health += self.consumable_regen * delta_time / 1000
            self.parent.reactor.current_power -= health_regenerated * self.recharge_power_ratio
        if self.current_health > self.health:
            self.current_health = self.health

        if self.parent.reactor.overheating:
            self.recharging = False

        elif not self.parent.reactor.overheating:
            self.recharging = True

    def equip_to_parent(self, parent):
        self.parent = parent
        self.mask = pygame.mask.from_surface(self.parent.image).outline()
