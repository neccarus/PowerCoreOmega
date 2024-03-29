from guipyg.utils.utils import Instance
import pygame
from src import ship_sprite_dict
from .controls import Controls


class Player(Instance):

    def __init__(self, name="player",
                 ship=None,
                 controls=Controls(),
                 faction="player"):
        self.name = name
        super().add_instance()  # Add player to instances (Instance)
        self.ship = ship
        if ship:
            self.ship.parent = self

            # Temporary
            self.ship.image = ship_sprite_dict["Python"].convert_alpha(self.ship.image)
            self.ship.rect = self.ship.image.get_rect()
            self.original_image = self.ship.image.copy()
            self.ship.mask = pygame.mask.from_surface(self.ship.image)

            # Temporary
            self.ship.horizontal_max_speed = 500
            self.ship.horizontal_acceleration = 500
            self.ship.vertical_max_speed = 250
            self.ship.vertical_acceleration = 250

        self.score = 0
        self.credits = 0
        self.controls = controls
        self.faction = faction
        self.actions = []
        self.consumables = {
            'heat_sinks': 0,
            'shield_boosters': 0,
            'power_surges': 0,
        }

    def update(self, delta_time, boundary, surface, *_, **__):

        if self.ship:
            self.ship.update(self.actions, delta_time, boundary, surface)

            self.ship.image = pygame.transform.rotate(self.ship.current_image, self.ship.angle)
            self.ship.rect = self.ship.image.get_rect(center=self.ship.rect.center)

    def acquire_ship(self, ship):
        self.ship = ship
        self.ship.parent = self
        self.ship.faction = self.faction

        # Temporary
        self.ship.image = ship_sprite_dict["Cestus"].convert_alpha()
        self.ship.image = pygame.transform.scale(self.ship.image, (64, 64))
        self.ship.image = pygame.transform.rotate(self.ship.image, 270)
        self.ship.rect = self.ship.image.get_rect()
        self.ship.width, self.ship.height = self.ship.rect.width, self.ship.rect.height
        self.ship.original_image = self.ship.image.copy()

        # Temporary
        self.ship.horizontal_max_speed = 500
        self.ship.horizontal_acceleration = 500
        self.ship.vertical_max_speed = 250
        self.ship.vertical_acceleration = 250
        # self.ship.get_mask()

    def kill(self):
        del self.ship
        del self

    def get_events(self, event):
        if event.type == pygame.KEYDOWN:
            self.actions.append(self.controls.get_signal(event))

        if event.type == pygame.KEYUP:
            if self.controls.get_signal(event) in self.actions:
                self.actions.remove(self.controls.get_signal(event))
