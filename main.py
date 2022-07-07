# import tracemalloc
# tracemalloc.start()

import pygame
import sys
from src import game_obj, screen
from src import player_settings
from src.ship import Ship
from src.player import Player
from src.npc import NPC
from src.weapons import Weapon
from src.shields import Shield
from src.reactors import Reactor
from src.guis import guis
from copy import copy
from guipyg.gui import GUI
from guipyg.gui_element.graph_elements import BarElement
from src.projectile import Explosion
from guipyg.gui_element.text_elements import Label
from src.game import Spawner
import random

main_surface = pygame.Surface(size=player_settings.screensize)
game_surface = pygame.Surface(size=player_settings.screensize)
pause_surface = pygame.Surface(size=player_settings.screensize)

clock = pygame.time.Clock()

shotgun = Weapon(name="shotgun", projectile_color=(255, 255, 0), damage=5, spread=8, projectiles=10,
                 projectile_grouping=3, fire_rate=1, speed=800, power_use=10)

blaster = Weapon(name="blaster", damage=5, spread=0.6, fire_rate=0.15, speed=1100)

splinter_gun = Weapon(name="splinter gun", projectile_color=(255, 150, 0), projectile_size=(4,),
                      projectiles=3, projectile_grouping=1.5, fire_rate=0.5, speed=950, damage=10, spread=3, power_use=5)

plasma_launcher = Weapon(name="plasma launcher", projectile_color=(50, 255, 10), projectile_size=(6,),
                         projectiles=1, fire_rate=1.5, damage=25, spread=1, power_use=12, speed=600,
                         effects=[Explosion(radius=50, explosion_lifetime=0.25, direct_damage=20,
                                            damage_over_time=40, duration=4, color=(170, 200, 20)), ])

weapon_list = [shotgun, blaster, splinter_gun, plasma_launcher]

basic_reactor = Reactor(name="basic reactor", recharge_rate=10, power_capacity=75,
                        cooling_rate=7.5, heat_capacity=400, heat_inefficiency=1.75, overheat_threshold=0.92)
advanced_reactor = Reactor(name="advanced reactor", recharge_rate=24, power_capacity=200,
                           cooling_rate=16, heat_capacity=500, heat_inefficiency=1.6, overheat_threshold=0.94)

reactor_list = [basic_reactor, advanced_reactor]

basic_shield = Shield(name="basic shield", health=40, regen=5, broken_recharge_time=4, recharge_power_ratio=1.5)
advanced_shield = Shield(name="advanced shield", health=140, regen=8, broken_recharge_time=5, recharge_power_ratio=1.65)
turbo_shield = Shield(name='turbo shield', health=65, regen=18, broken_recharge_time=2.5, recharge_power_ratio=1.8)

shield_list = [basic_shield, advanced_shield, turbo_shield]

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

