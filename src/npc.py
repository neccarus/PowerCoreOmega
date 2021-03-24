from .controls import Controls
import pygame


class NPC:

    def __init__(self, ship=None, ai=None):
        self.ship = ship
        if self.ship:
            self.ship.parent = self
            self.ship.angle = 270
        self.ai = ai  # self.AI(ai, self)
        self.enemies = []
        self.actions = []
        self.target = None

    def update(self, delta_time, boundary, surface, enemies=None):
        if enemies is None:
            self.enemies = []
        elif enemies:
            self.enemies = enemies
        if not self.target:
            self.ai.acquire_target()
        if self.target:
            self.ai.move_to_attack()
            self.ai.attack()
        self.ship.update(self.actions, delta_time, boundary, surface)
        self.actions = []

        self.ship.image = pygame.transform.rotate(self.original_image, self.ship.angle)
        self.ship.rect = self.ship.image.get_rect(center=self.ship.rect.center)

    def acquire_ship(self, ship):
        self.ai = self.AI("ai", self)
        self.ship = ship
        self.ship.parent = self

        # Temporary
        pygame.draw.polygon(self.ship.image, (255, 0, 0),
                            ((0, 0), (20, 10), (0, 20)))
        self.original_image = self.ship.image.copy()

        # Temporary
        self.ship.horizontal_max_speed = 450
        self.ship.horizontal_acceleration = 375
        self.ship.vertical_max_speed = 250
        self.ship.vertical_acceleration = 125
        self.ship.angle = 270
        self.ship.get_mask()

    def kill(self):
        del self.ship
        del self

    class AI:

        def __init__(self, name="ai", parent=None):
            self.name = name
            self.parent = parent
            self.controls = Controls("forward", "backward", "left", "right", "fire_weapon")

        #  TODO fix this method
        def acquire_target(self):
            shortest_distance = 0
            target = None

            # TODO rework this code to incorporate "Factions"
            # if self.parent.enemies:
            for enemy in self.parent.enemies:
                distance = self.parent.ship.pos.distance_to(enemy.ship.pos)
                if shortest_distance == 0 or distance < shortest_distance:
                    target = enemy.ship

            self.parent.target = target

        def move_to_attack(self):
            # TODO: redo calculations
            if self.parent.ship.rect.centerx < self.parent.target.rect.centerx:
                self.parent.actions.append(self.controls.get_signal("right"))
            if self.parent.ship.rect.centerx > self.parent.target.rect.centerx:
                self.parent.actions.append(self.controls.get_signal("left"))

        def attack(self):
            if self.parent.ship.rect.centerx in range(self.parent.target.rect.centerx - 60, self.parent.target.rect.centerx + 60):
                self.parent.actions.append(self.controls.get_signal("fire_weapon"))
