import pygame


class Controls:

    def __init__(self, forward=pygame.K_w, backward=pygame.K_s, left=pygame.K_a,
                 right=pygame.K_d, fire_weapon=pygame.K_SPACE, heat_sink=pygame.K_2,
                 shield_booster=pygame.K_1):
        self.signals = {
            "forward": self.Signal([forward], "forward"),
            "backward": self.Signal([backward], "backward"),
            "left": self.Signal([left], "left"),
            "right": self.Signal([right], "right"),
            "fire_weapon": self.Signal([fire_weapon], "fire"),
            "eject_heatsink": self.Signal([heat_sink], "heat_sink"),
            "boost_shields": self.Signal([shield_booster], "shield_booster")
        }

    def get_signal(self, _input):
        # print(_input)
        if hasattr(_input, "key"):
            signal = [signal for signal in self.signals.values() if _input.key in signal.inputs]
        else:
            signal = [signal for signal in self.signals.values() if _input in signal.inputs]
        # print(scheme)
        if len(signal) > 0:
            return signal[0].signal
        else:
            return None

    class Signal:

        def __init__(self, inputs=None, signal=""):
            if inputs is None:
                self.inputs = []
            else:
                self.inputs = inputs
            self.signal = signal
