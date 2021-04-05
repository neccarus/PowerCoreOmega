import pygame
import random


class Particle:
    particles = []

    def __init__(self, pos, velocity, timer, color=(255, 255, 255)):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(velocity)
        self.timer = timer
        self.radius = self.timer / 100
        self.color = color

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
    def particle_cluster(cls, amount, pos, velocity, velocity_variance, timer, color):
        for _ in range(amount):
            Particle.particles.append(Particle(pos,
                                               velocity + pygame.Vector2(random.randint(-velocity_variance, velocity_variance), random.randint(-velocity_variance, velocity_variance)),
                                               timer, color))

    def update(self, delta_time, surface):
        self.pos += self.velocity
        self.timer -= delta_time
        self.radius = self.timer / 100
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
