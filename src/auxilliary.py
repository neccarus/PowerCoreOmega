from src.equipment import Equipment

class InternalHeatSink(Equipment):

    def __init__(self, cooling_modifier=0, heat_capacity=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cooling_modifier = cooling_modifier
        self.heat_capacity = heat_capacity

    def equip_to_parent(self, parent):
        super().equip_to_parent(parent)
        # TODO: auxilliary modules should not DIRECTLY affect the ships attributes, it should be seperated
        parent.cooling_modifier = parent.cooling_modifier * (1 + self.cooling_modifier)
        parent.reactor.heat_capacity = parent.reactor.heat_capacity * (1 + self.heat_capacity)
