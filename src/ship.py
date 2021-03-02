from src.body import Body


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
                 armor=None, reactors=None, engines=None, weapons=None, shield_slots=0, armor_slots=0, reactor_slots=0,
                 engine_slots=0, weapon_slots=0, misc_slots=0, drone_slots=0, weapon_locations=None, *args, **kwargs):

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
