from .element_group import ElementGroup
from .element import Element
from pygame import Vector2
import pygame


class Graph(ElementGroup):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


class GraphElement(Element):

    def __init__(self, low_value=0, high_value=0, current_value=0,
                 empty_color=(0, 0, 0), related_object=None,
                 low_position=Vector2(0, 0), high_position=Vector2(0, 0),
                 angle=0, graph_color=(255, 255, 255), *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.low_value = low_value
        self.high_value = high_value
        self.current_value = current_value
        self.empty_color = empty_color
        self.related_object = related_object
        self.low_position = low_position
        self.high_position = high_position
        self.current_high_position = high_position
        self.ratio = self.current_value / self.high_value
        self.rect = pygame.Rect(self.low_position, self.high_position)
        self.pos_x = self.low_position[0]
        self.pos_y = self.low_position[1]
        self.angle = angle

    def add_to_graph(self, graph):

        self.parent = graph
        self.parent.elements.append(self)

    def update(self, *args, **kwargs):

        self.ratio = self.current_value / self.high_value

    def update_low(self, new_low):
        self.low_value = new_low

    def update_high(self, new_high):
        self.high_value = new_high


class BarElement(GraphElement):

    def __init__(self, thickness=1,  *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.thickness = thickness
        # pygame.draw.rect(self, self.color, (self.low_position, self.current_high_position))
        # self.original = self.copy()
        self.hide_text = True
        self.has_border = False
        # self.width, self.height = self.high_position

    def update(self, *args, **kwargs):

        super().update(*args, **kwargs)
        self.current_high_position = Vector2((self.width * self.ratio, self.height))

        self.draw()

    def draw(self):
        self.content_surface = pygame.Surface((abs(self.content_rect.width), abs(self.content_rect.height)))
        pygame.draw.rect(self.content_surface, self.color, (Vector2(0, 0), Vector2(self.current_high_position, self.height)))
        self.content_surface = pygame.transform.rotate(self.content_surface, self.angle)

    def blit_elements(self):

        self.update()
        super().blit_elements()
        self.need_update = True

    def fill_elements(self, surface):
        if self.need_update:
            if not self.corner_rounding:
                self.fill(self.get_colorkey(), self.rect)
                self.content_surface.fill(self.get_colorkey(), self.content_rect)
