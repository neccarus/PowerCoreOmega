import pygame

from src.body import Body
import math
from pygame import Vector2
from guipyg.utils.utils import Instance
from copy import copy
from src.consumables import consumable_dict
from src.shields import Shield


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

    def __init__(self, name="Python", ship_type="Interceptor", shield=None,
                 armor=None, reactor=None, engines=None, auxiliary_modules=None,
                 armor_slots=0, engine_slots=0, weapon_slots=2, misc_slots=0, drone_slots=0,
                 weapon_locations=None, weapons=None, parent=None, cooling_modifier=1, *args, **kwargs):

        super().__init__(*args, **kwargs)
        super().add_instance()

        self.armor_slots = armor_slots
        self.engine_slots = engine_slots
        self.weapon_slots = weapon_slots
        self.misc_slots = misc_slots
        self.drone_slots = drone_slots
        self.parent = parent
        self.cooling_modifier = cooling_modifier
        self.shielded = False
        self.shield_health = 0
        self.shield_boosters = 0
        self.heat_sinks = 0
        self.consumable_effects = []
        self.consumable_used = False
        self.consumable_cool_down = 5000
        self.current_consumable_cool_down = 0
        self.dot_effects = []
        self.shielded_image = None
        self.current_image = None

        if weapon_locations is None:
            self.weapon_locations = [(0, 0)]
        else:
            self.weapon_locations = weapon_locations

        self.weapons = [self.WeaponNode(pos=pos) for pos in self.weapon_locations]

        if weapons is not None:
            [self.equip_weapon(weapon, slot) for weapon, slot in weapons]

        self.name = name
        self.ship_type = ship_type

        if armor is None:
            self.armor = []
        else:
            self.armor = armor

        if reactor is not None:
            self.equip_reactor(reactor)
        else:
            self.reactor = reactor

        # if shield is not None:
        #     self.equip_shield(shield)
        # else:
        self.shield = shield

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

        self.shield = Shield(**shield.__dict__)
        self.shield.equip_to_parent(self)
        self.shielded = True
        self.shielded_image = self.original_image.copy()
        pygame.draw.polygon(self.shielded_image, self.shield.color, self.shield.mask, 1)

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

            if action == "fire_weapon":
                for weapon in self.weapons:
                    if weapon.weapon is not None:
                        weapon.weapon.firing = True

            if action == "eject_heat_sink":
                if not self.consumable_used:
                    self.add_consumable(copy(consumable_dict['heat_sink']))
                    self.consumable_used = True

            if action == "boost_shields":
                if not self.consumable_used:
                    self.add_consumable(copy(consumable_dict['shield_booster']))
                    self.consumable_used = True

        if "left" not in actions and "right" not in actions:
            self.horizontal_speed = self.decelerate(delta_time, "horizontal")

        if "forward" not in actions and "backward" not in actions:
            self.vertical_speed = self.decelerate(delta_time, "vertical")

        if "fire_weapon" not in actions:
            for weapon in self.weapons:
                if weapon.weapon is not None:
                    weapon.weapon.firing = False

        for effect in self.dot_effects:
            self.take_damage(effect.update(delta_time))

        for consumable in self.consumable_effects:
            consumable.update(delta_time)

        self.remove_expired_effects(self.consumable_effects)
        self.remove_expired_effects(self.dot_effects)

        if self.consumable_used:
            self.current_consumable_cool_down += delta_time
        if self.current_consumable_cool_down >= self.consumable_cool_down:
            self.current_consumable_cool_down = 0
            self.consumable_used = False

        for weapon in self.weapons:
            if weapon.weapon is not None:
                weapon.weapon.update(delta_time)

        self.direction = self.direction.rotate(-self.angle)
        self.move(delta_time, boundaries)

        self.shield.update(delta_time, surface)
        if self.shield.current_health > 0:
            self.shielded = True
        else:
            self.shielded = False

        if self.shielded:
            # pygame.draw.polygon(self.image, self.shield.color, self.shield.mask, 3)
            # self.dirty = 1
            self.current_image = self.shielded_image
        else:
            self.current_image = self.original_image
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
        if math.isclose(speed, 0, abs_tol=1):
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

    def take_damage(self, damage):
        if self.shielded:
            if 0 < self.shield.current_health <= damage:
                segmented_damage = damage - self.shield.current_health
                self.shield.current_health = 0
                damage -= segmented_damage
                self.shielded = False

            elif self.shield.current_health > 0 and damage < self.shield.current_health:
                self.shield.current_health -= damage

        if not self.shielded:
            self.current_health -= damage

    def receive_damage_over_time_effect(self, damage_over_time, duration):
        self.dot_effects.append(self.DOTEffect(damage_over_time, duration))

    def add_consumable(self, consumable):
        consumable.parent = self
        self.consumable_effects.append(consumable)

    @staticmethod
    def remove_expired_effects(effects):
        for effect in effects:
            if effect.expired:
                effects.remove(effect)
                # del effect

    class WeaponNode:

        def __init__(self, pos=(0, 0), weapon=None):
            self.pos = Vector2(pos)
            self.weapon = weapon

        def detach(self):
            self.weapon = None

    class DOTEffect:

        def __init__(self, damage, duration):
            self.damage = damage
            self.duration = duration
            self.current_duration = 0
            self.expired = False

        def update(self, delta_time):
            damage_dealt = (self.damage / (self.duration / 1000)) * (delta_time / 1000)
            self.current_duration += delta_time
            if self.current_duration >= self.duration:
                self.expired = True
            return damage_dealt
