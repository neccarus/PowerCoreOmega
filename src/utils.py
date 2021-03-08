from guipyg.utils.utils import Instance


class Settings(Instance):

    def __init__(self, controls=None, screensize=(1600, 900), fullscreen=False):
        self.controls = controls
        self.screensize = screensize
        self.fullscreen = fullscreen
