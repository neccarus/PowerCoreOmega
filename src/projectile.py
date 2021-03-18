from src.body import Body
import pygame


class Projectile(Body):

    def __init__(self, speed, pos, damage=0, color=(0, 255, 0), parent=None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.speed = speed
        self.pos = pygame.Vector2(pos)
        self.damage = damage
        self.color = color
        self.parent = parent

        # Temporary
        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, self.width, self.height))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, delta_time, display=None, *args, **kwargs):
        super().update(delta_time, *args, **kwargs)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.move(delta_time)
        if not display.get_surface().get_rect().contains(self.rect):
            self.kill()
            del self

    def move(self, delta_time):
        self.pos += (self.direction * self.speed * delta_time) / 1000
        self.rect.center = self.pos
