class Ship:
    """
    Ship class is what all ships in game are derived from.

    Ship objects can have various pieces of armor, shields, reactors, engines and weapons
    There is a total number of slots allocated to each type of equipment

    Attributes:
        width, height: passed in as a tuple "size", this is pretty self explanatory
        pos_x, pos_y: passed in as a tuple "pos", this is pretty self explanatory
        health: the max amount of health the ship has
        current_health: the current amount of health the ship has, if this drops to zero the ship is destroyed
        shields: the currently equipped shield modules
        armor: the currently equipped armor modules
        reactors: the currently equipped reactor modules
        engines: the currently equipped engine modules
        weapons: the currently equipped weapon modules
        armor_slots: the total amount of armor modules that can be equipped on this ship
        shield_slots: the total amount of shield modules that can be equipped on this ship
        reactor_slots: the total amount of reactor modules that can be equipped on this ship
        engine_slots: the total amount of engine modules that can be equipped on this ship
        weapon_slots: the total amount of weapons that can be equipped on this ship
        weapon_locations: a list containing the pixel locations of where the weapons fire from on the ship
    """

    def __init__(self, size=(20, 20), pos=(0, 0), health=100, shields=None,
                 armor=None, reactors=None, engines=None, weapons=None,
                 shield_slots=0, armor_slots=0,  reactor_slots=0, engine_slots=0,
                 weapon_slots=0, weapon_locations=None):

        self.width, self.height = size
        self.pos_x, self.pos_y = pos
        self.health = health
        self.current_health = self.health

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

        if weapon_locations is None:
            self.weapon_locations = [(0, 0)]
        else:
            self.weapon_locations = weapon_locations
