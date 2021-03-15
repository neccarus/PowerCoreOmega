from src.body import Body
import pygame


class Projectile(Body):

    def __init__(self, speed, pos, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.speed = speed
        self.pos = pygame.Vector2(pos)

        # Temporary
        pygame.draw.rect(self.image, (0, 255, 0), pygame.Rect(0, 0, 5, 5))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, delta_time, display=None, *args, **kwargs):
        super().update(delta_time, *args, **kwargs)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.move(delta_time)
        if not display.get_surface().get_rect().contains(self.rect):
            self.kill()

    def move(self, delta_time):
        self.pos += (self.direction * self.speed * delta_time) / 1000
        self.rect.center = self.pos