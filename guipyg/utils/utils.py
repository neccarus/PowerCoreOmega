import weakref


class Instance:

    #  Code Credit: http://effbot.org/pyfaq/how-do-i-get-a-list-of-all-instances-of-a-given-class.htm

    _instances = set()

    def add_instance(self):
        self._instances.add(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead
