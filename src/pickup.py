from src.body import Body


class Pickup(Body):

    def __init__(self, consumable=None, powerup=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumable = consumable
        self.powerup = powerup

    def update(self, delta_time, *args, **kwargs):
        if self.collided:
            for collision in self.colliding_with:
                if collision.parent.faction == 'player':
                    if hasattr(collision, 'ship'):
                        player = collision.parent
                        if self.consumable:
                            player.consumables[self.consumable] += 1
                        elif self.powerup:
                            pass
        else:
            super().update(delta_time=delta_time)
