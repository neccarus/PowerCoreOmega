# this module contains classes and functions to help with styling GUI objects
import pygame


class Style(object):

    def __init__(self):
        self.base_type = "Style"
        self.style_name = "default"
        self.margin_left = 0
        self.margin_right = 0
        self.margin_top = 0
        self.margin_bottom = 0
        self.has_border = False
        self.background_color = (255, 255, 255)
        self.alpha = 255
        self.border_thickness = 0
        self.border_color = (0, 0, 0)
        self.corner_rounding = 0
        # self.has_drop_shadow = False
        # self.drop_shadow_top = 0
        # self.drop_shadow_bottom = 0
        # self.drop_shadow_left = 0
        # self.drop_shadow_right = 0
        # self.drop_shadow_color = (0, 0, 0)
        # self.drop_shadow_alpha = 0

    def style_element(self, element):
        element.margin_left, element.margin_right = self.margin_left, self.margin_right
        element.margin_top, element.margin_bottom = self.margin_top, self.margin_bottom
        element.has_border = self.has_border
        element.color = self.background_color
        element.set_alpha(self.alpha)
        element.border_thickness = self.border_thickness
        element.border_color = self.border_color
        element.corner_rounding = self.corner_rounding
        # element.has_drop_shadow = self.has_drop_shadow
        # element.drop_shadow_top = self.drop_shadow_top
        # element.drop_shadow_bottom = self.drop_shadow_bottom
        # element.drop_shadow_left = self.drop_shadow_left
        # element.drop_shadow_right = self.drop_shadow_right
        # element.drop_shadow_color = self.drop_shadow_color
        # element.drop_shadow_alpha = self.drop_shadow_alpha
        element.rect = element.get_rect()
        element.fill((0, 0, 0), element.rect) # fill element before changing dimensions to avoid anomalies
        element.rect.width -= abs((element.border_thickness % 2) - 1) # TODO: this should probably be an Element side method
        element.rect.height -= abs((element.border_thickness % 2) - 1) # TODO: this should probably be an Element side method
        element.content_rect = pygame.Rect((element.margin_left,  # TODO: this should probably be an Element side method
                                            element.margin_top),
                                           (element.width - element.margin_right - element.border_thickness,
                                            element.height - element.margin_bottom - element.border_thickness))
        element.content_surface = pygame.Surface((abs(element.content_rect.width), abs(element.content_rect.height))) # TODO: this should probably be an Element side method
        if element.class_name == "TextBox":
            element.get_text_box()
        element.content_surface.set_colorkey(element.color)
        # element.set_drop_shadow()

class FontStyle(Style):

    def __init__(self):
        super().__init__()
        self.base_type = "FontStyle"
        self.font = "arial black"
        self.font_size = 14
        self.font_italic = False
        self.font_bold = False
        self.font_underline = False
        self.text_wrapping = True

    def style_text(self, element):
        element.font = self.font
        element.font_size = self.font_size
        element.font_italic = self.font_italic
        element.font_bold = self.font_bold
        element.font_underline = self.font_underline
        element.text_wrapping = self.text_wrapping


class Theme:
    # Pass Theme object to GUI to stylize all elements within the GUI

    def __init__(self, theme_name, element_group_style, element_style, element_group_font=None, element_font=None):
        self.theme_name = theme_name
        self.element_group_style = element_group_style
        self.element_style = element_style
        self.element_group_font = element_group_font
        self.element_font = element_font

    def style_gui(self, gui):
        for element in gui.elements:
            if element.class_name == "Menu" or element.class_name == "ElementGroup" or element.class_name == "PopUp":
                self.element_group_style.style_element(element)
            if hasattr(element, "elements"):
                for inner_element in element.elements:
                    self.element_style.style_element(inner_element)
