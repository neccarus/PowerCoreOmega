import pygame


class Controls:

    def __init__(self, forward=pygame.K_w, backward=pygame.K_s, left=pygame.K_a,
                 right=pygame.K_d, fire_weapon=pygame.K_SPACE):
        self.scheme = {
            "forward": self.Scheme([forward], "forward"),
            "backward": self.Scheme([backward], "backward"),
            "left": self.Scheme([left], "left"),
            "right": self.Scheme([right], "right"),
            "fire_weapon": self.Scheme([fire_weapon], "fire"),
        }

    def get_signal(self, _input):
        # print(_input)
        if hasattr(_input, "key"):
            scheme = [scheme for scheme in self.scheme.values() if _input.key in scheme.inputs]
        else:
            scheme = [scheme for scheme in self.scheme.values() if _input in scheme.inputs]
        # print(scheme)
        if len(scheme) > 0:
            return scheme[0].signal
        else:
            return None

    class Scheme:

        def __init__(self, inputs=None, signal=""):
            if inputs is None:
                self.inputs = []
            else:
                self.inputs = inputs
            self.signal = signal
