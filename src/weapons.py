from src.equipment import Equipment
from src.projectile import Projectile
import pygame
from random import uniform


class Weapon(Equipment):

    def __init__(self, damage=0, speed=800, fire_rate=0.1,
                 spread=0, projectiles=1, projectile_grouping=0, projectile_color=(0, 255, 0), parent=None,
            offset=pygame.Vector2(0, 0),
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
        self.parent = parent
        self.offset = offset
        self.angle = self.parent.angle - 90
        self.pos = self.parent.pos
        self.firing = False
        self.rotate()

    def fire(self):
        if self.firing and self.current_cool_down == 0:
            self.current_cool_down = self.cool_down
            self.firing = False
            projectiles = []
            for projectile in range(self.projectiles):
                projectile = Projectile(size=(5,),
                                        pos=self.pos + pygame.Vector2(uniform(-self.projectile_grouping,
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
            # return Projectile(size=(5,),
            #                   pos=self.pos,
            #                   health=0,
            #                   speed=self.speed,
            #                   direction=pygame.Vector2(1, 0).rotate
            #                   (-self.parent.angle +
            #                    uniform(-self.spread, self.spread)))

    def update(self, delta_time):
        if self.current_cool_down > 0:
            self.current_cool_down -= delta_time
        if self.current_cool_down < 0:
            self.current_cool_down = 0
        self.rotate()

    def rotate(self):
        offset_rotated = self.offset.rotate(self.angle)
        self.pos = self.parent.pos + offset_rotated
