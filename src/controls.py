import pygame


class Controls:

    def __init__(self, forward=(pygame.K_w, ), backward=(pygame.K_s, ), left=(pygame.K_a, ),
                 right=(pygame.K_d, ), fire_weapon=(pygame.K_SPACE, ), eject_heat_sink=(pygame.K_2, ),
                 boost_shields=(pygame.K_1, ), *args, **kwargs):
        self.forward = self.Signal([*forward], "forward")
        self.backward = self.Signal([*backward], "backward")
        self.left = self.Signal([*left], "left")
        self.right = self.Signal([*right], "right")
        self.fire_weapon = self.Signal([*fire_weapon], "fire_weapon")
        self.eject_heat_sink = self.Signal([*eject_heat_sink], "eject_heat_sink")
        self.boost_shields = self.Signal([*boost_shields], "boost_shields")
        self.signals = {
            "forward": self.forward,
            "backward": self.backward,
            "left": self.left,
            "right": self.right,
            "fire_weapon": self.fire_weapon,
            "eject_heat_sink": self.eject_heat_sink,
            "boost_shields": self.boost_shields
        }

    def get_signal(self, _input):
        if hasattr(_input, "key"):
            signal = [signal for signal in self.signals.values() if _input.key in signal.inputs]
        else:
            signal = [signal for signal in self.signals.values() if _input in signal.inputs]
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
