from src.body import Body
import math
from pygame import Vector2


class Ship(Body):
    """
    Ship class is what all ships in game are derived from, base class is Body.

    Ship objects can have various pieces of armor, shields, reactors, engines and weapons
    There is a total number of slots allocated to each type of equipment

    Attributes:
        name: the name of the ship
        ship_type: the type of ship: interceptor, fighter, heavy_fighter, etc.
        shields: the currently equipped shield modules, passed as a list
        armor: the currently equipped armor modules, passed as a list
        reactors: the currently equipped reactor modules, passed as a list
        engines: the currently equipped engine modules, passed as a list
        weapons: the currently equipped weapon modules, passed as a list
        armor_slots: the total amount of armor modules that can be equipped on this ship
        shield_slots: the total amount of shield modules that can be equipped on this ship
        reactor_slots: the total amount of reactor modules that can be equipped on this ship
        engine_slots: the total amount of engine modules that can be equipped on this ship
        weapon_slots: the total amount of weapons that can be equipped on this ship
        misc_slots: the total amount of miscellaneous slots available to the ship, weapons are not able to use these
        drone_slots: the total number of drone slots available to the ship
        weapon_locations: a list containing the pixel locations of where the weapons are located on the ship
    """

    def __init__(self, name="Python", ship_type="Interceptor", shields=None,
                 armor=None, reactors=None, engines=None, weapons=None, auxiliary_modules=None, shield_slots=0,
                 armor_slots=0, reactor_slots=0, engine_slots=0, weapon_slots=0, misc_slots=0, drone_slots=0,
                 weapon_locations=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.name = name
        self.ship_type = ship_type

        if shields is None:
            self.shields = []
        else:
            self.shields = shields

        if armor is None:
            self.armor = []
        else:
            self.armor = armor

        if reactors is None:
            self.reactors = []
        else:
            self.reactors = reactors

        if engines is None:
            self.engines = []
        else:
            self.engines = engines

        if weapons is None:
            self.weapons = []
        else:
            self.weapons = weapons

        if auxiliary_modules is None:
            self.auxiliary_modules = []
        else:
            self.auxiliary_modules = auxiliary_modules

        self.shield_slots = shield_slots
        self.armor_slots = armor_slots
        self.reactor_slots = reactor_slots
        self.engine_slots = engine_slots
        self.weapon_slots = weapon_slots
        self.misc_slots = misc_slots
        self.drone_slots = drone_slots

        if weapon_locations is None:
            self.weapon_locations = [(0, 0)]
        else:
            self.weapon_locations = weapon_locations

    def update(self, actions, delta_time, boundaries, *args, **kwargs) -> None:

        for action in actions:
            if action == "left":
                self.direction[0] = -1
                if self.horizontal_speed > -self.horizontal_max_speed:
                    self.horizontal_speed += (self.horizontal_acceleration * delta_time / 100) * self.direction[0]

            if action == "right":
                self.direction[0] = 1
                if self.horizontal_speed < self.horizontal_max_speed:
                    self.horizontal_speed += (self.horizontal_acceleration * delta_time / 100) * self.direction[0]

            if action == "forward":
                self.direction[1] = -1
                if self.vertical_speed > -self.vertical_max_speed:
                    self.vertical_speed += (self.vertical_acceleration * delta_time / 100) * self.direction[1]

            if action == "backward":
                self.direction[1] = 1
                if self.vertical_speed < self.vertical_max_speed:
                    self.vertical_speed += (self.vertical_acceleration * delta_time / 100) * self.direction[1]

        if "left" not in actions and "right" not in actions:
            self.horizontal_speed = self.decelerate(delta_time, "horizontal")

        if "forward" not in actions and "backward" not in actions:
            self.vertical_speed = self.decelerate(delta_time, "vertical")

        self.move(delta_time, boundaries)

    def decelerate(self, delta_time, direction):

        speed = 0
        acceleration = 0

        if direction == "horizontal":
            speed = self.horizontal_speed
            acceleration = self.horizontal_acceleration

        if direction == "vertical":
            speed = self.vertical_speed
            acceleration = self.vertical_acceleration

        if speed and speed > 0:
            speed -= (acceleration * delta_time / 100)
        elif speed < 0:
            speed += (acceleration * delta_time / 100)
        if math.isclose(speed, 0, abs_tol=0.1):
            speed = 0

        return speed

    def move(self, delta_time, boundary):

        self.pos += Vector2((delta_time * self.horizontal_speed) / 100,
                            (delta_time * self.vertical_speed) / 100)
        self.rect.center = self.pos
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos = self.rect.center
            self.horizontal_speed = 0
        elif self.rect.right > boundary.right:
            self.rect.right = boundary.right
            self.pos = self.rect.center
            self.horizontal_speed = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.pos = self.rect.center
            self.vertical_speed = 0
        elif self.rect.bottom > boundary.bottom:
            self.rect.bottom = boundary.bottom
            self.pos = self.rect.center
            self.vertical_speed = 0
