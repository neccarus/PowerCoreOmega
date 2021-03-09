from .ship import Ship
from guipyg.utils.utils import Instance
import pygame
from .controls import Controls
import math


class Player(Instance):

    def __init__(self, name="player", ship=Ship(pos=(800, 800)), controls=Controls()):
        self.name = name
        super().add_instance()  # Add player to instances (Instance)
        self.ship = ship
        self.score = 0
        self.credits = 0
        self.controls = controls
        self.actions = []

        # Temporary
        pygame.draw.polygon(self.ship.image, pygame.Color('dodgerblue'), ((0, 0), (20, 10), (0, 20)))
        self.original_image = self.ship.image.copy()

        # Temporary
        self.ship.horizontal_max_speed = 50
        self.ship.horizontal_acceleration = 5
        self.ship.vertical_max_speed = 25
        self.ship.vertical_acceleration = 2.5

    def update(self, delta_time, boundary):

        # Temporary
        for action in self.actions:

            if action == "left":
                self.ship.direction[0] = -1
                if self.ship.horizontal_speed > -self.ship.horizontal_max_speed:
                    self.ship.horizontal_speed += (self.ship.horizontal_acceleration * delta_time / 100) * self.ship.direction[0]

            if action == "right":
                self.ship.direction[0] = 1
                if self.ship.horizontal_speed < self.ship.horizontal_max_speed:
                    self.ship.horizontal_speed += (self.ship.horizontal_acceleration * delta_time / 100) * self.ship.direction[0]

            if action == "forward":
                self.ship.direction[1] = -1
                if self.ship.vertical_speed > -self.ship.vertical_max_speed:
                    self.ship.vertical_speed += (self.ship.vertical_acceleration * delta_time / 100) * self.ship.direction[1]

            if action == "backward":
                self.ship.direction[1] = 1
                if self.ship.vertical_speed < self.ship.vertical_max_speed:
                    self.ship.vertical_speed += (self.ship.vertical_acceleration * delta_time / 100) * self.ship.direction[1]

        if "left" not in self.actions and "right" not in self.actions:

            if self.ship.horizontal_speed > 0:
                self.ship.horizontal_speed -= (self.ship.horizontal_acceleration * delta_time / 100)
            elif self.ship.horizontal_speed < 0:
                self.ship.horizontal_speed += (self.ship.horizontal_acceleration * delta_time / 100)
            if math.isclose(self.ship.horizontal_speed, 0, abs_tol=0.1):
                self.ship.horizontal_speed = 0

        if "forward" not in self.actions and "backward" not in self.actions:

            if self.ship.vertical_speed > 0:
                self.ship.vertical_speed -= (self.ship.vertical_acceleration * delta_time / 100)
            elif self.ship.vertical_speed < 0:
                self.ship.vertical_speed += (self.ship.vertical_acceleration * delta_time / 100)
            if math.isclose(self.ship.vertical_speed, 0, abs_tol=0.1):
                self.ship.vertical_speed = 0

        self.ship.pos += pygame.Vector2((delta_time * self.ship.horizontal_speed) / 100, (delta_time * self.ship.vertical_speed) / 100)
        self.ship.rect.center = self.ship.pos
        if self.ship.rect.left < 0:
            self.ship.rect.left = 0
        elif self.ship.rect.right > boundary.right:
            self.ship.rect.right = boundary.right
        if self.ship.rect.top < 0:
            self.ship.rect.top = 0
        elif self.ship.rect.bottom > boundary.bottom:
            self.ship.rect.bottom = boundary.bottom

        self.ship.image = pygame.transform.rotate(self.original_image, self.ship.angle)
        self.ship.rect = self.ship.image.get_rect(center=self.ship.rect.center)

    def get_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.actions.append(self.controls.get_signal(event))

        if event.type == pygame.KEYUP:
            if self.controls.get_signal(event) in self.actions:
                self.actions.remove(self.controls.get_signal(event))
