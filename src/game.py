import pygame
from guipyg.utils.utils import Instance


class Game(Instance):
    """
        Game class is used to keep track of the state of the game

        This class is used to store all objects while keeping track of their states

        Attributes:
            name: name of the instance, used for GuiPyg's instancing of objects
            bodies: a list of all bodies present near the player
            dead_bodies: any bodies that are currently dead
            projectiles: a list of all projectiles that are currently active
            game_states: a list of the available game states
            running: is the game running
            playing: are we currently playing the game
            paused: is the game paused
            game_state: the current state the game is in ("running", "playing" or "paused"
            guis: this probably isn't needed here as it is handled in the game_state object
            display: the pygame.display object this Game object is drawing to
            screen: the screen object
            clock: the pygame.Clock object
            framerate: the fps that the game runs at
    """

    def __init__(self, name):
        self.name = name
        super().add_instance()
        self.controllers = []
        self.bodies = []
        self.dead_bodies = []
        self.projectiles = []
        self.game_states = {
            "running": self.GameState(name="running"),
            "playing": self.GameState(name="playing"),
            "paused": self.GameState(name="paused"),
        }
        self.running = True
        self.playing = False
        self.paused = False

        self.game_state = None

        self.guis = []
        self.display = None
        self.screen = None
        self.current_surface = None
        self.clock = None
        self.delta_time = 0
        self.framerate = None

    def update(self, fill_color=(0, 0, 0)):
        if len(self.game_state.guis) > 0:
            for gui in self.game_state.guis:
                gui.update(self.current_surface)

        self.screen.blit(self.current_surface, (0, 0))

        self.display.update()
        self.current_surface.fill(fill_color)
        for controller in self.controllers:
            controller.update(self.delta_time, self.current_surface.get_rect())
        if self.game_state.name == "playing":
            self.bodies.draw(self.current_surface)
        # self.clock.tick()
        self.delta_time = self.clock.tick(self.framerate)

    # should be handled in body class?
    def update_bodies(self):
        for body in self.bodies[::-1]:
            body.check_if_alive()
            if body.is_dead:
                self.dead_bodies.append(body)
                self.bodies.remove(body)

    def handle_events(self, event):
        # TODO: maybe this should operate based on game state

        if event.type == pygame.MOUSEBUTTONDOWN:
            current_mouse_pos = pygame.mouse.get_pos()
            for gui in self.game_state.guis:
                gui.select_element(current_mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            current_mouse_pos = pygame.mouse.get_pos()
            for gui in self.game_state.guis:
                gui.activate_selected(current_mouse_pos, gui)
                gui.let_go()

        if len(self.controllers) > 0:
            for controller in self.controllers:
                controller.get_events(event)

    def new_game_state(self, state="running", guis=None, surface=None):
        self.game_states[state] = self.GameState(state, guis, surface)

    def set_game_state(self, state):
        # self.game_state, = [st for st in self.game_states if st.name == state]
        self.game_state = self.game_states[state]
        self.current_surface = self.game_state.surface
        if self.screen:
            self.screen.fill((0, 0, 0))

    class GameState:
        """
        GameState object for Game object
        Stores guis for a given game state

        Attributes:
            name: the name of the state, used to determine which state the game is in
            guis: the guis associated with this GameState object
            surface: the surface this game state uses
        """
        #  TODO: seperate screen objects should be stored here so that game sprites are not drawn in menus
        def __init__(self, name="", guis=None, surface=None):

            self.name = name

            if guis is None:
                self.guis = []
            else:
                self.guis = guis

            self.surface = surface

    def toggle_pause(self, *_, **__):
        self.paused = not self.paused
        if self.paused:
            self.set_game_state("paused")
        else:
            self.set_game_state("playing")

    def toggle_playing(self, *_, **__):
        self.playing = not self.playing
        if self.playing and not self.paused:
            self.set_game_state("playing")
            print(self.game_state)

    def exit_game_loop(self, *_, **__):
        self.playing = False
        self.paused = False
        if self.running:
            self.set_game_state("running")
