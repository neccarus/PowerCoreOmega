from src.equipment import Equipment
import pygame


class Shield(Equipment):

    def __init__(self, health=10, regen=1, broken_recharge_time=5, color=(0, 0, 255, 100), *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.health = health
        self.current_health = health
        self.regen = regen
        self.broken_recharge_time = broken_recharge_time
        self.color = color
        self.current_recharge = 0
        self.recharging = True
        self.mask = None
        self.angle = 0
        self.shield_image = []
        self.original_image = None

    def update(self, delta_time, surface):
        self.pos = self.parent.pos
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.parent.rect.center)
        # print(self.current_health)

        if self.current_health < self.health and self.recharging:
            self.current_health += self.regen * delta_time / 1000

        if self.current_health > self.health:
            self.current_health = self.health

        if self.current_health <= 0 and self.current_recharge < self.broken_recharge_time:
            self.recharging = False
            self.current_health = 0
            self.current_recharge += delta_time / 1000
            if self.current_recharge >= self.broken_recharge_time:
                self.recharging = True
                self.current_recharge = 0

    def equip_to_parent(self, parent):
        self.parent = parent
        self.pos = parent.pos
        self.mask = pygame.mask.from_surface(self.parent.image)
        self.mask.scale((self.parent.width + 3, self.parent.height + 3))
        self.rect = self.mask.get_rect()
        self.width, self.height = self.rect.width, self.rect.height
        self.angle = parent.angle
        self.image = self.mask.to_surface(self.image, setcolor=self.color)
        self.image = self.image.convert_alpha()
        self.original_image = self.image
