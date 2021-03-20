import pygame
import os
import sys
from src import game_obj
from src import player_settings
from src.player import Player
from src.npc import NPC
from src.weapons import Weapon
from src.shields import Shield
from src.ship import Ship
from src.reactors import Reactor
# from src import SCREENSIZE
from src.guis import guis
from copy import copy

if os.name == 'posix':
    os.environ['SDL_AUDIODRIVER'] = 'dsp'

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Power Core Omega")
screen = pygame.display.set_mode(player_settings.screensize)

main_surface = pygame.Surface(size=player_settings.screensize)
game_surface = pygame.Surface(size=player_settings.screensize)
pause_surface = pygame.Surface(size=player_settings.screensize)

clock = pygame.time.Clock()

shotgun = Weapon(name="shotgun", projectile_color=(255, 255, 0), damage=5, spread=8, projectiles=10,
                 projectile_grouping=3, fire_rate=1, speed=800)

blaster = Weapon(name="blaster", damage=5, spread=0.7, fire_rate=0.2, speed=900)

splinter_gun = Weapon(name="splinter gun", projectile_color=(255, 150, 0), projectile_size=(4, ),
                      projectiles=3, projectile_grouping=1.5, fire_rate=0.5, damage=10, spread=3,
                      heat_generated=25, power_use=6)

basic_reactor = Reactor(name="basic reactor", recharge_rate=6, power_capacity=50,
                        cooling_rate=3, heat_capacity=400, heat_inefficiency=2)

basic_shield = Shield(name="basic shield", health=40, regen=5, broken_recharge_time=4)

player = Player(controls=player_settings.controls)

ai_ship = NPC()

game_obj.player = player

# Initialize game states
game_obj.new_game_state("paused", [guis["pause_gui"]], pause_surface, [player, ])
game_obj.new_game_state("running", [guis["start_gui"]], main_surface, [player, ])
game_obj.new_game_state("playing", None, game_surface, [player, ])

game_obj.set_game_state("running")

# Initialize game_obj attributes
game_obj.screen = screen
game_obj.display = pygame.display
game_obj.clock = clock
game_obj.framerate = 60

if __name__ == '__main__':

    while game_obj.running:

        # TODO: implement system in GuiPyg for handling basic menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            game_obj.handle_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or \
                        event.key == pygame.K_ESCAPE:
                    sys.exit()

        if game_obj.playing:

            print("initializing")
            player.acquire_ship(Ship(pos=(800, 800), weapon_locations=[(-5, 2), (5, 2)],
                                     cooling_modifier=1.25))
            player.ship.equip_weapon(copy(splinter_gun), 0)
            player.ship.equip_weapon(copy(splinter_gun), 1)
            player.ship.equip_shield(copy(basic_shield))
            player.ship.equip_reactor(copy(basic_reactor))

            enemy = copy(ai_ship)
            enemy.acquire_ship(Ship(pos=(800, 100), weapon_locations=[(-5, 2), (5, 2)]))
            enemy.ship.equip_weapon(copy(blaster), 0)
            enemy.ship.equip_weapon(copy(blaster), 1)
            enemy.ship.equip_shield(copy(basic_shield))
            enemy.ship.equip_reactor(copy(basic_reactor))
            # game_obj.shields.add(player.ship.shields, enemy.ship.shields)

            # Apply player object to game object
            game_obj.bodies.add(player.ship, enemy.ship)

            game_obj.ai_controllers.append(enemy)

        while game_obj.playing:
            # Game Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                game_obj.handle_events(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_obj.toggle_pause()

            while game_obj.paused:
                # Pause Loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    game_obj.handle_events(event)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_obj.toggle_pause()

                # Update pause loop
                game_obj.update(fill_color=(80, 80, 80))

            # Update game loop
            game_obj.update(fill_color=(0, 0, 0))

        # Update main menu loop
        game_obj.update(fill_color=(80, 80, 80))
