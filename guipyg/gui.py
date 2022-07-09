import pygame
import json
from json import JSONEncoder
from .gui_element.button import Button
from .gui_element.element import Element
from .gui_element.toggleable_element import ToggleableElement
from .gui_element.popup import Popup
from .gui_element.element_group import ElementGroup
from .gui_element.text_elements import TextBox
from .gui_element.menu import Menu
from .gui_style.style_item import theme_dict

#  TODO: there is probably a better way to store and retrieve these
class_types = {"Element": Element, "Button": Button, "Popup": Popup, "ToggleableElement": ToggleableElement,
               "ElementGroup": ElementGroup, "Menu": Menu, "TextBox": TextBox}


class GUI(ElementGroup):

    def __init__(self, *args, theme=None, color_key=(0, 0, 0), **kwargs):
        # if elements is None:
        self.elements = []
        super().__init__(*args, **kwargs)
        self.hide_text = True
        self.set_colorkey(color_key)
        self.elements_to_update = self.elements
        self.theme = theme  # receives a Theme object from style module, used to stylize all elements
        self.need_update = True
        self.selected_element = None
        self.dragging = None
        self.is_draggable = False
        self.clip_rect = None
        # self.set_clip_area()

    def apply_theme(self):
        if self.theme:
            for theme in theme_dict:
                if self.theme == theme_dict[theme].theme_name:
                    # print(f"found theme {theme}")
                    theme_dict[theme].style_gui(self)
                    self.elements_to_update = self.elements
                    self.apply_theme_to_elements(self.elements)
                    # break

    def apply_theme_to_elements(self, elements):
        for element in elements:
            element.need_update = True
            if hasattr(element, "elements"):
                self.apply_theme_to_elements(element.elements)

    def bring_element_to_front(self, element):
        for index, elements in enumerate(self.elements):
            if elements == element:
                self.elements += [self.elements.pop(index)]

    def fill_elements(self, surface):
        for element in self.elements_to_update:
            element.fill_elements(surface)

        self.elements_to_update = []

    def set_clip_area(self):
        left, top, right, bottom = 0, 0, self.width, self.height
        for element in self.elements:
            if element.rect.left < left:
                left = element.rect.left + element.pos_x
            if element.rect.top < top:
                top = element.rect.top + element.pos_y
            if element.rect.right > right:
                right = element.rect.right + element.pos_x
            if element.rect.bottom > bottom:
                bottom = element.rect.bottom + element.pos_y
        self.clip_rect = pygame.Rect(left, top, right - left, bottom - top)
        self.set_clip(self.clip_rect)

    def update(self,
               screen, need_update=False):  # TODO: there must be a more efficient way to do this than have every function loop over every element
        # screen to blit to
        if self.need_update and self.is_active:
            self.fill((0, 0, 0))
            self.set_clip_area()
            # self.draw_drop_shadows(self)
            self.fill_elements(screen)
            self.draw_text_to_elements()
            self.draw_element_border()
            self.blit_elements()
        screen.blit(self, (self.pos_x, self.pos_y))
        self.need_update = need_update

    def select_element(self, mouse_pos):
        if not self.selected_element:
            reversed_elements = self.elements[::-1]
            for index, element in enumerate(reversed_elements):
                if element.is_visible and element.is_draggable and \
                        element.rect.collidepoint(element.get_mouse_pos(mouse_pos)):
                    element.drag_toggle = True
                    self.selected_element = element
                    self.dragging = self.selected_element.drag_element(mouse_pos)
                    self.bring_element_to_front(element)
                    break

    def drag_selected(self):  # TODO: Figure out solution to drag elements from inside of other element_groups
        if self.selected_element:
            self.selected_element.pos_x, self.selected_element.pos_y = next(self.dragging)
            if self.selected_element.pos_x < 0:
                self.selected_element.pos_x = 0
            elif self.selected_element.pos_x + self.selected_element.width > self.width:
                self.selected_element.pos_x = self.width - self.selected_element.width
            if self.selected_element.pos_y < 0:
                self.selected_element.pos_y = 0
            elif self.selected_element.pos_y + self.selected_element.height > self.height:
                self.selected_element.pos_y = self.height - self.selected_element.height
            self.need_update = True

    def let_go(self):
        if self.selected_element:
            self.selected_element.drag_toggle = False
            next(self.dragging)
            self.selected_element = None
            self.dragging = None

    def activate_selected(self, mouse_pos, *args,
                          **kwargs):  # TODO: This should be changed to enable keyboard shortcuts to access the functions of any elements
        if self.selected_element:
            self.selected_element.click(mouse_pos, *args, **kwargs)
            self.need_update = True
            return True
        else:
            self.need_update = True
            return False


class GUIEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, "function"):
            o.function = encode_function(o.function)
            # print(o.function)
        if hasattr(o, "elements_to_update"):
            # o.elements_to_update = None
            del o.elements_to_update
        if hasattr(o, "__dict__"):
            # print(o.__dict__)
            return o.__dict__
        else:
            pass


def encode_function(function):
    # if function:
    # print(o.function)
    #  TODO: this method should be tidied up a bit
    encoded_function = {'path': function.path, 'module': function.module,
                        'function': function.function, 'baseclass': function.baseclass,
                        'target': function.target, 'parent': function.parent.name,
                        'args': [],
                        'kwargs': {}}
    # print(function.args)
    for arg in function.args:
        if hasattr(arg, "base_type") and arg.base_type == "Element":
            encoded_function['args'] += [arg.name]
        else:
            encoded_function['args'] += [arg]

    for kwarg in function.kwargs:
        if kwarg == 'arg' or kwarg == 'kwarg':
            continue
        if hasattr(kwarg, "base_type") and kwarg.base_type == "Element":
            encoded_function['kwargs'] += {kwarg.dict}
        else:
            encoded_function['kwargs'] += {kwarg}
    # print(encoded_function)
    return encoded_function


# def encode_gui(gui):
#     #  removed indent to reduce json file size (by quite a bit)
#     return json.dumps(gui, skipkeys=True, cls=GUIEncoder)


def save_gui(gui, file):
    with open(file, 'w') as w:
        # json.dump(encode_gui(gui), w)
        json.dump(gui, w, skipkeys=True, cls=GUIEncoder)  # , check_circular=False)


def decode_element(element, gui, cls=Element, class_types=None):
    #  TODO: this should probably be in the 'element' module
    if type(element) != dict:
        # print("Decode")
        element_decode = json.loads(element)
        element_obj = cls(**element_decode)
    else:
        # print(element)
        element_obj = cls(**element)
        # print(element_obj.__dict__)

        if hasattr(element_obj, "elements"):
            for index, element in enumerate(element_obj.elements):
                element_name = element["class_name"]
                obj = decode_element(element, class_types[element_name])
                # print(obj.__dict__)
                element_obj.elements[index] = obj
        if hasattr(element_obj, "function") and element_obj.function:
            # print("has a function")
            # element_obj.function = decode_function(element_obj.function, element_obj, gui)
            decode_function(element_obj.function, element_obj, gui)
        if element_obj.base_type == "StoredFunction":
            decode_function(element_obj, gui)

    # print(element_obj.__dict__)
    return element_obj


def decode_function(function, gui):
    # TODO: currently functions are either not being decoded, or aren't being attached to their respective elements
    if function['parent'] is not None:
        # function['parent'] = element

        for arg in function.args:
            for element in gui.elements:
                new_arg = check_for_element(arg, element)
                function['args'] += [new_arg]
            # print(function.args)
        for element in gui.elements:
            if function['parent'] == element.name:
                function_obj = element.StoredFunction(**function)
                # print(function_obj.__dict__)
        # return function_obj
                element.function = function_obj

# def decode_function(function, element, gui):
#     if function['parent'] is not None:
#         function['parent'] = element
#
#     for arg in function.args:
#         for element in gui.elements:
#             new_arg = check_for_element(arg, element)
#             function['args'] += [new_arg]
#         print(function.args)
#     function_obj = element.StoredFunction(**function)
#     print(function_obj.__dict__)
#     # return function_obj
#     element.function = function_obj


def check_for_element(check_for, element):
    if check_for in element:
        return element
    else:
        if hasattr(element, "elements"):
            check_for_element(check_for, element.elements)
        else:
            return check_for


def load_gui(file):
    with open(file, 'r') as r:
        gui_json = json.load(r)
    gui = decode_gui(gui_json)
    gui.apply_theme()
    return gui


def decode_gui(gui):
    # gui_decoded = json.loads(gui)
    # gui_obj = GUI(**gui_decoded)
    gui_obj = GUI(**gui)

    for index, element in enumerate(gui_obj.elements):
        element_name = element["class_name"]
        obj = decode_element(element, gui_obj, class_types[element_name], class_types)
        gui_obj.elements[index] = obj

    return gui_obj
