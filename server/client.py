from time import time


class Client:
    def __init__(self, socket, address):
        self.id = id(self)
        self.address = address
        self.dead = False
        self.last_service = time()
        self.socket = socket

    def service(self):
        self.last_service = time()

    def kill(self):
        self.dead = True

    def to_heap_item(self):
        return self.last_service, self.id, self
