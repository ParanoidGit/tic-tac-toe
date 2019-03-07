class Room:
    def __init__(self, capacity=2):
        assert capacity > 0
        self.id = id(self)
        self.capacity = capacity
        self.visitors = set()
        self.closed = False

    def close(self):
        self.closed = True

    def open(self):
        self.closed = False

    def allow_visitor(self, visitor):
        assert not self.full
        self.visitors.add(visitor)

    def kick_visitor(self, visitor):
        self.visitors.discard(visitor)

    @property
    def empty(self):
        return True if len(self.visitors) == 0 else False

    @property
    def full(self):
        return True if len(self.visitors) == self.capacity else False

    @property
    def occupancy(self):
        return len(self.visitors), self.capacity


class RoomsPool:
    def __init__(self, size):
        assert size > 0
        self.id = id(self)
        self.size = size
        self.rooms = set()

    def add_room(self, room):
        assert not self.full
        self.rooms.add(room)

    def remove_room(self, room):
        self.rooms.discard(room)

    @property
    def empty(self):
        return True if len(self.rooms) == 0 else False

    @property
    def full(self):
        return True if len(self.rooms) == self.size else False

    @property
    def occupancy(self):
        return len(self.rooms), self.size
