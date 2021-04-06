from src.effects import Particle
import random
from pygame import Vector2


class Consumable:

    def __init__(self, name, effect_power=0,
                 duration=0, delay=0, parent=None):
        self.name = name
        self.effect_power = effect_power
        self.duration = duration * 1000
        self.current_duration = 0
        self.delay = delay * 1000
        self.current_delay = 0
        self.finished_delay = False
        self.expired = False
        self.effect_applied = False
        self.parent = parent
        self.particle_spawn_rate = 60
        self.particle_spawn_counter = 0

    def update(self, delta_time):

        if not self.finished_delay and self.current_delay <= self.delay:
            self.current_delay += delta_time
            if self.current_delay >= self.delay:
                self.finished_delay = True

        if self.finished_delay:
            self.current_duration += delta_time
            if self.current_duration >= self.duration:
                self.expired = True


class ShieldBooster(Consumable):

    def __init__(self, heat_generated=1, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.heat_generated = heat_generated

    def update(self, delta_time):
        super().update(delta_time)
        if self.finished_delay:
            self.parent.reactor.apply_heat(self.heat_generated, delta_time)
            if not self.effect_applied and not self.expired:
                self.parent.shield.consumable_regen += self.effect_power
                self.effect_applied = True
            if self.expired:
                self.parent.shield.consumable_regen = 0

            self.particle_spawn_counter += delta_time

            if self.particle_spawn_counter >= self.particle_spawn_rate:
                particle_spawn = Vector2(random.choice(self.parent.shield.mask))
                particle_direction = particle_spawn - Vector2(self.parent.rect.width / 2, self.parent.rect.height / 2)
                particle_speed = random.uniform(1.0, 2.5) * particle_direction.normalize()
                Particle.particles.append(Particle(particle_spawn + Vector2(self.parent.rect.left, self.parent.rect.top),
                                                   (Vector2(self.parent.horizontal_speed, self.parent.vertical_speed) * delta_time / 1000) + particle_speed,
                                                   500, self.parent.shield.color))
                self.particle_spawn_counter = self.particle_spawn_counter - self.particle_spawn_rate


class HeatSink(Consumable):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def update(self, delta_time):
        super().update(delta_time)
        if self.finished_delay:
            if not self.effect_applied and not self.expired:
                self.parent.reactor.venting_multiplier += self.effect_power
                self.parent.reactor.is_venting = True
                self.effect_applied = True
            if self.expired:
                self.parent.reactor.venting_multiplier = 1
                self.parent.reactor.is_venting = False
            Particle.particles.append(Particle(self.parent.reactor.pos,
                                               (Vector2(self.parent.horizontal_speed, self.parent.vertical_speed) * delta_time / 1000) + Vector2(random.uniform(-0.9, 0.9), random.uniform(-0.9, 0.9)),
                                               500, (255, 0, 0)))


consumable_dict = {
    'heat_sink': HeatSink(name='heat_sink', effect_power=4, duration=4,
                          delay=3),
    'shield_booster': ShieldBooster(name='shield_booster', effect_power=6, duration=4,
                                    delay=1, heat_generated=25)
}
