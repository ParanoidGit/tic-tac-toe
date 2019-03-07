import asyncio
from server import Server
from request import *
from requesthandler import RequestHandler
from requestparser import RequestParser


handle_vectors = {
    RequestType.UNDEFINED: lambda req: print(req.id, req.type),
    RequestType.GAMEPLAY: lambda req: print(req.id, req.type, req.action),
    RequestType.PROFILE: lambda req: print(req.id, req.type, req.action),
}


server_config = {
    'host': '127.0.0.1',
    'port': 30,
    'queue_length': 10,
    'package_size': 1024,
    'clients_limit': 100,
    'polling_timeout': 0.1,
    'on_up': lambda srv: print('Server up...'),
    'on_down': lambda srv: print('\rServer down...'),
    'on_connect': lambda srv, client: print('Connect: ', client.address),
    'on_disconnect': lambda srv, client: print('Disconnect:', client.address),
    'request_parser': RequestParser(),
    'request_handler': RequestHandler(handle_vectors),
    'event_loop': asyncio.get_event_loop(),
}


server = Server(**server_config)
server.up()
