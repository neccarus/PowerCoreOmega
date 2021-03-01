from .element_group import ElementGroup


class Menu(ElementGroup): # TODO: this class needs to be fleshed out more, currently it does nothing more than its parent class

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_name = self.my_name()
