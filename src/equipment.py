from pygame import Vector2
from pygame import sprite
from pygame import Surface


class Equipment(sprite.Sprite):

    def __init__(self, name="default", weight=0, parent=None, size=(20,), pos=Vector2(0, 0), *args, **kwargs):
        super().__init__(*args)
        self.name = name
        self.weight = weight
        self.parent = parent
        if len(size) == 2:
            self.width, self.height = size
        elif len(size) == 1:
            self.width = size[0]
            self.height = size[0]
        self.pos = pos
        self.image = Surface((self.width, self.height))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = Vector2(self.rect.center)
        self.angle = 0

    def equip_to_parent(self, parent):

        self.parent = parent
        self.angle = self.parent.angle - 90
        self.pos = self.parent.pos
        # self.rotate()