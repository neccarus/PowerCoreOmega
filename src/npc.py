from .controls import Controls
import pygame
from guipyg.gui_element.graph_elements import BarElement
from guipyg.gui import GUI


class NPC:

    def __init__(self, ship=None, ai=None):
        self.ship = ship
        if self.ship:
            self.ship.parent = self
            self.ship.angle = 270
        self.ai = ai
        self.enemies = []
        self.actions = []
        self.target = None
        self.display_ui = None
        self.health_bar = None
        self.shield_bar = None

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
        # self.ship.mask = pygame.mask.from_surface(self.ship.image)
        self.ship.rect = self.ship.image.get_rect(center=self.ship.rect.center)
        self.set_display_ui_pos()
        self.health_bar.current_value = self.ship.current_health
        self.shield_bar.current_value = self.ship.shield.current_health
        self.display_ui.update(surface, need_update=True)

    def acquire_ship(self, ship):
        self.ai = self.AI("ai", self)
        self.ship = ship
        self.ship.parent = self

        # Temporary
        pygame.draw.polygon(self.ship.image, (255, 0, 0),
                            ((0, 0), (20, 10), (0, 20)))
        self.original_image = self.ship.image.copy()
        self.ship.mask = pygame.mask.from_surface(self.ship.image)

        # Temporary
        self.ship.horizontal_max_speed = 450
        self.ship.horizontal_acceleration = 375
        self.ship.vertical_max_speed = 250
        self.ship.vertical_acceleration = 125
        self.ship.angle = 270
        self.ship.get_mask()
        self.setup_ship_ui()

    def set_display_ui_pos(self):
        self.display_ui.pos_x, self.display_ui.pos_y = self.ship.pos[0] - self.ship.width, \
                                                       self.ship.pos[1] - (self.ship.height + 10)

    def setup_ship_ui(self):
        self.display_ui = GUI(pos_x=self.ship.pos[0] - self.ship.width,
                              pos_y=self.ship.pos[1] - (self.ship.height + 10),
                              width=self.ship.width * 2, height=10)
        self.health_bar = BarElement(low_value=0, high_value=self.ship.health,
                                     current_value=self.ship.current_health,
                                     pos_y=0, pos_x=0, color=(0, 255, 0),
                                     low_position=(0, 0), high_position=(self.ship.width * 2, 0),
                                     width=self.ship.width*2, height=5, related_object=self.ship)
        self.display_ui.elements.append(self.health_bar)

    def equip_shield(self, *args, **kwargs):

        self.ship.equip_shield(*args, **kwargs)
        self.shield_bar = BarElement(low_value=0, high_value=self.ship.shield.health,
                                     current_value=self.ship.shield.current_health,
                                     pos_y=5, pos_x=0, color=(0, 0, 255),
                                     low_position=(0, 5), high_position=(self.ship.width * 2, 5),
                                     width=self.ship.width*2, height=5, related_object=self.ship)
        self.display_ui.elements.append(self.shield_bar)

    def kill(self):
        del self.ship.shield
        self.ship.dot_effects = []
        del self.ship
        del self

    class AI:

        def __init__(self, name="ai", parent=None):
            self.name = name
            self.parent = parent
            self.controls = Controls(["forward", ], ["backward", ], ["left", ], ["right", ], ["fire_weapon", ])

        #  TODO fix this method
        def acquire_target(self):
            shortest_distance = 0
            target = None

            # TODO rework this code to incorporate "Factions"
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
            if self.parent.ship.rect.centerx in range(self.parent.target.rect.centerx - 60,
                                                      self.parent.target.rect.centerx + 60):
                self.parent.actions.append(self.controls.get_signal("fire_weapon"))
