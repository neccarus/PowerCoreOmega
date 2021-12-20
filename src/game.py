import pygame
from guipyg.utils.utils import Instance
from src.projectile import Projectile
from src.effects import Particle
import random
from copy import copy
from src.npc import NPC
from src.weapons import Weapon
from src.shields import Shield
from src.reactors import Reactor
from src.ship import Ship


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
        self.player = None
        self.ai_controllers = []
        self.bodies = []
        self.dead_bodies = []
        self.projectiles = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
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
        self.particles = Particle.particles
        self.spawner = None

    def update(self, fill_color=(0, 0, 0)):
        if len(self.game_state.guis) > 0:
            for gui in self.game_state.guis:
                gui.update(self.current_surface, need_update=True)

        self.player.update(self.delta_time, self.current_surface.get_rect(), self.current_surface)

        if self.game_state.name == "playing":

            if self.spawner:
                spawned = self.spawner.update(self.delta_time)
                if spawned:
                    spawned[0].pos = spawned[1]
                    enemy = NPC(faction='enemy')
                    enemy.acquire_ship(spawned[0])
                    enemy.equip_shield(spawned[0].shield)
                    enemy.ship.equip_reactor(spawned[0].reactor)
                    self.ai_controllers.append(enemy)
                    self.bodies.append(enemy.ship)

            for weapon in self.player.ship.weapons:
                self.update_weapon(weapon)

            self.projectiles.update(self.delta_time, self.display)
            self.explosions.update(self.delta_time)
            self.remove_expired_explosions()

            self.detect_projectile_hits(self.player.ship, self.projectiles)
            self.detect_explosion_hits(self.player.ship, self.explosions)

            for ai_controller in self.ai_controllers:
                self.detect_projectile_hits(ai_controller.ship, self.projectiles)
                self.detect_explosion_hits(ai_controller.ship, self.explosions)
                self.update_ai_controller(ai_controller)

            self.projectiles.draw(self.current_surface)
            for body in self.bodies:
                self.current_surface.blit(body.image, body.rect)

            for explosion in self.explosions:
                if not explosion.expired:
                    self.current_surface.blit(explosion.image, explosion.rect)

            Particle.update_particles(self.delta_time, self.current_surface)

        self.screen.blit(self.current_surface, (0, 0))

        self.display.update()
        self.current_surface.fill(fill_color)

        self.delta_time = self.clock.tick(self.framerate)

    def remove_expired_explosions(self):
        explosions_to_remove = []
        for explosion in self.explosions:
            if explosion.expired and len(explosion.groups()) > 0:
                explosions_to_remove.append(explosion)
                explosion = None

        del explosions_to_remove

    def update_weapon(self, weapon):
        if weapon.weapon is not None:
            if weapon.weapon.firing and weapon.weapon.current_cool_down == 0:
                projectiles_to_add = weapon.weapon.fire()
                if len(projectiles_to_add) > 0:
                    self.projectiles.add(projectiles_to_add)

    def update_ai_controller(self, ai_controller):
        ai_controller.update(self.delta_time, self.current_surface.get_rect(), self.current_surface, (self.player,))
        if ai_controller.ship.is_dead:
            self.bodies.remove(ai_controller.ship)
            self.ai_controllers.remove(ai_controller)
            ai_controller.kill()
            return
        for weapon in ai_controller.ship.weapons:
            self.update_weapon(weapon)

    def detect_projectile_hits(self, target,
                               projectiles):  # pass in projectiles as it could be from a seperate list in the future
        projectile_hits = pygame.sprite.spritecollide(target, projectiles, False)
        for projectile in projectile_hits:
            if projectile.parent != target and projectile.parent.faction != target.faction:
                target.take_damage(projectile.damage)
                Particle.particle_cluster(projectile.damage // 3, projectile.pos,
                                          ((
                                                   projectile.direction * -projectile.speed * self.delta_time / 1000) * projectile.damage / 100),
                                          3, random.randint(350, 450), projectile.color, glowing=True)
                if len(projectile.effects) > 0:
                    for effect in projectile.effects:
                        self.explosions.add(effect)
                        effect.spawn(pos=projectile.pos, parent=projectile)
                self.projectiles.remove(projectile)
                del projectile

    def detect_explosion_hits(self, target,
                              explosions):  # pass in explosions as it could be from a seperate list in the future
        explosion_hits = pygame.sprite.spritecollide(target, explosions, False)
        for explosion in explosion_hits:
            if explosion.parent.parent != target:
                if target not in explosion.targets_hit:
                    target.take_damage(explosion.direct_damage)
                    explosion.targets_hit.append(target)

    # TODO: should be handled in body class?
    def update_bodies(self):
        for body in self.bodies[::-1]:
            body.check_if_alive()
            if body.is_dead:
                self.dead_bodies.append(body)
                self.bodies.remove(body)
        self.dead_bodies = []

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
        self.bodies = []
        self.ai_controllers = []
        self.projectiles.empty()
        if self.running:
            self.set_game_state("running")


class Spawner:

    def __init__(self, wave, position, timer, ship,
                 weapon_selection=None, shield_selection=None, reactor_selection=None,
                 amount_to_spawn=1,
                 x_pos_min=0, x_pos_max=0,
                 y_pos_min=0, y_pos_max=0):
        self.wave = wave
        self.position = position
        self.x_pos_min = x_pos_min
        self.x_pos_max = x_pos_max
        self.y_pos_min = y_pos_min
        self.y_pos_max = y_pos_max
        self.timer = timer
        self.current_timer = 0
        self.ship = ship
        if weapon_selection is None:
            self.weapon_selection = []
        else:
            self.weapon_selection = weapon_selection
        if shield_selection is None:
            self.shield_selection = []
        else:
            self.shield_selection = shield_selection
        if reactor_selection is None:
            self.reactor_selection = []
        else:
            self.reactor_selection = reactor_selection
        self.amount_to_spawn = amount_to_spawn

    def set_random_pos(self):
        self.position = pygame.Vector2(random.randint(self.x_pos_min, self.x_pos_max + 1),
                                       random.randint(self.y_pos_min, self.y_pos_max + 1)
                                       )

    def update(self, delta_time):
        ship_spawn = None
        self.current_timer += delta_time
        if self.current_timer >= self.timer:
            self.current_timer -= self.timer
            self.set_random_pos()
            ship_spawn = self.spawn_ship()
        return ship_spawn

    def spawn_ship(self):
        ship = Ship(weapon_locations=[(-5, 2), (5, 2)],
                    shield=Shield(**random.choice(self.shield_selection).__dict__),
                    reactor=Reactor(**random.choice(self.reactor_selection).__dict__))
        for index, _ in enumerate(ship.weapon_locations):
            weapon = Weapon(**random.choice(self.weapon_selection).__dict__)
            ship.equip_weapon(weapon, index)
        return ship, self.position
