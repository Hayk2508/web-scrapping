import time
from core import logger


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        logger.bind(
            Request=f"{request.method} - {request.path}",
            StatusCode=response.status_code,
            Duration=duration,
        ).info("")
        return response
