from .ship import Ship
from guipyg.utils.utils import Instance
import pygame
from .controls import Controls


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

    def update(self):

        # self.get_events(event)

        # Temporary
        for action in self.actions:
            if action == "left":
                self.ship.speed = - 5

            if action == "right":
                self.ship.speed = 5

        if not self.actions:
            self.ship.speed = 0

        self.ship.direction = pygame.Vector2(1, 0).rotate(-self.ship.angle)
        self.ship.rect.centerx += self.ship.speed
        self.ship.image = pygame.transform.rotate(self.original_image, self.ship.angle)
        self.ship.rect = self.ship.image.get_rect(center=self.ship.rect.center)

    def get_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.actions.append(self.controls.get_signal(event))

        if event.type == pygame.KEYUP:
            if self.controls.get_signal(event) in self.actions:
                self.actions.remove(self.controls.get_signal(event))
