from src.equipment import Equipment
from src.projectile import Projectile
import pygame
from random import uniform


class Weapon(Equipment):

    def __init__(self, damage=0, speed=800, fire_rate=0.1,
                 spread=0, projectiles=1, projectile_grouping=0,
                 projectile_color=(0, 255, 0), projectile_size=(5,),
                 offset=pygame.Vector2(0, 0), power_use=0,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage = damage
        self.speed = speed
        self.fire_rate = fire_rate
        self.cool_down = self.fire_rate * 1000
        self.current_cool_down = 0
        self.spread = spread
        self.projectiles = projectiles
        self.projectile_grouping = projectile_grouping
        self.projectile_color = projectile_color
        self.projectile_size = projectile_size
        # self.parent = parent
        self.offset = offset
        self.power_use = power_use
        self.angle = 0
        # self.pos = pygame.Vector2(0, 0)
        self.firing = False

    def equip_to_parent(self, parent, slot):

        super().equip_to_parent(parent)
        self.offset = parent.weapons[slot].pos
        self.rotate()

    def fire(self):

        projectiles = []

        if self.firing and self.current_cool_down == 0 and self.parent.reactor.current_power >= self.power_use\
                and not self.parent.reactor.overheating:
            self.current_cool_down = self.cool_down
            self.parent.reactor.current_power -= self.power_use
            self.firing = False
            for projectile in range(self.projectiles):
                projectile = Projectile(size=self.projectile_size,
                                        pos=self.pos + pygame.Vector2(uniform(-self.projectile_grouping,
                                                                              self.projectile_grouping),
                                                                      uniform(-self.projectile_grouping,
                                                                              self.projectile_grouping)),
                                        health=0,
                                        speed=self.speed,
                                        damage=self.damage,
                                        color=self.projectile_color,
                                        parent=self.parent,
                                        direction=pygame.Vector2(1, 0).rotate
                                        (-self.parent.angle +
                                         uniform(-self.spread, self.spread)))
                projectiles.append(projectile)

        return projectiles

    def update(self, delta_time):
        if self.current_cool_down > 0:
            self.current_cool_down -= delta_time
        if self.current_cool_down < 0:
            self.current_cool_down = 0
        self.rotate()

    def rotate(self):
        offset_rotated = self.offset.rotate(self.angle)
        self.pos = self.parent.pos + offset_rotated
