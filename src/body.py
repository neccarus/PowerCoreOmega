import pygame


class Body(pygame.sprite.Sprite):
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
                 direction=pygame.Vector2(1, 0), *args):
        super().__init__(*args)
        if len(size) == 2:
            self.width, self.height = size
        elif len(size) == 1:
            self.width = size[0]
            self.height = size[0]
        # self.pos_x, self.pos_y = pos
        self.sprite = sprite
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        # self.rect.center = pos
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
        self.horizontal_acceleration = 0
        self.vertical_acceleration = 0
        self.mask = None
        self.get_mask()

    def check_if_alive(self):
        if self.current_health <= 0 and self.destructible:
            self.is_dead = True

    def update(self, delta_time, *args, **kwargs):
        self.check_if_alive()
        # self.move(delta_time)

    def get_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    # def move(self, delta_time):
    #     self.pos += pygame.Vector2((delta_time * self.horizontal_speed) / 1000,
    #                                (delta_time * self.vertical_speed) / 1000)
