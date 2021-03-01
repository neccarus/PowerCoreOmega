from .element_group import ElementGroup


class Popup(ElementGroup): # TODO: this class needs to be fleshed out

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.class_name = self.my_name()
