from src.body import Body
from src.weapons import Weapon
import math
from pygame import Vector2
from guipyg.utils.utils import Instance


class Ship(Body, Instance):
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
                 armor=None, reactor=None, engines=None, auxiliary_modules=None, shield_slots=0,
                 armor_slots=0, engine_slots=0, weapon_slots=2, misc_slots=0, drone_slots=0,
                 weapon_locations=None, parent=None, cooling_modifier=1, *args, **kwargs):

        super().__init__(*args, **kwargs)
        super().add_instance()

        self.shield_slots = shield_slots
        self.armor_slots = armor_slots
        self.engine_slots = engine_slots
        self.weapon_slots = weapon_slots
        self.misc_slots = misc_slots
        self.drone_slots = drone_slots
        self.parent = parent
        self.cooling_modifier = cooling_modifier
        self.shielded = False
        self.shield_health = 0

        if weapon_locations is None:
            self.weapon_locations = [(0, 0)]
        else:
            self.weapon_locations = weapon_locations

        self.weapons = [self.WeaponNode(pos=pos) for pos in self.weapon_locations]

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

        self.reactor = reactor

        if engines is None:
            self.engines = []
        else:
            self.engines = engines

        if auxiliary_modules is None:
            self.auxiliary_modules = []
        else:
            self.auxiliary_modules = auxiliary_modules

    def equip_weapon(self, weapon, slot):

        self.weapons[slot].weapon = weapon
        weapon.equip_to_parent(self, slot)

    def equip_shield(self, shield):

        self.shields.append(shield)
        shield.equip_to_parent(self)
        self.shielded = True

    def equip_reactor(self, reactor):

        self.reactor = reactor
        reactor.equip_to_parent(self)

    def update(self, actions, delta_time, boundaries, surface, *args, **kwargs) -> None:

        super().update(delta_time, *args, **kwargs)
        for action in actions:
            if action == "left":
                self.direction[0] = -1
                if self.horizontal_speed > -self.horizontal_max_speed:
                    self.horizontal_speed += (self.horizontal_acceleration * delta_time / 1000) * self.direction[0]

            if action == "right":
                self.direction[0] = 1
                if self.horizontal_speed < self.horizontal_max_speed:
                    self.horizontal_speed += (self.horizontal_acceleration * delta_time / 1000) * self.direction[0]

            if action == "forward":
                self.direction[1] = -1
                if self.vertical_speed > -self.vertical_max_speed:
                    self.vertical_speed += (self.vertical_acceleration * delta_time / 1000) * self.direction[1]

            if action == "backward":
                self.direction[1] = 1
                if self.vertical_speed < self.vertical_max_speed:
                    self.vertical_speed += (self.vertical_acceleration * delta_time / 1000) * self.direction[1]

            if action == "fire":
                for weapon in self.weapons:
                    if weapon.weapon is not None:
                        weapon.weapon.firing = True

            if action == "heatsink":
                self.reactor.is_venting = True

        if "left" not in actions and "right" not in actions:
            self.horizontal_speed = self.decelerate(delta_time, "horizontal")

        if "forward" not in actions and "backward" not in actions:
            self.vertical_speed = self.decelerate(delta_time, "vertical")

        if "fire" not in actions:
            for weapon in self.weapons:
                if weapon.weapon is not None:
                    weapon.weapon.firing = False

        if "heatsink" not in actions:
            self.reactor.is_venting = False

        for weapon in self.weapons:
            if weapon.weapon is not None:
                weapon.weapon.update(delta_time)

        self.direction = self.direction.rotate(-self.angle)
        self.move(delta_time, boundaries)

        # TODO: shield handling needs to be reworked for a single shield module and should be moved to the Shield class
        self.shield_health = 0
        for shield in self.shields:
            shield.update(delta_time, surface)
            self.shield_health += shield.current_health
        if self.shield_health > 0:
            self.shielded = True
        else:
            self.shielded = False

        self.reactor.update(delta_time)

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
            speed -= (acceleration * delta_time / 1000)
        elif speed < 0:
            speed += (acceleration * delta_time / 1000)
        if math.isclose(speed, 0, abs_tol=0.01):
            speed = 0

        return speed

    def move(self, delta_time, boundary):

        self.pos += Vector2((delta_time * self.horizontal_speed) / 1000,
                            (delta_time * self.vertical_speed) / 1000)
        self.rect.center = self.pos
        if self.rect.left < boundary.left:
            self.rect.left = boundary.left
            self.pos = self.rect.center
            self.horizontal_speed = 0
        elif self.rect.right > boundary.right:
            self.rect.right = boundary.right
            self.pos = self.rect.center
            self.horizontal_speed = 0

        if self.rect.top < boundary.top:
            self.rect.top = boundary.top
            self.pos = self.rect.center
            self.vertical_speed = 0
        elif self.rect.bottom > boundary.bottom:
            self.rect.bottom = boundary.bottom
            self.pos = self.rect.center
            self.vertical_speed = 0

    def take_damage(self, source):
        damage = source.damage
        if len(self.shields) > 0:
            if self.shielded:
                if self.shield_health > 0:
                    self.shield_health -= damage
                for shield in self.shields:
                    if 0 < shield.current_health <= damage:
                        segmented_damage = int(damage - shield.current_health)
                        shield.current_health -= segmented_damage
                        damage -= int(segmented_damage)
                        # print(damage)

                    elif shield.current_health > 0 and damage < shield.current_health:
                        shield.current_health -= damage
                        # print(damage)
                        break

            elif not self.shielded:
                self.current_health -= damage
        else:
            self.current_health -= damage

    class WeaponNode:

        def __init__(self, pos=(0, 0), weapon=None):
            self.pos = Vector2(pos)
            self.weapon = weapon

        def detach(self):
            self.weapon = None
