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
from guipyg.gui import GUI
from guipyg.gui_element.graph_elements import BarElement

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
                 projectile_grouping=3, fire_rate=1, speed=800, power_use=8)

blaster = Weapon(name="blaster", damage=5, spread=0.7, fire_rate=0.2, speed=900)

splinter_gun = Weapon(name="splinter gun", projectile_color=(255, 150, 0), projectile_size=(4,),
                      projectiles=3, projectile_grouping=1.5, fire_rate=0.5, damage=10, spread=3, power_use=5)

basic_reactor = Reactor(name="basic reactor", recharge_rate=10, power_capacity=75,
                        cooling_rate=7.5, heat_capacity=400, heat_inefficiency=1.75, overheat_threshold=0.92)

basic_shield = Shield(name="basic shield", health=40, regen=5, broken_recharge_time=4, recharge_power_ratio=1.5)

player = Player(controls=player_settings.controls)

ai_ship = NPC()

game_obj.player = player

# Initialize game states
game_obj.new_game_state("paused", [guis["pause_gui"]], pause_surface, [player, ])
game_obj.new_game_state("running", [guis["start_gui"]], main_surface, [player, ])
game_obj.new_game_state("playing", [guis["game_gui"]], game_surface, [player, ])

game_obj.set_game_state("running")

# Initialize game_obj attributes
game_obj.screen = screen
game_obj.display = pygame.display
game_obj.clock = clock
game_obj.framerate = 60

player_gui = GUI(pos_x=game_obj.screen.get_width() * 0.42, pos_y=game_obj.screen.get_height() * 0.8, width=250,
                 height=100,
                 hide_text=True, has_border=False)
game_obj.game_states['playing'].guis = [player_gui, ]

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
                                     cooling_modifier=1))
            player.ship.equip_weapon(copy(splinter_gun), 0)
            player.ship.equip_weapon(copy(shotgun), 1)
            player.ship.equip_shield(copy(basic_shield))
            player.ship.equip_reactor(copy(basic_reactor))

            # setup GUI related to player
            # TODO: this should maybe be stored in the player object

            player_gui.elements = []

            player_health_bar = BarElement(high_value=player.ship.health, current_value=player.ship.current_health,
                                           related_object=player.ship, low_position=(0, 20), high_position=(200, 20),
                                           color=(255, 75, 0), width=200, height=20)
            player_shield_bar = BarElement(high_value=player.ship.shield.health,
                                           current_value=player.ship.shield.current_health,
                                           related_object=player.ship, low_position=(0, 40), high_position=(200, 40),
                                           color=(0, 75, 255), width=200, height=20)
            player_power_bar = BarElement(high_value=player.ship.reactor.power_capacity,
                                          current_value=player.ship.reactor.current_power,
                                          related_object=player.ship, low_position=(0, 60), high_position=(200, 60),
                                          color=(255, 255, 0), width=200, height=20)
            player_heat_bar = BarElement(high_value=player.ship.reactor.heat_capacity,
                                         current_value=player.ship.reactor.current_heat,
                                         related_object=player.ship, low_position=(0, 80), high_position=(200, 80),
                                         color=(255, 0, 0), width=200, height=20)

            if player_health_bar not in player_gui.elements:
                player_gui.elements.append(player_health_bar)
            if player_shield_bar not in player_gui.elements:
                player_gui.elements.append(player_shield_bar)
            if player_power_bar not in player_gui.elements:
                player_gui.elements.append(player_power_bar)
            if player_heat_bar not in player_gui.elements:
                player_gui.elements.append(player_heat_bar)

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

            # TODO: this should maybe be taken care of in the player update method
            player_health_bar.current_value = player.ship.current_health
            player_shield_bar.current_value = player.ship.shield.current_health
            player_power_bar.current_value = player.ship.reactor.current_power
            player_heat_bar.current_value = player.ship.reactor.current_heat

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
