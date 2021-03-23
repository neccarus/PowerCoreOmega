import pygame
import json
from json import JSONEncoder
from guipyg.gui_style.style_item import style_dict
from guipyg.utils.utils import Instance
import importlib
import functools


class Element(pygame.Surface, Instance):
    id_ = 0
    # dict structure {element.name: element}
    _element_dict = {}

    _active_elements = []  # list all active elements
    # TODO: need to make use of active_elements or remove it

    @classmethod
    def my_name(cls):
        return cls.__name__

    @classmethod
    def new_id(cls, element):
        element.id_ = cls.id_
        cls.id_ += 1

    def update(self, *args, **kwargs):

        pass

    # @classmethod
    # def new_element(cls, element):
    #     cls._element_dict[element.name] = element
    #
    # @classmethod
    # def activate_element(cls, element):
    #     cls._active_elements.append(element)
    #
    # @classmethod
    # def deactivate_element(cls, element):
    #     cls._active_elements.remove(element)

    def class_name(self):
        return self.__class__.__name__

    def set_style(self):
        for style in style_dict:
            if self.style == style_dict[style].style_name:
                style_dict[style].style_element(self)

    # def set_drop_shadow(self):
    #     self.drop_shadow_thickness = (max(self.drop_shadow_left, self.drop_shadow_right,
    #                                       self.drop_shadow_top, self.drop_shadow_bottom)
    #                                   + self.corner_rounding)
    #     self.drop_shadow_rect = pygame.Rect(0, 0,
    #                                         self.width + self.drop_shadow_right + self.drop_shadow_left,
    #                                         self.height + self.drop_shadow_bottom + self.drop_shadow_top)
    #
    #     self.drop_shadow_rect.center = self.pos_x + (self.width // 2), self.pos_y + (self.height // 2)
        # self.drop_shadow_rect.center = self.rect.center

    # TODO: all inherited classes need to make proper use of **kwargs instead of writing them in each and every __init__
    # TODO: offer an alternative placement of argument "center" to be able to center the Element when placed
    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, name="Element", msg="", color=(255, 255, 255), style=None,
                 is_visible=True, font_color=(10, 10, 10), hide_text=False, **_):
        super().__init__((width, height), pygame.HWSURFACE)
        super().add_instance()
        self.base_type = "Element"
        Element.new_id(self)
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = name
        # Element.new_element(self)
        self.msg = msg
        self.color = color
        self.style = style
        self.is_visible = is_visible
        self.border_thickness = 1
        self.border_color = (1, 1, 1)
        self.corner_rounding = 0
        self.margin_top = 0
        self.margin_bottom = 0
        self.margin_left = 0
        self.margin_right = 0
        self.rect = self.get_rect()
        self.rect.width -= abs((self.border_thickness % 2) - 1)
        self.rect.height -= abs((self.border_thickness % 2) - 1)
        self.content_rect = pygame.Rect((self.margin_left,
                                         self.margin_top),
                                        (self.width - self.margin_right - self.border_thickness,
                                         self.height - self.margin_bottom - self.border_thickness))
        self.content_surface = pygame.Surface((abs(self.content_rect.width), abs(self.content_rect.height)))
        self.content_surface.set_colorkey(self.color)  # elements exhibit a weird behaviour without this
        self.class_name = self.my_name()
        self.font = pygame.font.SysFont("times new roman", 22)
        self.font_pos_x = 10
        self.font_pos_y = 0
        self.font_color = font_color
        self.text_obj = self.font.render(self.name, True, self.font_color)
        self.text_rect = self.text_obj.get_rect()
        self.text_rect.topleft = (self.font_pos_x, self.font_pos_y)
        # colorkey and fill to prevent weird behaviour on corners when there is corner rounding
        self.set_colorkey((0, 0, 0))
        self.fill((0, 0, 0), self.rect)
        self.has_border = True
        self.is_draggable = False
        self.drag_toggle = False
        self.set_style()
        self.need_update = True

        # hide text can be toggled, will prevent draw_text() from executing on this element
        self.hide_text = hide_text

        #  'parent' and 'children' attributes could be used for rendering efficiency?
        self.parent = None
        self.children = []

        #  TODO: should rethink drop shadow code, may do it as a class inside of 'Element'
        # self.has_drop_shadow = False
        # self.drop_shadow_right = 0
        # self.drop_shadow_left = 0
        # self.drop_shadow_top = 0
        # self.drop_shadow_bottom = 0
        # self.drop_shadow_thickness = 0
        # self.drop_shadow_alpha = 255
        # self.drop_shadow_color = (0, 0, 0, self.drop_shadow_alpha)
        # self.drop_shadow_rect = pygame.Rect(self.pos_x - self.drop_shadow_left,
        #                                     self.pos_y - self.drop_shadow_top,
        #                                     self.width + self.drop_shadow_right,
        #                                     self.height + self.drop_shadow_bottom)
        # self.drop_shadow_surface = pygame.Surface((self.width + self.drop_shadow_right + self.drop_shadow_left,
        #                                            self.height + self.drop_shadow_bottom + self.drop_shadow_top))
        # self.drop_shadow_position = self.rect.center # TODO: needs to be in relation to the element's parent, not the elements itself
        # self.set_drop_shadow()
        self.is_active = True
        # Element.activate_element(self)
        # print(f"{self.my_name()}: {self.id_}")

    def __str__(self):
        return f"{self.name}"

    def __del__(self):
        self.is_active = False
        #Element.deactivate_element(self)
        if self in Element._element_dict:
            Element._element_dict.pop(self.name)

    def toggle_hide_text(self, toggle_to):
        if toggle_to:
            self.hide_text = toggle_to
        else:
            self.hide_text = not self.hide_text

    def click(self, *args, **kwargs):
        return None

    def get_mouse_pos(self, mouse_pos=(0, 0)):
        # for compatibility with ElementGroup
        return mouse_pos

    def toggle_visibility(self, *_, **__):
        self.is_visible = not self.is_visible

    def fill_elements(self, surface):
        if self.need_update:
            # self.set_drop_shadow()
            # self.draw_drop_shadow()
            if not self.corner_rounding:
                self.fill(self.color, self.rect)
                self.content_surface.fill(self.color, self.content_rect)

            elif self.corner_rounding:
                pygame.draw.rect(self, self.color, self.rect, border_radius=self.corner_rounding)
                pygame.draw.rect(self.content_surface, self.color, self.content_rect,
                                 border_radius=self.corner_rounding)

    # def draw_drop_shadow(self):
    #     if self.need_update:
    #         if not self.corner_rounding:
    #             self.drop_shadow_surface.fill(self.drop_shadow_color, self.drop_shadow_rect)
    #
    #         elif self.corner_rounding:
    #             pygame.draw.rect(self, self.drop_shadow_color, self.drop_shadow_rect, border_radius=self.corner_rounding)

    # def blit_drop_shadow(self, surface):
    #     if self.need_update and self.has_drop_shadow:
    #         surface.blit(self.drop_shadow_surface, self.drop_shadow_rect.topleft)

    def blit_elements(self):
        if self.need_update:
            self.blit(self.content_surface, self.content_rect.topleft)
            self.need_update = False

    def draw_element_border(self):
        if self.need_update:
            pygame.draw.rect(self, self.border_color,
                             (0, 0, self.width - abs((self.border_thickness % 2) - 1),
                              self.height - abs((self.border_thickness % 2) - 1)),
                             self.border_thickness, border_radius=self.corner_rounding)

    def draw_text_to_elements(self):
        if self.need_update:
            self.draw_text(self.content_surface)

    def draw_text(self, surface):
        if not self.hide_text:
            surface.blit(self.text_obj, self.text_rect)

    def drag_element(self, mouse_pos=(0, 0)):
        mouse_pos_start = mouse_pos
        element_pos_x = self.pos_x
        element_pos_y = self.pos_y

        while self.drag_toggle:
            current_mouse_pos = pygame.mouse.get_pos()
            mouse_pos_delta = (current_mouse_pos[0] - mouse_pos_start[0], current_mouse_pos[1] - mouse_pos_start[1])
            element_pos_delta_x, element_pos_delta_y = (element_pos_x + mouse_pos_delta[0],
                                                        element_pos_y + mouse_pos_delta[1])
            yield element_pos_delta_x, element_pos_delta_y
        yield None

    class StoredFunction:

        def __init__(self, path="", module="", function=None, baseclass=None, target=None, parent=None, *args, **kwargs):
            self.base_type = "StoredFunction"
            self.path = path  # directory this function is found in
            self.module = module  # module this function is found in
            self.function = function
            self.baseclass = baseclass  # baseclass is used when referencing static methods, a class within the module
            # TODO: should find a better way to reference other object's than using their name, may need to make a simple baseclass for other classes to inherit from
            self.target = target  # target of the function by name
            self.parent = parent
            # print(f"kwargs: {[*kwargs]}")
            if args:
                self.args = [*args]
            else:
                self.args = []

            if kwargs:
                self.kwargs = {**kwargs}
                self.args += [*self.kwargs['args']]
                if "kwargs" in self.kwargs:
                    self.kwargs.pop('kwargs')
            else:
                self.kwargs = {}

            # for arg in [*self.args]:
            #     print(f"comparing {arg} to {[*self.kwargs['args']]}")
            #     if arg in [*self.kwargs["args"]]:
            #         print(f"deleting {arg}")
            #         self.kwargs.pop(arg)

            if "args" in self.kwargs:
                self.kwargs.pop("args")
                print(f"args: {self.args} kwargs: {self.kwargs}")

            #  if there is a target, the stored function should be a reference to that instance of the function
            #  this also means it is not a static method
            if self.target:
                self.object_reference = self.find_target(self.parent.get_instances())
                print(self.object_reference.name)
                self.stored_function = getattr(self.object_reference, self.function)

            #  if there is no target, then the function is just part of a module, but it could be a static method
            else:
                if self.baseclass:
                    self.stored_function = getattr(self.import_static(), str(self.function))
                else:
                    self.stored_function = getattr(self.import_module(), str(self.function))

        # TODO: functions don't seem to be working from json files again
        # TODO: if the function being called has a return value, we should try and handle the internally
        def __call__(self, *args, **kwargs):
            if args or kwargs:
                # print(self.args)
                # print(*self.kwargs["args"])
                return self.stored_function(*self.args, **self.kwargs)
            else:
                print("no args given")
                return self.stored_function(*args, **kwargs)

        def find_target(self, instances):
            # Users should have their classes they want referenced inheriting from
            # guipyg.utils.utils.Instance

            for instance in instances:
                if self.target == instance.name:
                    target_obj = instance
                    return target_obj

        def import_module(self):
            importlib.invalidate_caches()
            if self.path:
                return importlib.import_module(self.module, self.path)
            else:
                return importlib.import_module(self.module)

        def import_static(self):
            module = self.import_module()
            if self.baseclass in dir(module):
                return getattr(module, self.baseclass)


class ElementDecorators(object):

    @classmethod
    def toggle_visibility_wrapper(cls):
        """Activates function parameter before self.toggle_visibility()"""
        def wrapper(function):
            @functools.wraps(function)
            def wrapper_args(*args, **kwargs):
                print(*args)
                print(**kwargs)
                return function(*args, **kwargs)

            cls.toggle_visibility()
            return wrapper_args

        return wrapper


class ElementEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, "_id"):
            del o._id
        return o.__dict__


def encode_element(element):
    return json.dumps(element, cls=ElementEncoder)
