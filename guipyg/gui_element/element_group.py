from .element import Element


class ElementGroup(Element):
    # ElementGroup can be a group of any Element(s) or ElementGroup(s)

    @classmethod
    def deactivate_element(cls, element):
        for ele in element.elements:
            if hasattr(ele, "elements"):
                ElementGroup.deactivate_element(ele)
            else:
                Element.deactivate_element(ele)
        Element.deactivate_element(element)

    def __init__(self, *args, elements=[], **kwargs):
        # if elements is None:
        #     elements = []
        super().__init__(*args, **kwargs)
        if elements is not None:
            self.elements = elements
        self.class_name = self.my_name()
        self.is_draggable = True
        self.blit_list = []  # used to implement pygame.blits()

    # def draw_drop_shadows(self, surface):
    #     # for element in self.elements:
    #     if self.is_visible:
    #         # if hasattr(self, "elements"):
    #         #     self.draw_drop_shadows()
    #         if self.has_drop_shadow:
    #             pygame.draw.rect(surface,
    #                              self.drop_shadow_color,
    #                              self.drop_shadow_rect,
    #                              self.drop_shadow_thickness,
    #                              self.corner_rounding)

    def fill_elements(self, surface):
        for element in self.elements:
            # self.draw_drop_shadows(surface)
            element.fill_elements(surface)
        if self.need_update:  # if statement down here since we want to check individual elements for changes
            super().fill_elements(surface)

    def draw_element_border(self):
        # if self.is_visible:
        for element in self.elements:
            if element.has_border:
                element.draw_element_border()
        if self.need_update:
            super().draw_element_border()

    def draw_text_to_elements(self):
        if self.is_visible:
            for element in self.elements:
                if element.is_visible:
                    element.draw_text_to_elements()
            if self.need_update:
                self.draw_text(self)

    def blit_elements(self):
        if self.is_visible:
            for element in self.elements:
                if element.is_visible:
                    # element.blit_drop_shadow(self)
                    element.blit_elements()
                    self.blit_list.append((element, (element.pos_x, element.pos_y)))
            if self.need_update:
                self.blits(self.blit_list, doreturn=False)
                self.blit_list = []
            # surface.blit(self, (self.pos_x, self.pos_y))

    def setup(self):
        # run this after initializing the object or anytime a change is made in element positions
        self.blit_elements()

    def get_mouse_pos(self, mouse_pos=(0, 0)):
        # adjusts the position of the mouse within the ElementGroup
        adj_mouse_pos_x, adj_mouse_pos_y = mouse_pos
        adj_mouse_pos_x -= self.pos_x
        adj_mouse_pos_y -= self.pos_y

        return adj_mouse_pos_x, adj_mouse_pos_y

    def click(self, mouse_pos=(0, 0), *args, **kwargs):
        for element in self.elements:
            element.click(element.get_mouse_pos((self.get_mouse_pos(mouse_pos))), *args, **kwargs)
