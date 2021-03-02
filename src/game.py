class Game:
    """
        Game class is used to keep track of the state of the game

        This class is used to store all objects while keeping track of their states

        Attributes:
            bodies: a list of all bodies present near the player
            projectiles: a list of all projectiles that are currently active
    """

    def __init__(self):
        self.bodies = []
        self.projectiles = []
