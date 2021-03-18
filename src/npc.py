from .controls import Controls
from .ship import Ship
import pygame


class NPC:

    def __init__(self, ship=Ship(pos=(800, 100), weapon_locations=[(-5, 2), (5, 2)]), ai=None):
        self.ship = ship
        self.ship.parent = self
        self.ship.angle = 270
        self.ai = self.AI(ai, self)
        self.enemies = []
        self.actions = []
        self.target = None

        # Temporary
        pygame.draw.polygon(self.ship.image, (255, 0, 0), ((0, 0), (20, 10), (0, 20)))
        self.original_image = self.ship.image.copy()

        # Temporary
        self.ship.horizontal_max_speed = 250
        self.ship.horizontal_acceleration = 125
        self.ship.vertical_max_speed = 250
        self.ship.vertical_acceleration = 25
        self.ship.get_mask()

    def update(self, delta_time, boundary, enemies=None):
        if enemies is None:
            self.enemies = []
        else:
            self.enemies = enemies
        # self.get_events()
        if not self.target:
            self.ai.acquire_target()
        if self.target:
            self.ai.move_to_attack()
            self.ai.attack()
        self.ship.update(self.actions, delta_time, boundary)
        self.actions = []

        # self.ship.update(self.actions, delta_time, boundary)

        self.ship.image = pygame.transform.rotate(self.original_image, self.ship.angle)
        self.ship.rect = self.ship.image.get_rect(center=self.ship.rect.center)

    def kill(self):
        del self.ship
        del self

    # TODO: NPC needs to be separated from game object controllers
    # def get_events(self, *_, **__):
    #     if not self.target:
    #         self.ai.acquire_target()
    #     if self.target:
    #         self.ai.move_to_attack()
    #         self.ai.attack()

    class AI:

        def __init__(self, name="ai", parent=None):
            self.name = name
            self.parent = parent
            self.controls = Controls("forward", "backward", "left", "right", "fire_weapon")

        def acquire_target(self):
            shortest_distance = 0
            target = None

            # TODO rework this code to incorporate "Factions"
            # if self.parent.enemies:
            #     for enemy in self.parent.enemies:
            enemy_ship = self.parent.enemies.ship
            distance = self.parent.ship.pos.distance_to(enemy_ship.pos)
            if shortest_distance == 0 or distance < shortest_distance:
                target = enemy_ship

            self.parent.target = target
            print(self.parent.target.name)

        def move_to_attack(self):
            # TODO: redo calculations
            if self.parent.ship.rect.centerx < self.parent.target.rect.centerx:
                self.parent.actions.append(self.controls.get_signal("right"))
            if self.parent.ship.rect.centerx > self.parent.target.rect.centerx:
                self.parent.actions.append(self.controls.get_signal("left"))

        def attack(self):
            if self.parent.ship.rect.centerx in range(self.parent.target.rect.centerx - 60, self.parent.target.rect.centerx + 60):
                self.parent.actions.append(self.controls.get_signal("fire_weapon"))
