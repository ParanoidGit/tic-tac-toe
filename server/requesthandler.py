class RequestHandler:
    def __init__(self, handle_vectors):
        self._handle_vectors = handle_vectors

    def handle(self, request, on_success_callback=None, on_fail_callback=None):
        handle_vector = self._handle_vectors.get(request.type)
        request.start_service()
        try:
            handle_vector(request)
        except ...:
            if on_fail_callback is not None:
                on_fail_callback()
            else:
                raise RuntimeError
        else:
            if on_success_callback is not None:
                on_success_callback()
        finally:
            request.stop_service()
