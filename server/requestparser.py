import json
from request import *


class RequestParser:
    def __init__(self):
        self._requests_pool = []

    def _create_request_inside_pool(self, parsed_data):
        for request in self._requests_pool:
            if request.type == parsed_data['type_'] and \
                    request.status == RequestStatus.SERVICED:
                request.reinit(parsed_data)
                return request
        request = RequestFactory.make(parsed_data)
        self._requests_pool.append(request)
        return request

    def parse(self, raw_data):
        print(raw_data)
        parsed_data = json.loads(raw_data)
        return self._create_request_inside_pool(parsed_data)


if __name__ == '__main__':
    parser = RequestParser()

    raw = [
        '{"type_": "blalslas", "id_": 123456789, "client_id": 899975231}',
        '{"type_": 1, "id_": 12345677899, "client_id": 899975231, "action": "Hi"}',
        '{"type_": 2, "id_": 1234567789, "client_id": 899975231, "action": "Hello"}',
    ]

    for raw_req in raw:
        req = parser.parse(raw_req)
        print(req.id, req.client_id)



