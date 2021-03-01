import pygame
import os
import sys

# GuiPyg imports
from guipyg import gui
from guipyg.gui_element.menu import Menu
from guipyg.gui_element.button import Button
from guipyg.gui_element.text_elements import Label

# Initial setup
running = True
playing = False

if os.name == 'posix':
    os.environ['SDL_AUDIODRIVER'] = 'dsp'

os.environ['SDL_VIDEO_CENTERED'] = '1'

SCREENSIZE = (1600, 900)


def toggle_playing():
    # print(not is_playing)
    global playing
    playing = not playing


# Initialize Pygame
pygame.init()
pygame.display.set_caption("Power Core Omega")
screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()

# Initialize Start Menu (GUI)
start_gui = gui.GUI(SCREENSIZE[0], SCREENSIZE[1],
                    theme="blue_theme", name="Start GUI")

start_title = Label(text="Power Core Omega", width=200, height=50)
start_title.pos_x, start_title.pos_y = start_gui.rect.centerx - start_title.width / 2, 50

start_menu = Menu(400, 600, start_gui.rect.centerx - 200, start_gui.rect.centery - 300,
                  name="Start Menu", hide_text=True)

new_game_button = Button(start_menu.width, 50,
                         start_menu.rect.centerx - start_menu.width / 2,
                         20, name="New Game Button", msg="New Game")

quit_game_button = Button(start_menu.width, 50,
                          start_menu.rect.centerx - start_menu.width / 2,
                          90, name="Quit Game Button", msg="Quit Game")

# Button functions
new_game_button.function = new_game_button.StoredFunction(
    module="__main__",
    function="toggle_playing",
    parent=new_game_button
)
quit_game_button.function = quit_game_button.StoredFunction(
    module="sys",
    function="exit",
    parent=quit_game_button
)

start_menu.elements = [new_game_button, quit_game_button]
start_gui.elements = [start_title, start_menu]
start_gui.apply_theme()

if __name__ == '__main__':

    while running:
        # Menu
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

        while playing:
            # Game Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or \
                            event.key == pygame.K_ESCAPE:
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    current_mouse_pos = pygame.mouse.get_pos()
                    pass

                if event.type == pygame.MOUSEBUTTONUP:
                    current_mouse_pos = pygame.mouse.get_pos()
                    pass

            pygame.display.update()
            screen.fill((0, 0, 0))
            clock.tick()

            clock.tick(60)

        start_gui.update(screen)
        pygame.display.update()
        screen.fill((80, 80, 80))
        clock.tick()

        clock.tick(60)
