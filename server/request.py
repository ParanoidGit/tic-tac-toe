from enum import Enum


class RequestType(Enum):
    UNDEFINED = 0
    GAMEPLAY = 1
    PROFILE = 2


class RequestStatus(Enum):
    UNDEFINED = 0
    NOT_SERVICED = 1
    SERVICED = 2
    INTERRUPTED = 3


class Request:
    type = RequestType.UNDEFINED

    def __init__(self, id_, client_id):
        self.id = id_
        self.client_id = client_id
        self.status = RequestStatus.UNDEFINED

    def start_service(self):
        self.status = RequestStatus.NOT_SERVICED

    def stop_service(self):
        self.status = RequestStatus.SERVICED

    def interrupt_service(self):
        self.status = RequestStatus.INTERRUPTED

    def reinit(self, **new_values):
        self.id = new_values.get('id_')
        self.client_id = new_values.get('client_id')
        self.status = RequestStatus.UNDEFINED


class GameplayRequest(Request):
    type = RequestType.GAMEPLAY

    def __init__(self, id_, client_id, action):
        super().__init__(id_, client_id)
        self.action = action

    def reinit(self, **new_values):
        super().reinit(**new_values)
        self.action = new_values.get('action')


class ProfileRequest(Request):
    type = RequestType.GAMEPLAY

    def __init__(self, id_, client_id, action):
        super().__init__(id_, client_id)
        self.action = action

    def reinit(self, **new_values):
        super().reinit(**new_values)
        self.action = new_values.get('action')


class RequestFactory:
    _requests_constructors = {
        RequestType.UNDEFINED: Request,
        RequestType.GAMEPLAY: GameplayRequest,
        RequestType.PROFILE: ProfileRequest,
    }

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def make(cls, parsed_data):
        request_type_id = parsed_data.pop('type_', RequestType.UNDEFINED.value)
        request_type = None
        try:
            request_type = RequestType(request_type_id)
        except ValueError:
            request_type = RequestType.UNDEFINED
        finally:
            request_constructor = cls._requests_constructors.get(request_type)
            return request_constructor(**parsed_data)
