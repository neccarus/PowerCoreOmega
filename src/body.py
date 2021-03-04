class Body:
    """
    Body class is the base class for all other objects in space that can interact with each other
    Examples: ships, projectiles, etc.

    Attributes:
        width, height: passed in as a tuple "size", if 1 value is passed in then width and height are equal
        pos_x, pos_y: passed in as a tuple "pos", this is pretty self explanatory
        health: the max amount of health the ship has
        current_health: the current amount of health the ship has, if this drops to zero the ship is destroyed
        is_dead: when this bodies current_health reaches 0 this will be toggled on and whatever death event can be handled
        speed: the current speed of the body in pixels per second
        max_speed: the maximum speed this body can travel at
        acceleration: the speed at which this body can accelerate in pixels per second
    """

    def __init__(self, size=(20,), pos=(0, 0), health=100):
        if len(size) == 2:
            self.width, self.height = size
        elif len(size) == 1:
            self.width = size
            self.height = size
        self.pos_x, self.pos_y = pos
        if health == 0:
            self.destructible = False
        else:
            self.destructible = True
        self.health = health
        self.current_health = self.health
        self.is_dead = False
        self.speed = 0
        self.max_speed = 0
        self.acceleration = 0

    def check_if_alive(self):
        if self.current_health <= 0 and self.destructible:
            self.is_dead = True
