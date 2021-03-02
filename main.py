import pygame
import os
import sys
from src import game_obj
from src import game
from src import SCREENSIZE
from src.guis import guis

running = True

if os.name == 'posix':
    os.environ['SDL_AUDIODRIVER'] = 'dsp'

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Power Core Omega")
screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()

if __name__ == '__main__':

    while running:

        # TODO: implement system in GuiPyg for handling basic menu events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            game_obj.handle_events(event, [guis["start_gui"]])

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
                        game.toggle_pause(game_obj)

            while game_obj.paused:
                # Pause Loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    game_obj.handle_events(event, [guis["pause_gui"]])

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game.toggle_pause(game_obj)

                # Update pause loop
                game_obj.update([guis["pause_gui"]], display=pygame.display, screen=screen,
                                fill_color=(80, 80, 80), clock=clock, framerate=60)

            # Update game loop
            game_obj.update(display=pygame.display, screen=screen,
                            fill_color=(0, 0, 0), clock=clock, framerate=60)

        # Update main menu loop
        game_obj.update([guis["start_gui"]], display=pygame.display, screen=screen,
                        fill_color=(80, 80, 80), clock=clock, framerate=60)

