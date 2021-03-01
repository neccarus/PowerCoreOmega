from .toggleable_element import ToggleableElement


class Button(ToggleableElement):

    def __init__(self, width=0, height=0, pos_x=0, pos_y=0, function=None,
                 name="Button", msg="", color=(255, 255, 255),
                 style=None, is_visible=True, **kwargs):
        self.function = function
        super().__init__(width, height, pos_x, pos_y, name=name, msg=msg,
                         color=color, style=style, is_visible=is_visible, **kwargs)
        self.font_pos_x, self.font_pos_y = self.rect.center

    def toggle_click(self):  # TODO: does this do anything? Does it need to be here?
        self.toggle = not self.toggle

    def get_click(self, mouse_pos=(0, 0)):
        mouse_pos_x, mouse_pos_y = self.get_mouse_pos(mouse_pos)
        if self.pos_x <= mouse_pos_x <= (self.pos_x + self.width) and \
                self.pos_y <= mouse_pos_y <= (self.pos_y + self.height):
            self.toggle_click()

    def click(self, *args, **kwargs):  # TODO: this method needs to be restructured in some way
        self.get_click(args[0])
        if self.toggle:
            self.toggle_click()
            #  slice first arg off since it was used as the mouse position for 'get_click' method
            # print(self.function.args + " " + self.function.kwargs)
            return self.function(*self.function.args, **self.function.kwargs)

    def draw_text(self, surface):
        text_obj = self.font.render(self.msg, 1, self.font_color)
        text_rect = text_obj.get_rect()
        text_rect.center = (self.font_pos_x, self.font_pos_y)
        surface.blit(text_obj, text_rect)
