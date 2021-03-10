import pygame
import os
import sys
from src import game_obj
from src import player_settings
from src.player import Player
# from src import SCREENSIZE
from src.guis import guis


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

player = Player(controls=player_settings.controls)

# Apply player object to game object
game_obj.bodies.add(player.ship)
game_obj.controllers.append(player)

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
