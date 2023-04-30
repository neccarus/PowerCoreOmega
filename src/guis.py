from cx_Freeze import module

from guipyg.gui_element.menu import Menu
from guipyg.gui_element.button import Button
from guipyg.gui_element.text_elements import Label
from guipyg import gui
from . import game_obj
from . import player_settings

# guis stores all guis for easy access
guis = {}

# Initialize Start Menu (GUI) - start_gui
start_gui = gui.GUI(player_settings.screensize[0], player_settings.screensize[1],
                    theme="blue_theme", name="Start GUI")

start_title = Label(text="Power Core Omega", width=200, height=50)
start_title.has_border = False
start_title.pos_x, start_title.pos_y = start_gui.rect.centerx - start_title.width / 2, 50

start_menu = Menu(400, 600, start_gui.rect.centerx - 200, start_gui.rect.centery - 300,
                  name="Start Menu", hide_text=True)

new_game_button = Button(start_menu.width, 50,
                         start_menu.rect.centerx - start_menu.width / 2,
                         20, name="New Game Button", msg="New Game")

settings_button = Button(start_menu.width, 50,
                         start_menu.rect.centerx - start_menu.width / 2,
                         90, name="Settings Button", msg="Settings")

quit_game_button = Button(start_menu.width, 50,
                          start_menu.rect.centerx - start_menu.width / 2,
                          160, name="Quit Game Button", msg="Quit Game")

# Button functions
new_game_button.function = new_game_button.StoredFunction(
    module="src.game",
    function="toggle_playing",
    target="game",
    parent=game_obj,
    args=[game_obj]
)

settings_button.function = settings_button.StoredFunction(
    module="src.game",
    function="configure_settings",
    target="game",
    parent=settings_button,
)

quit_game_button.function = quit_game_button.StoredFunction(
    module="sys",
    function="exit",
    parent=quit_game_button
)

start_menu.elements = [new_game_button, settings_button, quit_game_button]
start_gui.elements = [start_title, start_menu]
start_gui.apply_theme()
# end of start_gui

# Initialize Settings Menu (GUI) - settings_gui
settings_gui = gui.GUI(player_settings.screensize[0], player_settings.screensize[1],
                       theme="blue_theme", name="Settings GUI")

settings_title = Label(text="Settings", width=200, height=50)
settings_title.has_border = False
settings_title.pos_x, settings_title.pos_y = start_gui.rect.centerx - settings_title.width / 2, 50

settings_menu = gui.GUI(400, 600, settings_gui.rect.centerx - 200,
                        settings_gui.rect.centery - 300, name="Settings Menu",
                        hide_text=True)

back_button = Button(settings_menu.width, 50,
                     settings_menu.rect.centerx - settings_menu.width / 2,
                     20, name="Back Button", msg="Back")

# Button functions
back_button.function = back_button.StoredFunction(
    module="src.game",
    function="back",
    target="game",
    parent=back_button,
)

settings_menu.elements = [back_button]
settings_gui.elements = [settings_title, settings_menu]
settings_gui.apply_theme()

# Initialize Pause Menu (GUI) - pause_gui
pause_gui = gui.GUI(player_settings.screensize[0], player_settings.screensize[1], theme="my_theme",
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
    args=[game_obj]
)

pm_quit_game_button.function = pm_quit_game_button.StoredFunction(
    module="sys",
    function="exit",
    parent=pm_quit_game_button
)

pause_menu.elements = [continue_button, main_menu_button, pm_quit_game_button]
pause_gui.elements = [pause_menu]
pause_gui.apply_theme()

guis["start_gui"] = start_gui
guis["pause_gui"] = pause_gui
guis["game_gui"] = None
guis["settings_gui"] = settings_gui
