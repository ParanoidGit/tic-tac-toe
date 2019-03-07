import asyncio
from heapq import heappush, heappop, heapify
import socket
import signal
from client import Client


class Server:
    def __init__(self, host, port, queue_length, package_size,
                 clients_limit, polling_timeout, on_up, on_down,
                 on_connect, on_disconnect, request_parser,
                 request_handler, event_loop):

        # TODO: connection timeout

        self.host = host
        self.port = port
        self.queue_length = queue_length
        self.package_size = package_size
        self.clients_limit = clients_limit
        self.polling_timeout = polling_timeout
        self.event_loop = event_loop
        self.clients = []

        self._on_up = on_up
        self._on_down = on_down
        self._on_connect = on_connect
        self._on_disconnect = on_disconnect
        self._request_parser = request_parser
        self._request_handler = request_handler
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setblocking(False)
        self._socket.bind((self.host, self.port))
        self._socket.listen(self.queue_length)

    def up(self):
        if self._on_up is not None:
            self._on_up(self)
        self._start()

    def down(self):
        if self._on_down is not None:
            self._on_down(self)
        self._shutdown()

    def _init_tasks(self):
        self.event_loop.create_task(self._accept())
        self.event_loop.create_task(self._listen())

    def _start(self):
        self._init_tasks()
        self.event_loop.add_signal_handler(signal.SIGINT, self.down)
        self.event_loop.run_forever()

    def _shutdown(self):
        self.event_loop.remove_signal_handler(signal.SIGINT)
        self.event_loop.stop()
        self._socket.close()

    def _connect(self, client_socket, client_address):
        client_socket.setblocking(False)
        client = Client(client_socket, client_address)
        heappush(self.clients, client.to_heap_item())
        if self._on_connect is not None:
            self._on_connect(self, client)

    def _disconnect(self, client_item):
        client = client_item[-1]
        client.socket.close()
        if self._on_disconnect is not None:
            self._on_disconnect(self, client)
        del client_item
        del client
        heapify(self.clients)

    async def _listen(self):
        while True:
            if self.clients:
                client_item = heappop(self.clients)
                client = client_item[-1]

                if client.dead:
                    self._disconnect(client_item)
                    continue

                future_sock_recv = \
                    self.event_loop.sock_recv(client.socket, self.package_size)

                try:
                    package = await asyncio.wait_for(future_sock_recv,
                                                     timeout=self.polling_timeout)
                except asyncio.TimeoutError:
                    pass
                else:
                    if package:
                        request = self._request_parser.parse(package)
                        self._request_handler.handle(request)
                    else:
                        client.kill()
                finally:
                    client.service()
                    heappush(self.clients, client.to_heap_item())

            else:
                await asyncio.sleep(self.polling_timeout)

    async def _accept(self):
        while True:
            client_socket, client_address = \
                await self.event_loop.sock_accept(self._socket)
            self._connect(client_socket, client_address)
