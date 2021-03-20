import pygame
from guipyg.utils.utils import Instance
from src.projectile import Projectile


class Game(Instance):
    """
        Game class is used to keep track of the state of the game

        This class is used to store all objects while keeping track of their states

        Attributes:
            name: name of the instance, used for GuiPyg's instancing of objects
            bodies: a list of all bodies present near the player
            dead_bodies: any bodies that are currently dead
            projectiles (list of Projectile): a list of all projectiles that are currently active
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
        # self.controllers = []
        self.player = None
        self.ai_controllers = []
        self.bodies = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        self.dead_bodies = []
        self.projectiles = pygame.sprite.Group()
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

        self.player.update(self.delta_time, self.current_surface.get_rect(), self.current_surface)

        if self.game_state.name == "playing":

            for weapon in self.player.ship.weapons:
                self.update_weapon(weapon)

            self.projectiles.update(self.delta_time, self.display)

            self.detect_projectile_hits(self.player.ship, self.projectiles)

            for ai_controller in self.ai_controllers:
                self.detect_projectile_hits(ai_controller.ship, self.projectiles)
                self.update_ai_controller(ai_controller)

            self.projectiles.draw(self.current_surface)

            self.bodies.draw(self.current_surface)

            for shield in self.player.ship.shields:

                if shield.current_health > 0 and shield not in self.shields:
                    self.shields.add(shield)

            for ai_controller in self.ai_controllers:
                for shield in ai_controller.ship.shields:
                    if shield.current_health > 0 and shield not in self.shields:
                        self.shields.add(shield)

            for shield in self.shields:
                if shield.current_health > 0:
                    self.current_surface.blit(shield.image, shield.rect)

        self.delta_time = self.clock.tick(self.framerate)

    def update_weapon(self, weapon):
        if weapon.weapon is not None:
            if weapon.weapon.firing and weapon.weapon.current_cool_down == 0:
                projectiles_to_add = weapon.weapon.fire()
                if len(projectiles_to_add) > 0:
                    self.projectiles.add(projectiles_to_add)

    def update_ai_controller(self, ai_controller):
        ai_controller.update(self.delta_time, self.current_surface.get_rect(), self.current_surface, (self.player, ))
        if ai_controller.ship.is_dead:
            self.bodies.remove(ai_controller.ship)
            self.ai_controllers.remove(ai_controller)
            ai_controller.kill()
            # print("killed")
            return
        for weapon in ai_controller.ship.weapons:
            self.update_weapon(weapon)

    def detect_projectile_hits(self, target, projectiles): # pass in projectiles as it could be from a seperate list in the future
        projectile_hits = pygame.sprite.spritecollide(target, projectiles, False)
        for projectile in projectile_hits:
            if projectile.parent != target:
                target.take_damage(projectile)
                self.projectiles.remove(projectile)
        # print(target.current_health)

    # TODO: should be handled in body class?
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

        if len(self.game_state.controllers) > 0:
            for controller in self.game_state.controllers:
                controller.get_events(event)

    def new_game_state(self, state="running", guis=None, surface=None, controllers=None):
        if controllers is None:
            controllers = []

        self.game_states[state] = self.GameState(state, guis, surface, controllers)

    def set_game_state(self, state):
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
        def __init__(self, name="", guis=None, surface=None, controllers=None):

            self.name = name

            if guis is None:
                self.guis = []
            else:
                self.guis = guis

            self.surface = surface
            if controllers is None:
                self.controllers = []
            else:
                self.controllers = controllers

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
        self.shields = pygame.sprite.Group()
        self.bodies.empty()
        self.ai_controllers = []
        self.projectiles.empty()
        if self.running:
            self.set_game_state("running")
