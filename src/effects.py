import pygame
import random


class Particle:
    particles = []

    def __init__(self, pos, velocity, timer, color=(255, 255, 255), glowing=False):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(velocity)
        self.timer = timer
        self.radius = self.timer / 100
        self.color = color
        self.glowing = glowing
        if self.glowing:
            self.glow = Glow(self.radius*2, self.pos, self.color)

    @classmethod
    def update_particles(cls, delta_time, surface):
        particles_to_remove = []
        for particle in cls.particles:
            particle.update(delta_time, surface)
            if particle.timer <= 0:
                particles_to_remove.append(particle)
        for r_particle in particles_to_remove:
            Particle.particles.remove(r_particle)

    @classmethod
    def particle_cluster(cls, amount, pos, velocity, velocity_variance, timer, color, glowing=False):
        for _ in range(amount):
            Particle.particles.append(Particle(pos,
                                               velocity + pygame.Vector2(random.randint(-velocity_variance, velocity_variance), random.randint(-velocity_variance, velocity_variance)),
                                               timer, color, glowing))

    def update(self, delta_time, surface):
        self.pos += self.velocity
        self.timer -= delta_time
        self.radius = self.timer / 100
        if self.glowing:
            self.glow.update(self.pos, self.radius*2)
            surface.blit(self.glow, self.pos - pygame.Vector2(self.glow.get_rect().center, self.glow.get_rect().center), special_flags=pygame.BLEND_RGB_ADD)
        pygame.draw.circle(surface, self.color, self.pos, self.radius)


class Glow(pygame.Surface):

    def __init__(self, radius, pos, color):
        self.radius = radius
        super().__init__((radius*2, radius*2))
        self.pos = pos - pygame.Vector2(self.radius*0.5, self.radius*0.5)
        self.color = self._set_color(color)
        self.set_colorkey((0, 0, 0))

    @staticmethod
    def _set_color(color):
        color = tuple([int(_color * 0.25) for _color in color])
        return color

    def update(self, pos, radius, color=None):
        self.fill(self.get_colorkey())
        self.pos = pos
        self.get_rect(center=self.pos)
        self.radius = radius
        if color is not None:
            self.color = self._set_color(color)
        pygame.draw.circle(self, self.color, self.get_rect().center, self.radius)

