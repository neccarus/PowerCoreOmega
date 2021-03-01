from .element import Element


class ToggleableElement(Element):

    def __init__(self, *args, **kwargs):
        self.toggle = False
        super().__init__(*args, **kwargs)

        self.class_name = self.my_name()
