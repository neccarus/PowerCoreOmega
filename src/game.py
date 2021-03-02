import pygame


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
        self.game_states = []
        self.current_state = None
        self.playing = False
        self.paused = False

    @staticmethod
    def update(guis=None, display=None, screen=None, fill_color=(0, 0, 0), clock=None, framerate=60):
        if guis is None:
            guis = []
        for gui in guis:
            gui.update(screen)
        if display:
            display.update()
        if screen:
            screen.fill(fill_color)
        if clock:
            clock.tick()

            clock.tick(framerate)

    @staticmethod
    def handle_events(event, guis=None):
        # TODO: maybe this should operate based on game state

        if guis is None:
            guis = []

        if event.type == pygame.MOUSEBUTTONDOWN:
            current_mouse_pos = pygame.mouse.get_pos()
            for gui in guis:
                gui.select_element(current_mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            current_mouse_pos = pygame.mouse.get_pos()
            for gui in guis:
                gui.activate_selected(current_mouse_pos, gui)
                gui.let_go()

    class GameState:

        def __init__(self, name="Game Loop", guis=None):

            self.name = name

            if guis is None:
                self.guis = []


def toggle_pause(game):
    game.paused = not game.paused


def toggle_playing(game):
    game.playing = not game.playing


def exit_game_loop(game):
    game.playing = False
    game.paused = False
