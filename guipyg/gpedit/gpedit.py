import os
import pygame
import sys
import json

from guipyg import gui
from guipyg.gui_element.menu import Menu
from guipyg.gui_element.button import Button
from guipyg.gui_element.element import ElementDecorators

if os.name == 'posix':
    os.environ['SDL_AUDIODRIVER'] = 'dsp'


def empty_func(*_, **__):
    print("Click")


# @ElementDecorators.toggle_visibility_wrapper(function=)
def toggle_menus(elements, target, *_, **__):
    for element in elements:
        if element.is_visible and element.name != "GPEdit_Menu":
            element.toggle_visibility()
    # TODO: currently does not toggle the menu off if it is on
    target.toggle_visibility()


def click_away(elements, *_, **__):
    for element in elements:
        print(element.name)
        if element.is_visible and element.name != "GPEdit_Menu":
            element.toggle_visibility()


screensize = (1280, 720)
pygame.init()
screen = pygame.display.set_mode(screensize)
clock = pygame.time.Clock()

# build the GUI
gpe_window = gui.GUI(*screensize, name="GPEdit", theme="blue_theme")
gpe_menu = Menu(gpe_window.width, 20, 0, 0, "GPEdit_Menu", hide_text=True)

# File Menu setup
file_button = Button(100, 20, 0, 0, name="File_Button", msg="File")
file_menu = Menu(200, 500, file_button.pos_x, file_button.rect.bottom, name="File_Menu", hide_text=True, is_visible=False)
file_button.function = file_menu.toggle_visibility
save_button = Button(file_menu.width, 20, 0, 0, name="Save_Button", msg="Save", function=empty_func)
save_as_button = Button(file_menu.width, 20, 0, 20, name="Save_As_Button", msg="Save As...", function=empty_func)
load_button = Button(file_menu.width, 20, 0, 40, name="Load_Button", msg="Load", function=empty_func)
file_menu.elements = [save_button, save_as_button, load_button]

# Edit Menu setup
edit_button = Button(100, 20, 100, 0, name="Edit_Button", msg="Edit", function=empty_func)

# New Menu setup
new_button = Button(100, 20, 200, 0, name="New_Button", msg="New")
new_menu = Menu(200, 500, new_button.pos_x, new_button.rect.bottom, name="New_Menu", hide_text=True, is_visible=False)

new_element_button = Button(new_menu.width, 20, 0, 0, name="New_Element_Button", msg="New Element", function=empty_func)
new_menu.elements = [new_element_button]


gpe_menu.elements = [file_button, edit_button, new_button]

gpe_window.elements += [gpe_menu, file_menu, new_menu]

#button functions
save_button.function = save_button.StoredFunction(module="__main__", function="empty_func", parent=new_button)
save_as_button.function = save_as_button.StoredFunction(module="__main__", function="empty_func", parent=save_as_button)
load_button.function = load_button.StoredFunction(module="__main__", function="empty_func", parent=load_button)
edit_button.function = edit_button.StoredFunction(module="__main__", function="empty_func", parent=edit_button)
file_button.function = file_button.StoredFunction(module="__main__", function="toggle_menus", parent=file_button,
                                                  args=(gpe_window.elements, gpe_window.elements[gpe_window.elements.index(file_menu)]))
new_button.function = new_button.StoredFunction(module="__main__", function="toggle_menus", parent=new_button,
                                                args=(gpe_window.elements, gpe_window.elements[gpe_window.elements.index(new_menu)]))
new_element_button.function = new_element_button.StoredFunction(module="__main__", function="empty_func", parent=new_element_button)

gpe_window.apply_theme()

if __name__ == "__main__":

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                current_mouse_pos = pygame.mouse.get_pos()
                gpe_window.select_element(current_mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                current_mouse_pos = pygame.mouse.get_pos()
                if not gpe_window.activate_selected(current_mouse_pos):
                    click_away(gpe_window.elements)
                gpe_window.let_go()
                gpe_window.need_update = True

        gpe_window.update(screen)

        pygame.display.update()

        screen.fill((80, 80, 85))

        clock.tick()
