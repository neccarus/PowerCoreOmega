from src.body import Body
import pygame


class Projectile(Body):

    def __init__(self, speed, pos, damage=0, color=(0, 255, 0), parent=None, effects=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.speed = speed
        self.pos = pygame.Vector2(pos)
        self.damage = damage
        self.color = color
        self.parent = parent
        if effects is None:
            self.effects = []
        else:
            self.effects = effects
        self.mask = pygame.mask.from_surface(self.image)


        # Temporary
        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, self.width, self.height))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, delta_time, display=None, *args, **kwargs):
        super().update(delta_time, *args, **kwargs)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.move(delta_time)
        # print(self.effects)
        if not display.get_surface().get_rect().contains(self.rect):
            self.kill()
            del self

    def move(self, delta_time):
        self.pos += (self.direction * self.speed * delta_time) / 1000
        self.rect.center = self.pos


class ProjectileEffect(Body):

    def __init__(self, direct_damage=0, damage_over_time=0, duration=0, parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direct_damage = direct_damage  # this is dealt on the initial hit with the target
        self.damage_over_time = damage_over_time  # this is dealt on every call of update()
        self.duration = duration * 1000
        self.current_duration = 0
        self.parent = parent
        self.targets_affected = []  # check which target(s) are affected by the effect
        self.targets_hit = []
        self.expired = False

    def spawn(self, pos, parent=None):
        self.pos = pos
        self.rect.center = pos
        self.parent = parent
        self.current_duration = 0
        self.expired = False
        self.targets_hit = []
        self.targets_affected = []

    def update(self, delta_time, *args, **kwargs):
        self.current_duration += delta_time
        if self.current_duration >= self.duration:
            self.expired = True
        for target in self.targets_hit:
            if target.is_dead:
                self.targets_hit.remove(target)
                if target in self.targets_affected:
                    self.targets_affected.remove(target)
            if target not in self.targets_affected:
                target.receive_damage_over_time_effect(self.damage_over_time, self.duration)
                self.targets_affected.append(target)


class Explosion(ProjectileEffect):

    def __init__(self, radius=0, explosion_lifetime=0.0, *args, **kwargs):
        self.radius = radius
        size = radius * 2
        super().__init__(size=(size, ), *args, **kwargs)
        self.explosion_lifetime = explosion_lifetime * 1000

    def update(self, delta_time, *args, **kwargs):
        super().update(delta_time, *args, **kwargs)
        self.move(delta_time)
        if self.current_duration >= self.explosion_lifetime:
            self.image.fill((0, 0, 0))
            # self.mask = self.image.get_masks()

    def spawn(self, *args, **kwargs):
        super().spawn(*args, **kwargs)
        self.direction = self.parent.direction
        self.speed = self.parent.speed / 4
        pygame.draw.circle(self.image, self.color, self.image.get_rect().center, self.radius)
        self.mask = self.image.get_masks()
        return Explosion(self.radius, self.explosion_lifetime, self.direct_damage, self.damage_over_time,
                         self.duration, self.color)


projectile_effect_dict = {'small_explosion': Explosion(radius=50, explosion_lifetime=0.25, direct_damage=40,
                                                       damage_over_time=40, duration=4, color=(170, 200, 20))}
