from .ship import Ship
from guipyg.utils.utils import Instance
import pygame
from .controls import Controls
import math


class Player(Instance):

    def __init__(self, name="player",
                 ship=None,
                 controls=Controls()):
        self.name = name
        super().add_instance()  # Add player to instances (Instance)
        self.ship = ship
        if ship:
            self.ship.parent = self

            # Temporary
            pygame.draw.polygon(self.ship.image, pygame.Color('dodgerblue'),
                                ((0, 0), (20, 10), (0, 20)))
            self.original_image = self.ship.image.copy()
            self.ship.mask = pygame.mask.from_surface(self.ship.image)

            # Temporary
            self.ship.horizontal_max_speed = 500
            self.ship.horizontal_acceleration = 500
            self.ship.vertical_max_speed = 250
            self.ship.vertical_acceleration = 250
            # self.ship.get_mask()

        self.score = 0
        self.credits = 0
        self.controls = controls
        self.actions = []

    def update(self, delta_time, boundary, surface, *_, **__):

        if self.ship:
            self.ship.update(self.actions, delta_time, boundary, surface)

            self.ship.image = pygame.transform.rotate(self.original_image, self.ship.angle)
            self.ship.rect = self.ship.image.get_rect(center=self.ship.rect.center)

    def acquire_ship(self, ship):
        self.ship = ship
        self.ship.parent = self

        # Temporary
        pygame.draw.polygon(self.ship.image, pygame.Color('dodgerblue'),
                            ((0, 0), (20, 10), (0, 20)))
        self.original_image = self.ship.image.copy()

        # Temporary
        self.ship.horizontal_max_speed = 500
        self.ship.horizontal_acceleration = 225
        self.ship.vertical_max_speed = 250
        self.ship.vertical_acceleration = 125
        self.ship.get_mask()

    def kill(self):
        del self.ship
        del self

    def get_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.actions.append(self.controls.get_signal(event))

        if event.type == pygame.KEYUP:
            if self.controls.get_signal(event) in self.actions:
                self.actions.remove(self.controls.get_signal(event))
