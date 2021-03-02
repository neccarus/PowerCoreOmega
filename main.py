import pygame
import os
import sys
from src import game_obj
from src import game
from src import SCREENSIZE
from src.guis import start_gui, pause_gui

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or \
                        event.key == pygame.K_ESCAPE:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                current_mouse_pos = pygame.mouse.get_pos()
                start_gui.select_element(current_mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                current_mouse_pos = pygame.mouse.get_pos()
                start_gui.activate_selected(current_mouse_pos, start_gui)
                start_gui.let_go()

        while game_obj.playing:
            # Game Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.toggle_pause(game_obj)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_mouse_pos = pygame.mouse.get_pos()
                    pass

                if event.type == pygame.MOUSEBUTTONUP:
                    current_mouse_pos = pygame.mouse.get_pos()
                    pass

            while game_obj.paused:
                # Pause Loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game.toggle_pause(game_obj)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        current_mouse_pos = pygame.mouse.get_pos()
                        pause_gui.select_element(current_mouse_pos)

                    if event.type == pygame.MOUSEBUTTONUP:
                        current_mouse_pos = pygame.mouse.get_pos()
                        pause_gui.activate_selected(current_mouse_pos, start_gui)
                        pause_gui.let_go()

                pause_gui.update(screen)
                pygame.display.update()
                screen.fill((80, 80, 80))
                clock.tick()

                clock.tick(60)

            pygame.display.update()
            screen.fill((0, 0, 0))
            clock.tick()

            clock.tick(60)

        start_gui.update(screen)
        pygame.display.update()
        screen.fill((80, 80, 80))
        clock.tick()

        clock.tick(60)
