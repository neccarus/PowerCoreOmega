from guipyg.gui_element.menu import Menu
from guipyg.gui_element.button import Button
from guipyg.gui_element.text_elements import Label
from guipyg import gui
from . import game_obj
from . import SCREENSIZE

# guis stores all guis for easy access
guis = {}

# Initialize Start Menu (GUI) - start_gui
start_gui = gui.GUI(SCREENSIZE[0], SCREENSIZE[1],
                    theme="blue_theme", name="Start GUI")

start_title = Label(text="Power Core Omega", width=200, height=50)
start_title.has_border = False
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
    module="src.game",
    function="toggle_playing",
    target="game",
    parent=game_obj,
    args=[game_obj]
)
quit_game_button.function = quit_game_button.StoredFunction(
    module="sys",
    function="exit",
    parent=quit_game_button
)

start_menu.elements = [new_game_button, quit_game_button]
start_gui.elements = [start_title, start_menu]
start_gui.apply_theme()
# end of start_gui

# Initialize Pause Menu (GUI) - pause_gui
pause_gui = gui.GUI(SCREENSIZE[0], SCREENSIZE[1], theme="my_theme",
                    name="Pause Gui")

pause_menu = Menu(400, 600, pause_gui.rect.centerx - 200,
                  pause_gui.rect.centery - 300, name="Start Menu",
                  hide_text=True)

continue_button = Button(pause_menu.width, 50,
                         pause_menu.rect.centerx - pause_menu.width / 2,
                         20, name="Continue Button", msg="Continue")

main_menu_button = Button(pause_menu.width, 50,
                          pause_menu.rect.centerx - pause_menu.width / 2,
                          90, name="Main Menu Button", msg="Quit to Main Menu")

pm_quit_game_button = Button(pause_menu.width, 50,
                             pause_menu.rect.centerx - pause_menu.width / 2,
                             160, name="Quit Game Button", msg="Quit to Desktop")

# Button functions
continue_button.function = continue_button.StoredFunction(
    module="src.game",
    function="toggle_pause",
    target="game",
    parent=continue_button,
    args=[game_obj]
)

main_menu_button.function = main_menu_button.StoredFunction(
    module="src.game",
    function="exit_game_loop",
    target="game",
    parent=main_menu_button,
    args=[game_obj])

pm_quit_game_button.function = pm_quit_game_button.StoredFunction(
    module="sys",
    function="exit",
    parent=quit_game_button)

pause_menu.elements = [continue_button, main_menu_button, pm_quit_game_button]
pause_gui.elements = [pause_menu]
pause_gui.apply_theme()

guis["start_gui"] = start_gui
guis["pause_gui"] = pause_gui