player_gui = GUI(pos_x=game_obj.screen.get_width() * 0.85, pos_y=game_obj.screen.get_height() * 0.85, width=200,
                 height=100, hide_text=True, has_border=False)
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
            player.acquire_ship(Ship(pos=(800, 800), weapon_locations=[(-10, 2), (10, 2), (-19, 6), (19, 6), (-27, 9), (27, 9)],
                                     cooling_modifier=1.45))
            player.ship.equip_weapon(copy(splinter_gun), 0)
            player.ship.equip_weapon(copy(splinter_gun), 1)
            player.ship.equip_weapon(copy(splinter_gun), 2)
            player.ship.equip_weapon(copy(splinter_gun), 3)
            player.ship.equip_weapon(copy(splinter_gun), 4)
            player.ship.equip_weapon(copy(splinter_gun), 5)
            player.ship.equip_shield(copy(advanced_shield))
            player.ship.equip_reactor(copy(advanced_reactor))

            # setup GUI related to player
            # TODO: this should maybe be stored in the player object

            player_gui.elements = []

            player_health_label = Label(text="Health", pos_x=0, pos_y=0, height=20, width=100, font_color=(0, 255, 0),
                                        font_size=20)
            player_shield_label = Label(text="Shield", pos_x=0, pos_y=20, height=20, width=100, font_color=(0, 75, 255),
                                        font_size=20)
            player_power_label = Label(text="Power", pos_x=0, pos_y=40, height=20, width=100, font_color=(255, 255, 0),
                                       font_size=20)
            player_heat_label = Label(text="Heat", pos_x=0, pos_y=60, height=20, width=100, font_color=(255, 0, 0),
                                      font_size=20)
            player_health_bar = BarElement(high_value=player.ship.health, current_value=player.ship.current_health,
                                           related_object=player.ship, low_position=(100, 0), high_position=(200, 20),
                                           color=(0, 255, 0), width=100, height=20)
            player_shield_bar = BarElement(high_value=player.ship.shield.health,
                                           current_value=player.ship.shield.current_health,
                                           related_object=player.ship, low_position=(100, 20), high_position=(200, 40),
                                           color=(0, 75, 255), width=100, height=20)
            player_power_bar = BarElement(high_value=player.ship.reactor.power_capacity,
                                          current_value=player.ship.reactor.current_power,
                                          related_object=player.ship, low_position=(100, 40), high_position=(200, 60),
                                          color=(255, 255, 0), width=100, height=20)
            player_heat_bar = BarElement(high_value=player.ship.reactor.heat_capacity,
                                         current_value=player.ship.reactor.current_heat,
                                         related_object=player.ship, low_position=(100, 60), high_position=(200, 80),
                                         color=(255, 0, 0), width=100, height=20)

            player_gui.elements.append(player_health_label)
            player_gui.elements.append(player_shield_label)
            player_gui.elements.append(player_power_label)
            player_gui.elements.append(player_heat_label)
            if player_health_bar not in player_gui.elements:
                player_gui.elements.append(player_health_bar)
            if player_shield_bar not in player_gui.elements:
                player_gui.elements.append(player_shield_bar)
            if player_power_bar not in player_gui.elements:
                player_gui.elements.append(player_power_bar)
            if player_heat_bar not in player_gui.elements:
                player_gui.elements.append(player_heat_bar)

            enemy = NPC(faction='enemy')
            enemy.acquire_ship(Ship(pos=(800, 100), weapon_locations=[(-5, 2), (5, 2)]))
            enemy.ship.equip_weapon(copy(plasma_launcher), 0)
            enemy.ship.equip_weapon(copy(plasma_launcher), 1)
            enemy.equip_shield(copy(basic_shield))
            enemy.ship.equip_reactor(copy(basic_reactor))

            enemy2 = NPC(faction='enemy')
            enemy2.acquire_ship(Ship(pos=(300, 200), weapon_locations=[(-5, 2), (5, 2)]))
            enemy2.ship.equip_weapon(copy(blaster), 0)
            enemy2.ship.equip_weapon(copy(blaster), 1)
            enemy2.equip_shield(copy(basic_shield))
            enemy2.ship.equip_reactor(copy(basic_reactor))

            # Apply player object to game object
            game_obj.bodies.append(player.ship) #, enemy.ship, enemy2.ship)
            game_obj.bodies.append(enemy.ship)
            game_obj.bodies.append(enemy2.ship)
            game_obj.explosions = pygame.sprite.Group()
            # game_obj.shields = pygame.sprite.Group()
            game_obj.ai_controllers.append(enemy)
            game_obj.ai_controllers.append(enemy2)
            game_obj.spawner = Spawner(1, pygame.Vector2(200, 200), 10000,
                                       Ship(weapon_locations=[(-5, 2), (5, 2)],),
                                            # weapons=[(weapon, slot) for weapon, slot in [(copy(random.choice(weapon_list)), 0), (copy(random.choice(weapon_list)), 1)]]),
                                       amount_to_spawn=1000,
                                       weapon_selection=weapon_list,
                                       shield_selection=shield_list,
                                       reactor_selection=reactor_list,
                                       x_pos_min=10, x_pos_max=game_obj.screen.get_width()-10,
                                       y_pos_min=50, y_pos_max=300)

        while game_obj.playing:

            # current, peak = tracemalloc.get_traced_memory()
            # print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")

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

    # tracemalloc.stop()
