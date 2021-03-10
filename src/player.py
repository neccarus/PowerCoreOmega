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

        self.ship.update(self.actions, delta_time, boundary)

        self.ship.image = pygame.transform.rotate(self.original_image, self.ship.angle)
        self.ship.rect = self.ship.image.get_rect(center=self.ship.rect.center)

    def get_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.actions.append(self.controls.get_signal(event))

        if event.type == pygame.KEYUP:
            if self.controls.get_signal(event) in self.actions:
                self.actions.remove(self.controls.get_signal(event))
