

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
            # self.parent.reactor.current_heat += self.heat_generated * delta_time / 1000
            self.parent.reactor.apply_heat(self.heat_generated, delta_time)
            if not self.effect_applied and not self.expired:
                self.parent.shield.consumable_regen += self.effect_power
                self.effect_applied = True
            if self.expired:
                self.parent.shield.consumable_regen = 0


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


consumable_dict = {
    'heat_sink': HeatSink(name='heat_sink', effect_power=4, duration=4,
                          delay=3),
    'shield_booster': ShieldBooster(name='shield_booster', effect_power=6, duration=4,
                                    delay=1, heat_generated=25)
}
