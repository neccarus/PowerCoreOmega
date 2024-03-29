import pygame


class Body(pygame.sprite.DirtySprite):
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

    def __init__(self, size=(20,), pos=(0, 0), health=100, sprite=None, vertical_speed=0, angle=90,
                 direction=pygame.Vector2(1, 0), color=(1, 1, 1), faction=None, *args, **kwargs):
        super().__init__(*args)
        if len(size) == 2:
            self.width, self.height = size
        elif len(size) == 1:
            self.width = size[0]
            self.height = size[0]
        # self.sprite = sprite
        self.dirty = 0
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        if health == 0:
            self.destructible = False
        else:
            self.destructible = True
        self.health = health

        self.current_health = self.health
        self.is_dead = False
        self.horizontal_speed = 0
        self.vertical_speed = vertical_speed
        self.horizontal_max_speed = 0
        self.vertical_max_speed = 0
        self.angle = angle
        self.direction = direction
        self.color = color
        self.faction = faction
        self.horizontal_acceleration = 0
        self.vertical_acceleration = 0
        self.mask = None
        self.get_mask()
        self.collided = False
        self.colliding_with = []

    def check_if_alive(self):
        if self.current_health <= 0 and self.destructible:
            self.is_dead = True

    def update(self, delta_time, *args, **kwargs):
        self.check_if_alive()

    def get_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, delta_time):
        self.pos += (self.direction * self.speed * delta_time) / 1000
        self.rect.center = self.pos
